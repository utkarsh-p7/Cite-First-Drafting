"""Deterministic context assembler (no retrieval).

case_id -> one structured context:
  (a) fact-find fields          FF:C0xx:<field_path>
  (b) transcript segments       TR:C0xx:<utt_id>   (IDs preserved verbatim from source)
  (c) factsheet sections        FS:<ISA|GIA>:<section>  (IDs preserved verbatim from headings)
  (d) KB extracts               KB:<FILE>:<NN>_<slug>   (assigned by ##-heading order)

No ranking, no selection beyond wrapper match (recommendation_context.recommended_wrapper).
Output is byte-identical across runs (sorted keys, fixed separators, no timestamps).

Ported unchanged in logic from the dissertation artefact (assemble_context.py); only the
data-folder layout is parameterised.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from cite_first_drafting.config import Settings, get_settings

# Profile rows (initial_report.md) -> KB files. Fixed order = file order in profile.
KB_FILES = ["COBS_9A_3.md", "COBS_9A_2.md", "COBS_4_2.md", "PRIN_2A.md", "FG22_5.md", "COBS_2_1.md"]

WRAPPER_TO_FS = {"ss_isa": ["ISA"], "gia": ["GIA"], "both": ["ISA", "GIA"]}

_FS_HEADING = re.compile(r"^## (FS:(ISA|GIA):\d+)\s*[—-]\s*(.*)$")
_slug_re = re.compile(r"[^a-z0-9]+")
# Citable KB sections only: scope + operative paraphrase. Housekeeping sections
# (Material quote, Relevance to tool, Flags, metadata) are excluded so they can
# never be cited as evidence. Deterministic title-prefix rule.
_KB_INCLUDE = re.compile(r"^(Applies to|What )", re.IGNORECASE)

_METADATA_PATHS = ("case_id", "label_fictitious", "schema_version", "generator_seed", "condition")


def _flatten(obj, prefix=""):
    """Depth-first, key order as in file (json preserves insertion order)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            out.extend(_flatten(v, path))
    elif isinstance(obj, list):
        out.append((prefix, obj))  # lists kept whole: one span per list field
    else:
        out.append((prefix, obj))
    return out


def fact_find_spans(ff: dict, case_id: str) -> list[dict]:
    spans = []
    for path, value in _flatten(ff):
        if path in _METADATA_PATHS:
            continue  # metadata, not client evidence
        spans.append({"span_id": f"FF:{case_id}:{path}", "field_path": path, "value": value})
    return spans


def transcript_spans(tr: dict) -> list[dict]:
    return [
        {
            "span_id": seg["utt_id"],
            "speaker": seg["speaker"],
            "start_s": seg["start_s"],
            "end_s": seg["end_s"],
            "text": seg["text"],
        }
        for seg in tr["segments"]
    ]


def factsheet_spans(path: Path) -> list[dict]:
    """Section IDs read verbatim from '## FS:<ISA|GIA>:<n> - title' headings."""
    spans, current = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _FS_HEADING.match(line)
        if m:
            if current:
                current["text"] = current["text"].strip()
                spans.append(current)
            current = {"span_id": m.group(1), "title": m.group(3).strip(), "text": ""}
        elif current is not None:
            current["text"] += line + "\n"
    if current:
        current["text"] = current["text"].strip()
        spans.append(current)
    return spans


def kb_spans(kb_dir: Path) -> list[dict]:
    """One span per *included* ##-section per KB file, in fixed file order.
    ID: KB:<FILE_STEM>:<NN>_<slug>. NN numbered over included sections only."""
    spans = []
    for fname in KB_FILES:
        stem = Path(fname).stem
        text = (kb_dir / fname).read_text(encoding="utf-8")
        sections, current = [], None
        for line in text.splitlines():
            if line.startswith("## "):
                if current:
                    sections.append(current)
                current = {"title": line[3:].strip(), "text": ""}
            elif current is not None:
                current["text"] += line + "\n"
        if current:
            sections.append(current)
        sections = [s for s in sections if _KB_INCLUDE.match(s["title"])]
        for i, sec in enumerate(sections, 1):
            slug = _slug_re.sub("_", sec["title"].lower()).strip("_")[:40]
            spans.append(
                {
                    "span_id": f"KB:{stem}:{i:02d}_{slug}",
                    "kb_file": fname,
                    "title": sec["title"],
                    "text": sec["text"].strip(),
                }
            )
    return spans


class ContextAssembler:
    """Builds the single structured context for a case from the data folder."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def list_case_ids(self) -> list[str]:
        return sorted(p.stem.removeprefix("fact_find_") for p in self.settings.fact_finds_dir.glob("fact_find_*.json"))

    def load_fact_find(self, case_id: str) -> dict:
        p = self.settings.fact_finds_dir / f"fact_find_{case_id}.json"
        if not p.exists():
            raise FileNotFoundError(f"fact-find for {case_id} not found at {p}")
        return json.loads(p.read_text(encoding="utf-8"))

    def load_transcript(self, case_id: str) -> dict:
        p = self.settings.transcripts_dir / f"transcript_{case_id}.json"
        if not p.exists():
            raise FileNotFoundError(f"transcript for {case_id} not found at {p}")
        return json.loads(p.read_text(encoding="utf-8"))

    def assemble(self, case_id: str) -> dict:
        ff = self.load_fact_find(case_id)
        tr = self.load_transcript(case_id)
        wrapper = ff["recommendation_context"]["recommended_wrapper"]
        fs: list[dict] = []
        for code in WRAPPER_TO_FS[wrapper]:
            fs.extend(factsheet_spans(self.settings.factsheets_dir / f"factsheet_{code}_FICTITIOUS.md"))
        return {
            "case_id": case_id,
            "label_fictitious": True,
            "recommended_wrapper": wrapper,
            "fact_find_spans": fact_find_spans(ff, case_id),
            "transcript_spans": transcript_spans(tr),
            "factsheet_spans": fs,
            "kb_spans": kb_spans(self.settings.kb_dir),
        }


def context_span_ids(ctx: dict) -> set[str]:
    ids: set[str] = set()
    for key in ("fact_find_spans", "transcript_spans", "factsheet_spans", "kb_spans"):
        ids.update(s["span_id"] for s in ctx[key])
    return ids


def render_prompt(ctx: dict) -> str:
    L: list[str] = []
    a = L.append
    a(f"# CASE {ctx['case_id']} — SOURCE EVIDENCE (all data FICTITIOUS/synthetic)")
    a(f"Recommended wrapper: {ctx['recommended_wrapper']}")
    a("\n## FACT-FIND (cite as the FF: span-ID shown)")
    for s in ctx["fact_find_spans"]:
        a(f"[{s['span_id']}] = {json.dumps(s['value'], ensure_ascii=False)}")
    a("\n## MEETING TRANSCRIPT (cite as the TR: span-ID shown)")
    for s in ctx["transcript_spans"]:
        a(f"[{s['span_id']}] {s['speaker']}: {s['text']}")
    a("\n## PRODUCT FACTSHEET(S) (cite as the FS: span-ID shown)")
    for s in ctx["factsheet_spans"]:
        a(f"[{s['span_id']}] {s['title']}: {s['text']}")
    a("\n## REGULATORY KB EXTRACTS (cite as the KB: span-ID shown)")
    for s in ctx["kb_spans"]:
        a(f"[{s['span_id']}] ({s['kb_file']}) {s['title']}:\n{s['text']}")
    return "\n".join(L)


def context_json(ctx: dict) -> str:
    """Canonical serialisation, byte-identical to the frozen research contexts."""
    return json.dumps(ctx, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
