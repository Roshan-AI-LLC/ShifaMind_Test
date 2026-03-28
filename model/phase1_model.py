"""
ShifaMind Phase 1 Model — inference-only definition.

Architecture (reconstructed from checkpoint 20260301_112200, epoch 10,
macro_f1=0.451):

  base_model       BioClinicalBERT (12-layer, vocab=28996)
  concept_embeddings  nn.Parameter [111, 768]  (learnable concept prototypes)
  fusion_modules   ConceptFusionModule at BERT layers 9 and 11
                     — cross-attention: BERT tokens (Q) attend to concepts (K,V)
                     — gated residual + LayerNorm
  concept_head     nn.Linear(768 → 111)  applied to pooler [CLS] output
  diagnosis_head   nn.Linear(768 → 50)   applied to pooler [CLS] output

State-dict key prefix:  base_model.*  (not bert.*)
BertConfig is hardcoded from checkpoint weight shapes — no HuggingFace
download needed for the model itself (tokenizer loaded separately).
"""

import math
import torch
import torch.nn as nn
from transformers import BertConfig, BertModel


# ── Concept Fusion Module ─────────────────────────────────────────────────────

class ConceptFusionModule(nn.Module):
    """
    Cross-attention fusion between BERT hidden states and concept embeddings.

    BERT hidden states act as queries; concept embeddings act as keys/values.
    A two-layer gating MLP controls how much concept signal is blended in.
    Applied as a residual on top of the BERT layer output.

    gate_net indices (4-element Sequential, only 0 and 3 have weights):
        [0] Linear(1536 → 768)
        [1] GELU
        [2] Dropout(0.1)
        [3] Linear(768 → 768)
    """

    def __init__(self, hidden_size: int = 768):
        super().__init__()
        self.query    = nn.Linear(hidden_size, hidden_size)
        self.key      = nn.Linear(hidden_size, hidden_size)
        self.value    = nn.Linear(hidden_size, hidden_size)
        self.out_proj = nn.Linear(hidden_size, hidden_size)
        self.gate_net = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),  # index 0
            nn.GELU(),                                 # index 1
            nn.Dropout(0.1),                           # index 2
            nn.Linear(hidden_size, hidden_size),       # index 3
        )
        self.layer_norm = nn.LayerNorm(hidden_size)

    def forward(
        self,
        hidden_states: torch.Tensor,       # (B, seq_len, H)
        concept_embeddings: torch.Tensor,  # (num_concepts, H)  — shared Parameter
    ) -> torch.Tensor:
        B = hidden_states.shape[0]
        scale = math.sqrt(hidden_states.shape[-1])

        # Expand concept embeddings to batch
        C = concept_embeddings.unsqueeze(0).expand(B, -1, -1)  # (B, 111, H)

        # Cross-attention: hidden tokens attend to concepts
        q = self.query(hidden_states)  # (B, seq_len, H)
        k = self.key(C)                # (B, 111, H)
        v = self.value(C)              # (B, 111, H)

        attn_weights = torch.softmax(
            torch.bmm(q, k.transpose(1, 2)) / scale, dim=-1
        )                              # (B, seq_len, 111)
        attn_out = torch.bmm(attn_weights, v)  # (B, seq_len, H)
        attn_out = self.out_proj(attn_out)

        # Gated residual: sigmoid(gate_net([hidden, attn_out])) * attn_out
        gate_in = torch.cat([hidden_states, attn_out], dim=-1)  # (B, seq_len, 2H)
        gate    = torch.sigmoid(self.gate_net(gate_in))          # (B, seq_len, H)
        fused   = self.layer_norm(hidden_states + gate * attn_out)
        return fused


# ── Main Model ────────────────────────────────────────────────────────────────

class ShifaMind2Phase1(nn.Module):
    """
    Concept Bottleneck Model on top of BioClinicalBERT.

    forward() returns a dict so inference.py can access named outputs:
        concept_scores:   (B, 111)  sigmoid-activated, values in [0, 1]
        diagnosis_probs:  (B, 50)   sigmoid-activated, values in [0, 1]
        diagnosis_logits: (B, 50)   raw (for completeness)
    """

    # Hardcoded from checkpoint weight shapes — matches Bio_ClinicalBERT
    _BERT_CONFIG = BertConfig(
        vocab_size=28996,            # word_embeddings.weight [28996, 768]
        hidden_size=768,
        num_hidden_layers=12,        # layers 0-11
        num_attention_heads=12,
        intermediate_size=3072,      # intermediate.dense.weight [3072, 768]
        max_position_embeddings=512, # position_embeddings.weight [512, 768]
        type_vocab_size=2,           # token_type_embeddings.weight [2, 768]
        pad_token_id=0,
    )

    def __init__(
        self,
        num_concepts: int = 111,
        num_classes: int = 50,
        fusion_layers: list[int] | None = None,
    ):
        super().__init__()
        if fusion_layers is None:
            fusion_layers = [9, 11]

        self.num_concepts   = num_concepts
        self.num_classes    = num_classes
        self.fusion_layers  = fusion_layers
        H = self._BERT_CONFIG.hidden_size  # 768

        # BioClinicalBERT backbone (weights loaded from checkpoint, no HF download)
        self.base_model = BertModel(self._BERT_CONFIG, add_pooling_layer=True)

        # Learnable concept prototype matrix (nn.Parameter — not nn.Embedding)
        self.concept_embeddings = nn.Parameter(torch.zeros(num_concepts, H))

        # Concept-aware fusion at specified BERT encoder layers
        self.fusion_modules = nn.ModuleDict({
            str(i): ConceptFusionModule(H) for i in fusion_layers
        })

        # Classification heads applied to pooler [CLS] output
        self.concept_head   = nn.Linear(H, num_concepts)
        self.diagnosis_head = nn.Linear(H, num_classes)

    # ── Forward ──────────────────────────────────────────────────────────────

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:

        # 1. Token + position + type embeddings
        hidden_states = self.base_model.embeddings(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
        )

        # 2. BERT extended attention mask (-10000 for padding positions)
        extended_mask = self.base_model.get_extended_attention_mask(
            attention_mask, input_ids.shape
        )

        # 3. Layer-by-layer encoding with concept fusion at layers 9 and 11
        for i, layer in enumerate(self.base_model.encoder.layer):
            layer_out     = layer(hidden_states, attention_mask=extended_mask)
            hidden_states = layer_out[0]
            if str(i) in self.fusion_modules:
                hidden_states = self.fusion_modules[str(i)](
                    hidden_states, self.concept_embeddings
                )

        # 4. Pool: tanh(dense([CLS]))  — matches base_model.pooler
        pooled = self.base_model.pooler(hidden_states)  # (B, H)

        # 5. Concept and diagnosis predictions from the same pooled representation
        concept_logits   = self.concept_head(pooled)            # (B, 111)
        diagnosis_logits = self.diagnosis_head(pooled)          # (B, 50)

        concept_scores  = torch.sigmoid(concept_logits)         # (B, 111)
        diagnosis_probs = torch.sigmoid(diagnosis_logits)       # (B, 50)

        return {
            "concept_scores":   concept_scores,
            "diagnosis_probs":  diagnosis_probs,
            "diagnosis_logits": diagnosis_logits,
        }
