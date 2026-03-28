"""
Model loader — downloads Phase 1 weights from S3 (or local path)
and keeps a singleton in memory for the lifetime of the process.
"""
import json
import logging
import sys
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# Global model state populated by load_model() at startup
model_state: dict = {
    "loaded": False,
    "model": None,
    "tokenizer": None,
    "thresholds": None,   # dict[str, float] — per-code optimal thresholds
    "device": "cpu",
}


def _download_from_s3(bucket: str, key: str, dest: Path, settings) -> None:
    """Download a single object from S3 into dest."""
    import boto3

    s3 = boto3.client(
        "s3",
        region_name=settings.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
    )
    logger.info(f"Downloading s3://{bucket}/{key} → {dest}")
    s3.download_file(bucket, key, str(dest))


async def load_model(settings) -> None:
    """
    Load Phase 1 model + tokenizer + thresholds into model_state.
    Called once from FastAPI lifespan at startup.
    """
    # Check that heavy deps are available
    try:
        import torch
        from transformers import AutoTokenizer
    except ImportError:
        logger.warning(
            "torch / transformers not installed — model will NOT be loaded. "
            "Install them with: pip install torch transformers"
        )
        return

    # Add model/ dir to path so we can import ShifaMind2Phase1
    repo_root = Path(__file__).resolve().parents[3]  # models/ → app/ → backend/ → repo root
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    try:
        from model.phase1_model import ShifaMind2Phase1
        from model.config import BIOCLINICALBERT_MODEL, NUM_CONCEPTS, NUM_CODES
    except ImportError as exc:
        logger.error(f"Cannot import model definition: {exc}")
        return

    device = settings.DEVICE
    model_state["device"] = device

    # ── Resolve weight file ──
    if settings.MODEL_SOURCE == "s3":
        with tempfile.TemporaryDirectory() as tmpdir:
            weights_path = Path(tmpdir) / "phase1_best.pt"
            thresholds_path = Path(tmpdir) / "optimal_thresholds.json"
            try:
                _download_from_s3(settings.S3_BUCKET, settings.S3_MODEL_KEY, weights_path, settings)
                _download_from_s3(settings.S3_BUCKET, settings.S3_THRESHOLDS_KEY, thresholds_path, settings)
            except Exception as exc:
                logger.error(f"S3 download failed: {exc}. Model will not be loaded.")
                return
            _load_weights(weights_path, thresholds_path, device)
    else:
        weights_path = Path(settings.LOCAL_MODEL_PATH)
        thresholds_path = Path(settings.LOCAL_THRESHOLDS_PATH)
        if not weights_path.exists():
            logger.warning(
                f"Local model not found at {weights_path}. "
                "Place phase1_best.pt there or set MODEL_SOURCE=s3."
            )
            return
        _load_weights(weights_path, thresholds_path, device)


def _load_weights(weights_path: Path, thresholds_path: Path, device: str) -> None:
    import torch
    from transformers import AutoTokenizer
    from model.phase1_model import ShifaMind2Phase1
    from model.config import BIOCLINICALBERT_MODEL

    logger.info("Loading BioClinicalBERT tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BIOCLINICALBERT_MODEL)

    logger.info(f"Loading model weights from {weights_path}...")
    model = ShifaMind2Phase1()
    state_dict = torch.load(weights_path, map_location=device)
    # Handle wrapped state dicts (e.g. {"model_state_dict": ...})
    if "model_state_dict" in state_dict:
        state_dict = state_dict["model_state_dict"]
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # Thresholds
    thresholds = {}
    if thresholds_path.exists():
        with open(thresholds_path) as f:
            thresholds = json.load(f)
        logger.info(f"Loaded {len(thresholds)} tuned thresholds.")
    else:
        logger.warning("optimal_thresholds.json not found — using default 0.35")

    model_state.update({
        "loaded": True,
        "model": model,
        "tokenizer": tokenizer,
        "thresholds": thresholds,
    })
    logger.info("Phase 1 model loaded successfully.")
