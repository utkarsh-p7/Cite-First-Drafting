"""Deterministic evidence-map parser (PARSER_VERSION evmap-1.3.0).

Builds the evidence map from a draft with NO second LLM call:
  status: supported    >=1 cited span that exists in the assembled context
          insufficient [INSUFFICIENT EVIDENCE: ...] marker present
          unsupported  sentence carries neither citations nor marker
Hallucinated span IDs (cited but absent from context) are kept in spans[] with
"span_valid": false so the evaluation harness can count them.

Logic ported unchanged from the dissertation artefact (draft_tool.py).
"""

from __future__ import annotations

import re

PARSER_VERSION = "evmap-1.3.0"  # bracket-normalize + paren-span + fragment-merge + flag-detect

_PAREN_SPAN_RE = re.compile(r"\(((?:FF|TR|FS|KB):[^()\s\]]+)\)")
SPAN_RE = re.compile(r"\[((?:FF|TR|FS|KB):[^\]\s]+)\]")
INSUFF_RE = re.compile(r"\[INSUFFICIENT EVIDENCE[^\]]*\]")
FLAG_RE = re.compile(r"^\s*(?:[-*•]\s*)?(?:\*\*)?ADVISER FLAG:", re.MULTILINE)
_BRACKET_RE = re.compile(r"\[[^\]]*\]")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def normalize(text: str) -> str:
    """Normalize citation variants the model may emit so citations parse:
    fullwidth CJK brackets -> ASCII; (SPAN-ID) -> [SPAN-ID] only when the
    parenthesised content exactly matches span-ID grammar (prose parens kept)."""
    text = text.replace("【", "[").replace("】", "]")
    return _PAREN_SPAN_RE.sub(r"[\1]", text)


def split_sentences(text: str):
    """Split into sentences with bracketed chunks (citations/flags) protected:
    span IDs contain dots (FF dot-paths) and must never be split."""
    stash: list[str] = []

    def _stash(m):
        stash.append(m.group(0))
        return f"\x00{len(stash) - 1}\x00"

    protected = _BRACKET_RE.sub(_stash, text)
    for part in _SENT_SPLIT.split(protected):
        part = part.strip()
        if part:
            yield re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], part)


def _prose(sent: str) -> str:
    """Sentence content with all bracketed chunks and markdown furniture removed."""
    s = _BRACKET_RE.sub("", sent)
    return re.sub(r"[\s\*\-•.:;,()]+", "", s)


def build_evidence_map(case_id: str, draft: str, valid_ids: set[str]) -> list[dict]:
    draft = normalize(draft)
    # split, then merge citation-only fragments into the preceding statement
    # (models often place citations after the sentence-ending full stop)
    merged: list[str] = []
    for sent in split_sentences(draft):
        if not sent or sent.startswith("#"):
            continue
        if merged and not _prose(sent) and (SPAN_RE.search(sent) or INSUFF_RE.search(sent)):
            merged[-1] = merged[-1] + " " + sent
        else:
            merged.append(sent)
    out, n = [], 0
    for sent in merged:
        spans = SPAN_RE.findall(sent)
        insuff = bool(INSUFF_RE.search(sent))
        if spans:
            status = "supported"
        elif insuff:
            status = "insufficient"
        else:
            status = "unsupported"
        n += 1
        out.append(
            {
                "statement_id": f"{case_id}-S{n:03d}",
                "text": sent,
                "spans": [{"span_id": s, "span_valid": s in valid_ids} for s in spans],
                "status": status,
            }
        )
    return out


def count_flags(draft: str) -> int:
    return len(FLAG_RE.findall(normalize(draft)))


def summarize(emap: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for s in emap:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    invalid = sum(1 for s in emap for sp in s["spans"] if not sp["span_valid"])
    return {"statements": len(emap), "by_status": counts, "invalid_spans": invalid}
