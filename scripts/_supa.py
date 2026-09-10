"""Tiny Supabase REST helpers for the seed scripts.

Deliberately NOT `supabase-py`. That library validates the key as a JWT at
client construction and raises `SupabaseException("Invalid API key")` on the
newer `sb_secret_…` / `sb_publishable_…` key format, which is what new projects
now issue. The REST API itself accepts either format, and the backend already
talks to Supabase this way, so these scripts do too. One less thing that can
disagree with production.
"""

from __future__ import annotations

import os
import sys


def env() -> tuple[str, str]:
    base = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not base or not key:
        print("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env",
              file=sys.stderr)
        raise SystemExit(1)
    return base, key


def headers(key: str, prefer: str | None = None) -> dict:
    h = {"apikey": key, "Authorization": f"Bearer {key}",
         "Content-Type": "application/json"}
    if prefer:
        h["Prefer"] = prefer
    return h


def create_user(client, base: str, key: str, email: str, password: str) -> tuple[str | None, str]:
    """Create an auth user. Returns (user_id, status) where status is
    'created', 'exists' or an error string."""
    r = client.post(
        f"{base}/auth/v1/admin/users",
        headers=headers(key),
        json={"email": email, "password": password, "email_confirm": True},
    )
    if r.status_code in (200, 201):
        return r.json().get("id"), "created"
    body = r.text.lower()
    if r.status_code in (400, 422) and ("already" in body or "exists" in body):
        return find_user(client, base, key, email), "exists"
    return None, f"HTTP {r.status_code}: {r.text[:200]}"


def find_user(client, base: str, key: str, email: str) -> str | None:
    """Look up an existing auth user by email, paging until found."""
    for page in range(1, 21):
        r = client.get(f"{base}/auth/v1/admin/users",
                       headers=headers(key),
                       params={"page": page, "per_page": 200})
        if r.status_code != 200:
            return None
        users = r.json().get("users", [])
        if not users:
            return None
        for u in users:
            if (u.get("email") or "").lower() == email.lower():
                return u.get("id")
    return None


def upsert_doctor(client, base: str, key: str, row: dict) -> tuple[bool, str]:
    r = client.post(
        f"{base}/rest/v1/doctors",
        headers=headers(key, prefer="resolution=merge-duplicates,return=minimal"),
        json=row,
    )
    if r.status_code in (200, 201, 204):
        return True, "ok"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"
