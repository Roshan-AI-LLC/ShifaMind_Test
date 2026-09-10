#!/usr/bin/env python3
"""Assemble the five full-code artifacts under the names the loader expects.

The release folder names things after the training run (`w768_honest_best.pt`);
the loader wants stable names so a future seed swap is a file replacement rather
than a code change. This makes symlinks, so the 758MB checkpoint is not copied.

The resulting directory is exactly what gets uploaded to S3 in Phase 4, under
the same five names.

    python scripts/stage_fullcode_artifacts.py \
        --released "<...>/shifamind_released" \
        --out artifacts/fullcode
"""

from __future__ import annotations

import argparse
from pathlib import Path

MAP = {
    "model.pt":            "w768_honest_best.pt",
    "thresholds.json":     "RELEASED/w768_honest_thresholds.json",
    "label_vocab.json":    "data/mimiciv_icd10_full/label_vocab.json",
    "concept_bank.jsonl":  "concepts/banks/merged_umls_records.jsonl",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--released", required=True)
    ap.add_argument("--out", default="artifacts/fullcode")
    ap.add_argument("--copy", action="store_true",
                    help="copy instead of symlink (needed if the target FS "
                         "cannot follow links)")
    args = ap.parse_args()

    rel, out = Path(args.released), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    missing = []
    for name, src_rel in MAP.items():
        src = rel / src_rel
        dst = out / name
        if not src.exists():
            missing.append(str(src)); continue
        if dst.exists() or dst.is_symlink():
            dst.unlink()
        if args.copy:
            import shutil; shutil.copy2(src, dst)
        else:
            dst.symlink_to(src.resolve())
        size = src.stat().st_size / 1e6
        print(f"  {name:22} <- {src_rel}  ({size:,.1f} MB)")

    titles = out / "code_titles.json"
    if titles.exists():
        print(f"  {'code_titles.json':22} already present "
              f"({titles.stat().st_size / 1e3:,.0f} KB)")
    else:
        missing.append(f"{titles} (run scripts/build_code_titles.py first)")

    if missing:
        print("\nMISSING:")
        for m in missing:
            print("  ", m)
        return 1
    print(f"\nstaged into {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
