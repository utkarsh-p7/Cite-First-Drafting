# evaluate.py — harness notes (eval-harness v1.2.1, 2026-08-18)

Deterministic RQ1 scoring harness. No API calls. Reads label + evidence-map JSON +
draft md; writes nothing except an optional `--out` JSON.

## Version history
- v1.0.0 → v1.1.0: dual precision figures (ruled 2026-08-16).
- v1.1.0 → v1.2.0 (**ruling 21**, code-freeze exemption): omission denominator =
  case's own inventory (ss_isa 17 / gia 16 / both 20); shape-strict label
  validation per wrapper (anything else = hard error); detectors refined
  (primary_objective = content-token match, tokens ≥6 chars; isa_allowance_used
  = "allowance"+"used"; wrapper "both" = ISA∧GIA); block coverage additionally
  counts a block as cited if any line physically contains a span citation
  (handles parser-split citation-only fragments, e.g. C002-S022).
- v1.2.0 → v1.2.1 (**RATIFIED — ruling 22, 2026-08-18**): tool-side contradiction catch reads
  flag-line citations from the frozen parser's evidence map (citation authority
  for all other metrics; normalises non-ASCII brackets — C039's flag cites both
  correct spans via fullwidth 【】). Strict ASCII draft-text figure kept as
  `contradiction_caught_textstrict` (footnote). Baseline catch: draft-text
  (no evidence map exists).

## Run
- Single case: `python evaluate.py --label <label.json> --evidence-map <map.json> --tool-draft <tool.md> --baseline-draft <baseline.md> [--out r.json]`
- Unit tests: `python evaluate.py --selftest <ROOT>`; ROOT holds `dev_archive/`
  (canonical C004/C001), `labels/` (label_C001/C004), and `batch/` (frozen batch
  C002/C003 label + evidence map + tool + baseline files).

## Metric definitions as implemented (ruled decisions encoded)
- **unsupported_rate** (sentence-strict, PRIMARY): status `unsupported` / scored statements; stubs (lead-ins ending ':', "None identified.") excluded, counted.
- **unsupported_rate_block** (SENSITIVITY): unsupported counts as covered if its blank-line/heading-delimited block has a validly-cited statement OR a line physically containing a span citation. Presence-based note: the batch's single invalid citation (1/1,689, C021) cannot materially shift this figure.
- **insufficient_rate**: status `insufficient` / scored. Separate column.
- **omission_rate** (ruling 21): label-inventory facts whose value is undetectable in the draft / case's own inventory size (17/16/20; mix 27/5/8). Text-based, pipeline-symmetric detectors; 'missing'-status keys count absent for both pipelines; in 'both' cases each duplicated product pair shares one detector (moves together — granularity limitation). Structural-row presence = check_structure output, separate.
- **contradiction_catch**: labelled `contradictory` facts with a line-start `ADVISER FLAG:` citing ≥1 span of that fact — span source per v1.2.1 above.
- **em_precision_fact** (PRIMARY) / **em_precision_all** (secondary, footnoted): as v1.1.0; KB: = regulatory grounding, span_valid-validated only.
- **em_recall**: labelled supported facts with ≥1 own span cited / all supported facts (unchanged by ruling 21).
- **invalid_span_rate**: `span_valid:false` instances / all citation instances. Separate.
- **Baseline**: unsupported 1.0 by construction; recall 0.0; precision/invalid n/a; omission + catch from draft text.

## Unit-test expected values (all hand-computed; selftest 71 assertions)
| metric | C004 tool (dev) | C001 tool (dev) | C003 tool (gia) | C002 tool (both) |
|---|---|---|---|---|
| statements / stubs / scored | 30 / 2 / 28 | 31 / 2 / 29 | 33 / 1 / 32 | 37 / 0 / 37 |
| unsupported (strict / block) | 1/28 / 0 | 3/29 / 0 | 3/32 / 2/32 | 2/37 / 0 |
| insufficient | 0 | 0 | 0 | 2/37 |
| omission (denominator) | 2/17 | 2/17 | 2/16 | 3/20 |
| omitted keys | client_identity, isa_allowance_used | same | client_identity, investment_horizon (missing) | client_identity, capacity_for_loss (missing), liabilities |
| contradiction catch | n/a | 1/1 (baseline 0/1) | n/a | n/a |
| em precision fact / all | 18/27 / 18/28 | 16/27 / 16/28 | 20/32 / 20/33 | 19/36 / 19/37 |
| em recall | 15/17 | 14/16 | 13/15 | 17/19 |
| invalid / citations | 0/42 | 0/40 | 0/41 | 0/56 |
| baseline omission | 2/17 | 2/17 | 2/16 | 2/20 |

Selftest PASS, byte-identical across repeated runs; full 40-case T2 run also
byte-identical across repeated runs (task2-runner v1.1.0).
