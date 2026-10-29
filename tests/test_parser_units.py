"""Unit behaviour of the deterministic evidence-map parser."""

from cite_first_drafting.drafting.parser import SPAN_RE, build_evidence_map, count_flags, normalize, summarize

VALID = {"FF:C001:objectives.horizon_years", "TR:C001:u03", "KB:COBS_9A_3:01_applies_to"}


def test_fullwidth_brackets_are_normalised():
    assert normalize("fact 【FF:C001:objectives.horizon_years】") == "fact [FF:C001:objectives.horizon_years]"


def test_parenthesised_span_becomes_citation_but_prose_parens_survive():
    out = normalize("Horizon is ten years (FF:C001:objectives.horizon_years) (about a decade).")
    assert "[FF:C001:objectives.horizon_years]" in out and "(about a decade)" in out


def test_statuses_and_invalid_span_detection():
    draft = (
        "## Section\n"
        "Horizon is ten years [FF:C001:objectives.horizon_years].\n"
        "Costs are 0.5% a year [FS:ISA:99].\n"
        "The client has no debts.\n"
        "Capacity for loss is [INSUFFICIENT EVIDENCE: not recorded in the fact-find].\n"
    )
    emap = build_evidence_map("C001", draft, VALID)
    statuses = [s["status"] for s in emap]
    assert statuses == ["supported", "supported", "unsupported", "insufficient"]
    assert emap[1]["spans"][0]["span_valid"] is False  # FS:ISA:99 is not in the context
    assert summarize(emap) == {
        "statements": 4,
        "by_status": {"supported": 2, "unsupported": 1, "insufficient": 1},
        "invalid_spans": 1,
    }


def test_bare_insufficient_marker_line_merges_into_previous_statement():
    # A marker with no prose of its own is a citation-only fragment: it attaches to the
    # statement before it (same rule as trailing span citations). This is v1 behaviour.
    draft = "The client has no debts.\n[INSUFFICIENT EVIDENCE: liabilities not recorded]\n"
    emap = build_evidence_map("C001", draft, VALID)
    assert len(emap) == 1 and emap[0]["status"] == "insufficient"


def test_trailing_citation_fragment_merges_into_previous_statement():
    draft = "The client is 45 years old. [FF:C001:objectives.horizon_years]"
    emap = build_evidence_map("C001", draft, VALID)
    assert len(emap) == 1 and emap[0]["status"] == "supported"


def test_dotted_span_ids_are_not_split_as_sentences():
    draft = "Horizon is ten years [FF:C001:objectives.horizon_years][TR:C001:u03]. Next sentence here."
    emap = build_evidence_map("C001", draft, VALID)
    assert len(emap) == 2 and len(emap[0]["spans"]) == 2
    assert SPAN_RE.findall(emap[0]["text"]) == ["FF:C001:objectives.horizon_years", "TR:C001:u03"]


def test_adviser_flag_lines_counted_only_at_line_start():
    draft = (
        "ADVISER FLAG: ATR vs capacity [FF:C001:a][TR:C001:u03]\n"
        "The adviser flag: mentioned in prose.\n"
        "- **ADVISER FLAG:** second\n"
    )
    assert count_flags(draft) == 2


def test_statement_ids_are_sequential_and_headings_skipped():
    emap = build_evidence_map("C009", "## Heading\nOne [TR:C001:u03]. Two.", VALID)
    assert [s["statement_id"] for s in emap] == ["C009-S001", "C009-S002"]
