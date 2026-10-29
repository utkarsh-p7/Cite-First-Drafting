"""Provider interface: one method, typed request and result, three implementations.

replay    serves the frozen v1 outputs (default; no API key, no cost, deterministic)
groq      OpenAI-compatible endpoint (model openai/gpt-oss-120b by default)
anthropic Claude models via the Anthropic SDK
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class ProviderError(RuntimeError):
    """Base class for provider failures (network, auth, malformed response)."""


class ProviderNotConfigured(ProviderError):
    """Provider selected but its API key or dependency is missing."""


class ProviderRateLimited(ProviderError):
    """Upstream returned a rate-limit (HTTP 429) response."""

    def __init__(self, message: str, retry_after_s: float | None = None):
        super().__init__(message)
        self.retry_after_s = retry_after_s


class FrozenOutputMissing(ProviderError):
    """Replay provider has no frozen output for this case/pipeline."""


@dataclass(frozen=True)
class DraftRequest:
    case_id: str
    pipeline: str  # "tool" | "baseline"
    system: str
    user: str
    max_tokens: int = 3000
    seed: int = 42
    model: str | None = None


@dataclass
class Completion:
    text: str
    provider: str
    model: str
    stop_reason: str | None = None
    usage: dict = field(default_factory=dict)
    wall_clock_s: float = 0.0
    params: dict = field(default_factory=dict)
    replayed: bool = False
    recorded_at_utc: str | None = None


class Provider(Protocol):
    name: str

    def complete(self, request: DraftRequest) -> Completion: ...
