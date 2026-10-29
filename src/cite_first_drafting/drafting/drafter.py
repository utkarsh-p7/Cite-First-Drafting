"""Drafter: context -> provider -> deterministic evidence map -> structural check."""

from __future__ import annotations

import datetime as dt
import logging
from dataclasses import asdict, dataclass, field

from cite_first_drafting.config import Settings, get_settings
from cite_first_drafting.context.assembler import ContextAssembler, context_span_ids, render_prompt
from cite_first_drafting.drafting.parser import PARSER_VERSION, build_evidence_map, count_flags, summarize
from cite_first_drafting.drafting.prompts import MAX_TOKENS, SYSTEM_BY_PIPELINE
from cite_first_drafting.drafting.structure import check as structure_check
from cite_first_drafting.providers import DraftRequest, Provider, get_provider

log = logging.getLogger(__name__)

PIPELINES = ("tool", "baseline")


@dataclass
class DraftResult:
    case_id: str
    pipeline: str
    text: str
    evidence_map: list[dict]
    structure: list[dict]
    summary: dict
    flags: int
    provider: str
    model: str
    replayed: bool
    wall_clock_s: float
    usage: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    parser_version: str = PARSER_VERSION
    stop_reason: str | None = None
    drafted_at_utc: str = ""
    recorded_at_utc: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class Drafter:
    def __init__(self, settings: Settings | None = None, provider: Provider | None = None):
        self.settings = settings or get_settings()
        self.assembler = ContextAssembler(self.settings)
        self.provider = provider or get_provider(settings=self.settings)

    def draft(self, case_id: str, pipeline: str = "tool", context: dict | None = None) -> DraftResult:
        if pipeline not in PIPELINES:
            raise ValueError(f"pipeline must be one of {PIPELINES}")
        ctx = context or self.assembler.assemble(case_id)
        request = DraftRequest(
            case_id=case_id,
            pipeline=pipeline,
            system=SYSTEM_BY_PIPELINE[pipeline],
            user=render_prompt(ctx),
            max_tokens=MAX_TOKENS,
            seed=self.settings.seed,
            model=self.settings.model,
        )
        completion = self.provider.complete(request)
        text = completion.text
        emap = build_evidence_map(case_id, text, context_span_ids(ctx)) if pipeline == "tool" else []
        result = DraftResult(
            case_id=case_id,
            pipeline=pipeline,
            text=text,
            evidence_map=emap,
            structure=structure_check(text),
            summary=summarize(emap) if emap else {"statements": 0, "by_status": {}, "invalid_spans": 0},
            flags=count_flags(text),
            provider=completion.provider,
            model=completion.model,
            replayed=completion.replayed,
            wall_clock_s=completion.wall_clock_s,
            usage=completion.usage,
            params=completion.params,
            stop_reason=completion.stop_reason,
            drafted_at_utc=dt.datetime.now(dt.UTC).isoformat(),
            recorded_at_utc=completion.recorded_at_utc,
        )
        log.info(
            "drafted case=%s pipeline=%s provider=%s model=%s statements=%d invalid_spans=%d flags=%d wall_s=%.3f",
            case_id,
            pipeline,
            result.provider,
            result.model,
            result.summary["statements"],
            result.summary["invalid_spans"],
            result.flags,
            result.wall_clock_s,
        )
        return result
