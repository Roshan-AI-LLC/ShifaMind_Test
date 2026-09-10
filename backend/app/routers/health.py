from fastapi import APIRouter

from ..config import get_settings
from ..schemas.models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Public health check."""
    settings = get_settings()
    from ..models.fullcode import fullcode_state

    return HealthResponse(
        status="ok",
        model_loaded=fullcode_state.get("loaded", False),
        llm_provider=settings.LLM_PROVIDER,
    )


@router.get("/health/model", tags=["health"])
async def model_health():
    """What is actually serving. More detailed than /health on purpose: during
    a cutover the only thing that matters is telling two deployments apart from
    the outside, and "status: ok" cannot do that."""
    from ..models.fullcode import health as fullcode_health
    from ..models.fullcode_inference import MAX_CONCURRENCY

    out = fullcode_health()
    out["max_concurrency"] = MAX_CONCURRENCY
    return out
