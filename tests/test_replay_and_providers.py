"""Replay provider and drafter end to end, plus provider registry guards."""

import json

import pytest

from cite_first_drafting.drafting.drafter import Drafter
from cite_first_drafting.providers import FrozenOutputMissing, ProviderNotConfigured, get_provider
from cite_first_drafting.providers.base import DraftRequest
from cite_first_drafting.providers.replay import ReplayProvider


def test_replay_lists_frozen_cases(settings, case_ids):
    assert ReplayProvider(settings).available_cases("tool") == case_ids
    assert ReplayProvider(settings).available_cases("baseline") == case_ids


def test_replay_returns_frozen_text_and_metadata(settings, frozen):
    c = ReplayProvider(settings).complete(DraftRequest("C001", "tool", "sys", "user"))
    assert c.replayed and c.provider == "replay" and c.model == "openai/gpt-oss-120b"
    assert c.text + "\n" == (frozen / "tool" / "C001_tool.md").read_text(encoding="utf-8")
    assert c.usage["input_tokens"] > 0 and c.wall_clock_s > 0


def test_replay_missing_case_raises(settings):
    with pytest.raises(FrozenOutputMissing):
        ReplayProvider(settings).complete(DraftRequest("C999", "tool", "sys", "user"))


def test_drafter_replay_reproduces_frozen_evidence_map(settings, frozen):
    result = Drafter(settings, ReplayProvider(settings)).draft("C001", "tool")
    want = json.loads((frozen / "tool" / "C001_evidence_map.json").read_text(encoding="utf-8"))
    assert result.evidence_map == want
    assert result.summary["statements"] == len(want) and result.flags >= 1
    assert result.parser_version == "evmap-1.3.0" and result.replayed


def test_drafter_baseline_has_no_evidence_map(settings):
    result = Drafter(settings, ReplayProvider(settings)).draft("C001", "baseline")
    assert result.evidence_map == [] and result.summary["statements"] == 0
    assert any(r["row_id"] == 13 and r["status"] == "absent" for r in result.structure)


def test_drafter_rejects_unknown_pipeline(settings):
    with pytest.raises(ValueError):
        Drafter(settings, ReplayProvider(settings)).draft("C001", "nope")


def test_registry_defaults_to_replay(settings):
    assert get_provider(settings=settings).name == "replay"


def test_registry_rejects_unknown_and_unconfigured(settings, monkeypatch):
    with pytest.raises(ProviderNotConfigured):
        get_provider("bogus", settings)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProviderNotConfigured):
        get_provider("groq", settings)
    with pytest.raises(ProviderNotConfigured):
        get_provider("anthropic", settings)
