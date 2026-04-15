import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(url, key)

users = client.auth.admin.list_users()
for user in users:
    print(user.id, user.email)
