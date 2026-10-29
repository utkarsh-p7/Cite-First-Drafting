"""Shared fixtures. All data under test is synthetic and fictitious."""

from __future__ import annotations

from pathlib import Path

import pytest

from cite_first_drafting.config import Settings

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "fixtures"


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(data_dir=REPO_ROOT / "data", research_dir=REPO_ROOT / "research" / "v1", provider="replay")


@pytest.fixture(scope="session")
def frozen(settings: Settings) -> Path:
    return settings.frozen_outputs_dir


@pytest.fixture(scope="session")
def case_ids(frozen: Path) -> list[str]:
    ids = sorted(p.name.removesuffix("_tool.md") for p in (frozen / "tool").glob("C*_tool.md"))
    assert len(ids) == 40, "expected the frozen 40-case batch"
    return ids
