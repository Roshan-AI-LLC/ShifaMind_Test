from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import health, predict, notes, chat, reviews, admin
from .models.fullcode import load_fullcode

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load model. Shutdown: clean up."""
    settings = get_settings()
    logger.info("ShifaMind API starting up...")
    # Blocking and CPU-bound: ~5s warm, minutes on a cold artifact cache. Run it
    # off the event loop so /api/health can answer while the model loads.
    import anyio

    await anyio.to_thread.run_sync(load_fullcode, settings)
    logger.info("Startup complete.")
    yield
    logger.info("ShifaMind API shutting down.")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="ShifaMind API",
        description="Concept-grounded ICD-10 coding across the full 7,940-code space",
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
    app.include_router(predict.router, prefix="/api")
    app.include_router(notes.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(reviews.router, prefix="/api")
    app.include_router(admin.router, prefix="/api")

    return app


app = create_app()
