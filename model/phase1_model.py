"""
ShifaMind Phase 1 Model — inference-only definition (v2.1).

Architecture: ShifaMindMCB — Multiplicative Concept Bottleneck
  backbone         BioClinical-ModernBERT (thomas-sounack/BioClinical-ModernBERT-base)
  concept_embeddings  nn.Embedding(num_concepts, 768)
  cross_attn       nn.MultiheadAttention(768, 8) — concepts attend to tokens
  concept_head     nn.Linear(768 → num_concepts) — from CLS pool
  gate_net         Linear(1536→768,ReLU) → Linear(768→768,Sigmoid)
  bottleneck_norm  nn.LayerNorm(768)
  diagnosis_head   nn.Linear(768 → num_labels)

State-dict key prefix: encoder.*, concept_embeddings.*, cross_attn.*, etc.
Checkpoint format: {"model_state_dict": ..., "config": {...}, ...}
"""

import torch
import torch.nn as nn
from transformers import AutoModel

HIDDEN_SIZE = 768
NUM_HEADS = 8


class ShifaMindMCB(nn.Module):
    """
    Multiplicative Concept Bottleneck with BioClinical ModernBERT.

    forward() returns a dict so inference.py can access named outputs:
        diagnosis_logits: (B, num_labels)   raw — apply sigmoid for probabilities
        concept_logits:   (B, num_concepts) raw — apply sigmoid for scores
        concept_repr:     (B, 768)          concept-grounded text representation
        text_repr:        (B, 768)          CLS pooled text representation
    """

    def __init__(self, num_concepts: int, num_labels: int, model_name: str,
                 attn_impl: str = "eager"):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(
            model_name,
            attn_implementation=attn_impl,
        )

        self.concept_embeddings = nn.Embedding(num_concepts, HIDDEN_SIZE)

        self.cross_attn = nn.MultiheadAttention(
            embed_dim=HIDDEN_SIZE,
            num_heads=NUM_HEADS,
            batch_first=True,
            dropout=0.1,
        )

        self.concept_head = nn.Linear(HIDDEN_SIZE, num_concepts)

        self.gate_net = nn.Sequential(
            nn.Linear(HIDDEN_SIZE * 2, HIDDEN_SIZE),
            nn.ReLU(),
            nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE),
            nn.Sigmoid(),
        )

        self.bottleneck_norm = nn.LayerNorm(HIDDEN_SIZE)
        self.diagnosis_head = nn.Linear(HIDDEN_SIZE, num_labels)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        B = input_ids.size(0)

        # 1. Encode text → H [B, L, 768]
        H = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
        ).last_hidden_state

        # 2. CLS token pool → [B, 768]
        pooled_text = H[:, 0, :]

        # 3. Cross-attention: concept queries attend to token keys/values
        #    key_padding_mask: True = ignore padding, False = attend
        key_padding_mask = (attention_mask == 0)  # [B, L]
        concept_queries = self.concept_embeddings.weight.unsqueeze(0).expand(B, -1, -1)
        Z_c, _ = self.cross_attn(
            query=concept_queries,
            key=H,
            value=H,
            key_padding_mask=key_padding_mask,
        )  # [B, num_concepts, 768]

        # 4. Mean-pool concept representations
        pooled_context = Z_c.mean(dim=1)  # [B, 768]

        # 5. Concept logits from CLS pool
        concept_logits = self.concept_head(pooled_text)  # [B, num_concepts]

        # 6. Gate: combine text + concept-grounded representations
        gate = self.gate_net(
            torch.cat([pooled_text, pooled_context], dim=-1)
        )  # [B, 768]

        # 7. Multiplicative bottleneck + LayerNorm
        bottleneck = self.bottleneck_norm(gate * pooled_context)  # [B, 768]

        # 8. Diagnosis logits
        diagnosis_logits = self.diagnosis_head(bottleneck)  # [B, num_labels]

        return {
            "diagnosis_logits": diagnosis_logits,
            "concept_logits": concept_logits,
            "concept_repr": pooled_context,
            "text_repr": pooled_text,
        }
