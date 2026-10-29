#!/usr/bin/env python3
"""evaluate.py — RQ1 scoring harness (Eval agent, Task 1).

Inputs per case: frozen label JSON (ground truth), evidence-map JSON + tool draft md
(tool pipeline), baseline draft md (baseline pipeline). Fully deterministic; no API
calls; no writes outside the chosen --out path.

Metrics (names as Ch3 §3.5 / evaluation_rubric.md; ruled decisions encoded):
  unsupported_rate        material statements with no valid evidence link
                          (sentence-strict PRIMARY; block-level as sensitivity)
  insufficient_rate       statements flagged insufficient-evidence (reported separately)
  omission_rate           label inventory keys absent from draft; denominator =
                          the case's OWN inventory (ruling 21: ss_isa 17, gia 16,
                          both 20 with the product triplet once per FS family);
                          text-based, pipeline-symmetric; in 'both' cases each
                          duplicated product pair shares one detector (pair moves
                          together — granularity limitation, footnoted)
  contradiction_catch     labelled contradictory facts with a line-start
                          'ADVISER FLAG:' (exact prefix) citing >=1 correct span
  em_precision_fact       PRIMARY (ruled 2026-08-16): unique cited valid FF:/TR:/FS:
                          spans that appear in the label's span inventory / all unique
                          cited valid FF:/TR:/FS: spans (label-matchable by construction)
  em_precision_all        SECONDARY, footnoted: same numerator / all unique cited valid
                          spans incl. KB:. KB: citations are regulatory grounding,
                          validated by span_valid only — never label-matchable
  em_recall               labelled supported facts with >=1 of their spans cited
  invalid_span_rate       citation instances with span_valid == false (separate)
Boilerplate stubs are excluded from statement denominators; stub count reported.
Baseline: no citations -> unsupported_rate 1.0 by construction; em_precision/
invalid_span_rate not applicable; em_recall 0.0; omission + contradiction-catch
computed from draft text.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HARNESS_VERSION = "eval-harness v1.2.1 (2026-08-18)"
FLAG_PREFIX = "ADVISER FLAG:"
SPAN_RE = re.compile(r"\[((?:FF|TR|FS|KB):[^\]\s]+)\]")

EXPECTED_FACT_KEYS = [
    "client_identity", "investable_amount", "contribution_type",
    "recommended_wrapper", "primary_objective", "investment_horizon",
    "risk_tolerance_atr", "capacity_for_loss", "income",
    "essential_expenditure", "emergency_fund", "liabilities",
    "knowledge_experience", "isa_allowance_used", "product_key_risks",
    "product_charges", "product_tax_treatment",
]

# ---------------------------------------------------------------- text utils

def norm(text: str) -> str:
    """Deterministic normalisation: NFKC, unicode hyphens -> '-', curly quotes
    -> straight, NBSP -> space, lowercase, collapse whitespace."""
    t = unicodedata.normalize("NFKC", text)
    for h in "‐‑‒–—―":
        t = t.replace(h, "-")
    for q in "‘’":
        t = t.replace(q, "'")
    for q in "“”":
        t = t.replace(q, '"')
    t = t.replace(" ", " ")
    t = t.lower()
    return re.sub(r"\s+", " ", t).strip()


def strip_markup(text: str) -> str:
    """Remove citations, bold markers and list markers for stub detection."""
    t = SPAN_RE.sub("", text)
    t = t.replace("**", "")
    t = re.sub(r"^\s*[-*]\s+", "", t)
    return t.strip()


def is_stub(text: str) -> bool:
    """Boilerplate stub: bare lead-in ending ':' or a 'None identified.' filler."""
    t = strip_markup(text)
    if not t:
        return True
    if t.endswith(":"):
        return True
    return norm(t) in {"none identified.", "none identified"}


def fmt_amount_variants(v) -> list:
    """'14500' -> ['14,500', '14500'] (thousands separator optional)."""
    try:
        n = int(v)
    except (TypeError, ValueError):
        return [str(v)]
    return [f"{n:,}", str(n)]

# ------------------------------------------------------- fact-key detectors
# Each detector answers: does the draft state this labelled fact's VALUE?
# Ruled: status 'missing' keys have no value to state -> counted absent (both
# pipelines symmetrically; footnoted in results). Contradictory keys count as
# present if any conflicting value appears with a year/unit context.


def _amount_in(v, t) -> bool:
    return any(x in t for x in fmt_amount_variants(v))


def detect_fact(fact: dict, t: str) -> bool:
    key, val, status = fact["fact_key"], fact.get("value"), fact["status"]
    if status == "missing":
        return False
    if status == "contradictory":
        vals = list((fact.get("conflict") or {}).get("values_by_span", {}).values())
        if key == "investment_horizon":
            return any(re.search(rf"\b{v}\s*-?\s*year", t) for v in vals)
        if key == "risk_tolerance_atr":
            return any(re.search(rf"(atr\s*score|score)\s*(of\s*)?{v}\b", t) for v in vals)
        return any(str(v).replace("_", " ") in t for v in vals)
    if key == "client_identity":
        return norm(val["name"]) in t
    if key == "investable_amount":
        return _amount_in(val, t)
    if key == "contribution_type":
        if val == "lump_sum":
            return "lump-sum" in t or "lump sum" in t
        return str(val).replace("_", " ") in t
    if key == "recommended_wrapper":
        if val == "ss_isa":
            return ("stocks & shares isa" in t or "stocks and shares isa" in t
                    or "ss isa" in t or "ss_isa" in t)
        if val == "gia":
            return "general investment account" in t or "gia" in t
        if val == "both":
            isa = ("stocks & shares isa" in t or "stocks and shares isa" in t
                   or "ss isa" in t or "ss_isa" in t or "isa" in t)
            gia = "general investment account" in t or "gia" in t
            return isa and gia
        return str(val) in t
    if key == "primary_objective":
        # content-token match: every alphabetic token of length >=6 in the
        # labelled objective must appear in the draft (phrase-order agnostic)
        toks = [w for w in re.findall(r"[a-z]+", norm(str(val))) if len(w) >= 6]
        return all(w in t for w in toks) if toks else norm(str(val)) in t
    if key == "investment_horizon":
        return bool(re.search(rf"\b{val}\s*-?\s*year", t))
    if key == "risk_tolerance_atr":
        desc = norm(str(val.get("descriptor", "")).replace("_", " "))
        score = val.get("score")
        return (desc and desc in t) or bool(
            re.search(rf"(atr\s*score|score)\s*(is\s*|of\s*)?{score}\b", t))
    if key == "capacity_for_loss":
        return "capacity" in t and norm(str(val)) in t
    if key == "income":
        return _amount_in(val, t)
    if key == "essential_expenditure":
        return _amount_in(val, t)
    if key == "emergency_fund":
        return "emergency fund" in t and "month" in t
    if key == "liabilities":
        return "liabilit" in t
    if key == "knowledge_experience":
        freq = norm(str(val.get("frequency", "")))
        return "previously held" in t or (freq and freq in t) or "knowledge" in t
    if key == "isa_allowance_used":
        return "allowance used" in t or ("allowance" in t and "used" in t)
    if key == "product_key_risks":
        return "market risk" in t
    if key == "product_charges":
        return "ocf" in t or "platform fee" in t or "0.60" in t
    if key == "product_tax_treatment":
        return "tax" in t
    raise KeyError(f"no detector for fact_key {key!r}")

# ------------------------------------------------------------------ loading

def load_json(p: Path):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_text(p: Path) -> str:
    return open(p, encoding="utf-8").read()


PRODUCT_KEYS = ["product_key_risks", "product_charges", "product_tax_treatment"]


def _wrapper(label: dict) -> str:
    w = [f for f in label["facts"] if f["fact_key"] == "recommended_wrapper"]
    if len(w) != 1:
        raise ValueError(f"label {label['case_id']}: recommended_wrapper count != 1")
    return w[0]["value"]


def _fs_family(fact: dict) -> str:
    fams = {s.split(":")[1] for s in fact["spans"] if s.startswith("FS:")}
    return fams.pop() if len(fams) == 1 else "?"


def validate_label(label: dict):
    """Shape-strict per wrapper (ruling 21e): ss_isa = exact canonical 17;
    gia = canonical minus isa_allowance_used (16); both = canonical + the
    product triplet duplicated, exactly once per FS:ISA / FS:GIA family (20).
    Anything else = hard error (corruption-detection power retained)."""
    cid, keys = label["case_id"], [f["fact_key"] for f in label["facts"]]
    w = _wrapper(label)
    if w == "ss_isa":
        expected = sorted(EXPECTED_FACT_KEYS)
    elif w == "gia":
        expected = sorted(k for k in EXPECTED_FACT_KEYS if k != "isa_allowance_used")
    elif w == "both":
        expected = sorted(EXPECTED_FACT_KEYS + PRODUCT_KEYS)
    else:
        raise ValueError(f"label {cid}: unknown wrapper {w!r}")
    if sorted(keys) != expected:
        raise ValueError(f"label {cid}: inventory mismatch for wrapper {w!r}: "
                         f"got {sorted(keys)}")
    if w == "both":
        for k in PRODUCT_KEYS:
            fams = sorted(_fs_family(f) for f in label["facts"] if f["fact_key"] == k)
            if fams != ["GIA", "ISA"]:
                raise ValueError(f"label {cid}: {k} FS families {fams}, "
                                 f"expected one ISA + one GIA")


def fact_display_key(fact: dict, keys_count: dict) -> str:
    """Disambiguate duplicated product keys by FS family for reporting."""
    k = fact["fact_key"]
    if keys_count.get(k, 0) > 1:
        return f"{k}[{_fs_family(fact)}]"
    return k

# ------------------------------------------------------------- flag parsing

def flag_lines(draft: str) -> list:
    return [ln.strip() for ln in draft.splitlines() if ln.strip().startswith(FLAG_PREFIX)]


def _fact_conflict_spans(fact: dict) -> set:
    return set(fact["spans"]) | set(
        (fact.get("conflict") or {}).get("values_by_span", {}).keys())


def contradiction_catch(label: dict, draft: str, emap: list = None):
    """(n_caught, n_contradictory). Catch = exact-prefix 'ADVISER FLAG:' line
    citing >=1 span belonging to the contradictory fact. Span source: the
    frozen parser's evidence map when provided (tool pipeline — the citation
    authority for all other metrics; handles the parser's bracket
    normalisation, e.g. C039's fullwidth brackets); raw draft-text regex
    otherwise (baseline: no citations exist, so text is the only source)."""
    contradictory = [f for f in label["facts"] if f["status"] == "contradictory"]
    if not contradictory:
        return (None, 0)
    if emap is not None:
        flag_span_sets = [
            {sp["span_id"] for sp in s["spans"] if sp["span_valid"]}
            for s in emap if s["text"].strip().startswith(FLAG_PREFIX)]
    else:
        flag_span_sets = [set(SPAN_RE.findall(ln)) for ln in flag_lines(draft)]
    caught = 0
    for fact in contradictory:
        fact_spans = _fact_conflict_spans(fact)
        if any(fs & fact_spans for fs in flag_span_sets):
            caught += 1
    return (caught, len(contradictory))


def contradiction_catch_textstrict(label: dict, draft: str):
    """Strict ASCII draft-text variant (footnote figure)."""
    contradictory = [f for f in label["facts"] if f["status"] == "contradictory"]
    if not contradictory:
        return (None, 0)
    caught = sum(1 for fact in contradictory
                 if any(set(SPAN_RE.findall(ln)) & _fact_conflict_spans(fact)
                        for ln in flag_lines(draft)))
    return (caught, len(contradictory))

# ------------------------------------------------------------ block mapping

def block_of_statements(draft: str, statements: list) -> dict:
    """Map statement_id -> block index. Blocks = contiguous non-empty,
    non-heading line runs in the draft. A statement maps to the first draft
    line containing its normalised 60-char prefix; unmatched -> own block."""
    lines = draft.splitlines()
    block_id, blocks = -1, []
    prev_blank = True
    for ln in lines:
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            blocks.append(None)
            prev_blank = True
            continue
        if prev_blank:
            block_id += 1
        blocks.append(block_id)
        prev_blank = False
    nlines = [norm(strip_markup(ln)) for ln in lines]
    out, next_free = {}, block_id + 1
    for st in statements:
        probe = norm(strip_markup(st["text"]))[:60]
        hit = None
        if probe:
            for i, nl in enumerate(nlines):
                if blocks[i] is not None and probe and probe in nl:
                    hit = blocks[i]
                    break
        if hit is None:
            hit, next_free = next_free, next_free + 1
        out[st["statement_id"]] = hit
    return out

def _line_cited_blocks(draft: str) -> set:
    """Blocks physically containing a span citation on any line (grounds
    block-level coverage when the parser split a trailing citation-only
    fragment into its own statement). Presence-based: the batch's single
    invalid citation (1/1,689) cannot materially shift this sensitivity
    figure — footnoted."""
    lines = draft.splitlines()
    block_id, out = -1, set()
    prev_blank = True
    for ln in lines:
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            prev_blank = True
            continue
        if prev_blank:
            block_id += 1
        prev_blank = False
        if SPAN_RE.search(ln):
            out.add(block_id)
    return out


# ---------------------------------------------------------------- scoring

def omission(label: dict, draft: str):
    """Ruling 21: per-fact, text-based, pipeline-symmetric. Denominator =
    the case's own inventory size (ss_isa 17 / gia 16 / both 20). Duplicated
    product keys share one detector (pair moves together). Returns
    (omitted display keys, inventory size)."""
    t = norm(draft)
    keys_count = {}
    for f in label["facts"]:
        keys_count[f["fact_key"]] = keys_count.get(f["fact_key"], 0) + 1
    omitted = [fact_display_key(f, keys_count) for f in label["facts"]
               if not detect_fact(f, t)]
    return omitted, len(label["facts"])


def score_tool(label: dict, emap: list, draft: str) -> dict:
    stubs = [s for s in emap if is_stub(s["text"])]
    scored = [s for s in emap if not is_stub(s["text"])]
    n = len(scored)
    unsupported = [s for s in scored if s["status"] == "unsupported"]
    insufficient = [s for s in scored if s["status"] == "insufficient"]

    # block-level sensitivity: unsupported covered if its block holds a
    # statement with >=1 valid citation
    blocks = block_of_statements(draft, emap)
    cited_blocks = {blocks[s["statement_id"]] for s in emap
                    if any(sp["span_valid"] for sp in s["spans"])}
    cited_blocks |= _line_cited_blocks(draft)
    unsupported_block = [s for s in unsupported
                         if blocks[s["statement_id"]] not in cited_blocks]

    all_citations = [sp for s in emap for sp in s["spans"]]
    invalid = [sp for sp in all_citations if not sp["span_valid"]]

    label_spans = set()
    for f in label["facts"]:
        label_spans |= set(f["spans"])
        label_spans |= set((f.get("conflict") or {}).get("values_by_span", {}).keys())
    cited_valid_unique = {sp["span_id"] for sp in all_citations if sp["span_valid"]}
    matched = cited_valid_unique & label_spans
    cited_fact_unique = {s for s in cited_valid_unique
                         if s.startswith(("FF:", "TR:", "FS:"))}
    matched_fact = cited_fact_unique & label_spans

    supported_facts = [f for f in label["facts"] if f["status"] == "supported"]
    recalled = [f for f in supported_facts
                if set(f["spans"]) & cited_valid_unique]

    omitted, n_inventory = omission(label, draft)

    caught, n_contra = contradiction_catch(label, draft, emap)
    caught_ts, _ = contradiction_catch_textstrict(label, draft)
    return {
        "pipeline": "tool",
        "n_statements": len(emap),
        "n_stubs": len(stubs),
        "n_scored": n,
        "unsupported_rate": len(unsupported) / n if n else None,
        "unsupported_rate_block": len(unsupported_block) / n if n else None,
        "insufficient_rate": len(insufficient) / n if n else None,
        "omission_rate": len(omitted) / n_inventory,
        "n_inventory": n_inventory,
        "omitted_keys": omitted,
        "contradiction_caught": caught,
        "contradiction_caught_textstrict": caught_ts,
        "contradiction_total": n_contra,
        "em_precision_fact": len(matched_fact) / len(cited_fact_unique) if cited_fact_unique else None,
        "em_precision_fact_matched": len(matched_fact),
        "em_precision_fact_cited_unique": len(cited_fact_unique),
        "em_precision_all": len(matched) / len(cited_valid_unique) if cited_valid_unique else None,
        "em_precision_all_matched": len(matched),
        "em_precision_all_cited_unique": len(cited_valid_unique),
        "em_recall": len(recalled) / len(supported_facts) if supported_facts else None,
        "em_recall_recalled": len(recalled),
        "em_recall_supported_facts": len(supported_facts),
        "invalid_span_rate": len(invalid) / len(all_citations) if all_citations else None,
        "n_citations": len(all_citations),
        "n_flags": len(flag_lines(draft)),
    }


def score_baseline(label: dict, draft: str) -> dict:
    omitted, n_inventory = omission(label, draft)
    caught, n_contra = contradiction_catch(label, draft)
    return {
        "pipeline": "baseline",
        "n_statements": None, "n_stubs": None, "n_scored": None,
        "unsupported_rate": 1.0,          # no citations, by construction
        "unsupported_rate_block": 1.0,
        "insufficient_rate": None,
        "omission_rate": len(omitted) / n_inventory,
        "n_inventory": n_inventory,
        "omitted_keys": omitted,
        "contradiction_caught": caught,
        "contradiction_caught_textstrict": caught,   # baseline is text-based
        "contradiction_total": n_contra,
        "em_precision_fact": None, "em_precision_fact_matched": None,
        "em_precision_fact_cited_unique": None,
        "em_precision_all": None, "em_precision_all_matched": None,
        "em_precision_all_cited_unique": None,
        "em_recall": 0.0, "em_recall_recalled": 0,
        "em_recall_supported_facts": sum(1 for f in label["facts"]
                                         if f["status"] == "supported"),
        "invalid_span_rate": None, "n_citations": 0,
        "n_flags": len(flag_lines(draft)),
    }


def evaluate_case(label_p, emap_p, tool_p, baseline_p) -> dict:
    label = load_json(Path(label_p))
    validate_label(label)
    out = {"case_id": label["case_id"], "condition": label["condition"],
           "harness_version": HARNESS_VERSION}
    if emap_p and tool_p:
        out["tool"] = score_tool(label, load_json(Path(emap_p)), load_text(Path(tool_p)))
    if baseline_p:
        out["baseline"] = score_baseline(label, load_text(Path(baseline_p)))
    return out

# ---------------------------------------------------------------- selftest

def approx(a, b, eps=1e-9):
    return (a is None and b is None) or (a is not None and b is not None
                                         and abs(a - b) < eps)


def selftest(root: Path) -> int:
    """Unit tests: canonical dev_archive C004 + C001 vs hand-computed values."""
    da, labels = root / "dev_archive", root / "labels"
    failures = []

    def check(name, got, want):
        ok = approx(got, want) if isinstance(want, float) or want is None \
            else got == want
        if not ok:
            failures.append(f"{name}: got {got!r} want {want!r}")

    r4 = evaluate_case(labels / "label_C004.json", da / "C004_evidence_map.json",
                       da / "C004_tool.md", da / "C004_baseline.md")
    t4, b4 = r4["tool"], r4["baseline"]
    # C004 tool — hand-computed
    check("C004 tool n_statements", t4["n_statements"], 30)
    check("C004 tool n_stubs", t4["n_stubs"], 2)            # S007, S030
    check("C004 tool n_scored", t4["n_scored"], 28)
    check("C004 tool unsupported", t4["unsupported_rate"], 1 / 28)   # S001
    check("C004 tool unsupported_block", t4["unsupported_rate_block"], 0.0)
    check("C004 tool insufficient", t4["insufficient_rate"], 0.0)
    check("C004 tool omission", t4["omission_rate"], 2 / 17)
    check("C004 tool omitted", sorted(t4["omitted_keys"]),
          ["client_identity", "isa_allowance_used"])
    check("C004 tool contradiction", t4["contradiction_caught"], None)
    check("C004 tool precision_fact", t4["em_precision_fact"], 18 / 27)
    check("C004 tool precision_all", t4["em_precision_all"], 18 / 28)
    check("C004 tool recall", t4["em_recall"], 15 / 17)
    check("C004 tool invalid", t4["invalid_span_rate"], 0.0)
    check("C004 tool n_citations", t4["n_citations"], 42)
    check("C004 tool flags", t4["n_flags"], 1)
    # C004 baseline
    check("C004 base unsupported", b4["unsupported_rate"], 1.0)
    check("C004 base omission", b4["omission_rate"], 2 / 17)
    check("C004 base omitted", sorted(b4["omitted_keys"]),
          ["client_identity", "isa_allowance_used"])
    check("C004 base flags", b4["n_flags"], 0)
    check("C004 base recall", b4["em_recall"], 0.0)

    r1 = evaluate_case(labels / "label_C001.json", da / "C001_evidence_map.json",
                       da / "C001_tool.md", da / "C001_baseline.md")
    t1, b1 = r1["tool"], r1["baseline"]
    # C001 tool — hand-computed
    check("C001 tool n_statements", t1["n_statements"], 31)
    check("C001 tool n_stubs", t1["n_stubs"], 2)            # S008, S031
    check("C001 tool n_scored", t1["n_scored"], 29)
    check("C001 tool unsupported", t1["unsupported_rate"], 3 / 29)  # S001,S025,S026
    check("C001 tool unsupported_block", t1["unsupported_rate_block"], 0.0)
    check("C001 tool omission", t1["omission_rate"], 2 / 17)
    check("C001 tool omitted", sorted(t1["omitted_keys"]),
          ["client_identity", "isa_allowance_used"])
    check("C001 tool contradiction", t1["contradiction_caught"], 1)
    check("C001 tool contradiction_total", t1["contradiction_total"], 1)
    check("C001 tool precision_fact", t1["em_precision_fact"], 16 / 27)
    check("C001 tool precision_all", t1["em_precision_all"], 16 / 28)
    check("C001 tool recall", t1["em_recall"], 14 / 16)
    check("C001 tool invalid", t1["invalid_span_rate"], 0.0)
    check("C001 tool n_citations", t1["n_citations"], 40)
    check("C001 tool flags", t1["n_flags"], 1)
    # C001 baseline — silent horizon resolution: no flag -> catch 0/1
    check("C001 base contradiction", b1["contradiction_caught"], 0)
    check("C001 base contradiction_total", b1["contradiction_total"], 1)
    check("C001 base omission", b1["omission_rate"], 2 / 17)
    check("C001 base unsupported", b1["unsupported_rate"], 1.0)
    check("C001 base flags", b1["n_flags"], 0)

    # ---- ruling-21 fixtures (frozen batch outputs, hand-computed 2026-08-18)
    batch = root / "batch"
    r3 = evaluate_case(batch / "label_C003.json", batch / "C003_evidence_map.json",
                       batch / "C003_tool.md", batch / "C003_baseline.md")
    t3, b3 = r3["tool"], r3["baseline"]
    check("C003 gia n_inventory", t3["n_inventory"], 16)
    check("C003 tool n_statements", t3["n_statements"], 33)
    check("C003 tool n_stubs", t3["n_stubs"], 1)
    check("C003 tool unsupported", t3["unsupported_rate"], 3 / 32)   # S001,S032,S033
    check("C003 tool unsupported_block", t3["unsupported_rate_block"], 2 / 32)
    check("C003 tool insufficient", t3["insufficient_rate"], 0.0)
    check("C003 tool omission", t3["omission_rate"], 2 / 16)
    check("C003 tool omitted", sorted(t3["omitted_keys"]),
          ["client_identity", "investment_horizon"])   # horizon = missing status
    check("C003 tool precision_fact", t3["em_precision_fact"], 20 / 32)
    check("C003 tool precision_all", t3["em_precision_all"], 20 / 33)
    check("C003 tool recall", t3["em_recall"], 13 / 15)
    check("C003 tool invalid", t3["invalid_span_rate"], 0.0)
    check("C003 tool n_citations", t3["n_citations"], 41)
    check("C003 tool flags", t3["n_flags"], 0)
    check("C003 base omission", b3["omission_rate"], 2 / 16)
    r2 = evaluate_case(batch / "label_C002.json", batch / "C002_evidence_map.json",
                       batch / "C002_tool.md", batch / "C002_baseline.md")
    t2, b2 = r2["tool"], r2["baseline"]
    check("C002 both n_inventory", t2["n_inventory"], 20)
    check("C002 tool n_statements", t2["n_statements"], 37)
    check("C002 tool n_stubs", t2["n_stubs"], 0)
    check("C002 tool unsupported", t2["unsupported_rate"], 2 / 37)   # S001,S021
    check("C002 tool unsupported_block", t2["unsupported_rate_block"], 0.0)
    check("C002 tool insufficient", t2["insufficient_rate"], 2 / 37)  # S036,S037
    check("C002 tool omission", t2["omission_rate"], 3 / 20)
    check("C002 tool omitted", sorted(t2["omitted_keys"]),
          ["capacity_for_loss", "client_identity", "liabilities"])
    check("C002 tool precision_fact", t2["em_precision_fact"], 19 / 36)
    check("C002 tool precision_all", t2["em_precision_all"], 19 / 37)
    check("C002 tool recall", t2["em_recall"], 17 / 19)
    check("C002 tool invalid", t2["invalid_span_rate"], 0.0)
    check("C002 tool n_citations", t2["n_citations"], 56)
    check("C002 tool flags", t2["n_flags"], 0)
    check("C002 base omission", b2["omission_rate"], 2 / 20)

    print(HARNESS_VERSION)
    if failures:
        print(f"SELFTEST FAIL ({len(failures)}):")
        for f in failures:
            print("  ", f)
        return 1
    print(f"SELFTEST PASS — 71 assertions, C004+C001, tool+baseline")
    for cid, res in (("C004", r4), ("C001", r1)):
        t = res["tool"]
        print(f"  {cid}: statements={t['n_statements']} stubs={t['n_stubs']} "
              f"unsupported={t['unsupported_rate']:.4f} "
              f"omission={t['omission_rate']:.4f} "
              f"precision_fact={t['em_precision_fact']:.4f} "
              f"precision_all={t['em_precision_all']:.4f} recall={t['em_recall']:.4f} "
              f"invalid={t['invalid_span_rate']:.4f} flags={t['n_flags']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--label"), ap.add_argument("--evidence-map")
    ap.add_argument("--tool-draft"), ap.add_argument("--baseline-draft")
    ap.add_argument("--out", help="write JSON result here (only write the harness does)")
    ap.add_argument("--selftest", metavar="ROOT",
                    help="run unit tests; ROOT holds dev_archive/ and labels/")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest(Path(a.selftest)))
    if not a.label:
        ap.error("--label required (or --selftest ROOT)")
    res = evaluate_case(a.label, a.evidence_map, a.tool_draft, a.baseline_draft)
    js = json.dumps(res, indent=1)
    if a.out:
        Path(a.out).write_text(js, encoding="utf-8")
    print(js)


if __name__ == "__main__":
    main()
