"""
seed_doctors.py — Create 15 demo doctor accounts in Supabase Auth + doctors table.

Usage:
    python scripts/seed_doctors.py

Uses the Supabase REST API directly rather than `supabase-py`, which rejects the
newer `sb_secret_…` service keys as invalid JWTs. Idempotent: existing accounts
are found and their doctors row is refreshed rather than failing.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import os  # noqa: E402
from _supa import create_user, env, upsert_doctor  # noqa: E402

DEFAULT_PASSWORD = os.environ.get("SEED_PASSWORD", "ShifaMind2025!")

DOCTORS = [
    # (full_name, specialty, institution, email, role)
    ("Dr. Sarah Chen", "Internal Medicine", "General Hospital", "s.chen@shifamind.dev", "doctor"),
    ("Dr. James Okafor", "Cardiology", "Heart Institute", "j.okafor@shifamind.dev", "doctor"),
    ("Dr. Amara Patel", "Pulmonology", "City Medical Center", "a.patel@shifamind.dev", "doctor"),
    ("Dr. Marcus Webb", "Emergency Medicine", "Metro ER", "m.webb@shifamind.dev", "doctor"),
    ("Dr. Fatima Al-Hassan", "Nephrology", "Renal Care Clinic", "f.alhassan@shifamind.dev", "doctor"),
    ("Dr. Elena Vasquez", "Endocrinology", "Diabetes Center", "e.vasquez@shifamind.dev", "doctor"),
    ("Dr. Kwame Asante", "Gastroenterology", "GI Associates", "k.asante@shifamind.dev", "doctor"),
    ("Dr. Priya Nair", "Neurology", "Neuro Institute", "p.nair@shifamind.dev", "doctor"),
    ("Dr. Thomas Müller", "Infectious Disease", "University Hospital", "t.muller@shifamind.dev", "doctor"),
    ("Dr. Aisha Bello", "Hospitalist Medicine", "General Hospital", "a.bello@shifamind.dev", "doctor"),
    ("Dr. Carlos Rivera", "Cardiology", "Heart Institute", "c.rivera@shifamind.dev", "doctor"),
    ("Dr. Mei-Ling Zhang", "Internal Medicine", "Academic Medical Center", "m.zhang@shifamind.dev", "doctor"),
    # Admins
    ("Dr. Omar Shaikh", "Clinical Informatics", "ShifaMind Research", "o.shaikh@shifamind.dev", "admin"),
    ("Dr. Rania Haddad", "Health AI", "ShifaMind Research", "r.haddad@shifamind.dev", "admin"),
    ("Dr. David Kim", "Medical Director", "ShifaMind Research", "d.kim@shifamind.dev", "admin"),
]


def main():
    import httpx

    base, key = env()
    print(f"target: {base}")
    created = updated = failed = 0

    with httpx.Client(timeout=30.0) as client:
        for full_name, specialty, institution, email, role in DOCTORS:
            print(f"  {email:32} ({role})...", end=" ", flush=True)
            user_id, status = create_user(client, base, key, email, DEFAULT_PASSWORD)
            if user_id is None:
                print(f"FAILED — {status}")
                failed += 1
                continue

            ok, msg = upsert_doctor(client, base, key, {
                "id": user_id,
                "full_name": full_name,
                "specialty": specialty,
                "institution": institution,
                "email": email,
                "role": role,
                "is_active": True,
            })
            if not ok:
                print(f"auth {status}, but doctors row FAILED — {msg}")
                failed += 1
            elif status == "created":
                print(f"created ({user_id[:8]}...)")
                created += 1
            else:
                print(f"already existed, row refreshed ({user_id[:8]}...)")
                updated += 1

    print(f"\n{created} created, {updated} refreshed, {failed} failed")
    if failed:
        return 1
    print(f"password for all demo accounts: {DEFAULT_PASSWORD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
