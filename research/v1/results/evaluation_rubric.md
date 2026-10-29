# Evaluation rubric (distinct from KB)

## (a) Structural-compliance criteria — from /profiles/initial_report.md
Scoring per report: **present / partial / absent** per row. Machine-checkable rows only (#1, 2, 5, 6-link, 7-flag, 10-presence, 11-presence, 13, 14). Substantive rows (#3, 4-adequacy, 8, 9, 12) are **flag-only**: tool surfaces evidence; human panel judges. Never auto-scored.

Primary RQ1 metrics on the seeded synthetic corpus (metric names as Ch3 §3.5):
- **Unsupported-statement rate**: material statements with no valid supporting evidence link.
- **Omission rate** (ruling 21, 2026-08-18): material-fact inventory keys absent from the draft, over the case's OWN label inventory — ss_isa 17 keys (27 cases) · gia 16 (5 cases; isa_allowance_used absent by construction) · both 20 (8 cases; product triplet once per FS:ISA/FS:GIA family). Aggregate = mean of per-case proportions; detection text-based and pipeline-symmetric; duplicated product pairs share one detector (granularity limitation, footnoted).
- **Contradiction catch-rate**: labelled contradictory facts for which the draft contains a line beginning exactly "ADVISER FLAG:" citing ≥1 correct span.
- **Evidence-map precision** (two figures, ruled 2026-08-16 — definitional fix pre-results): **primary = fact-citation precision** — cited spans matching the label's supporting span, over cited FF:/TR:/FS: spans only (label-matchable by construction); **secondary (footnoted) = all-citation precision** — same numerator over all cited spans incl. KB:. KB: citations are regulatory grounding, validated by span_valid only, never label-matchable.
- **Evidence-map recall**: labelled supported facts that received a citation, over all labelled supported facts.
- **Invalid-span rate**: citations with span_valid = false; reported separately from the unsupported-statement rate.

("False-evidence rate" removed 2026-08-13 — superseded by evidence-map precision + invalid-span rate.)

### Scoring-unit decisions (ruled, final — do not reopen)
- Sentence-strict scoring = **primary**.
- Block-level scoring (one citation covers its contiguous block) = **sensitivity analysis only**.
- Boilerplate stubs excluded from all denominators; stub count footnoted.
- Invalid-span rate reported separately from unsupported rate.

## (b) Suitability dimensions — FSA 2010 suitability-assessment template (ARCHIVAL)
Dimensions retained as analytic lenses only: needs/objectives match · ATR-vs-recommendation · switch/replacement justification · cost & value-for-money · ongoing-review arrangements.
**Flag: FSA template is archival (pre-2013 regulator).** Current authority = COBS 9A + Consumer Duty (PRIN 2A / FG22/5). Each dimension maps to profile rows: needs→#3, ATR→#4/#7, cost→#10, review→#5. Switch justification: out of v1 scope (no replacement business) — recorded, unused.

## (c) Explainability & timing (RQ2/RQ3) — analytic, no instruments administered (PIVOT 2026-08-04)
- **RQ3 — explainability-by-design**: assessed analytically by mapping evidence-map features (span citations, insufficient-evidence flags, ADVISER FLAG lines, missing-info checklist, invalid-span validation) against the explanation-goodness criteria of Hoffman et al. (2018, arXiv:1812.04608). **No instruments administered** (no ESS, no TIAS); no human participants. Practitioner validation stated as **future work**.
- **RQ2 — timing**: machine-timed time-to-first-draft (per-draft wall-clock from run_log.jsonl), contextualised against published industry drafting-time figures — explicitly indicative; no like-for-like claim.
