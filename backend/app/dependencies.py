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

    if resp.status_code != 200 or not resp.json():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor account not found or inactive",
        )

    doctor = resp.json()[0]
    if not doctor.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    doctor["_token"] = token
    return doctor


async def get_admin_doctor(doctor: dict = Depends(get_current_doctor)) -> dict:
    if doctor.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return doctor
