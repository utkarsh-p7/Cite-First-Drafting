"""The ported parser must rebuild every frozen v1 evidence map and structure check exactly."""

import json

from cite_first_drafting.context.assembler import context_span_ids
from cite_first_drafting.drafting.parser import build_evidence_map
from cite_first_drafting.drafting.structure import check


def _ctx_ids(frozen, cid):
    return context_span_ids(json.loads((frozen / "contexts" / f"{cid}_context.json").read_text(encoding="utf-8")))


def test_evidence_maps_match_frozen(frozen, case_ids):
    bad = []
    for cid in case_ids:
        draft = (frozen / "tool" / f"{cid}_tool.md").read_text(encoding="utf-8")
        got = json.dumps(build_evidence_map(cid, draft, _ctx_ids(frozen, cid)), ensure_ascii=False, indent=1) + "\n"
        want = (frozen / "tool" / f"{cid}_evidence_map.json").read_text(encoding="utf-8")
        if got != want:
            bad.append(cid)
    assert not bad, f"evidence maps differ from frozen v1 for: {bad}"


def test_structure_checks_match_frozen(frozen, case_ids):
    bad = []
    for cid in case_ids:
        for pipeline in ("tool", "baseline"):
            p = frozen / pipeline / f"{cid}_{pipeline}_structure.json"
            if not p.exists():
                continue
            draft = (frozen / pipeline / f"{cid}_{pipeline}.md").read_text(encoding="utf-8")
            if check(draft) != json.loads(p.read_text(encoding="utf-8"))["rows"]:
                bad.append(f"{cid}:{pipeline}")
    assert not bad, f"structure rows differ from frozen v1 for: {bad}"
