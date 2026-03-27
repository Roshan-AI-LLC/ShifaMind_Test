"""
Phase 1 inference — tokenize → predict → threshold → ranked output.
"""
import time
import sys
from pathlib import Path

# Ensure model/ directory is importable
repo_root = Path(__file__).resolve().parents[4]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from model.config import CONCEPTS, ICD10_CODES, DEFAULT_THRESHOLD, DEFAULT_CONCEPT_THRESHOLD
from .loader import model_state


def _load_icd10_descriptions() -> dict[str, str]:
    import json
    desc_path = repo_root / "model" / "icd10_descriptions.json"
    if desc_path.exists():
        with open(desc_path) as f:
            return json.load(f)
    return {code: code for code in ICD10_CODES}


_ICD10_DESCRIPTIONS: dict[str, str] = {}


def get_icd10_descriptions() -> dict[str, str]:
    global _ICD10_DESCRIPTIONS
    if not _ICD10_DESCRIPTIONS:
        _ICD10_DESCRIPTIONS = _load_icd10_descriptions()
    return _ICD10_DESCRIPTIONS


def run_inference(text: str, apply_tuned_thresholds: bool = True) -> dict:
    """
    Run Phase 1 inference on a clinical note.

    Returns:
        {
          "predictions": [...],
          "activated_concepts": [...],
          "metadata": {...}
        }
    """
    import torch

    if not model_state["loaded"]:
        raise RuntimeError("Model not loaded. Check startup logs.")

    model = model_state["model"]
    tokenizer = model_state["tokenizer"]
    thresholds_map = model_state["thresholds"] or {}
    device = model_state["device"]
    icd10_desc = get_icd10_descriptions()

    # ── Tokenize ──
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length",
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # ── Inference ──
    t0 = time.perf_counter()
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    inference_ms = int((time.perf_counter() - t0) * 1000)

    concept_scores = outputs["concept_scores"][0].cpu().tolist()   # (111,)
    diagnosis_probs = outputs["diagnosis_probs"][0].cpu().tolist() # (50,)

    # ── Build predictions ──
    predictions = []
    for idx, (code, prob) in enumerate(zip(ICD10_CODES, diagnosis_probs)):
        threshold = (
            thresholds_map.get(code, DEFAULT_THRESHOLD)
            if apply_tuned_thresholds
            else DEFAULT_THRESHOLD
        )
        predictions.append({
            "rank": 0,  # filled after sort
            "code": code,
            "description": icd10_desc.get(code, code),
            "confidence": round(prob, 4),
            "threshold": round(threshold, 4),
            "above_threshold": bool(prob >= threshold),
        })

    # Sort by confidence descending, assign ranks
    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    for rank, pred in enumerate(predictions, start=1):
        pred["rank"] = rank

    # ── Build activated concepts ──
    activated_concepts = []
    for concept, score in zip(CONCEPTS, concept_scores):
        activated_concepts.append({
            "concept": concept,
            "score": round(score, 4),
            "active": bool(score >= DEFAULT_CONCEPT_THRESHOLD),
        })
    activated_concepts.sort(key=lambda x: x["score"], reverse=True)

    threshold_source = "tuned" if (apply_tuned_thresholds and thresholds_map) else "default"

    return {
        "predictions": predictions,
        "activated_concepts": activated_concepts,
        "metadata": {
            "inference_time_ms": inference_ms,
            "model_version": "phase1_v1",
            "threshold_source": threshold_source,
        },
    }
