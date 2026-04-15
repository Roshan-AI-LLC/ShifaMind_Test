from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from .config import get_settings

security = HTTPBearer()


async def get_current_doctor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Verify the Supabase JWT and return the doctor's profile.
    Raises 401 if token is invalid or doctor not found.
    """
    settings = get_settings()
    token = credentials.credentials

    async with httpx.AsyncClient() as client:
        # Verify JWT by calling Supabase /auth/v1/user
        resp = await client.get(
            f"{settings.SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = resp.json()
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # Fetch doctor profile from Supabase REST
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/doctors",
            params={"id": f"eq.{user_id}", "select": "*"},
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )

    if resp.status_code == 200 and resp.json():
        doctor = resp.json()[0]
    else:
        # No doctors row yet — auto-create from auth user data (first login)
        full_name = (
            user.get("user_metadata", {}).get("full_name")
            or user.get("user_metadata", {}).get("name")
            or user.get("email", "").split("@")[0]
        )
        new_doctor = {
            "id": user_id,
            "email": user.get("email", ""),
            "full_name": full_name,
            "role": "doctor",
            "is_active": True,
        }
        async with httpx.AsyncClient() as client:
            # Use service role key to insert into restricted table
            create_resp = await client.post(
                f"{settings.SUPABASE_URL}/rest/v1/doctors",
                params={"on_conflict": "id"},
                headers={
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                    "Content-Type": "application/json",
                    "Prefer": "return=representation,resolution=merge-duplicates",
                },
                json=new_doctor,
            )
        if create_resp.status_code not in (200, 201) or not create_resp.json():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Doctor account could not be created",
            )
        doctor = create_resp.json()[0]

    if not doctor.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    doctor["_token"] = token
    return doctor


async def get_admin_doctor(doctor: dict = Depends(get_current_doctor)) -> dict:
    if doctor.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return doctor
