import logging

from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from ..dependencies import get_current_doctor
from ..schemas.models import SampleNote
from ..config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/notes", response_model=list[SampleNote], tags=["notes"])
async def list_notes(doctor: dict = Depends(get_current_doctor)):
    """Return all active sample notes for the note selector dropdown."""
    settings = get_settings()
    token = doctor.get("_token", "")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/sample_notes",
            params={
                "select": "id,title,category,text,note_length,expected_codes",
                "is_active": "eq.true",
                "order": "category.asc,title.asc",
                "limit": "100",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )

    if resp.status_code != 200:
        logger.error(f"Supabase notes fetch failed: {resp.text}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to fetch notes")

    return resp.json()


@router.get("/notes/{note_id}", response_model=SampleNote, tags=["notes"])
async def get_note(note_id: str, doctor: dict = Depends(get_current_doctor)):
    """Return a single sample note by ID."""
    settings = get_settings()
    token = doctor.get("_token", "")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/sample_notes",
            params={
                "id": f"eq.{note_id}",
                "is_active": "eq.true",
                "select": "id,title,category,text,note_length,expected_codes",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )

    if resp.status_code != 200 or not resp.json():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return resp.json()[0]
