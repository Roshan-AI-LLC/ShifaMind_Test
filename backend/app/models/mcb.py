# VENDORED from ShifaMind-MoE `shifamind/model/mcb.py`.
# Byte-for-byte except for import paths. Do not edit and do not tidy:
# the checkpoint's parameter names and the forward semantics are pinned
# to this file. If the training repo changes, re-copy it here and re-run
# scripts/parity_router.py and scripts/smoke_fullcode.py.

"""ShifaMind-MoE: a multiplicative concept bottleneck at full-code scale.

The published model cross-attends 160 concept queries to the note, mean-pools the
result into ONE 768-d vector, and gates that. Three things break when you take
that to 16,245 concepts and 7,940 codes, and this module is the answer to each.

**The mean-pool destroys concept identity.** ``pooled = Z_c.mean(dim=1)`` means
the gate cannot express *which* concept mattered — it sees an average. Here the
gate is per-concept, ``g in R^K``, so the gate vector IS the explanation:
"this code fired because concepts 47, 892 and 3301 were open."

**The concept head was a side-channel.** It read from the CLS pool, not from the
bottleneck, so the scalar scores shown to a clinician came from a branch that did
not carry the diagnosis — the flat AUC-Int curve in the preprint is that fact
showing up as a number. Here the concept score for concept k is computed from
``Z_k`` and IS the gate ``g_k``. One quantity does both jobs, so what is shown is
provably what routed the prediction.

**Attending with all 16,245 concepts does not fit.** Routing is a hard mask: the
matcher says which concepts a note contains, and only those attend. p99 is 362
concepts per note, so K=384 covers essentially every note. Every active concept
is then a literal string with a character span, which is the strongest
interpretability property available.

Routing cannot conjure evidence that is not in the text, and a third of gold
codes have none in their own note. So there is an explicit **residual pathway**
from the pooled text, and the model reports how much of each prediction came
through concepts versus through the residual. That number is a result, not an
apology.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import torch
import torch.nn as nn
import torch.nn.functional as F

log = logging.getLogger(__name__)


@dataclass
class MCBConfig:
    n_concepts: int = 16_245
    n_labels: int = 7_940
    hidden: int = 768
    top_k: int = 384                 # p99 of concepts firing per note is 362
    n_heads: int = 8
    dropout: float = 0.1

    backbone: str = "thomas-sounack/BioClinical-ModernBERT-base"
    max_len: int = 6_144
    freeze_backbone_layers: int = 0
    #: eager | sdpa | flash_attention_2. None lets transformers choose. At
    #: 6,144 tokens this is not a micro-optimisation: attention memory is where
    #: the batch size is won or lost.
    attn_implementation: str | None = None
    #: Recompute backbone activations in the backward pass. Costs ~30% step
    #: time and buys back most of the activation memory.
    gradient_checkpointing: bool = False

    #: Per-concept scalar gate. The alternative, a per-concept x per-dimension
    #: gate, is more expressive but stops being readable as concept importance —
    #: the one thing Phase 2 actually ablates.
    gate: str = "concept"            # concept | two_level
    #: Concept score and gate are the same quantity. Setting this False restores
    #: the published behaviour and exists only so the ablation can be run.
    gate_tied: bool = True
    #: Gate activation. "sigmoid" gives g in (0,1): a concept can only ADD its
    #: vector, so a NEGATED mention -- "no chest pain", "father had diabetes" --
    #: can at best contribute nothing. The note's strongest statements about a
    #: concept are exactly the ones a (0,1) bottleneck cannot express, and the
    #: five named channels were an attempt to buy that back with 5x the
    #: parameters (measured: parity, not gain).
    #: "tanh" gives g in (-1,1) with tanh(0) = 0, so ONE displayed scalar per
    #: concept carries the assertion in its SIGN and the confidence in its
    #: MAGNITUDE. Leakage is still zero by exactly the argument that made
    #: concept_width 0 honest -- the note reaches the logit only through g.
    #: It also removes the reason w_sparse never worked: closing a sigmoid gate
    #: needs s -> -inf, fighting the concept BCE, whereas closing a tanh gate is
    #: s -> 0, which is where it starts.
    gate_act: str = "sigmoid"        # sigmoid | tanh

    #: NAMED MULTI-CHANNEL GATES.
    #: Each routed concept gets one scalar PER CHANNEL, and every channel has a
    #: clinical name the coder reads: affirmed / negated / hypothetical /
    #: family / historical. u_k = sum_c a[k,c] * E_c[k], where E_c[k] carries no
    #: note information at all. So the note reaches the logit ONLY through the
    #: a[k,c] scalars -- every one of which is displayed -- and leakage is zero
    #: by exactly the argument that made concept_width 0 honest, while the
    #: channel is C times wider. C = 1 reproduces the single-gate model.
    #: The supervision is free: 12_silver_labels.py already computes all five
    #: assertion classes per note per concept and the trainer discarded four.
    concept_channels: int = 1
    channel_names: tuple = ("affirmed",)
    w_channel: float = 1.0
    use_residual: bool = True

    focal_gamma: float = 2.0
    focal_alpha: float = 0.75
    #: Weight on the concept-BCE term, relative to a focal loss normalised
    #: per gold code. Under the old normalisation (focal meaned over all
    #: B x 7,940 cells) the concept term was 96% of the loss and the coder was
    #: being starved — focal sat flat at 0.0019 for 1,300 steps while the
    #: concept term kept falling. See loss() for the fix.
    w_concept: float = 1.0

    # ---- V2 arms. Every default below reproduces the V1 forward exactly, so
    # ---- --eval-only on an existing checkpoint is unaffected.

    #: Residual (non-concept) pathway. "pool" is ONE mean-pooled note vector
    #: shared by all 7,940 codes — the model then has no label-specific view of
    #: raw text at all, everything label-specific goes through concepts. "seg"
    #: mean-pools into `seg_len`-token segments and gives every code its own
    #: attention over them, which is what PLM-ICD's decoder does over tokens,
    #: at 1/seg_len the memory.
    residual: str = "pool"           # pool | seg
    seg_len: int = 128
    #: Label-concept attention. A softmax is a convex combination, so six pieces
    #: of concept evidence for a code produce the same logit magnitude as one.
    #: "sigmoid" drops the normalisation so evidence accumulates, rescaled by
    #: sqrt(routed) to keep the magnitude comparable across note lengths.
    label_attn: str = "softmax"      # softmax | sigmoid
    #: Per-category low-rank adapters on the gated concept vectors. This is the
    #: parameter specialisation that hard routing has always lacked, and the
    #: assignment is a lookup from the bank's `category` field, not a learned
    #: gate — so the mixture stays readable rather than adding another opaque
    #: component.
    experts: str = "none"            # none | category
    n_experts: int = 0
    expert_rank: int = 64
    #: ICD-10 parent (3-character) auxiliary head. The child logit inherits a
    #: scaled copy of its parent's evidence, which for a code with six training
    #: examples is the only signal that is not noise.
    hier: bool = False
    n_parents: int = 0
    w_hier: float = 0.3

    # ---- the bottleneck itself -------------------------------------------
    #: How many numbers ABOUT THE NOTE may flow through one concept slot.
    #:   -1  legacy: u_k = g_k * Z_k, the full cross-attention readout.
    #:    0  scalar: u_k = g_k * E[k]. The gate is the ONLY note-dependent
    #:       quantity, so the concept's NAME cannot lie about what the slot
    #:       carries. This is the real concept bottleneck.
    #:    r  u_k = g_k * (E[k] + Up_r(Down_r(Z_k))). The note may say r things
    #:       about the concept -- severity, laterality, acuity -- and no more.
    #: Exact attribution holds at every width; honest NAMING is what width buys.
    concept_width: int = -1
    #: Cross-attention depth. One layer collapses every mention of a concept in
    #: the note into a single averaged vector.
    concept_layers: int = 1
    #: Heads in the label-concept attention. Attribution stays exact -- the
    #: contribution is summed over heads -- so this buys capacity for free.
    label_heads: int = 1
    #: strict   nothing reaches a logit except through a multiplicative gate
    #: licensed the text pathway exists but is scaled by concept support, so
    #:          zeroing every gate still collapses the model to the prior
    #: free     ungated additive residual -- the bypass, kept only so the
    #:          earlier runs remain reproducible
    compose: str = "free"            # strict | licensed | free
    #: L1 on the gate. Measured without it: mean gate 0.909, median open-rate
    #: 1.000 -- a multiplier that is always on is not a bottleneck.
    w_sparse: float = 0.0
    #: InfoNCE recovering a concept's identity from its own slot vector. Without
    #: it nothing forces Z_k to be ABOUT concept k.
    w_fidelity: float = 0.0
    fidelity_temp: float = 0.07
    fidelity_slots: int = 4096

    #: The alignment loss is absent by design: the published ablation shows
    #: removing it improves Macro-F1 and Macro-AUC by +0.003 each.
    extras: dict = field(default_factory=dict)


class ShifaMindMoE(nn.Module):
    def __init__(self, cfg: MCBConfig, backbone: nn.Module | None = None,
                 concept_init: torch.Tensor | None = None,
                 label_init: torch.Tensor | None = None,
                 label_prior: torch.Tensor | None = None):
        super().__init__()
        self.cfg = cfg
        d = cfg.hidden

        if backbone is None:
            from transformers import AutoModel
            kw = ({} if cfg.attn_implementation is None
                  else {"attn_implementation": cfg.attn_implementation})
            backbone = AutoModel.from_pretrained(cfg.backbone, **kw)
        self.backbone = backbone
        if cfg.freeze_backbone_layers:
            self._freeze_lower(cfg.freeze_backbone_layers)
        if cfg.gradient_checkpointing:
            self._enable_checkpointing()

        # Concept queries — learnable, initialised from the concept names so a
        # query for "reduced ejection fraction" starts near the spans that say it.
        self.concept_queries = nn.Embedding(cfg.n_concepts, d)
        if concept_init is not None:
            assert concept_init.shape == (cfg.n_concepts, d), concept_init.shape
            self.concept_queries.weight.data.copy_(concept_init.float())

        self.cross_attn = nn.MultiheadAttention(
            d, cfg.n_heads, dropout=cfg.dropout, batch_first=True)
        self.q_norm = nn.LayerNorm(d)
        if cfg.concept_layers > 1:
            self.cross_attn_extra = nn.ModuleList([
                nn.MultiheadAttention(d, cfg.n_heads, dropout=cfg.dropout,
                                      batch_first=True)
                for _ in range(cfg.concept_layers - 1)])
            self.slot_norm = nn.ModuleList([
                nn.LayerNorm(d) for _ in range(cfg.concept_layers - 1)])

        # What a concept MEANS, independent of any note. At concept_width 0 this
        # is the only thing the gate multiplies, so the note reaches the
        # prediction through exactly one number per concept.
        if cfg.concept_width >= 0:
            self.concept_value = nn.Embedding(cfg.n_concepts, d)
            if concept_init is not None:
                self.concept_value.weight.data.copy_(concept_init.float())
            else:
                nn.init.normal_(self.concept_value.weight, std=0.02)
            if cfg.concept_width > 0:
                r = min(cfg.concept_width, d)
                self.slot_down = nn.Linear(d, r, bias=False)
                self.slot_up = nn.Linear(r, d, bias=False)
                # zero-init: the slot starts as pure concept identity, and any
                # note information it later carries had to be earned.
                nn.init.zeros_(self.slot_up.weight)

        # Concept score -> gate. One scalar per concept, from that concept's own
        # cross-attended vector.
        self.concept_score = nn.Linear(d, 1)
        if cfg.gate == "two_level":
            self.feature_gate = nn.Sequential(nn.Linear(d, d), nn.Sigmoid())
        if not cfg.gate_tied:
            self.gate_head = nn.Linear(d, 1)

        if cfg.concept_channels > 1:
            if cfg.concept_width != 0:
                raise ValueError(
                    "concept_channels > 1 requires concept_width 0 — the point "
                    "is that no anonymous dimension exists beside the named ones")
            self.channel_value = nn.Embedding(cfg.n_concepts,
                                              cfg.concept_channels * d)
            nn.init.normal_(self.channel_value.weight, std=0.02)
            self.channel_score = nn.Linear(d, cfg.concept_channels)

        # Label-wise attention over the GATED concept vectors. Gives per-label,
        # per-concept attribution for free: alpha[l,k] * g[k].
        self.label_queries = nn.Embedding(cfg.n_labels, d)
        if label_init is not None:
            assert label_init.shape == (cfg.n_labels, d), label_init.shape
            self.label_queries.weight.data.copy_(label_init.float())
        else:
            nn.init.normal_(self.label_queries.weight, std=0.02)
        self.label_out = nn.Linear(d, cfg.n_labels)      # w_l . z_l  + b_l
        if label_prior is not None:
            # Per-code prior bias, b_l = logit(p_l). Without it every one of the
            # 7,940 logits starts near zero, i.e. p=0.5, on a task whose base
            # rate is 0.2% — so the first thousands of steps are spent learning
            # nothing but "codes are rare", and the tail never gets past it
            # because a single shared bias can only encode the AVERAGE rate.
            # This is the initialisation the focal-loss paper prescribes; here
            # it is per-code rather than global, which is the part that should
            # move macro-F1 rather than micro.
            pr = label_prior.float().clamp(1e-6, 1 - 1e-6)
            self.label_out.bias.data.copy_(torch.log(pr / (1 - pr)))
            log.info("label bias initialised from the code priors: "
                     "median %.1f, range %.1f to %.1f",
                     float(self.label_out.bias.median()),
                     float(self.label_out.bias.min()), float(self.label_out.bias.max()))

        # Per-category expert adapters. exp_b is zero-initialised so the block
        # is exactly the identity at step 0 and cannot destabilise the start.
        if cfg.experts in ("category", "type"):
            if cfg.n_experts < 1:
                raise ValueError(f"experts={cfg.experts!r} needs n_experts >= 1")
            self.exp_a = nn.Parameter(torch.empty(cfg.n_experts, d, cfg.expert_rank))
            nn.init.normal_(self.exp_a, std=0.02)
            self.exp_b = nn.Parameter(torch.zeros(cfg.n_experts, cfg.expert_rank, d))
            self.register_buffer("concept_expert",
                                 torch.zeros(cfg.n_concepts, dtype=torch.long),
                                 persistent=False)

        if cfg.hier:
            if cfg.n_parents < 1:
                raise ValueError("hier=True needs n_parents >= 1")
            self.parent_queries = nn.Embedding(cfg.n_parents, d)
            nn.init.normal_(self.parent_queries.weight, std=0.02)
            self.parent_out = nn.Linear(d, cfg.n_parents)
            # tanh(0) = 0: the parent term starts contributing nothing, so the
            # arm cannot lose to its own initialisation.
            self.hier_scale = nn.Parameter(torch.zeros(()))
            self.register_buffer("label_parent",
                                 torch.zeros(cfg.n_labels, dtype=torch.long),
                                 persistent=False)

        if cfg.use_residual:
            if cfg.residual == "seg":
                self.res_queries = nn.Embedding(cfg.n_labels, d)
                if label_init is not None:
                    self.res_queries.weight.data.copy_(label_init.float())
                else:
                    nn.init.normal_(self.res_queries.weight, std=0.02)
                # The prior bias stays on label_out (the concept pathway),
                # where V1 put it. Moving it here would halve the reported
                # concept_share overnight and the drop would be an accounting
                # artefact, not a finding. res_out.bias starts at zero so the
                # base rate is applied exactly once.
                self.res_out = nn.Linear(d, cfg.n_labels)
                nn.init.zeros_(self.res_out.bias)
                self.res_norm = nn.LayerNorm(d)
            else:
                self.residual = nn.Sequential(
                    nn.Dropout(cfg.dropout), nn.Linear(d, cfg.n_labels))
        self.drop = nn.Dropout(cfg.dropout)

    # ------------------------------------------------------------------
    def _attend(self, U, Wq, Wo, bias, concept_mask, want_contrib=False):
        """logit_l = sum_h sum_k alpha_h[l,k] * (w_{l,h} . u_{k,h}) + b_l.

        Factored so the (B, n_labels, d) tensor never exists, and EXACT: the
        per-(label, concept) contributions sum to the logit with no remainder.
        That decomposition IS the interpretability claim, so it is returned
        rather than reconstructed approximately by anything downstream.
        """
        B, K, d = U.shape
        H = max(1, self.cfg.label_heads)
        if d % H:
            raise ValueError(f"hidden {d} not divisible by label_heads {H}")
        dh, Lb = d // H, Wq.shape[0]
        u = U.view(B, K, H, dh)
        sc = torch.einsum("bkhe,lhe->bhlk", u, Wq.view(Lb, H, dh)) / (dh ** 0.5)
        proj = torch.einsum("bkhe,lhe->bhlk", u, Wo.view(Lb, H, dh))
        live = (concept_mask > 0)[:, None, None, :]
        if self.cfg.label_attn == "sigmoid":
            a = torch.sigmoid(sc) * live
            # Without this a 380-concept note gets ~19x the logit magnitude of a
            # 1-concept note purely from length. sqrt, not linear: linear is a
            # mean again and gives back exactly what softmax was doing wrong.
            n = concept_mask.sum(-1).clamp(min=1).to(a.dtype).sqrt()
            a = a / n.view(-1, 1, 1, 1)
        else:
            a = torch.softmax(sc.masked_fill(~live, float("-inf")), dim=-1)
            # A note with zero routed concepts gives all -inf -> NaN. Zero it.
            a = torch.nan_to_num(a, nan=0.0)
        contrib = a * proj                                     # (B,H,Lb,K)
        out = contrib.sum(3).sum(1)                            # (B,Lb)
        if bias is not None:
            out = out + bias
        alpha = a.sum(1) if H > 1 else a.squeeze(1)            # (B,Lb,K)
        return out, alpha, (contrib if want_contrib else None)

    def _expert_mix(self, U, concept_ids, concept_mask):
        """Route each slot to its category's adapter. Batched over all experts
        rather than looped with .nonzero(): the loop costs one host sync per
        expert per forward, the batched form costs 1.7 GFLOP."""
        B, K, d = U.shape
        E = self.cfg.n_experts
        flat = U.reshape(-1, d)
        eid = self.concept_expert[concept_ids].reshape(-1)
        live = (concept_mask.reshape(-1) > 0)
        m = F.one_hot(eid.clamp(0, E - 1), E).to(U.dtype) * live.unsqueeze(-1)
        h1 = torch.einsum("nd,edr->ner", flat, self.exp_a) * m.unsqueeze(-1)
        delta = torch.einsum("ner,erd->nd", h1, self.exp_b)
        return (flat + delta).view(B, K, d)

    def _enable_checkpointing(self) -> None:
        fn = getattr(self.backbone, "gradient_checkpointing_enable", None)
        if fn is None:
            log.warning("backbone has no gradient_checkpointing_enable; skipped")
            return
        # use_reentrant=False is not optional here: the reentrant implementation
        # silently produces no gradients when the checkpointed block's inputs do
        # not require grad, which is exactly the case with a frozen embedding.
        fn(gradient_checkpointing_kwargs={"use_reentrant": False})
        log.info("gradient checkpointing on")

    def _freeze_lower(self, n: int) -> None:
        mods = getattr(self.backbone, "layers", None)
        if mods is None:
            enc = getattr(self.backbone, "encoder", None)
            mods = getattr(enc, "layer", None) if enc is not None else None
        if mods is None:
            log.warning("could not locate backbone layers; nothing frozen")
            return
        emb = getattr(self.backbone, "embeddings", None)
        if emb is not None:
            for p in emb.parameters():
                p.requires_grad = False
        for layer in list(mods)[:n]:
            for p in layer.parameters():
                p.requires_grad = False
        log.info("froze embeddings + %d backbone layers", n)

    # ------------------------------------------------------------------
    def forward(self, input_ids, attention_mask, concept_ids, concept_mask,
                labels=None, concept_targets=None, explain: bool = False,
                slot_z=None):
        """
        input_ids       (B, L)          token ids
        attention_mask  (B, L)          1 for real tokens
        concept_ids     (B, K)          routed concept indices, matcher-selected
        concept_mask    (B, K)          1 where the slot holds a real concept
        labels          (B, n_labels)   multi-hot, optional
        concept_targets (B, K)          per-slot silver presence, optional
        slot_z          callable(Z, concept_ids, concept_mask) -> Z', or None.

        `slot_z` substitutes the note representation used to build the SLOT while
        leaving the GATE computed from the true Z. That isolates the one thing the
        interpretability claim cannot check by inspection: whether the anonymous
        note-dependent content of a slot changes the prediction, given that the
        displayed per-concept scalar is held fixed. When None -- always, in
        training and evaluation -- the forward is bit-identical to before.
        """
        h = self.backbone(input_ids=input_ids,
                          attention_mask=attention_mask).last_hidden_state  # (B,L,d)

        q = self.q_norm(self.concept_queries(concept_ids))                  # (B,K,d)
        # key_padding_mask marks positions to IGNORE, hence the inversion.
        Z, attn = self.cross_attn(q, h, h,
                                  key_padding_mask=(attention_mask == 0),
                                  need_weights=explain, average_attn_weights=True)
        if self.cfg.concept_layers > 1:
            # One cross-attention layer averages every mention of a concept in
            # the note into a single vector. Extra layers let it aggregate
            # several mentions non-linearly, which is where the capacity a
            # bypass used to supply has to come from instead.
            for att, nrm in zip(self.cross_attn_extra, self.slot_norm, strict=True):
                Z = Z + att(nrm(Z), h, h,
                            key_padding_mask=(attention_mask == 0),
                            need_weights=False)[0]
        Z = self.drop(Z)                                                    # (B,K,d)

        s = self.concept_score(Z).squeeze(-1)                               # (B,K)
        # Dead slots must not contribute anywhere: a large negative before the
        # sigmoid makes the gate ~0, and the softmax below cannot attend to them.
        s = s.masked_fill(concept_mask == 0, -30.0)
        concept_logits = s
        gs = s if self.cfg.gate_tied else (
            self.gate_head(Z).squeeze(-1).masked_fill(concept_mask == 0, -30.0))
        if self.cfg.gate_act == "tanh":
            # tanh(-30) = -1.0, NOT 0, so the mask MUST be applied
            # multiplicatively here or every padded slot would contribute
            # -E[k]. It also makes a dead slot contribute EXACTLY zero, which
            # sigmoid(-30) = 9.4e-14 does not -- the sufficiency proof stops
            # being approximate. The sigmoid branch below is left bit-for-bit
            # as it was so every existing checkpoint re-evaluates identically.
            g = torch.tanh(gs) * concept_mask.to(Z.dtype)
        else:
            g = torch.sigmoid(gs)

        # The bottleneck. concept_width decides how many numbers about the
        # note may pass; the gate multiplies whatever does.
        channel_logits = None
        if self.cfg.concept_channels > 1:
            B_, K_, d_ = Z.shape
            C_ = self.cfg.concept_channels
            cl_ = self.channel_score(Z)                                     # (B,K,C)
            cl_ = cl_.masked_fill(concept_mask.unsqueeze(-1) == 0, -30.0)
            channel_logits = cl_
            # Multiply by the mask explicitly. sigmoid(-30) is 1e-13, not 0, and
            # the suppression ablation needs a suppressed slot to contribute
            # EXACTLY zero or the sufficiency proof is only approximate.
            act_ = torch.tanh if self.cfg.gate_act == "tanh" else torch.sigmoid
            a_ = act_(cl_) * concept_mask.unsqueeze(-1).to(Z.dtype)
            E_ = self.channel_value(concept_ids).view(B_, K_, C_, d_)
            U = torch.einsum("bkc,bkcd->bkd", a_, E_)                       # (B,K,d)
            g = a_[..., 0]              # affirmed is the headline gate
            concept_logits = cl_[..., 0]
        else:
            if self.cfg.concept_width < 0:
                slot = Z                                      # legacy
            elif self.cfg.concept_width == 0:
                slot = self.concept_value(concept_ids)        # scalar channel
            else:
                # The gate above came from the TRUE Z. Only the slot's note content
                # is substituted, so the displayed scalar is held fixed by
                # construction rather than by convention.
                Zs = Z if slot_z is None else slot_z(Z, concept_ids, concept_mask)
                slot = self.concept_value(concept_ids) + self.slot_up(self.slot_down(Zs))
            U = slot * g.unsqueeze(-1)                                      # (B,K,d)
        if self.cfg.gate == "two_level":
            U = U * self.feature_gate(Z)
        if self.cfg.experts in ("category", "type"):
            U = self._expert_mix(U, concept_ids, concept_mask)

        concept_pathway, alpha, contrib = self._attend(
            U, self.label_queries.weight, self.label_out.weight,
            self.label_out.bias, concept_mask, want_contrib=explain)

        logits = concept_pathway
        parent_logits = None
        if self.cfg.hier:
            parent_logits, _, _ = self._attend(
                U, self.parent_queries.weight, self.parent_out.weight,
                self.parent_out.bias, concept_mask)
            logits = logits + torch.tanh(self.hier_scale) * \
                parent_logits.index_select(1, self.label_parent)

        # Composition. Under "strict" there is no path to a logit that does not
        # pass through g; under "licensed" the text pathway exists but cannot
        # speak about a code no concept supports.
        residual_logits, support = None, None
        want_res = self.cfg.use_residual and self.cfg.compose != "strict"
        if want_res:
            residual_logits = self._residual(h, attention_mask)
            if self.cfg.compose == "licensed":
                support = (alpha * g.unsqueeze(1)).sum(-1).clamp(0, 1)   # (B,Lb)
                logits = logits + support * residual_logits
            else:
                logits = logits + residual_logits

        out = {"logits": logits, "concept_logits": concept_logits, "gate": g,
               "channel_logits": channel_logits,
               "concept_pathway_logits": concept_pathway,
               "parent_logits": parent_logits, "concept_support": support,
               "residual_logits": residual_logits}
        if self.cfg.w_fidelity:
            out["slot_raw"], out["concept_ids"] = Z, concept_ids
        if explain:
            out.update({"alpha": alpha, "token_attn": attn,
                        "concept_vectors": Z, "contrib": contrib})
        if labels is not None:
            out.update(self.loss(out, labels, concept_targets, concept_mask))
        return out

    # ------------------------------------------------------------------
    def _residual(self, h, attention_mask):
        if self.cfg.residual != "seg":
            m = attention_mask.unsqueeze(-1).to(h.dtype)
            pooled = (h * m).sum(1) / m.sum(1).clamp(min=1e-6)
            return self.residual(pooled)

        # Segment-level label attention. The (B, 7940, 6144) tensor PLM-ICD's
        # decoder implies does not fit; pooling 128 tokens first makes it
        # (B, 7940, 48), which is 1.5M floats at batch 4.
        B, L, d = h.shape
        S = self.cfg.seg_len
        pad = (-L) % S
        hh = F.pad(h, (0, 0, 0, pad))
        mm = F.pad(attention_mask, (0, pad)).to(h.dtype)
        hh = hh.view(B, -1, S, d)
        mm = mm.view(B, -1, S)
        n = mm.sum(2)                                                    # (B,S')
        e = (hh * mm.unsqueeze(-1)).sum(2) / n.clamp(min=1e-6).unsqueeze(-1)
        e = self.res_norm(e)
        seg_live = (n > 0)
        sc = torch.einsum("bsd,ld->bls", e, self.res_queries.weight) / (d ** 0.5)
        sc = sc.masked_fill(~seg_live.unsqueeze(1), float("-inf"))
        beta = torch.nan_to_num(torch.softmax(sc, dim=-1), nan=0.0)
        pr = torch.einsum("bsd,ld->bls", e, self.res_out.weight)
        return (beta * pr).sum(-1) + self.res_out.bias

    # ------------------------------------------------------------------
    def loss(self, out, labels, concept_targets, concept_mask):
        cfg = self.cfg
        z = out["logits"]
        p = torch.sigmoid(z)
        ce = F.binary_cross_entropy_with_logits(z, labels, reduction="none")
        p_t = p * labels + (1 - p) * (1 - labels)
        a_t = cfg.focal_alpha * labels + (1 - cfg.focal_alpha) * (1 - labels)
        # Normalised by the number of GOLD CODES, not by B x n_labels. At 0.2%
        # positive rate a mean over all cells is ~99.8% easy negatives, which
        # drives the term to ~0.002 and leaves it there — measured flat across
        # 1,300 steps while the concept term did all the learning. Per-positive
        # normalisation is what focal loss was defined with (RetinaNet divides
        # by the number of assigned anchors) and it keeps the term O(1), so
        # w_concept becomes a knob with a usable range instead of one whose
        # entire action lives below 0.01.
        n_pos = labels.sum().clamp(min=1.0)
        focal = (a_t * (1 - p_t).pow(cfg.focal_gamma) * ce).sum() / n_pos

        total = focal
        parts = {"loss_focal": focal.detach()}
        # Targets arrive as (B, K, C) once the dataset emits every assertion
        # class. Channel 0 is `affirmed` and keeps the original w_concept
        # semantics so concept_frac stays comparable across runs.
        channel_targets = None
        if concept_targets is not None and concept_targets.dim() == 3:
            channel_targets = concept_targets
            concept_targets = concept_targets[..., 0]
        if concept_targets is not None and cfg.w_concept:
            # Only real slots supervise; padding must not be trained toward 0.
            cl = F.binary_cross_entropy_with_logits(
                out["concept_logits"], concept_targets.float(), reduction="none")
            n = concept_mask.sum().clamp(min=1)
            c_loss = (cl * concept_mask).sum() / n
            total = total + cfg.w_concept * c_loss
            parts["loss_concept"] = c_loss.detach()
            # The share of the loss the concept head is taking. This is the
            # number that hid the problem: it has to be logged, not inferred.
            parts["concept_frac"] = (cfg.w_concept * c_loss / total.clamp(min=1e-9)).detach()
        if (channel_targets is not None and cfg.w_channel
                and out.get("channel_logits") is not None
                and channel_targets.shape[-1] > 1):
            # Channel 0 is already supervised by w_concept; 1.. are negated,
            # hypothetical, family, historical.
            chl = F.binary_cross_entropy_with_logits(
                out["channel_logits"][..., 1:], channel_targets[..., 1:].float(),
                reduction="none")
            m = concept_mask.unsqueeze(-1)
            ch_loss = (chl * m).sum() / (m.sum().clamp(min=1) * chl.shape[-1])
            total = total + cfg.w_channel * ch_loss
            parts["loss_channel"] = ch_loss.detach()
        if cfg.hier and out.get("parent_logits") is not None:
            # Parent multi-hot, derived from the child labels rather than stored:
            # index_add_ scatters each code's column onto its parent's.
            pt = torch.zeros(labels.shape[0], cfg.n_parents,
                             device=labels.device, dtype=labels.dtype)
            pt.index_add_(1, self.label_parent, labels)
            pt = pt.clamp(max=1.0)
            pz = out["parent_logits"]
            pp = torch.sigmoid(pz)
            pce = F.binary_cross_entropy_with_logits(pz, pt, reduction="none")
            ppt = pp * pt + (1 - pp) * (1 - pt)
            pat = cfg.focal_alpha * pt + (1 - cfg.focal_alpha) * (1 - pt)
            h_loss = (pat * (1 - ppt).pow(cfg.focal_gamma) * pce).sum() \
                / pt.sum().clamp(min=1.0)
            total = total + cfg.w_hier * h_loss
            parts["loss_hier"] = h_loss.detach()
            parts["hier_scale"] = torch.tanh(self.hier_scale).detach()
        if cfg.w_sparse:
            # L1 toward zero on live gates. A gate that is always open is an
            # identity function wearing a bottleneck's name.
            n = concept_mask.sum().clamp(min=1)
            # |g|: under tanh a gate at -1 is as far from closed as one at +1,
            # and a signed mean would let the two cancel and report "sparse".
            sp = (out["gate"].abs() * concept_mask).sum() / n
            total = total + cfg.w_sparse * sp
            parts["gate_mean"] = sp.detach()
        if cfg.w_fidelity and out.get("slot_raw") is not None:
            # Can the concept be recovered from its own slot? If not, the name
            # on the slot is decoration. Negatives are the other concepts in
            # this batch, which is cheap and is the hard case anyway.
            d = out["slot_raw"].shape[-1]
            live = concept_mask.reshape(-1) > 0
            zf = out["slot_raw"].reshape(-1, d)[live]
            ids = out["concept_ids"].reshape(-1)[live]
            if zf.shape[0] > cfg.fidelity_slots:
                pick = torch.randperm(zf.shape[0], device=zf.device)[:cfg.fidelity_slots]
                zf, ids = zf[pick], ids[pick]
            if zf.shape[0] > 1:
                uniq, inv = torch.unique(ids, return_inverse=True)
                E = F.normalize(self.concept_value(uniq).float(), dim=-1)
                sim = F.normalize(zf.float(), dim=-1) @ E.T / cfg.fidelity_temp
                f_loss = F.cross_entropy(sim, inv)
                total = total + cfg.w_fidelity * f_loss
                parts["loss_fidelity"] = f_loss.detach()
                parts["slot_recall"] = (sim.argmax(-1) == inv).float().mean().detach()
        parts["loss"] = total
        return parts

    # ------------------------------------------------------------------
    @torch.no_grad()
    def contributions(self, out, code_idx, top_n: int = 10):
        """The exact per-concept decomposition of one code's logit.

        logit_l = b_l + sum_k c[l,k]. No approximation, no saliency heuristic,
        and it is asserted to reconcile -- an explanation that does not add up
        to the prediction is not an explanation.
        """
        if out.get("contrib") is None:
            raise ValueError("call forward(..., explain=True) for contributions")
        c = out["contrib"][:, :, code_idx, :].sum(1)            # (B,K)
        b = self.label_out.bias[code_idx]
        recon = c.sum(-1) + b
        got = out["concept_pathway_logits"][:, code_idx]
        err = (recon - got).abs().max()
        if not torch.isfinite(err) or err > 1e-2:
            raise AssertionError(f"contributions do not reconcile: {float(err):.4g}")
        v, i = c.abs().topk(min(top_n, c.shape[-1]), dim=-1)
        return {"contrib": c, "bias": b, "top_idx": i,
                "top_value": torch.gather(c, 1, i), "recon_error": float(err)}

    # ------------------------------------------------------------------
    @torch.no_grad()
    def grounding_split(self, out, threshold: float = 0.5) -> dict:
        """How much of each positive prediction came through concepts?

        The honest accounting for the third of codes with no textual evidence:
        report the share rather than let the residual quietly carry them.
        """
        if out["residual_logits"] is None:
            # Under strict there is no other pathway, so the share is 1.0 by
            # construction -- but n_pred still has to be reported or the
            # accumulator in validate() skips it and the run logs "nan%" for
            # the one number that is trivially, provably perfect.
            pred = torch.sigmoid(out["logits"].float()) > threshold
            return {"concept_share": 1.0, "n_pred": int(pred.sum())}
        pred = torch.sigmoid(out["logits"].float()) > threshold
        # float() is not cosmetic: under bf16/fp16 autocast quantile() raises
        # "input tensor must be either float or double dtype", and it would only
        # raise on the GPU, after the run.
        c = out["concept_pathway_logits"].float()[pred]
        r = out["residual_logits"].float()[pred]
        if c.numel() == 0:
            return {"concept_share": float("nan"), "n_pred": 0}
        share = c.abs() / (c.abs() + r.abs() + 1e-6)
        return {"concept_share": float(share.mean()),
                "concept_share_p10": float(share.quantile(0.10)),
                "n_pred": int(pred.sum())}
