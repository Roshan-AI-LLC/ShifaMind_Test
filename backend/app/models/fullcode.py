"""Full-code ShifaMind: config, artifacts and loading.

Serves `w768_honest` (seed 10): 7,940 codes, 16,227 concepts, 384 routed slots.
This is the only model the service loads; the 50-code path has been removed.
Rollback is redeploying the previously tagged image, not a switch in here.

EVERY MCBConfig FIELD IS PINNED BELOW. None are inherited. `MCBConfig` defaults
`n_concepts` to 16,245 while the released artifacts have 16,227, and it defaults
`compose` to "free" — an ungated residual bypass — while this checkpoint was
trained "strict". Inheriting either default produces a model that loads without
error and is wrong: the first silently mismatches the concept embedding table,
the second breaks the 100% attribution guarantee the product is sold on.

Source of truth: `RELEASED/w768_honest_log.jsonl` line 0, the training args.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

#: Label space split, for the UI and for sanity checks at load.
N_LABELS = 7_940
N_CONCEPTS = 16_227

#: Validation-selected. `RELEASED/w768_honest_thresholds.json` carries
#: {"micro": 0.3, "macro": 0.1, "split": "val"}. Micro is the default because
#: macro at 0.1 yields precision 0.43 on test, which floods a human reviewer.
DEFAULT_THRESHOLD = 0.30

#: Composition mode. "strict" means no pathway reaches a logit without
#: passing through a concept gate, which is what makes concept_share 1.0
#: and what the 100% attribution claim rests on.
COMPOSE = "strict"

fullcode_state: dict = {
    "loaded": False,
    "model": None,
    "tokenizer": None,
    "router": None,
    "label_vocab": None,       # list[str], checkpoint order
    "code_titles": None,       # {code: {"title":..., "kind": "diag"|"proc"}}
    "threshold": DEFAULT_THRESHOLD,
    "device": "cpu",
    "tag": "w768_honest",
    "seed": 10,
}


def build_config():
    """MCBConfig for this checkpoint. Pinned, field by field."""
    from .mcb import MCBConfig
    return MCBConfig(
        n_concepts=N_CONCEPTS,
        n_labels=N_LABELS,
        hidden=768,
        top_k=384,
        n_heads=8,
        dropout=0.1,
        backbone="thomas-sounack/BioClinical-ModernBERT-base",
        max_len=6_144,
        freeze_backbone_layers=0,
        # Training passed attn=null, so neither kernel is pinned by the
        # checkpoint and the two are mathematically equivalent. "eager"
        # materialises the full (heads, seq, seq) attention matrix, which at
        # ~2,900 tokens is where most of the transient memory goes; "sdpa" uses
        # the memory-efficient path. Switchable so the two can be A/B'd on the
        # real box without a code change: ATTN_IMPL=sdpa.
        attn_implementation=os.environ.get("ATTN_IMPL", "eager"),
        gradient_checkpointing=False,
        gate="concept",
        gate_tied=True,
        gate_act="sigmoid",
        concept_channels=1,
        channel_names=("affirmed",),
        concept_width=768,
        concept_layers=1,
        label_heads=1,
        label_attn="softmax",
        compose=COMPOSE,          # THE attribution guarantee. Do not change.
        # DERIVED, never set independently. 16_train.py:714 reads
        #     use_residual=(not args.no_residual and args.compose != "strict")
        # so under strict the residual module is never CONSTRUCTED and its
        # parameters are absent from the checkpoint. Setting this True builds
        # residual.1.{weight,bias} and load_state_dict(strict=True) fails on two
        # missing keys. It is irrelevant to the forward pass under strict, which
        # is exactly why it is easy to get wrong: the mistake is in __init__,
        # not in forward.
        use_residual=(COMPOSE != "strict"),
        experts="none",
        n_experts=0,
        hier=False,
        n_parents=0,
        w_sparse=0.05,
        w_fidelity=0.3,
        focal_gamma=0.0,
        focal_alpha=0.5,
    )


#: Where S3 artifacts are cached BETWEEN BOOTS. The default sits on the
#: instance's EBS volume, so it survives `docker rm` and an instance stop/start
#: and only a terminate loses it. Downloading 758 MB on every boot is what makes
#: a cold start slow, and this server is only ever cold.
CACHE_DIR = os.environ.get("FULLCODE_CACHE_DIR", "/var/lib/shifamind/fullcode")

ARTIFACTS = {
    "model":      ("S3_FULLCODE_MODEL_KEY",      "model.pt"),
    "thresholds": ("S3_FULLCODE_THRESHOLDS_KEY", "thresholds.json"),
    "labels":     ("S3_FULLCODE_LABELS_KEY",     "label_vocab.json"),
    "bank":       ("S3_FULLCODE_BANK_KEY",       "concept_bank.jsonl"),
    "titles":     ("S3_FULLCODE_TITLES_KEY",     "code_titles.json"),
}


def _fetch_cached(settings, bucket: str, key: str, dest: Path) -> Path:
    """Download only if the cached copy is missing or the wrong size.

    Size, not mtime: a partial download from an interrupted boot has a
    plausible mtime and truncated bytes, and torch.load on a truncated
    checkpoint fails in a way that does not obviously say "re-download me".
    """
    import boto3

    s3 = boto3.client(
        "s3",
        region_name=getattr(settings, "AWS_DEFAULT_REGION", None),
        aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None) or None,
        aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None) or None,
    )
    remote = s3.head_object(Bucket=bucket, Key=key)["ContentLength"]

    if dest.exists() and dest.stat().st_size == remote:
        logger.info("cache hit  %s (%.1f MB)", dest.name, remote / 1e6)
        return dest

    if dest.exists():
        logger.warning("cache size mismatch for %s (%d local vs %d remote), "
                       "re-downloading", dest.name, dest.stat().st_size, remote)

    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    logger.info("downloading s3://%s/%s -> %s (%.1f MB)",
                bucket, key, dest, remote / 1e6)
    s3.download_file(bucket, key, str(part))
    # Atomic rename: an interrupted download leaves a .part, never a file that
    # looks complete and is not.
    part.replace(dest)
    return dest


def _artifact_paths(settings) -> dict[str, Path]:
    """Resolve the five artifacts, from a local dir or from S3 via the cache."""
    if getattr(settings, "MODEL_SOURCE", "s3") != "s3":
        root = Path(getattr(settings, "LOCAL_FULLCODE_DIR", "./artifacts/fullcode"))
        return {k: root / fname for k, (_, fname) in ARTIFACTS.items()}

    cache = Path(getattr(settings, "FULLCODE_CACHE_DIR", CACHE_DIR))
    out = {}
    for k, (setting_name, fname) in ARTIFACTS.items():
        key = getattr(settings, setting_name, "")
        if not key:
            raise RuntimeError(f"{setting_name} is not configured")
        out[k] = _fetch_cached(settings, settings.S3_BUCKET, key, cache / fname)
    return out


def load_fullcode(settings) -> None:
    """Populate `fullcode_state`. Raises on anything that would serve wrongly."""
    import torch
    from transformers import AutoTokenizer

    from .mcb import ShifaMindMoE
    from .router import ConceptRouter

    device = getattr(settings, "DEVICE", "cpu")
    cfg = build_config()

    paths = _artifact_paths(settings)
    label_vocab = json.loads(Path(paths["labels"]).read_text())
    if len(label_vocab) != N_LABELS:
        raise RuntimeError(
            f"label_vocab has {len(label_vocab)} codes, expected {N_LABELS}. "
            "Wrong artifact for this checkpoint.")

    code_titles = {}
    if Path(paths["titles"]).exists():
        code_titles = json.loads(Path(paths["titles"]).read_text())
        missing = [c for c in label_vocab if c not in code_titles]
        if missing:
            logger.warning("%d of %d codes have no title; the UI will show "
                           "the bare code for those", len(missing), N_LABELS)
    else:
        logger.warning("no code_titles.json — every code will render bare. "
                       "Build it with scripts/build_code_titles.py")

    raw = json.loads(Path(paths["thresholds"]).read_text())
    threshold = float(getattr(settings, "THRESHOLD", 0) or raw.get("micro", DEFAULT_THRESHOLD))
    if raw.get("split") != "val":
        logger.warning("thresholds file does not say split=val (%r). These "
                       "must be validation-selected, never tuned on test.",
                       raw.get("split"))

    router = ConceptRouter(Path(paths["bank"]), top_k=cfg.top_k)
    if len(router.concept_ids) != N_CONCEPTS:
        raise RuntimeError(
            f"concept bank has {len(router.concept_ids)} concepts, expected "
            f"{N_CONCEPTS}. Wrong bank for this checkpoint.")

    tokenizer = AutoTokenizer.from_pretrained(cfg.backbone)

    logger.info("building model (7,940 codes x 16,227 concepts)...")
    model = ShifaMindMoE(cfg)

    logger.info("loading weights from %s", paths["model"])
    # Trained on an A100; tensors carry cuda:0 in the pickle.
    ckpt = torch.load(paths["model"], map_location="cpu", weights_only=False)
    state = ckpt["model"] if isinstance(ckpt, dict) and "model" in ckpt else ckpt

    # strict=True on purpose. A missing or unexpected key here means the
    # config does not match the checkpoint, and a model that half-loads
    # returns plausible codes with meaningless gates.
    model.load_state_dict(state, strict=True)
    model.to(device).eval()

    if isinstance(ckpt, dict):
        logger.info("checkpoint step=%s epoch=%s",
                    ckpt.get("step"), ckpt.get("epoch"))

    fullcode_state.update({
        "loaded": True,
        "model": model,
        "tokenizer": tokenizer,
        "router": router,
        "label_vocab": label_vocab,
        "code_titles": code_titles,
        "threshold": threshold,
        "device": device,
    })
    logger.info("full-code model ready: %d codes, %d concepts, top_k=%d, "
                "threshold=%.2f, compose=%s",
                N_LABELS, N_CONCEPTS, cfg.top_k, threshold, cfg.compose)


def health() -> dict:
    """What /api/health reports. Enough to tell two deployments apart."""
    s = fullcode_state
    return {
        "variant": "fullcode",
        "tag": s["tag"],
        "seed": s["seed"],
        "loaded": s["loaded"],
        "codes": N_LABELS if s["loaded"] else 0,
        "concepts": N_CONCEPTS if s["loaded"] else 0,
        "threshold": s["threshold"],
        "device": s["device"],
        "compose": COMPOSE,
    }
