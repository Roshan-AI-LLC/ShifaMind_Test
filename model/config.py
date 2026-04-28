"""
ShifaMind Phase 1 — model configuration (v2.1).

ICD-10 codes and concept list are loaded at runtime from JSON files
(top50_icd10_info.json and concept_list.json) downloaded from S3.
These constants are fallback defaults only.
"""

# ── Model backbone ────────────────────────────────────────────────────────────
MODERNBERT_MODEL = "thomas-sounack/BioClinical-ModernBERT-base"
MAX_SEQ_LENGTH = 6144          # training context length — do not change
INFERENCE_MAX_LENGTH = 4096    # Increased from 1024 to better match training distribution (6144). Discharge summaries need long context for accurate ICD-10 prediction.

# ── Architecture constants ────────────────────────────────────────────────────
HIDDEN_SIZE = 768
NUM_HEADS = 8

# ── Default thresholds (overridden by optimal_thresholds.json at runtime) ─────
DEFAULT_THRESHOLD = 0.50
DEFAULT_CONCEPT_THRESHOLD = 0.50

# ── Fallback counts (actual lists loaded from JSON at startup) ─────────────────
NUM_CONCEPTS = 111  # updated from concept_list.json at load time
NUM_CODES = 50      # always 50 (top50_icd10_info.json)
