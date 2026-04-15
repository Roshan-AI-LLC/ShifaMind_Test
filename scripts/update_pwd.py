import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()
base = os.environ.get("SUPABASE_URL", "").rstrip("/")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}

def update_pwd(email, new_pwd):
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(f"{base}/auth/v1/admin/users", headers=headers)
        if resp.status_code == 200:
            users = resp.json().get("users", [])
            for u in users:
                if u.get("email") == email:
                    uid = u["id"]
                    upd = client.put(f"{base}/auth/v1/admin/users/{uid}", headers=headers, json={"password": new_pwd})
                    print(f"Updated {email} status: {upd.status_code}")
                    return
        print(f"User {email} not found.")

update_pwd("demo@shifamind.me", "Demo@Shifa2025!")
update_pwd("admin@shifamind.me", "Admin@Shifa2025!")
