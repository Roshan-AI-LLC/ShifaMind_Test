"""
POST /api/chat — SSE streaming chat endpoint.

SSE event format:
  data: {"type": "token",   "content": "...token..."}\n\n
  data: {"type": "done",    "session_id": "uuid"}\n\n
  data: {"type": "error",   "content": "error message"}\n\n
"""
import json
import logging
import uuid
from typing import AsyncIterator

import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from ..dependencies import get_current_doctor
from ..schemas.models import ChatRequest
from ..services.llm_provider import get_llm_provider
from ..prompts.medical import build_system_prompt, build_general_system_prompt
from ..config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Supabase helpers ──────────────────────────────────────────────────────────

async def _fetch_prediction(prediction_id: str, token: str, settings) -> dict | None:
    """Fetch a prediction row from Supabase."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/predictions",
            params={"id": f"eq.{prediction_id}", "select": "*"},
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )
    if resp.status_code == 200 and resp.json():
        return resp.json()[0]
    return None


async def _fetch_session_messages(session_id: str, token: str, settings) -> list[dict]:
    """Fetch all messages for an existing chat session."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/chat_messages",
            params={
                "session_id": f"eq.{session_id}",
                "select": "role,content",
                "order": "created_at.asc",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            },
        )
    if resp.status_code == 200:
        return [{"role": m["role"], "content": m["content"]} for m in resp.json()
                if m["role"] in ("user", "assistant")]
    return []


async def _create_session(
    doctor_id: str,
    prediction_id: str | None,
    token: str,
    settings,
) -> str:
    """Create a new chat_session row and return its ID."""
    session_id = str(uuid.uuid4())
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.SUPABASE_URL}/rest/v1/chat_sessions",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json={
                "id": session_id,
                "doctor_id": doctor_id,
                "prediction_id": prediction_id,
                "llm_provider": settings.LLM_PROVIDER,
                "llm_model": settings.OPENROUTER_MODEL
                    if settings.LLM_PROVIDER == "openrouter"
                    else settings.BEDROCK_PRIMARY_MODEL,
            },
        )
    return session_id


async def _save_message(
    session_id: str,
    role: str,
    content: str,
    token: str,
    settings,
) -> None:
    """Persist a chat message to Supabase (fire-and-forget, non-fatal)."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{settings.SUPABASE_URL}/rest/v1/chat_messages",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": settings.SUPABASE_ANON_KEY,
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal",
                },
                json={
                    "id": str(uuid.uuid4()),
                    "session_id": session_id,
                    "role": role,
                    "content": content,
                },
            )
    except Exception as exc:
        logger.warning(f"Failed to save message: {exc}")


# ── SSE generator ─────────────────────────────────────────────────────────────

def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def _stream_response(
    message: str,
    session_id: str,
    history: list[dict],
    system_prompt: str,
    token: str,
    settings,
) -> AsyncIterator[str]:
    """Core generator: stream LLM tokens as SSE, then persist messages."""
    provider = get_llm_provider()

    # Build message list for LLM (history + new user message)
    llm_messages = [*history, {"role": "user", "content": message}]

    # Persist user message
    await _save_message(session_id, "user", message, token, settings)

    full_response = ""
    try:
        async for token_text in provider.stream_chat(
            messages=llm_messages,
            system_prompt=system_prompt,
        ):
            full_response += token_text
            yield _sse({"type": "token", "content": token_text})

    except Exception as exc:
        logger.exception("LLM streaming error")
        yield _sse({"type": "error", "content": str(exc)})
        return

    # Persist assistant response
    if full_response:
        await _save_message(session_id, "assistant", full_response, token, settings)

    yield _sse({"type": "done", "session_id": session_id})


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.post("/chat", tags=["chat"])
async def chat(
    request: ChatRequest,
    doctor: dict = Depends(get_current_doctor),
):
    """
    Streaming chat endpoint — returns SSE text/event-stream.
    Creates a new session if session_id is null; resumes existing session otherwise.
    """
    settings = get_settings()
    token = doctor.get("_token", "")
    doctor_id = doctor["id"]

    # ── Resolve session ──
    if request.session_id:
        session_id = request.session_id
        history = await _fetch_session_messages(session_id, token, settings)
    else:
        session_id = await _create_session(doctor_id, request.prediction_id, token, settings)
        history = []

    # ── Build system prompt ──
    if request.prediction_id:
        prediction = await _fetch_prediction(request.prediction_id, token, settings)
        if prediction:
            system_prompt = build_system_prompt(
                clinical_note=prediction.get("input_text", ""),
                predictions=prediction.get("predicted_codes", []),
                concepts=prediction.get("activated_concepts", []),
            )
        else:
            system_prompt = build_general_system_prompt()
    else:
        system_prompt = build_general_system_prompt()

    # ── Stream ──
    return StreamingResponse(
        _stream_response(
            message=request.message,
            session_id=session_id,
            history=history,
            system_prompt=system_prompt,
            token=token,
            settings=settings,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable Nginx buffering
        },
    )
