#!/usr/bin/env python3
"""Create ONE real account (yours) in Supabase Auth + the doctors table.

`seed_doctors.py` creates 15 fictional demo accounts on @shifamind.dev. This
creates a single real one you can actually log in with, with `email_confirm`
set so you skip the confirmation email entirely.

    python scripts/create_admin.py --email you@example.com --name "Your Name"

Prompts for the password if --password is omitted, so it stays out of your
shell history. Idempotent: re-running updates the doctors row instead of
failing, and reports if the auth user already exists.
"""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> int:
    import httpx

    from _supa import create_user, env, upsert_doctor

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--password", default="")
    ap.add_argument("--role", default="admin", choices=["admin", "doctor"])
    ap.add_argument("--specialty", default="Clinical Informatics")
    ap.add_argument("--institution", default="Roshan AI")
    args = ap.parse_args()

    base, key = env()
    print(f"target: {base}")

    password = args.password or getpass.getpass("password for the new account: ")
    if len(password) < 8:
        print("password must be at least 8 characters")
        return 1

    with httpx.Client(timeout=30.0) as client:
        user_id, status = create_user(client, base, key, args.email, password)
        if user_id is None:
            print(f"could not create or find the auth user: {status}")
            return 1
        print(f"auth user {status}: {user_id}")
        if status == "exists":
            print("note: the existing password was NOT changed")

        ok, msg = upsert_doctor(client, base, key, {
            "id": user_id,
            "full_name": args.name,
            "specialty": args.specialty,
            "institution": args.institution,
            "email": args.email,
            "role": args.role,
            "is_active": True,
        })
        if not ok:
            print(f"doctors row failed: {msg}")
            return 1

    print(f"doctors row upserted, role={args.role}")
    print("\nyou can now sign in with this email and password")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
