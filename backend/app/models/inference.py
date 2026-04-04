"""
Phase 1 inference — tokenize → predict → threshold → ranked output (v2.1).
"""
import time

from model.config import DEFAULT_THRESHOLD, DEFAULT_CONCEPT_THRESHOLD, INFERENCE_MAX_LENGTH
from .loader import model_state


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
    concepts = model_state["concepts"]
    icd_codes = model_state["icd_codes"]
    icd_descriptions = model_state["icd_descriptions"] or {}

    # ── Tokenize ──
    # Use INFERENCE_MAX_LENGTH (not MAX_SEQ_LENGTH) and no padding so we only
    # process the actual tokens in the note — critical for CPU inference speed.
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=INFERENCE_MAX_LENGTH,
        truncation=True,
        padding=False,
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # ── Inference ──
    t0 = time.perf_counter()
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    inference_ms = int((time.perf_counter() - t0) * 1000)

    # Apply sigmoid to raw logits
    concept_scores = torch.sigmoid(outputs["concept_logits"])[0].cpu().tolist()
    diagnosis_probs = torch.sigmoid(outputs["diagnosis_logits"])[0].cpu().tolist()

    # ── Build predictions ──
    predictions = []
    for idx, (code, prob) in enumerate(zip(icd_codes, diagnosis_probs)):
        threshold = (
            thresholds_map.get(code, DEFAULT_THRESHOLD)
            if apply_tuned_thresholds
            else DEFAULT_THRESHOLD
        )
        predictions.append({
            "rank": 0,  # filled after sort
            "code": code,
            "description": icd_descriptions.get(code, code),
            "confidence": round(prob, 4),
            "threshold": round(threshold, 4),
            "above_threshold": bool(prob >= threshold),
        })

    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    for rank, pred in enumerate(predictions, start=1):
        pred["rank"] = rank

    # ── Build activated concepts ──
    activated_concepts = []
    for concept, score in zip(concepts, concept_scores):
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
            "model_version": "mcb_v2.1",
            "threshold_source": threshold_source,
        },
    }
