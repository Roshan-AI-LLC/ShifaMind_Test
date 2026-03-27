"""
LLM Provider abstraction.
Swap between OpenRouter and AWS Bedrock with a single env var: LLM_PROVIDER.
"""
from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):
    """Abstract base — all providers implement stream_chat."""

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[dict],
        system_prompt: str,
    ) -> AsyncIterator[str]:
        """
        Yield string tokens as they stream from the LLM.

        Args:
            messages:      List of {"role": "user"|"assistant", "content": "..."}
            system_prompt: Formatted medical system prompt string
        Yields:
            str token fragments
        """
        ...  # pragma: no cover


def get_llm_provider() -> LLMProvider:
    """
    Factory — reads LLM_PROVIDER env var and returns the right implementation.
    Default: openrouter
    """
    from ..config import get_settings
    settings = get_settings()

    if settings.LLM_PROVIDER == "bedrock":
        from .bedrock import BedrockProvider
        return BedrockProvider()

    from .openrouter import OpenRouterProvider
    return OpenRouterProvider()
