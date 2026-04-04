import asyncio
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_doctor
from ..schemas.models import PredictRequest, PredictResponse
from ..models.loader import model_state
from ..models.inference import run_inference
from ..config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Single-worker executor keeps torch from blocking the event loop
_inference_executor = ThreadPoolExecutor(max_workers=1)


@router.post("/predict", response_model=PredictResponse, tags=["predict"])
async def predict(
    request: PredictRequest,
    doctor: dict = Depends(get_current_doctor),
):
    """
    Run Phase 1 inference on a clinical note.
    Returns ranked ICD-10 predictions + activated clinical concepts.
    """
    if not model_state["loaded"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please try again shortly.",
        )

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            _inference_executor,
            partial(run_inference, request.text, request.apply_tuned_thresholds),
        )
    except Exception as exc:
        logger.exception("Inference failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(exc)}",
        )

    # Persist prediction to Supabase
    prediction_id = str(uuid.uuid4())
    try:
        import httpx
        settings = get_settings()
        token = doctor.get("_token", "")

        async with httpx.AsyncClient() as client:
            await client.post(
                f"{settings.SUPABASE_URL}/rest/v1/predictions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": settings.SUPABASE_ANON_KEY,
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal",
                },
                json={
                    "id": prediction_id,
                    "doctor_id": doctor["id"],
                    "note_source": "custom",
                    "input_text": request.text,
                    "predicted_codes": result["predictions"],
                    "activated_concepts": result["activated_concepts"],
                    "thresholds_used": {p["code"]: p["threshold"] for p in result["predictions"]},
                    "inference_time_ms": result["metadata"]["inference_time_ms"],
                },
            )
    except Exception as exc:
        logger.warning(f"Failed to persist prediction: {exc}")
        # Non-fatal — still return result

    return PredictResponse(
        predictions=result["predictions"],
        activated_concepts=result["activated_concepts"],
        metadata=result["metadata"],
        prediction_id=prediction_id,
    )
