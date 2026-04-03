"""
Model loader — downloads Phase 1 weights + metadata from S3 (or local path)
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
    "concepts": None,     # list[str] — concept names in checkpoint order
    "icd_codes": None,    # list[str] — ICD-10 codes in checkpoint order
    "icd_descriptions": None,  # dict[str, str] — code → human description
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
    Load Phase 1 model + tokenizer + thresholds + metadata into model_state.
    Called once from FastAPI lifespan at startup.
    """
    try:
        import torch
        from transformers import AutoTokenizer
    except ImportError:
        logger.warning(
            "torch / transformers not installed — model will NOT be loaded. "
            "Install them with: pip install torch transformers"
        )
        return

    # Add repo root to sys.path so we can import model/
    repo_root = Path(__file__).resolve().parents[3]  # models/→app/→backend/→repo root
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    try:
        from model.phase1_model import ShifaMindMCB
        from model.config import MODERNBERT_MODEL
    except ImportError as exc:
        logger.error(f"Cannot import model definition: {exc}")
        return

    device = settings.DEVICE
    model_state["device"] = device

    if settings.MODEL_SOURCE == "s3":
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            files = {
                "weights":       (settings.S3_MODEL_KEY,       tmp / "phase1_best.pt"),
                "thresholds":    (settings.S3_THRESHOLDS_KEY,  tmp / "optimal_thresholds.json"),
                "concept_list":  (settings.S3_CONCEPT_LIST_KEY, tmp / "concept_list.json"),
                "icd10_info":    (settings.S3_ICD10_INFO_KEY,   tmp / "top50_icd10_info.json"),
            }
            for name, (key, dest) in files.items():
                try:
                    _download_from_s3(settings.S3_BUCKET, key, dest, settings)
                except Exception as exc:
                    logger.error(f"S3 download failed for {name} ({key}): {exc}. Model will not be loaded.")
                    return
            _load_weights(
                tmp / "phase1_best.pt",
                tmp / "optimal_thresholds.json",
                tmp / "concept_list.json",
                tmp / "top50_icd10_info.json",
                device,
                MODERNBERT_MODEL,
            )
    else:
        weights_path      = Path(settings.LOCAL_MODEL_PATH)
        thresholds_path   = Path(settings.LOCAL_THRESHOLDS_PATH)
        concept_list_path = Path(settings.LOCAL_CONCEPT_LIST_PATH)
        icd10_info_path   = Path(settings.LOCAL_ICD10_INFO_PATH)

        if not weights_path.exists():
            logger.warning(
                f"Local model not found at {weights_path}. "
                "Place phase1_best.pt there or set MODEL_SOURCE=s3."
            )
            return
        _load_weights(weights_path, thresholds_path, concept_list_path, icd10_info_path,
                      device, MODERNBERT_MODEL)


def _load_weights(
    weights_path: Path,
    thresholds_path: Path,
    concept_list_path: Path,
    icd10_info_path: Path,
    device: str,
    model_name: str,
) -> None:
    import torch
    from transformers import AutoTokenizer
    from model.phase1_model import ShifaMindMCB

    # ── Load metadata files first ──────────────────────────────────────────────
    if not concept_list_path.exists():
        logger.error(f"concept_list.json not found at {concept_list_path}")
        return
    if not icd10_info_path.exists():
        logger.error(f"top50_icd10_info.json not found at {icd10_info_path}")
        return

    with open(concept_list_path) as f:
        concepts = json.load(f)  # list[str]
    with open(icd10_info_path) as f:
        icd10_info = json.load(f)

    # top50_icd10_info.json has key "top_50_codes" → list[str]
    icd_codes = icd10_info["top_50_codes"]

    # Build description map — icd10_info may carry descriptions too
    icd_descriptions = icd10_info.get("descriptions", {})
    if not icd_descriptions:
        # Fall back to repo model/icd10_descriptions.json if available
        repo_root = Path(__file__).resolve().parents[3]
        desc_path = repo_root / "model" / "icd10_descriptions.json"
        if desc_path.exists():
            with open(desc_path) as f:
                icd_descriptions = json.load(f)

    num_concepts = len(concepts)
    num_labels = len(icd_codes)
    logger.info(f"Concept list: {num_concepts} concepts, ICD-10 list: {num_labels} codes")

    # ── Load tokenizer ──────────────────────────────────────────────────────────
    logger.info(f"Loading ModernBERT tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # ── Load checkpoint ─────────────────────────────────────────────────────────
    logger.info(f"Loading model weights from {weights_path}...")
    ckpt = torch.load(weights_path, map_location=device, weights_only=False)

    # Config stored in checkpoint overrides our constants
    ckpt_config = ckpt.get("config", {})
    ckpt_model_name = ckpt_config.get("model_name", model_name)
    ckpt_num_concepts = ckpt_config.get("num_concepts", num_concepts)
    ckpt_num_labels = ckpt_config.get("num_labels", num_labels)

    model = ShifaMindMCB(
        num_concepts=ckpt_num_concepts,
        num_labels=ckpt_num_labels,
        model_name=ckpt_model_name,
        attn_impl="eager",  # CPU inference — eager avoids SDPA dtype issues
    )

    state_dict = ckpt.get("model_state_dict", ckpt)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # ── Thresholds ──────────────────────────────────────────────────────────────
    # optimal_thresholds.json structure:
    #   {"per_label_thresholds": {"E785": 0.4, ...}, "global_threshold": 0.5, ...}
    thresholds = {}
    if thresholds_path.exists():
        with open(thresholds_path) as f:
            raw = json.load(f)
        # Support both flat dict (legacy) and nested format from v2.1 training
        if "per_label_thresholds" in raw:
            thresholds = raw["per_label_thresholds"]
        else:
            thresholds = raw
        logger.info(f"Loaded {len(thresholds)} tuned thresholds.")
    else:
        logger.warning("optimal_thresholds.json not found — using default 0.50")

    model_state.update({
        "loaded": True,
        "model": model,
        "tokenizer": tokenizer,
        "thresholds": thresholds,
        "concepts": concepts,
        "icd_codes": icd_codes,
        "icd_descriptions": icd_descriptions,
    })
    logger.info(
        f"ShifaMindMCB v2.1 loaded — {num_concepts} concepts, {num_labels} codes, device={device}"
    )
