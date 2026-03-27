from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import health
from .models.loader import load_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load model. Shutdown: clean up."""
    settings = get_settings()
    logger.info("ShifaMind API starting up...")
    await load_model(settings)
    logger.info("Startup complete.")
    yield
    logger.info("ShifaMind API shutting down.")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="ShifaMind API",
        description="Clinical decision support — Phase 1 inference + LLM chat",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health.router, prefix="/api")
    # predict, notes, chat, reviews — added in Parts 2 & 3

    return app


app = create_app()
