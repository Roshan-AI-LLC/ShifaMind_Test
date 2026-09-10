#!/usr/bin/env python3
"""Build `code_titles.json` — human-readable titles for all 7,940 codes.

The release folder ships `label_vocab.json` (the codes, in checkpoint order) but
no titles, and the UI cannot show a coder "I50.22" with nothing beside it. Titles
come from MIMIC-IV's own dictionaries, which are credentialed, so this runs on
your machine and its output is uploaded as an artifact.

The label space is NOT diagnoses alone:
    5,802  ICD-10-CM  diagnoses   (carry a decimal point, e.g. A02.0)
    2,138  ICD-10-PCS procedures  (7 alphanumeric chars, e.g. 008Q4ZZ)
so both dictionaries are needed. The join is the fiddly part, which is why this
reuses the training repo's `reformat_icd` rather than reimplementing it: our
label space carries decimals because that is what AMC's pipeline produces, while
MIMIC stores them stripped.

    python scripts/build_code_titles.py \
        --moe   "<...>/ShifaMind-MoE/MoE" \
        --hosp  "<...>/mimiciv/3.1/hosp" \
        --labels "<...>/shifamind_released/data/mimiciv_icd10_full/label_vocab.json" \
        --out    artifacts/fullcode/code_titles.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PCS_RE = re.compile(r"^[A-Z0-9]{7}$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--moe", required=True, help="ShifaMind-MoE/MoE repo root")
    ap.add_argument("--hosp", required=True,
                    help="MIMIC-IV hosp/ dir with d_icd_diagnoses.csv.gz "
                         "and d_icd_procedures.csv.gz")
    ap.add_argument("--labels", required=True, help="label_vocab.json")
    ap.add_argument("--out", default="artifacts/fullcode/code_titles.json")
    args = ap.parse_args()

    sys.path.insert(0, args.moe)
    from shifamind.concepts.descriptions import load_icd_descriptions

    labels: list[str] = json.loads(Path(args.labels).read_text())
    print(f"label space: {len(labels)} codes")

    df = load_icd_descriptions(args.hosp, icd_version=10)
    print(f"MIMIC dictionaries: {len(df)} ICD-10 entries")

    # Same string can name both a diagnosis and a procedure, so index by kind
    # and pick using the code's shape rather than hoping the first row wins.
    by_kind = {
        "diag": dict(zip(df[df.kind == "diag"].code, df[df.kind == "diag"].title)),
        "proc": dict(zip(df[df.kind == "proc"].code, df[df.kind == "proc"].title)),
    }

    out: dict[str, dict] = {}
    missing: list[str] = []
    for code in labels:
        kind = "proc" if (PCS_RE.match(code) and "." not in code) else "diag"
        title = by_kind[kind].get(code)
        if title is None:                       # fall back to the other book
            other = "diag" if kind == "proc" else "proc"
            title = by_kind[other].get(code)
            if title is not None:
                kind = other
        if title is None:
            missing.append(code)
            continue
        out[code] = {"title": title, "kind": kind}

    n_diag = sum(1 for v in out.values() if v["kind"] == "diag")
    n_proc = sum(1 for v in out.values() if v["kind"] == "proc")
    print(f"resolved {len(out)}/{len(labels)}  ({n_diag} diagnoses, {n_proc} procedures)")

    if missing:
        print(f"\n{len(missing)} codes have no title, first 20: {missing[:20]}")
        print("These will render as a bare code in the UI. If the count is "
              "large, the hosp/ dir is probably the wrong MIMIC version.")

    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=0, sort_keys=True))
    print(f"\nwrote {dest}  ({dest.stat().st_size / 1024:.0f} KB)")
    return 0 if len(out) >= len(labels) * 0.95 else 1


if __name__ == "__main__":
    raise SystemExit(main())
