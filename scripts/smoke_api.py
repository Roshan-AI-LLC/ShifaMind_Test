#!/usr/bin/env python3
"""Phase 6 smoke checks against the DEPLOYED API.

scripts/smoke_fullcode.py loads the model in-process; it proves the checkpoint
is sane and says nothing about the service. This exercises the thing a user
actually hits: sign in, POST notes, and check the response is not merely
HTTP 200 but structurally usable.

Each check exists because its failure is silent from the outside:

  * empty code list          -> the UI renders a blank result and looks broken
  * code outside the vocab   -> label_vocab and the checkpoint disagree, which
                                means every code shown is the wrong label
  * concept with no span     -> the evidence link is decorative. This is the
                                product claim; a code we cannot point at a
                                quoted span for is worse than no code
  * concept_share != 1.0     -> composition regressed away from strict, so the
                                100% attribution claim is false

Usage:
    python scripts/smoke_api.py --url https://api.roshan-ai.com \
        --email demo@roshan-ai.com --password '…' --limit 20
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="API base, no trailing slash")
    ap.add_argument("--email", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--vocab", default="artifacts/fullcode/label_vocab.json")
    a = ap.parse_args()

    load_env()
    base = os.environ["SUPABASE_URL"].rstrip("/")
    anon = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.environ["SUPABASE_ANON_KEY"]
    api = a.url.rstrip("/")

    vocab_raw = json.loads(Path(a.vocab).read_text())
    vocab = set(vocab_raw if isinstance(vocab_raw, list) else vocab_raw.keys())
    print(f"vocabulary: {len(vocab):,} codes")

    c = httpx.Client(timeout=180.0)

    # ── model identity, before anything else ─────────────────────────────
    r = c.get(f"{api}/api/health/model")
    if r.status_code != 200:
        print(f"FAIL  /api/health/model -> HTTP {r.status_code} {r.text[:200]}")
        return 1
    h = r.json()
    print("deployed model:", json.dumps(h, indent=None)[:300])
    for field, want in (("codes", 7940), ("concepts", 16227), ("compose", "strict")):
        got = h.get(field)
        if got != want:
            print(f"FAIL  health.{field} = {got!r}, expected {want!r}")
            return 1

    # ── auth ─────────────────────────────────────────────────────────────
    r = c.post(f"{base}/auth/v1/token", params={"grant_type": "password"},
               headers={"apikey": anon, "Content-Type": "application/json"},
               json={"email": a.email, "password": a.password})
    if r.status_code != 200:
        print(f"FAIL  sign-in -> HTTP {r.status_code} {r.text[:200]}")
        print("      (if this is 'Invalid API key', the box and this .env are on "
              "different Supabase projects)")
        return 1
    tok = r.json()["access_token"]
    auth = {"Authorization": f"Bearer {tok}"}

    # ── notes ────────────────────────────────────────────────────────────
    r = c.get(f"{base}/rest/v1/sample_notes",
              params={"select": "id,title,text", "is_active": "eq.true",
                      "limit": str(a.limit)},
              headers={"apikey": anon, **auth})
    notes = r.json() if r.status_code == 200 else []
    if not notes:
        # PostgREST answers 400 for a column that does not exist, and the body
        # names it. Printing it turns a schema drift into a one-line fix.
        print(f"FAIL  no sample notes (HTTP {r.status_code}) {r.text[:300]}")
        return 1
    print(f"notes: {len(notes)}\n")

    lat, fails = [], []
    for i, n in enumerate(notes, 1):
        t0 = time.perf_counter()
        r = c.post(f"{api}/api/predict", headers=auth,
                   json={"text": n["text"], "top_concepts": 8})
        dt = (time.perf_counter() - t0) * 1000
        title = (n.get("title") or "")[:38]

        if r.status_code != 200:
            fails.append(f"{title}: HTTP {r.status_code} {r.text[:120]}")
            print(f"  {i:2}. FAIL  {title:40} HTTP {r.status_code}")
            continue

        d = r.json()
        lat.append(dt)
        picked = [x for x in d["codes"] if x["above_threshold"]]
        why = []

        if not picked and not d.get("no_code_met_threshold"):
            why.append("empty code list")
        bad = [x["code"] for x in picked if x["code"] not in vocab]
        if bad:
            why.append(f"codes outside vocab: {bad[:3]}")
        spanless = [x["code"] for x in picked
                    if not any(cc.get("spans") for cc in x.get("concepts", []))]
        if spanless:
            why.append(f"no concept with a span: {spanless[:3]}")
        share = d.get("concept_share")
        if share is not None and abs(share - 1.0) > 1e-6:
            why.append(f"concept_share={share}")

        mark = "FAIL " if why else "ok   "
        if why:
            fails.append(f"{title}: {'; '.join(why)}")
        print(f"  {i:2}. {mark} {title:40} {len(picked):3} codes  "
              f"{d['routing']['concepts_routed']:4} routed  "
              f"{d['routing']['concepts_suppressed']:3} suppressed  {dt:7.0f} ms")

    print()
    if lat:
        lat.sort()
        p95 = lat[min(len(lat) - 1, int(len(lat) * 0.95))]
        print(f"latency  median {statistics.median(lat):.0f} ms   "
              f"p95 {p95:.0f} ms   max {lat[-1]:.0f} ms")
    print(f"result   {len(lat) - len(fails)}/{len(notes)} clean")
    for f in fails:
        print("  !", f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
