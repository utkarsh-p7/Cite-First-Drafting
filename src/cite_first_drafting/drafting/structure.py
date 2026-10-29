"""Structural checker: machine-checkable profile rows on any draft.

Presence/absence only; substantive adequacy is NEVER scored (rows 8, 9, 12 emit
"human_review_required"). Logic ported unchanged from check_structure.py.
"""

from __future__ import annotations

import re

from cite_first_drafting.drafting.parser import FLAG_RE, INSUFF_RE, PARSER_VERSION, SPAN_RE, normalize
from cite_first_drafting.drafting.template import SECTIONS, TOOL_EXTRA_SECTION

STAMP = "checked against COBS 9A as at 2026-07-07"
CHECKER_VERSION = "structcheck-1.0.0"

_H = {sid: h for sid, h, _ in SECTIONS + [TOOL_EXTRA_SECTION]}

ROW4_ELEMENTS = {
    "investment_term": re.compile(r"\b(horizon|term|year)", re.I),
    "knowledge_experience": re.compile(r"\b(knowledge|experience)", re.I),
    "attitude_to_risk": re.compile(r"\b(attitude to risk|risk (?:attitude|tolerance)|atr)\b", re.I),
    "capacity_for_loss": re.compile(r"\bcapacity for loss\b", re.I),
}

SUBSTANTIVE_ONLY = {
    8: "fair, clear, not misleading (COBS 4.2.1R)",
    9: "plain-English / consumer understanding (PRIN 2A.5, FG22/5 ch.8)",
    12: "client's best interests (COBS 2.1.1R)",
}


def _section_present(draft: str, heading: str) -> bool:
    return re.search(rf"^##\s+{re.escape(heading)}\s*$", draft, re.M) is not None


def _sec_status(draft: str, sid: str) -> str:
    return "present" if _section_present(draft, _H[sid]) else "absent"


def check(draft: str) -> list[dict]:
    draft = normalize(draft)
    rows: list[dict] = []

    def add(rid, status, note=""):
        rows.append({"row_id": rid, "status": status, **({"note": note} if note else {})})

    add(1, _sec_status(draft, "delivery_note"))
    add(2, _sec_status(draft, "advice_given"))
    add(3, _sec_status(draft, "why_suitable"), "presence only; adequacy = human review")
    if _section_present(draft, _H["why_suitable"]):
        missing = [k for k, rx in ROW4_ELEMENTS.items() if not rx.search(draft)]
        add(
            4,
            "present" if not missing else "absent",
            "elements missing: " + ", ".join(missing)
            if missing
            else "all art.54(12) elements mentioned; adequacy = human review",
        )
    else:
        add(4, "absent", "why_suitable section missing")
    add(5, _sec_status(draft, "ongoing_review"))
    add(6, _sec_status(draft, "your_circumstances"))
    nflags = len(FLAG_RE.findall(draft))
    add(
        7,
        "flagged" if nflags else "absent",
        f"ADVISER FLAG lines: {nflags}; whether one is required = ground-truth/eval question",
    )
    for rid, desc in SUBSTANTIVE_ONLY.items():
        add(rid, "human_review_required", desc)
    add(10, _sec_status(draft, "costs_charges"))
    add(11, _sec_status(draft, "risks_disadvantages"))
    has_evidence = bool(SPAN_RE.search(draft) or INSUFF_RE.search(draft))
    add(13, "present" if has_evidence else "absent", "span citations / insufficiency markers")
    add(14, _sec_status(draft, "missing_information"))
    return sorted(rows, key=lambda r: r["row_id"])


def structure_report(draft: str, draft_file: str = "") -> dict:
    return {
        "draft_file": draft_file,
        "stamp": STAMP,
        "checker_version": CHECKER_VERSION,
        "parser_version": PARSER_VERSION,
        "rows": check(draft),
    }
