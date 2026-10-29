# Cite-First Drafting

> **All data in this repository is synthetic and fictitious.** No real clients, advisers or firms. Nothing here is financial advice.

Evidence-linked AI drafting for regulated financial reports. Every material sentence the model writes carries the exact source span it rests on, so a human reviewer checks pointers instead of rereading the file.

Built from my MSc Applied AI dissertation artefact (WMG, University of Warwick, 2026): an evidence-linked generative AI tool that drafts FCA-compliant initial suitability reports for UK micro-adviser firms, evaluated statement by statement on a seeded synthetic corpus of 40 cases against an unlinked baseline.

**Frozen dissertation artefact:** [original repo](https://github.com/utkarsh-p7/MSc-Dissertation-Tailored-evidence-linking-tool-for-compliance-based-report-drafting)

## Quick start

```bash
pip install -e ".[dev]"
pytest            # 71-assertion harness self-test + regression tests against frozen v1 outputs
```

The core package is pure standard library. `pip install -e ".[providers]"` adds live Groq/Anthropic drafting; the default `replay` provider serves the frozen outputs with no API key.

## Headline v1 results (frozen, 40 cases, tool vs unlinked baseline)

| Metric | Tool | Baseline |
|---|---|---|
| Unsupported-statement rate | 0.079 | 1.000 (by construction) |
| Omission rate | 0.130 | 0.122 (difference not significant, p = 0.189) |
| Seeded contradictions caught | 2 of 3 | 0 of 3 |
| Evidence-map precision (fact) / recall | 0.596 / 0.885 | n/a |
| Invalid (hallucinated) span citations | 1 of 1,689 | n/a |

Honest reading: evidence linking makes drafts checkable and surfaces some gaps; it does not by itself prevent omissions. v2 targets exactly that.

## Layout

```
src/cite_first_drafting/
  context/     deterministic context assembly (FF:/TR:/FS:/KB: spans, no retrieval)
  drafting/    prompts, template, evidence-map parser (evmap-1.3.0), structural check, drafter
  providers/   replay (default) · groq · anthropic
  evaluation/  the dissertation scoring harness, verbatim (eval-harness v1.2.1)
data/          synthetic corpus, labels, regulatory KB extracts
research/v1/   frozen dissertation outputs and results (never edited)
tests/         regression + unit tests
```

Licensed under PolyForm Noncommercial 1.0.0: free to view, modify and use for non-commercial and academic purposes with the notice kept intact; commercial use requires permission from the author. This is a source-available licence, not an OSI open-source licence.
