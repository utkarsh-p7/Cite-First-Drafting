"""Groq provider (OpenAI-compatible chat completions)."""

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

DEFAULT_MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://api.groq.com/openai/v1"


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.model = model or DEFAULT_MODEL
        if not self.api_key:
            raise ProviderNotConfigured("GROQ_API_KEY is not set")
        try:
            import openai
        except ImportError as e:  # pragma: no cover
            raise ProviderNotConfigured("install with: pip install 'cite-first-drafting[providers]'") from e
        self._openai = openai
        self._client = openai.OpenAI(base_url=BASE_URL, api_key=self.api_key)

    def complete(self, request: DraftRequest) -> Completion:
        model = request.model or self.model
        extra = {"reasoning_effort": "low"} if "gpt-oss" in model else {}
        t0 = time.perf_counter()
        try:
            resp = self._client.chat.completions.create(
                model=model,
                max_tokens=request.max_tokens,
                temperature=0,
                seed=request.seed,
                messages=[
                    {"role": "system", "content": request.system},
                    {"role": "user", "content": request.user},
                ],
                extra_body=extra,
            )
        except self._openai.RateLimitError as e:
            retry = None
            headers = getattr(getattr(e, "response", None), "headers", None)
            if headers and headers.get("retry-after"):
                try:
                    retry = float(headers["retry-after"])
                except ValueError:
                    retry = None
            raise ProviderRateLimited(f"groq rate limit: {e}", retry_after_s=retry) from e
        except self._openai.APIError as e:
            raise ProviderError(f"groq API error: {e}") from e
        wall = time.perf_counter() - t0
        choice = resp.choices[0]
        return Completion(
            text=choice.message.content or "",
            provider=self.name,
            model=resp.model,
            stop_reason=choice.finish_reason,
            usage={"input_tokens": resp.usage.prompt_tokens, "output_tokens": resp.usage.completion_tokens},
            wall_clock_s=round(wall, 3),
            params={"temperature": 0, "max_tokens": request.max_tokens, "seed": request.seed, **extra},
        )
