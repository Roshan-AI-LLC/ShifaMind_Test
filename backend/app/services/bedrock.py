"""
AWS Bedrock LLM provider — boto3 converse_stream API.
Primary model:  meta.llama3-3-70b-instruct-v1:0
Fallback model: anthropic.claude-sonnet-4-20250514-v1:0
"""
import logging
from typing import AsyncIterator

from .llm_provider import LLMProvider
from ..config import get_settings

logger = logging.getLogger(__name__)


class BedrockProvider(LLMProvider):
    async def stream_chat(
        self,
        messages: list[dict],
        system_prompt: str,
    ) -> AsyncIterator[str]:
        """
        Use boto3 bedrock-runtime converse_stream.
        boto3 is synchronous, so we run it in a thread pool to stay async-friendly.
        """
        import asyncio
        import functools
        import boto3

        settings = get_settings()

        bedrock = boto3.client(
            "bedrock-runtime",
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
        )

        # Convert messages to Bedrock converse format
        bedrock_messages = [
            {"role": msg["role"], "content": [{"text": msg["content"]}]}
            for msg in messages
        ]

        async def _call_bedrock(model_id: str):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                functools.partial(
                    bedrock.converse_stream,
                    modelId=model_id,
                    system=[{"text": system_prompt}],
                    messages=bedrock_messages,
                    inferenceConfig={"temperature": 0.3, "maxTokens": 1500},
                ),
            )

        # Try primary model, fall back on error
        for model_id in [settings.BEDROCK_PRIMARY_MODEL, settings.BEDROCK_FALLBACK_MODEL]:
            try:
                response = await _call_bedrock(model_id)
                logger.info(f"Bedrock: using model {model_id}")
                break
            except Exception as exc:
                logger.warning(f"Bedrock model {model_id} failed: {exc}")
                if model_id == settings.BEDROCK_FALLBACK_MODEL:
                    raise RuntimeError(f"Both Bedrock models failed: {exc}") from exc

        # Stream tokens from the response event stream
        stream = response.get("stream")
        if not stream:
            raise RuntimeError("No stream in Bedrock response")

        loop = asyncio.get_event_loop()
        queue: asyncio.Queue = asyncio.Queue()

        def _consume():
            try:
                for event in stream:
                    if "contentBlockDelta" in event:
                        delta = event["contentBlockDelta"].get("delta", {})
                        text = delta.get("text", "")
                        if text:
                            loop.call_soon_threadsafe(queue.put_nowait, text)
            except Exception as exc:
                loop.call_soon_threadsafe(queue.put_nowait, exc)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

        import threading
        thread = threading.Thread(target=_consume, daemon=True)
        thread.start()

        while True:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, Exception):
                raise item
            yield item
