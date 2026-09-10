"""Why is Prediction History empty?

Predictions return fine but no row lands in `predictions`. Three things can
cause that and they need different fixes, so this separates them in one run:

  1. Rows ARE there  -> the backend is fine, the frontend query is wrong.
  2. Insert refused  -> RLS, a column type, or a CHECK constraint. The exact
                        PostgREST message says which.
  3. Insert accepted -> the persist call in predict.py never runs (stale
                        process, exception before it, wrong doctor id).

Run from the repo root with the venv python:

    backend/.venv/bin/python scripts/diag_history.py you@example.com 'password'

The dummy row it writes is deleted again before the script exits.
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main() -> int:
    load_env()
    base = os.environ["SUPABASE_URL"].rstrip("/")
    # config.py reads NEXT_PUBLIC_SUPABASE_ANON_KEY; use the same name the
    # backend does so this script cannot disagree with it.
    anon = (os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
            or os.environ["SUPABASE_ANON_KEY"])
    svc = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    email, password = sys.argv[1], sys.argv[2]

    c = httpx.Client(timeout=20.0)
    svc_h = {"apikey": svc, "Authorization": f"Bearer {svc}"}

    print("project:", base)

    # ── 1. What is actually in the table, ignoring RLS entirely ──────────
    r = c.get(f"{base}/rest/v1/predictions",
              params={"select": "id,doctor_id,created_at,inference_time_ms",
                      "order": "created_at.desc", "limit": "5"},
              headers={**svc_h, "Prefer": "count=exact"})
    print(f"\n[1] service-role read      HTTP {r.status_code}  "
          f"count={r.headers.get('content-range', '?')}")
    if r.status_code == 200:
        for row in r.json():
            print("     ", row["created_at"], row["id"][:8],
                  "doctor", row["doctor_id"][:8], "ms", row["inference_time_ms"])
    else:
        print("     ", r.text[:300])

    # ── 2. Sign in the way the browser does ──────────────────────────────
    r = c.post(f"{base}/auth/v1/token", params={"grant_type": "password"},
               headers={"apikey": anon, "Content-Type": "application/json"},
               json={"email": email, "password": password})
    print(f"\n[2] password sign-in       HTTP {r.status_code}")
    if r.status_code != 200:
        print("     ", r.text[:300])
        return 1
    tok = r.json()["access_token"]
    uid = r.json()["user"]["id"]
    print("      auth.uid() =", uid)

    # ── 3. The doctors row the backend would resolve ─────────────────────
    r = c.get(f"{base}/rest/v1/doctors", params={"id": f"eq.{uid}", "select": "id,email,role,is_active"},
              headers={"apikey": anon, "Authorization": f"Bearer {tok}"})
    print(f"\n[3] doctors row (own JWT)  HTTP {r.status_code}  {r.text[:200]}")

    # ── 4. The exact insert _persist() makes, same headers, same shape ───
    pid = str(uuid.uuid4())
    body = {
        "id": pid,
        "doctor_id": uid,
        "note_source": "custom",
        "input_text": "diag_history.py probe row",
        "predicted_codes": [{"code": "I50.22", "title": "probe", "probability": 0.9}],
        "activated_concepts": [{"code": "I50.22", "concept": "C1", "name": "probe",
                                "contribution": 1.0, "gate": 0.99}],
        "thresholds_used": {"I50.22": 0.3},
        "inference_time_ms": 1234,
    }
    r = c.post(f"{base}/rest/v1/predictions",
               headers={"apikey": anon, "Authorization": f"Bearer {tok}",
                        "Content-Type": "application/json", "Prefer": "return=minimal"},
               json=body)
    print(f"\n[4] insert as the doctor   HTTP {r.status_code}")
    if r.status_code >= 300:
        print("      REFUSED ->", r.text[:400])
        print("      This is the bug. The message above names the column or policy.")
    else:
        print("      accepted. RLS and the column types are fine, so persist()")
        print("      in predict.py is not running or is raising before the POST.")

    # ── 5. What the history page would see ───────────────────────────────
    r = c.get(f"{base}/rest/v1/predictions",
              params={"select": "id,input_text,predicted_codes,created_at",
                      "doctor_id": f"eq.{uid}", "order": "created_at.desc", "limit": "5"},
              headers={"apikey": anon, "Authorization": f"Bearer {tok}"})
    n = len(r.json()) if r.status_code == 200 else -1
    print(f"\n[5] history query (own JWT) HTTP {r.status_code}  rows={n}")
    if r.status_code != 200:
        print("     ", r.text[:300])

    # ── clean up the probe row ───────────────────────────────────────────
    d = c.delete(f"{base}/rest/v1/predictions", params={"id": f"eq.{pid}"}, headers=svc_h)
    print(f"\n      probe row deleted (HTTP {d.status_code})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
