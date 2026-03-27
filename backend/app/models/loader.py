"""
Model loader — downloads Phase 1 weights from S3 (or local path) and
keeps a singleton in memory. Will be fully wired in Part 2.
"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Global model state — populated by load_model() at app startup
model_state: dict = {
    "loaded": False,
    "model": None,
    "tokenizer": None,
    "thresholds": None,
}


async def load_model(settings) -> None:
    """
    Placeholder loader called from FastAPI lifespan.
    Full implementation (BioClinicalBERT + CBM) added in Part 2.
    """
    logger.info("Model loader: skipping (Part 2 implementation pending)")
    model_state["loaded"] = False
