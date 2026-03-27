"""
OpenRouter LLM provider — OpenAI-compatible API, streaming via SSE.
Default model: meta-llama/llama-3.3-70b-instruct:free (200 req/day free tier)
"""
import json
import logging
from typing import AsyncIterator

import httpx

from .llm_provider import LLMProvider
from ..config import get_settings

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterProvider(LLMProvider):
    async def stream_chat(
        self,
        messages: list[dict],
        system_prompt: str,
    ) -> AsyncIterator[str]:
        settings = get_settings()

        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages,
            ],
            "stream": True,
            "temperature": 0.3,
            "max_tokens": 1500,
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://platform.shifamind.me",
            "X-Title": "ShifaMind Platform",
        }

        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST",
                f"{OPENROUTER_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
            ) as resp:
                if resp.status_code != 200:
                    body = await resp.aread()
                    raise RuntimeError(
                        f"OpenRouter error {resp.status_code}: {body.decode()[:300]}"
                    )

                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0].get("delta", {})
                        token = delta.get("content", "")
                        if token:
                            yield token
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
