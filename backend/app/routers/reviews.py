import logging
import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_doctor
from ..schemas.models import ReviewRequest, ReviewResponse
from ..config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/reviews", response_model=ReviewResponse, tags=["reviews"])
async def submit_review(
    request: ReviewRequest,
    doctor: dict = Depends(get_current_doctor),
):
    """Submit a feedback review for a prediction."""
    settings = get_settings()
    token = doctor.get("_token", "")
    review_id = str(uuid.uuid4())

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.SUPABASE_URL}/rest/v1/reviews",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            json={
                "id": review_id,
                "prediction_id": request.prediction_id,
                "doctor_id": doctor["id"],
                "rating": request.rating,
                "accuracy_rating": request.accuracy_rating,
                "interpretability_rating": request.interpretability_rating,
                "comment": request.comment,
                "corrections": request.corrections,
            },
        )

    if resp.status_code not in (200, 201):
        body = resp.json()
        # Handle unique constraint (already reviewed)
        if "duplicate" in str(body).lower() or resp.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reviewed this prediction.",
            )
        logger.error(f"Review save failed: {body}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to save review")

    row = resp.json()[0] if isinstance(resp.json(), list) else resp.json()
    return ReviewResponse(id=row["id"], created_at=row["created_at"])
