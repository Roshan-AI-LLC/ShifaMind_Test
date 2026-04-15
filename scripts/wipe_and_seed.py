import os
import sys
import httpx
import uuid
import subprocess
from dotenv import load_dotenv

load_dotenv()

base = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
pwd = os.environ.get("SEED_PASSWORD", "ShifaMind2025!").strip()

if not base or not key:
    print("Keys missing")
    sys.exit(1)

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}

with httpx.Client(timeout=60.0) as client:
    resp = client.get(f"{base}/auth/v1/admin/users", headers=headers)
    if resp.status_code == 200:
        users = resp.json().get("users", [])
        for u in users:
            uid = u["id"]
            client.delete(f"{base}/auth/v1/admin/users/{uid}", headers=headers)
        print(f"Deleted {len(users)} legacy users.")
    else:
        print(f"Failed to fetch users: {resp.text}")

subprocess.run([sys.executable, "scripts/seed_notes.py"])
print("Sample notes re-seeded.")

accounts = [
    {"email": "demo@shifamind.me", "role": "doctor", "name": "Demo Doctor"},
    {"email": "admin@shifamind.me", "role": "admin", "name": "Admin ShifaMind"},
]

with httpx.Client(timeout=30.0) as client:
    for acc in accounts:
        auth_resp = client.post(f"{base}/auth/v1/admin/users", headers=headers, json={
            "email": acc["email"],
            "password": pwd,
            "email_confirm": True
        })
        if auth_resp.status_code in (200, 201):
            uid = auth_resp.json()["id"]
            insert_headers = {**headers, "Prefer": "return=minimal"}
            client.post(f"{base}/rest/v1/doctors", headers=insert_headers, json={
                "id": uid,
                "email": acc["email"],
                "full_name": acc["name"],
                "role": acc["role"],
                "is_active": True
            })
            print(f"Created {acc['email']} - {acc['role']}")
        else:
            print(f"Failed to create {acc['email']}: {auth_resp.text}")

print("Initialization complete.")
