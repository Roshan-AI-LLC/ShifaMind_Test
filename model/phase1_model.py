"""
ShifaMind Phase 1 Model — inference-only definition.

Architecture:
  1. BioClinicalBERT encoder → [CLS] embedding (768-dim)
  2. Concept head: Linear(768 → 111) → sigmoid → concept_scores
  3. Learnable concept embeddings: (111, 768)
  4. Cross-attention injection at BERT layers [9, 11]:
       - concept_scores used as attention bias
  5. Multiplicative gate: concept_scores[:, :, None] * concept_embeddings
       → pooled concept feature (768-dim)
  6. Diagnosis head: Linear(768 → 50) → logits → sigmoid
  7. Concept completeness coefficient = 1.0 (fully concept-bottlenecked)

Only forward() is included — no training logic.
"""

import torch
import torch.nn as nn
from transformers import AutoModel

from .config import (
    BIOCLINICALBERT_MODEL,
    NUM_CONCEPTS,
    NUM_CODES,
    CROSS_ATTENTION_LAYERS,
)


class ConceptCrossAttention(nn.Module):
    """
    Injects concept information into a BERT layer via cross-attention.
    concept_scores shape: (B, C)  where C = NUM_CONCEPTS
    hidden_state shape:   (B, T, H)
    """

    def __init__(self, hidden_size: int, num_concepts: int):
        super().__init__()
        self.num_concepts = num_concepts
        # Project concept scores to per-token attention bias
        self.concept_proj = nn.Linear(num_concepts, hidden_size, bias=False)
        self.gate = nn.Linear(hidden_size * 2, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, hidden_state: torch.Tensor, concept_scores: torch.Tensor) -> torch.Tensor:
        # concept_scores: (B, C) → (B, H)
        concept_feat = self.concept_proj(concept_scores)  # (B, H)
        concept_feat = concept_feat.unsqueeze(1).expand_as(hidden_state)  # (B, T, H)

        # Gated fusion
        combined = torch.cat([hidden_state, concept_feat], dim=-1)  # (B, T, 2H)
        gate_val = torch.sigmoid(self.gate(combined))  # (B, T, H)
        fused = hidden_state * gate_val + concept_feat * (1 - gate_val)
        return self.norm(fused)


class ShifaMind2Phase1(nn.Module):
    """
    Concept Bottleneck Model on top of BioClinicalBERT.
    Concept completeness = 1.0 — diagnoses predicted solely through concepts.
    """

    def __init__(
        self,
        bert_model_name: str = BIOCLINICALBERT_MODEL,
        num_concepts: int = NUM_CONCEPTS,
        num_codes: int = NUM_CODES,
        cross_attention_layers: list[int] = CROSS_ATTENTION_LAYERS,
    ):
        super().__init__()

        self.num_concepts = num_concepts
        self.num_codes = num_codes
        self.cross_attention_layers = cross_attention_layers

        # 1. BioClinicalBERT backbone
        self.bert = AutoModel.from_pretrained(bert_model_name)
        hidden_size = self.bert.config.hidden_size  # 768

        # 2. Concept head: CLS → concept logits
        self.concept_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size // 2, num_concepts),
        )

        # 3. Learnable concept embeddings (111, 768)
        self.concept_embeddings = nn.Embedding(num_concepts, hidden_size)

        # 4. Cross-attention modules for specified BERT layers
        self.cross_attn = nn.ModuleDict({
            str(layer_idx): ConceptCrossAttention(hidden_size, num_concepts)
            for layer_idx in cross_attention_layers
        })

        # 5. Concept bottleneck projection
        self.bottleneck_proj = nn.Linear(hidden_size, hidden_size)

        # 6. Diagnosis head: concept-gated features → ICD-10 logits
        self.diagnosis_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size // 2, num_codes),
        )

    def _encode_with_concept_injection(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        concept_scores: torch.Tensor,
    ) -> torch.Tensor:
        """
        Run BERT encoder, injecting concept context at layers 9 and 11.
        Returns final [CLS] hidden state.
        """
        # Embedding layer
        embedding_output = self.bert.embeddings(input_ids=input_ids)
        hidden_state = embedding_output

        # Build extended attention mask (BERT convention)
        extended_mask = self.bert.get_extended_attention_mask(
            attention_mask, input_ids.shape
        )

        # Run through each encoder layer
        for i, layer in enumerate(self.bert.encoder.layer):
            layer_out = layer(hidden_state, attention_mask=extended_mask)
            hidden_state = layer_out[0]

            if str(i) in self.cross_attn:
                hidden_state = self.cross_attn[str(i)](hidden_state, concept_scores)

        return hidden_state[:, 0, :]  # [CLS] token

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:
        """
        Args:
            input_ids:      (B, T)
            attention_mask: (B, T)
            token_type_ids: (B, T) — optional, ignored if absent

        Returns dict with:
            concept_scores:   (B, 111)  values in [0, 1]
            diagnosis_logits: (B, 50)   raw logits
            diagnosis_probs:  (B, 50)   values in [0, 1]
        """
        # ── Step 1: Initial BERT pass to get CLS for concept head ──
        initial_out = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )
        cls_initial = initial_out.last_hidden_state[:, 0, :]  # (B, H)

        # ── Step 2: Concept scores from initial CLS ──
        concept_logits = self.concept_head(cls_initial)  # (B, C)
        concept_scores = torch.sigmoid(concept_logits)   # (B, C)

        # ── Step 3: Second pass with concept injection ──
        cls_concept_aware = self._encode_with_concept_injection(
            input_ids, attention_mask, concept_scores
        )

        # ── Step 4: Multiplicative gate — concept scores × concept embeddings ──
        # concept_scores: (B, C) → (B, C, 1)
        # concept_embeddings weight: (C, H)
        concept_emb = self.concept_embeddings.weight.unsqueeze(0)  # (1, C, H)
        gated = concept_scores.unsqueeze(-1) * concept_emb          # (B, C, H)
        concept_feature = gated.sum(dim=1)                          # (B, H) pooled

        # ── Step 5: Blend concept-aware CLS with concept feature ──
        bottleneck = self.bottleneck_proj(cls_concept_aware + concept_feature)  # (B, H)

        # ── Step 6: Diagnosis prediction through bottleneck ──
        diagnosis_logits = self.diagnosis_head(bottleneck)      # (B, 50)
        diagnosis_probs = torch.sigmoid(diagnosis_logits)        # (B, 50)

        return {
            "concept_scores": concept_scores,
            "diagnosis_logits": diagnosis_logits,
            "diagnosis_probs": diagnosis_probs,
        }
