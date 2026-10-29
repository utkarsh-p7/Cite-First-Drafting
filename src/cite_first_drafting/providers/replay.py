"""Replay provider: serves the frozen v1 batch outputs instead of calling a model.

This is the public demo's default. It makes the service deterministic, free, and
honest: what you see is exactly what the dissertation evaluated.
"""

from __future__ import annotations

import json
from pathlib import Path

from cite_first_drafting.config import Settings, get_settings
from cite_first_drafting.providers.base import Completion, DraftRequest, FrozenOutputMissing


class ReplayProvider:
    name = "replay"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._logs: dict[str, dict[str, dict]] = {}

    def _outputs_dir(self, pipeline: str) -> Path:
        return self.settings.frozen_outputs_dir / pipeline

    def _run_log(self, pipeline: str) -> dict[str, dict]:
        if pipeline not in self._logs:
            entries: dict[str, dict] = {}
            p = self._outputs_dir(pipeline) / "run_log.jsonl"
            if p.exists():
                for line in p.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        e = json.loads(line)
                        entries[e["case_id"]] = e  # last entry per case wins
            self._logs[pipeline] = entries
        return self._logs[pipeline]

    def available_cases(self, pipeline: str = "tool") -> list[str]:
        suffix = f"_{pipeline}.md"
        return sorted(p.name[: -len(suffix)] for p in self._outputs_dir(pipeline).glob(f"*{suffix}"))

    def complete(self, request: DraftRequest) -> Completion:
        path = self._outputs_dir(request.pipeline) / f"{request.case_id}_{request.pipeline}.md"
        if not path.exists():
            raise FrozenOutputMissing(
                f"no frozen {request.pipeline} output for {request.case_id}; "
                "switch CFD_PROVIDER to groq or anthropic to draft live"
            )
        text = path.read_text(encoding="utf-8")
        if text.endswith("\n"):
            text = text[:-1]  # batch writer appended one newline on save
        meta = self._run_log(request.pipeline).get(request.case_id, {})
        return Completion(
            text=text,
            provider=self.name,
            model=meta.get("model", "frozen-v1"),
            stop_reason=meta.get("stop_reason"),
            usage=meta.get("usage", {}),
            wall_clock_s=float(meta.get("wall_clock_s", 0.0)),
            params=meta.get("params", {}),
            replayed=True,
            recorded_at_utc=meta.get("timestamp_utc"),
        )
