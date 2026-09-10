# VENDORED from ShifaMind-MoE `shifamind/model/explain.py`.
# Byte-for-byte except for import paths. Do not edit and do not tidy:
# the checkpoint's parameter names and the forward semantics are pinned
# to this file. If the training repo changes, re-copy it here and re-run
# scripts/parity_router.py and scripts/smoke_fullcode.py.

"""Turn a prediction into evidence a coder can check against the chart.

The model already carries everything needed: ``gate[k]`` says how open concept k
was, ``alpha[l,k]`` says how much label l leaned on it, and the routing means
every active concept is a literal string that appears in the note. What is
missing is the last hop — *where* in the note — and that is recovered here by
re-running the matcher with spans on the one note being explained.

Spans are recomputed rather than cached because storing character offsets for the
whole corpus costs ~2 GB to serve the handful of notes anyone ever inspects.

The export is deliberately unglamorous: code, concept, the exact quoted text, its
character range, and the ConText assertion. A coder can hold it against the chart
and say yes or no, which is the only test of an explanation that matters.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field

import torch

log = logging.getLogger(__name__)


@dataclass
class Evidence:
    concept_id: str
    concept_name: str
    gate: float                  # how open the concept was, 0-1
    attention: float             # alpha[l, k] for this label
    contribution: float          # EXACT signed logit contribution for (l, k)
    spans: list[dict] = field(default_factory=list)   # {text, start, end, assertion}


@dataclass
class CodeExplanation:
    code: str
    probability: float
    concept_share: float         # of |concept| + |residual|
    concept_logit: float
    residual_logit: float
    evidence: list[Evidence] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["evidence"] = [asdict(e) if not isinstance(e, dict) else e
                         for e in self.evidence]
        return d


def concept_spans(text: str, bank: dict, concept_ids: list[str],
                  numeric: bool = True) -> dict[str, list[dict]]:
    """Character spans for the given concepts in one note, with assertion."""
    from ..concepts.bank import surface_map
    from ..concepts.negex import ConceptMatcher

    wanted = set(concept_ids)
    sub = {cid: v["surface_forms"] for cid, v in bank.items() if cid in wanted}
    if not sub:
        return {}
    rules = nmap = None
    if numeric:
        from ..concepts.evalsetup_numeric import numeric_map_for
        from ..concepts.numeric import RULES
        rules = RULES
        nmap = {k: [c for c in v if c in wanted]
                for k, v in numeric_map_for(bank).items()}
        nmap = {k: v for k, v in nmap.items() if v}

    m = ConceptMatcher(surface_map(sub) if not numeric else
                       {cid: v["surface_forms"] for cid, v in bank.items() if cid in wanted},
                       numeric_rules=rules, numeric_map=nmap)
    _, spans = m.match(text or "", keep_spans=True)
    out: dict[str, list[dict]] = {}
    for sp in spans:
        if sp.concept_id in wanted:
            out.setdefault(sp.concept_id, []).append({
                "text": text[sp.start:sp.end],
                "start": int(sp.start), "end": int(sp.end),
                "assertion": sp.assertion.value,
            })
    return out


@torch.no_grad()
def explain_note(out: dict, note_text: str, bank: dict, concept_index: list[str],
                 codes: list[str], row: int = 0, top_codes: int = 10,
                 top_concepts: int = 5, threshold: float = 0.5,
                 with_spans: bool = True) -> list[CodeExplanation]:
    """Explanations for one note's top predicted codes.

    ``out`` must come from a forward pass with ``explain=True`` so ``alpha`` is
    present. ``concept_index`` maps a model concept column back to its bank id;
    it must be the SAME order the queries were built in, or every explanation
    names the wrong concept while looking entirely plausible.
    """
    if "alpha" not in out or out.get("contrib") is None:
        raise ValueError("forward() must be called with explain=True")

    probs = torch.sigmoid(out["logits"][row])
    order = torch.argsort(probs, descending=True)[:top_codes]
    gate = out["gate"][row]
    alpha = out["alpha"][row]
    # The EXACT signed decomposition, not a proxy for it. contrib is
    # (B, H, Lb, K) and sums over heads and concepts to the logit less the
    # bias, so a concept that pushes a code DOWN carries a negative number
    # here. gate*alpha is >= 0 under a sigmoid gate, so ranking on that
    # product could never surface one -- the explanation would show only
    # supporting evidence and silently drop every objection.
    contrib_all = out["contrib"][row].sum(0)                   # (Lb, K)
    cpath = out["concept_pathway_logits"][row]
    resid = (out["residual_logits"][row] if out.get("residual_logits") is not None
             else torch.zeros_like(cpath))

    # Concept columns for this row, in the order the model saw them.
    cids_row = out.get("concept_ids_row")
    if cids_row is None:
        raise ValueError(
            "pass the batch's concept_ids row as out['concept_ids_row'] — the "
            "model does not keep it, and guessing the mapping is how an "
            "explanation ends up naming the wrong concept")

    results: list[CodeExplanation] = []
    span_cache: dict[str, list[dict]] = {}
    if with_spans:
        # strict=: if the row of concept ids and the gate row ever disagree in
        # length, zip would silently drop the tail and the explanation would be
        # quietly incomplete rather than wrong-looking.
        # abs(), not > 0: under sigmoid a padded slot is 9.4e-14 which is
        # ">0" and was silently listing dead slots as live, and under tanh a
        # NEGATIVE gate is displayed evidence that must not be dropped.
        live = [concept_index[int(c)] for c, m in
                zip(cids_row, out["gate"][row].abs() > 1e-6, strict=True) if m]
        span_cache = concept_spans(note_text, bank, live)

    for li in order.tolist():
        if float(probs[li]) < threshold and len(results) >= 1:
            break
        contrib = contrib_all[li]
        # abs(), matching MCB.contributions(): the strongest evidence is the
        # largest |contribution| whichever way it points. Sorting the signed
        # value hides every objection behind top_concepts supporting concepts.
        top = torch.argsort(contrib.abs(), descending=True)[:top_concepts]
        ev = []
        for k in top.tolist():
            # Liveness, not a sign test: a padded slot must go, a concept
            # arguing against the code must stay.
            if abs(float(gate[k])) <= 1e-6:
                continue
            cid = concept_index[int(cids_row[k])]
            ev.append(Evidence(
                concept_id=cid,
                concept_name=str(bank[cid]["name"]) if cid in bank else cid,
                gate=float(gate[k]), attention=float(alpha[li, k]),
                contribution=float(contrib[k]),
                spans=span_cache.get(cid, [])[:4],
            ))
        c, r = float(cpath[li]), float(resid[li])
        results.append(CodeExplanation(
            code=codes[li], probability=float(probs[li]),
            concept_share=abs(c) / (abs(c) + abs(r) + 1e-6),
            concept_logit=c, residual_logit=r, evidence=ev))
    return results


def render(exps: list[CodeExplanation], max_codes: int = 5) -> str:
    """Plain text, the form a coder would actually read."""
    lines = []
    for e in exps[:max_codes]:
        lines.append(f"{e.code}  p={e.probability:.3f}  "
                     f"concept-grounded {e.concept_share:.0%}")
        for ev in e.evidence:
            q = ev.spans[0]["text"] if ev.spans else "(no span — routed but unquoted)"
            asrt = ev.spans[0]["assertion"] if ev.spans else "-"
            lines.append(f"    {ev.contribution:6.3f}  {ev.concept_name[:38]:40s} "
                         f"{asrt:10s} \"{q[:44]}\"")
        lines.append("")
    return "\n".join(lines)
