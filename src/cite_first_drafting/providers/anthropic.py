"""Anthropic provider (Messages API)."""

from __future__ import annotations

import os
import time

from cite_first_drafting.providers.base import (
    Completion,
    DraftRequest,
    ProviderError,
    ProviderNotConfigured,
    ProviderRateLimited,
)

DEFAULT_MODEL = "claude-sonnet-4-6"


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model or DEFAULT_MODEL
        if not self.api_key:
            raise ProviderNotConfigured("ANTHROPIC_API_KEY is not set")
        try:
            import anthropic
        except ImportError as e:  # pragma: no cover
            raise ProviderNotConfigured("install with: pip install 'cite-first-drafting[providers]'") from e
        self._anthropic = anthropic
        self._client = anthropic.Anthropic(api_key=self.api_key)

    def complete(self, request: DraftRequest) -> Completion:
        model = request.model or self.model
        t0 = time.perf_counter()
        try:
            resp = self._client.messages.create(
                model=model,
                max_tokens=request.max_tokens,
                temperature=0,
                system=request.system,
                messages=[{"role": "user", "content": request.user}],
            )
        except self._anthropic.RateLimitError as e:
            raise ProviderRateLimited(f"anthropic rate limit: {e}") from e
        except self._anthropic.APIError as e:
            raise ProviderError(f"anthropic API error: {e}") from e
        wall = time.perf_counter() - t0
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        return Completion(
            text=text,
            provider=self.name,
            model=resp.model,
            stop_reason=resp.stop_reason,
            usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
            wall_clock_s=round(wall, 3),
            params={"temperature": 0, "max_tokens": request.max_tokens},
        )
