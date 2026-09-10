#!/usr/bin/env python3
"""Phase 2a — router parity. Run this on the Mac, in the MoE training venv.

Asserts that the SERVING router (`backend/app/models/router.py`) produces
byte-identical routing to the TRAINING path, on the same notes.

Why this and not F1: a router that drifts by two surface forms in a hundred
notes still lands inside 0.001 micro-F1, while the gate values shown to a
clinician on those notes are wrong. Metric parity cannot see that. This can.

The reference side does not approximate training, it re-runs it: the same
`ConceptMatcher` construction as `shifamind/concepts/silver.py:_silver_chunk`,
the same scipy CSR assembly as `build_silver`, and the same top-k selection as
`ShifaMindDataset.__getitem__`, including CSR's ascending-index ordering.

    python scripts/parity_router.py \
        --moe "/Users/<you>/Documents/Claude/Projects/ShifaMind-MoE/MoE" \
        --bank "/Users/<you>/Documents/Personal/Code Repos/shifamind_released/concepts/banks/merged_umls_records.jsonl"

Exit code 0 means every array matched. Anything else means do not deploy.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

TOP_K = 384
ROUTE = ("affirmed", "negated")


def load_notes(args) -> list[str]:
    if args.notes:
        p = Path(args.notes)
        if p.suffix == ".feather":
            import pandas as pd
            df = pd.read_feather(p)
            for col in ("text", "text_light", "note", "TEXT"):
                if col in df.columns:
                    return df[col].astype(str).tolist()[: args.limit]
            raise SystemExit(
                f"{p.name} has no text column. Columns are: {list(df.columns)}. "
                f"This file is probably splits only, not note text.")
        data = json.loads(p.read_text())
        rows = data if isinstance(data, list) else list(data.values())
        return [r["text"] for r in rows][: args.limit]
    seed = Path(__file__).parent / "sample_notes_seed.json"
    rows = json.loads(seed.read_text())
    print(f"no --notes given, using {len(rows)} bundled sample notes")
    return [r["text"] for r in rows][: args.limit]


def reference_routing(texts: list[str], bank_path: Path, top_k: int = TOP_K):
    """The training path, re-run. Not a reimplementation of it."""
    from scipy import sparse

    from shifamind.concepts.bank import canonicalize, surface_map
    from shifamind.concepts.evalsetup import numeric_map_for
    from shifamind.concepts.negex import Assertion, ConceptMatcher
    from shifamind.concepts.numeric import RULES
    from shifamind.data.text import LIGHT_PREPROCESSOR
    import pandas as pd

    records = [json.loads(l) for l in bank_path.read_text().splitlines() if l.strip()]
    bank, _ = canonicalize(records)
    cids = list(bank.keys())
    index = {c: i for i, c in enumerate(cids)}

    # 12_silver_labels.py --text-col text_light (its default)
    light = LIGHT_PREPROCESSOR(pd.Series(texts)).tolist()

    m = ConceptMatcher(surface_map(bank), numeric_rules=RULES,
                       numeric_map=numeric_map_for(bank))

    # build_silver: one CSR per assertion class, counts not presence
    rows, cols, vals = [], [], []
    for i, t in enumerate(light):
        summary, _ = m.match(t or "")
        for a in ROUTE:
            for cid, n in summary.bucket(Assertion(a)).items():
                if n:
                    rows.append(i); cols.append(index[cid]); vals.append(float(n))
    route = sparse.csr_matrix((vals, (rows, cols)),
                              shape=(len(light), len(cids)), dtype=np.float32)
    route.sum_duplicates()          # affirmed + negated land in the same cell

    # ShifaMindDataset.__getitem__
    out = []
    for i in range(route.shape[0]):
        r = route[i]
        c, n = r.indices, r.data
        if len(c) > top_k:
            keep = np.lexsort((c, -n))[:top_k]
            c = c[keep]
        out.append(c.astype(np.int64))
    return out, light


def candidate_routing(texts: list[str], bank_path: Path, backend: Path,
                      top_k: int = TOP_K):
    sys.path.insert(0, str(backend))
    from app.models.router import ConceptRouter, light_text
    r = ConceptRouter(bank_path, top_k=top_k)
    return [r.route(t, keep_spans=False).concept_ids for t in texts], \
           [light_text(t) for t in texts]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--moe", required=True, help="ShifaMind-MoE/MoE repo root")
    ap.add_argument("--bank", required=True, help="merged_umls_records.jsonl")
    ap.add_argument("--notes", default="", help="feather or json; default = bundled samples")
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--top-k", type=int, default=TOP_K,
                    help="lower it (e.g. 50) to force the overflow branch: the "
                         "lexsort tie-break only runs when a note routes more "
                         "concepts than top_k, and short notes never reach 384")
    args = ap.parse_args()

    sys.path.insert(0, args.moe)
    backend = Path(__file__).resolve().parent.parent / "backend"
    bank_path = Path(args.bank)

    texts = load_notes(args)
    print(f"comparing {len(texts)} notes at top_k={args.top_k}\n")

    ref, ref_light = reference_routing(texts, bank_path, args.top_k)
    cand, cand_light = candidate_routing(texts, bank_path, backend, args.top_k)

    fails = 0

    # 0. text preprocessing must agree before anything else is meaningful
    for i, (a, b) in enumerate(zip(ref_light, cand_light)):
        if a != b:
            fails += 1
            print(f"note {i}: LIGHT TEXT MISMATCH")
            for j, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"   first diff at char {j}: ref {x!r} vs serving {y!r}")
                    break
            print(f"   len ref {len(a)} vs serving {len(b)}")
            break

    # 1. routing arrays must be identical, element for element
    for i, (a, b) in enumerate(zip(ref, cand)):
        if a.shape == b.shape and np.array_equal(a, b):
            print(f"note {i:3d}  {a.size:4d} concepts  OK")
            continue
        fails += 1
        print(f"note {i:3d}  MISMATCH  ref {a.size} vs serving {b.size}")
        sa, sb = set(a.tolist()), set(b.tolist())
        only_ref, only_cand = sorted(sa - sb)[:10], sorted(sb - sa)[:10]
        if only_ref:
            print(f"   in training only : {only_ref}")
        if only_cand:
            print(f"   in serving only  : {only_cand}")
        if sa == sb:
            print("   same concepts, DIFFERENT ORDER — check the top-k lexsort "
                  "and the CSR ascending-index path")

    over = sum(1 for a in ref if a.size == args.top_k)
    print()
    if over:
        print(f"overflow branch exercised on {over}/{len(ref)} notes "
              f"(routed > top_k, lexsort tie-break ran)")
    else:
        print(f"WARNING: no note exceeded top_k={args.top_k}, so the lexsort "
              f"tie-break was NEVER TESTED. Re-run with a smaller --top-k.")
    if fails:
        print(f"FAIL — {fails} mismatch(es). Do not deploy. Fix the router first.")
        return 1
    print(f"PASS — {len(ref)} notes, routing identical. Phase 2a gate cleared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
