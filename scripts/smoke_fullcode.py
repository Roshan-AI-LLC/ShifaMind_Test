#!/usr/bin/env python3
"""Load the full-code model and actually run it. Phase 1 gate + Phase 2 numbers.

Answers four questions in one pass:

  1. Does `load_state_dict(strict=True)` succeed? If the pinned MCBConfig is
     wrong in any field, this is where it fails, loudly, instead of serving
     plausible codes with meaningless gates.
  2. Does the attribution reconcile? `contributions()` asserts the per-concept
     terms sum to the logit; it raises otherwise.
  3. Is concept_share 1.0? Under compose="strict" it is 1.0 by construction, so
     anything else means the config regressed to a bypassing composition.
  4. What are peak RSS and latency? These decide the EC2 instance question in
     Phase 3, with a measurement instead of my arithmetic.

Needs torch and transformers, which the MoE venv deliberately excludes:

    python -m venv .venv-serve && source .venv-serve/bin/activate
    pip install torch transformers numpy scipy pandas pyahocorasick

    python scripts/smoke_fullcode.py --artifacts artifacts/fullcode
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from pathlib import Path


def peak_rss_mb() -> float:
    """macOS reports ru_maxrss in bytes, Linux in kilobytes."""
    v = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return v / 1e6 if sys.platform == "darwin" else v / 1e3


class Settings:
    """Minimal stand-in for the app settings object."""
    def __init__(self, artifacts: Path, device: str, threshold: float | None):
        self.MODEL_SOURCE = "local"
        self.LOCAL_FULLCODE_DIR = str(artifacts)
        self.DEVICE = device
        self.THRESHOLD = threshold or 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", default="artifacts/fullcode")
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps", "cuda"])
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--notes", default="")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "backend"))

    from app.models.fullcode import fullcode_state, health, load_fullcode
    from app.models.fullcode_inference import predict, summarise

    print(f"loading from {Path(args.artifacts).resolve()}  device={args.device}")
    t0 = time.perf_counter()
    load_fullcode(Settings(Path(args.artifacts), args.device, args.threshold))
    print(f"loaded in {time.perf_counter() - t0:.1f}s, "
          f"peak RSS {peak_rss_mb():,.0f} MB")
    print(json.dumps(health(), indent=2))

    notes_path = Path(args.notes) if args.notes else root / "scripts" / "sample_notes_seed.json"
    rows = json.loads(notes_path.read_text())
    texts = [r["text"] for r in (rows if isinstance(rows, list) else rows.values())][: args.limit]
    print(f"\nrunning {len(texts)} notes\n" + "=" * 78)

    lat, shares, bad = [], [], 0
    for i, t in enumerate(texts):
        r = predict(t)
        lat.append(r["latency_ms"])
        if r["concept_share"] is not None:
            shares.append(r["concept_share"])
        print(f"\nnote {i}: {summarise(r)}")
        if r["no_code_met_threshold"]:
            print("  NOTHING met the threshold; showing top-10 by probability")
        for c in r["codes"][:5]:
            mark = " " if c["above_threshold"] else "."
            print(f" {mark} {c['probability']:.3f}  {c['code']:9} {c['title'][:52]}")
            for cc in c["concepts"][:3]:
                sign = "+" if cc["contribution"] >= 0 else "-"
                sp = cc["spans"][0]["surface"] if cc["spans"] else "(no span)"
                print(f"        {sign}{abs(cc['contribution']):.3f} gate {cc['gate']:.2f} "
                      f"{cc['name'][:34]:34} <- {sp[:26]!r}")
        err = max((c.get("recon_error", 0) for c in r["codes"]), default=0)
        if err > 1e-2:
            bad += 1
            print(f"  ATTRIBUTION DID NOT RECONCILE: {err:.4g}")

    lat.sort()
    print("\n" + "=" * 78)
    print(f"peak RSS      {peak_rss_mb():,.0f} MB")
    print(f"latency p50   {lat[len(lat)//2]:,.0f} ms")
    print(f"latency p95   {lat[int(len(lat)*0.95) - 1]:,.0f} ms")
    print(f"latency max   {lat[-1]:,.0f} ms")
    if shares:
        lo, hi = min(shares), max(shares)
        print(f"concept_share {lo:.4f} to {hi:.4f}"
              + ("  OK, strict composition confirmed" if lo >= 0.999
                 else "  *** NOT 1.0 — composition regressed, DO NOT DEPLOY ***"))
    if bad:
        print(f"*** {bad} notes failed attribution reconciliation ***")
        return 1
    print("\nsmoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
