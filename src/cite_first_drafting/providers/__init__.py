"""Provider registry."""

from __future__ import annotations

from cite_first_drafting.config import Settings, get_settings
from cite_first_drafting.providers.base import (
    Completion,
    DraftRequest,
    FrozenOutputMissing,
    Provider,
    ProviderError,
    ProviderNotConfigured,
    ProviderRateLimited,
)

PROVIDER_NAMES = ("replay", "groq", "anthropic")


def get_provider(name: str | None = None, settings: Settings | None = None) -> Provider:
    settings = settings or get_settings()
    name = (name or settings.provider).lower()
    if name == "replay":
        from cite_first_drafting.providers.replay import ReplayProvider

        return ReplayProvider(settings)
    if name == "groq":
        from cite_first_drafting.providers.groq import GroqProvider

        return GroqProvider(model=settings.model)
    if name == "anthropic":
        from cite_first_drafting.providers.anthropic import AnthropicProvider

        return AnthropicProvider(model=settings.model)
    raise ProviderNotConfigured(f"unknown provider '{name}'; choose one of {PROVIDER_NAMES}")


__all__ = [
    "Completion",
    "DraftRequest",
    "FrozenOutputMissing",
    "PROVIDER_NAMES",
    "Provider",
    "ProviderError",
    "ProviderNotConfigured",
    "ProviderRateLimited",
    "get_provider",
]
