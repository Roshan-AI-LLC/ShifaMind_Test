import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Query

from ..dependencies import get_admin_doctor
from ..config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


def _service_role_headers(settings) -> dict:
    """
    Build headers that bypass RLS for both key formats:
      - Old JWT keys (eyJ...): Authorization JWT carries role=service_role
      - New sb_secret_ keys:   Supabase allows same value in both headers (backward compat)
    Either way, PostgREST treats the request as service_role → RLS bypassed.
    """
    key = settings.SUPABASE_SERVICE_ROLE_KEY
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


@router.get("/admin/stats", tags=["admin"])
async def get_stats(admin: dict = Depends(get_admin_doctor)):
    """Platform-wide usage statistics (admin only)."""
    settings = get_settings()
    headers = _service_role_headers(settings)

    async with httpx.AsyncClient() as client:
        pred_resp, chat_resp, review_resp, doctor_resp = await _gather(
            client,
            settings.SUPABASE_URL,
            headers,
        )

    predictions_count = _parse_count(pred_resp)
    chat_count = _parse_count(chat_resp)
    review_count = _parse_count(review_resp)
    active_doctors = _parse_count(doctor_resp)

    # Avg rating from reviews
    avg_rating = None
    if review_resp.status_code == 200 and review_resp.json():
        ratings = [r["rating"] for r in review_resp.json() if r.get("rating")]
        if ratings:
            avg_rating = round(sum(ratings) / len(ratings), 2)

    # Top ICD-10 codes from latest predictions
    top_codes: list[dict] = []
    try:
        async with httpx.AsyncClient() as client:
            p_resp = await client.get(
                f"{settings.SUPABASE_URL}/rest/v1/predictions",
                params={"select": "predicted_codes", "order": "created_at.desc", "limit": "200"},
                headers=headers,
            )
        if p_resp.status_code == 200:
            code_freq: dict[str, int] = {}
            for row in p_resp.json():
                for pred in row.get("predicted_codes", []):
                    if pred.get("above_threshold"):
                        code = pred["code"]
                        code_freq[code] = code_freq.get(code, 0) + 1
            top_codes = [
                {"code": k, "count": v}
                for k, v in sorted(code_freq.items(), key=lambda x: -x[1])[:10]
            ]
    except Exception as exc:
        logger.warning(f"Top codes computation failed: {exc}")

    return {
        "total_predictions": predictions_count,
        "total_chat_sessions": chat_count,
        "total_reviews": review_count,
        "active_doctors": active_doctors,
        "avg_rating": avg_rating,
        "top_icd10_codes": top_codes,
    }


@router.get("/admin/reviews", tags=["admin"])
async def list_all_reviews(
    admin: dict = Depends(get_admin_doctor),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Paginated list of all reviews (admin only)."""
    settings = get_settings()
    headers = _service_role_headers(settings)

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/reviews",
            params={
                "select": "id,rating,accuracy_rating,interpretability_rating,comment,created_at,"
                          "doctor:doctors(full_name,email,specialty),"
                          "prediction:predictions(id,input_text)",
                "order": "created_at.desc",
                "limit": str(limit),
                "offset": str(offset),
            },
            headers={**headers, "Prefer": "count=exact"},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to fetch reviews")

    total = int(resp.headers.get("content-range", "0/0").split("/")[-1] or 0)
    return {"reviews": resp.json(), "total": total, "limit": limit, "offset": offset}


# ── helpers ───────────────────────────────────────────────────────────────────

async def _gather(client, base_url, headers):
    import asyncio

    async def get_count(table: str, extra_params: dict = {}):
        return await client.get(
            f"{base_url}/rest/v1/{table}",
            params={"select": "id", "limit": "1", **extra_params},
            headers={**headers, "Prefer": "count=exact"},
        )

    return await asyncio.gather(
        get_count("predictions"),
        get_count("chat_sessions"),
        get_count("reviews"),
        get_count("doctors", {"is_active": "eq.true"}),
    )


def _parse_count(resp) -> int:
    try:
        cr = resp.headers.get("content-range", "0/0")
        return int(cr.split("/")[-1] or 0)
    except Exception:
        return 0
