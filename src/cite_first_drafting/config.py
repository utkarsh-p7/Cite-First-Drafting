"""Runtime configuration. Everything comes from environment variables with safe defaults.

CFD_DATA_DIR      folder holding fact_finds/, transcripts/, factsheets/, kb/, labels/
CFD_RESEARCH_DIR  folder holding the frozen v1 outputs (used by the replay provider)
CFD_PROVIDER      replay | groq | anthropic   (default: replay, works with no API key)
CFD_MODEL         provider model override (optional)
GROQ_API_KEY / ANTHROPIC_API_KEY  only needed for live providers
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _env_path(name: str, default: Path) -> Path:
    raw = os.environ.get(name)
    return Path(raw).expanduser().resolve() if raw else default


@dataclass(frozen=True)
class Settings:
    data_dir: Path = field(default_factory=lambda: _env_path("CFD_DATA_DIR", _REPO_ROOT / "data"))
    research_dir: Path = field(default_factory=lambda: _env_path("CFD_RESEARCH_DIR", _REPO_ROOT / "research" / "v1"))
    provider: str = field(default_factory=lambda: os.environ.get("CFD_PROVIDER", "replay"))
    model: str | None = field(default_factory=lambda: os.environ.get("CFD_MODEL") or None)
    seed: int = field(default_factory=lambda: int(os.environ.get("CFD_SEED", "42")))
    log_level: str = field(default_factory=lambda: os.environ.get("CFD_LOG_LEVEL", "INFO"))

    @property
    def fact_finds_dir(self) -> Path:
        return self.data_dir / "fact_finds"

    @property
    def transcripts_dir(self) -> Path:
        return self.data_dir / "transcripts"

    @property
    def factsheets_dir(self) -> Path:
        return self.data_dir / "factsheets"

    @property
    def kb_dir(self) -> Path:
        return self.data_dir / "kb"

    @property
    def labels_dir(self) -> Path:
        return self.data_dir / "labels"

    @property
    def frozen_outputs_dir(self) -> Path:
        return self.research_dir / "outputs"


def get_settings() -> Settings:
    return Settings()
