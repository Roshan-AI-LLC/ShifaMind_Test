"""
seed_doctors.py — Create 15 doctor accounts in Supabase Auth + doctors table.

Usage:
    pip install supabase python-dotenv
    SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python scripts/seed_doctors.py

The script is idempotent: it skips accounts whose email already exists.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
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
    try:
        from supabase import create_client
    except ImportError:
        print("Error: supabase package not installed. Run: pip install supabase")
        sys.exit(1)

    client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    created, skipped, failed = 0, 0, 0

    for full_name, specialty, institution, email, role in DOCTORS:
        print(f"  Creating {email} ({role})...", end=" ")
        try:
            # Create auth user
            auth_resp = client.auth.admin.create_user({
                "email": email,
                "password": DEFAULT_PASSWORD,
                "email_confirm": True,
            })
            user_id = auth_resp.user.id

            # Upsert doctor profile
            client.table("doctors").upsert({
                "id": user_id,
                "full_name": full_name,
                "specialty": specialty,
                "institution": institution,
                "email": email,
                "role": role,
                "is_active": True,
            }).execute()

            print(f"OK (id={user_id[:8]}...)")
            created += 1

        except Exception as e:
            err = str(e)
            if "already been registered" in err or "already exists" in err:
                print("SKIPPED (already exists)")
                skipped += 1
            else:
                print(f"FAILED — {err}")
                failed += 1

    print(f"\nDone: {created} created, {skipped} skipped, {failed} failed")
    print(f"Default password: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    main()
