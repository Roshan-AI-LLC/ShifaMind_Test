from fastapi import APIRouter
from ..schemas.models import HealthResponse
from ..config import get_settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Public health check endpoint."""
    settings = get_settings()

    # Import here to avoid circular import; model state managed in main.py
    from ..models.loader import model_state

    return HealthResponse(
        status="ok",
        model_loaded=model_state.get("loaded", False),
        llm_provider=settings.LLM_PROVIDER,
    )
