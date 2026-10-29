"""The ported assembler must reproduce every frozen v1 context byte for byte."""

import pytest

from cite_first_drafting.context.assembler import ContextAssembler, context_json, render_prompt


@pytest.fixture(scope="module")
def assembler(settings):
    return ContextAssembler(settings)


def test_lists_all_forty_cases(assembler, case_ids):
    assert assembler.list_case_ids() == case_ids


def test_contexts_match_frozen(assembler, frozen, case_ids):
    mismatches = []
    for cid in case_ids:
        ctx = assembler.assemble(cid)
        want_ctx = (frozen / "contexts" / f"{cid}_context.json").read_text(encoding="utf-8")
        want_prompt = (frozen / "contexts" / f"{cid}_prompt.txt").read_text(encoding="utf-8")
        if context_json(ctx) != want_ctx or render_prompt(ctx) + "\n" != want_prompt:
            mismatches.append(cid)
    assert not mismatches, f"contexts differ from frozen v1 for: {mismatches}"


def test_span_id_families_present(assembler):
    ctx = assembler.assemble("C001")
    assert ctx["fact_find_spans"] and ctx["transcript_spans"] and ctx["factsheet_spans"] and ctx["kb_spans"]
    assert all(s["span_id"].startswith("FF:C001:") for s in ctx["fact_find_spans"])
    assert all(s["span_id"].startswith("TR:") for s in ctx["transcript_spans"])
    assert all(s["span_id"].startswith("KB:") for s in ctx["kb_spans"])
