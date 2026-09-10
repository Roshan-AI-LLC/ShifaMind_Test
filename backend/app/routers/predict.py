"""Prediction endpoint. Full-code ShifaMind: 7,940 codes, 16,227 concepts.

The response is the product. Every code carries the concepts that produced it,
each with a signed contribution, its gate value, and the character spans in the
note that fired it. A code without its evidence is what every other ICD coder
already returns.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import numpy as np

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field

from ..config import get_settings
from ..dependencies import get_current_doctor
from ..models.fullcode import fullcode_state
from ..models.fullcode_inference import ModelBusy, predict as run_fullcode, summarise

router = APIRouter()
logger = logging.getLogger(__name__)

#: The model serialises itself with its own semaphore; this executor only keeps
#: the blocking forward pass off the event loop so a queued request cannot stall
#: the health endpoint. max_workers exceeds MAX_CONCURRENCY on purpose: the
#: extra threads wait on the semaphore, they do not run extra forwards.
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="fullcode")

#: The encoder truncates at 6,144 tokens anyway; this stops a multi-megabyte
#: paste from being tokenised at all.
MAX_CHARS = 200_000


def _jsonable(o):
    """Coerce the numpy scalars that ride along in a prediction.

    Concept ids and names are read out of the router's numpy arrays, so a
    payload can carry np.str_/np.int64/np.float32 even though every value
    looks like a plain Python one. httpx's own serialiser raises TypeError on
    those, and inside _persist's except block that is indistinguishable from a
    network failure. Coercing here means the audit write cannot fail for a
    reason the log cannot name."""
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"{type(o).__name__} is not JSON serialisable")


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1)
    threshold: float | None = Field(
        None, ge=0.0, le=1.0,
        description="Override the deployed threshold for this request. Omit to "
                    "use the validation-selected value (0.3).")
    top_concepts: int = Field(8, ge=1, le=64)


@router.post("/predict", tags=["predict"])
async def predict(
    request: PredictRequest,
    response: Response,
    doctor: dict = Depends(get_current_doctor),
):
    if not fullcode_state["loaded"]:
        response.headers["Retry-After"] = "30"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is still loading. A cold start pulls the checkpoint "
                   "and can take a few minutes.")
    if len(request.text) > MAX_CHARS:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Note is {len(request.text):,} characters; "
                   f"the limit is {MAX_CHARS:,}.")

    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(
            _executor,
            partial(run_fullcode, request.text, request.threshold,
                    request.top_concepts),
        )
    except ModelBusy as exc:
        # Not an error: the box holds one forward at a time on purpose, because
        # two concurrent ones exceed its memory.
        logger.warning("rejected, all slots busy: %s", exc)
        response.headers["Retry-After"] = "30"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is busy with another note. Retry shortly.")
    except AssertionError as exc:
        # contributions() refused to reconcile. Never return a prediction whose
        # explanation does not add up: a clinician cannot detect that, and an
        # unverifiable explanation is worse than none.
        logger.exception("attribution failed to reconcile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Attribution did not reconcile: {exc}")
    except Exception as exc:
        logger.exception("inference failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {exc}")

    logger.info("doctor=%s %s", doctor.get("id", "?"), summarise(result))

    prediction_id = str(uuid.uuid4())
    result["prediction_id"] = prediction_id
    await _persist(result, request.text, doctor, prediction_id)
    return result


async def _persist(result: dict, text: str, doctor: dict,
                   prediction_id: str) -> None:
    """Write the prediction to Supabase. Failure here is logged, never fatal:
    a coder waiting on a result should not lose it because the audit write
    timed out."""
    try:
        import httpx

        settings = get_settings()
        token = doctor.get("_token", "")
        codes = [c for c in result["codes"] if c["above_threshold"]]

        payload = {
            "id": prediction_id,
            "doctor_id": doctor["id"],
            "note_source": "custom",
            "input_text": text,
            "predicted_codes": [
                {"code": c["code"], "title": c["title"],
                 "probability": c["probability"]} for c in codes],
            "activated_concepts": [
                {"code": c["code"], "concept": cc["concept"],
                 "name": cc["name"], "contribution": cc["contribution"],
                 "gate": cc["gate"]}
                for c in codes for cc in c["concepts"]],
            "thresholds_used": {c["code"]: result["threshold"]
                                for c in codes},
            # INT column in 001_initial_schema.sql. latency_ms is a
            # float (1109.6), and Postgres rejects that for an integer,
            # which made every persist fail silently and history stay
            # empty while predictions returned fine.
            "inference_time_ms": int(round(result["latency_ms"])),
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{settings.SUPABASE_URL}/rest/v1/predictions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": settings.SUPABASE_ANON_KEY,
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal",
                },
                content=json.dumps(payload, default=_jsonable),
            )
        # Logged on every call, not only on failure. Silence in the log is
        # then unambiguous: it means this code never ran.
        logger.info("persist %s: HTTP %s", prediction_id, resp.status_code)
        if resp.status_code >= 300:
            # Loud on purpose. This failing quietly is what made every
            # prediction succeed while the history page stayed empty.
            logger.error("persist rejected for %s: HTTP %s %s",
                         prediction_id, resp.status_code, resp.text[:300])
    except Exception as exc:
        logger.error("failed to persist prediction %s: %s", prediction_id, exc)
