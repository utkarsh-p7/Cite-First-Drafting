# Task 2 — RQ1 results, frozen batch (n=40)

Scored by eval-harness v1.2.1 (2026-08-18) · task2-runner v1.1.0 (2026-08-18, ruling 21) · selftest 71/71 PASS re-run pre-batch. Sentence-strict = PRIMARY; block-level = sensitivity only. Baseline unsupported-rate = 1.0 by construction (no citations); baseline precision/invalid-span n/a.

## 1. Per-case paired table (tool vs baseline)

| case | condition | pipeline | unsup (strict) | unsup (block) | insuff | omission | catch | prec-fact | prec-all | recall | invalid | stubs | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C001 | hard:contradiction | tool | 0.033 | 0.000 | 0.000 | 0.118 | 1/1 | 0.581 | 0.562 | 0.875 | 0.000 | 2 | 1 |
| C001 | hard:contradiction | baseline | 1.000 | 1.000 | — | 0.118 | 0/1 | — | — | 0.000 | — | — | 0 |
| C002 | hard:absent_capacity | tool | 0.054 | 0.000 | 0.054 | 0.150 | n/a | 0.528 | 0.514 | 0.895 | 0.000 | 0 | 0 |
| C002 | hard:absent_capacity | baseline | 1.000 | 1.000 | — | 0.100 | n/a | — | — | 0.000 | — | — | 0 |
| C003 | hard:ambiguous_horizon | tool | 0.094 | 0.062 | 0.000 | 0.125 | n/a | 0.625 | 0.606 | 0.867 | 0.000 | 1 | 0 |
| C003 | hard:ambiguous_horizon | baseline | 1.000 | 1.000 | — | 0.125 | n/a | — | — | 0.000 | — | — | 0 |
| C004 | clean | tool | 0.031 | 0.000 | 0.000 | 0.118 | n/a | 0.515 | 0.500 | 0.882 | 0.000 | 2 | 0 |
| C004 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C005 | clean | tool | 0.000 | 0.000 | 0.000 | 0.176 | n/a | 0.516 | 0.500 | 0.882 | 0.000 | 1 | 0 |
| C005 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C006 | clean | tool | 0.036 | 0.000 | 0.000 | 0.118 | n/a | 0.654 | 0.630 | 0.882 | 0.000 | 1 | 1 |
| C006 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C007 | clean | tool | 0.036 | 0.000 | 0.071 | 0.059 | n/a | 0.643 | 0.621 | 1.000 | 0.000 | 0 | 0 |
| C007 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C008 | hard:absent_capacity | tool | 0.032 | 0.000 | 0.000 | 0.235 | n/a | 0.593 | 0.571 | 0.875 | 0.000 | 0 | 0 |
| C008 | hard:absent_capacity | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C009 | hard:missing_risk | tool | 0.042 | 0.000 | 0.042 | 0.176 | n/a | 0.621 | 0.600 | 0.938 | 0.000 | 0 | 1 |
| C009 | hard:missing_risk | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C010 | clean | tool | 0.160 | 0.000 | 0.000 | 0.176 | n/a | 0.577 | 0.556 | 0.824 | 0.000 | 2 | 0 |
| C010 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C011 | clean | tool | 0.036 | 0.000 | 0.000 | 0.100 | n/a | 0.613 | 0.594 | 0.900 | 0.000 | 2 | 0 |
| C011 | clean | baseline | 1.000 | 1.000 | — | 0.150 | n/a | — | — | 0.000 | — | — | 0 |
| C012 | clean | tool | 0.150 | 0.000 | 0.000 | 0.176 | n/a | 0.625 | 0.600 | 0.765 | 0.000 | 1 | 0 |
| C012 | clean | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C013 | clean | tool | 0.103 | 0.000 | 0.000 | 0.150 | n/a | 0.571 | 0.556 | 0.900 | 0.000 | 1 | 0 |
| C013 | clean | baseline | 1.000 | 1.000 | — | 0.150 | n/a | — | — | 0.000 | — | — | 0 |
| C014 | clean | tool | 0.037 | 0.000 | 0.000 | 0.176 | n/a | 0.538 | 0.519 | 0.765 | 0.000 | 1 | 0 |
| C014 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C015 | clean | tool | 0.032 | 0.000 | 0.000 | 0.059 | n/a | 0.548 | 0.515 | 0.941 | 0.000 | 1 | 1 |
| C015 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C016 | clean | tool | 0.038 | 0.000 | 0.000 | 0.125 | n/a | 0.704 | 0.655 | 0.812 | 0.000 | 2 | 0 |
| C016 | clean | baseline | 1.000 | 1.000 | — | 0.062 | n/a | — | — | 0.000 | — | — | 0 |
| C017 | clean | tool | 0.040 | 0.000 | 0.000 | 0.118 | n/a | 0.571 | 0.552 | 0.882 | 0.000 | 1 | 0 |
| C017 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C018 | clean | tool | 0.069 | 0.000 | 0.034 | 0.100 | n/a | 0.562 | 0.545 | 0.800 | 0.000 | 1 | 0 |
| C018 | clean | baseline | 1.000 | 1.000 | — | 0.150 | n/a | — | — | 0.000 | — | — | 0 |
| C019 | clean | tool | 0.030 | 0.000 | 0.000 | 0.050 | n/a | 0.667 | 0.650 | 0.950 | 0.000 | 2 | 0 |
| C019 | clean | baseline | 1.000 | 1.000 | — | 0.050 | n/a | — | — | 0.000 | — | — | 0 |
| C020 | clean | tool | 0.286 | 0.000 | 0.000 | 0.118 | n/a | 0.630 | 0.607 | 0.941 | 0.000 | 1 | 0 |
| C020 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C021 | clean | tool | 0.036 | 0.000 | 0.000 | 0.062 | n/a | 0.621 | 0.600 | 0.938 | 0.025 | 2 | 0 |
| C021 | clean | baseline | 1.000 | 1.000 | — | 0.312 | n/a | — | — | 0.000 | — | — | 0 |
| C022 | clean | tool | 0.065 | 0.032 | 0.032 | 0.059 | n/a | 0.562 | 0.545 | 1.000 | 0.000 | 1 | 0 |
| C022 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C023 | clean | tool | 0.036 | 0.000 | 0.000 | 0.118 | n/a | 0.615 | 0.571 | 0.824 | 0.000 | 1 | 0 |
| C023 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C024 | clean | tool | 0.148 | 0.000 | 0.000 | 0.118 | n/a | 0.545 | 0.529 | 1.000 | 0.000 | 2 | 0 |
| C024 | clean | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C025 | clean | tool | 0.103 | 0.000 | 0.000 | 0.059 | n/a | 0.600 | 0.581 | 0.941 | 0.000 | 1 | 1 |
| C025 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C026 | clean | tool | 0.037 | 0.000 | 0.000 | 0.118 | n/a | 0.600 | 0.581 | 0.941 | 0.000 | 1 | 0 |
| C026 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C027 | clean | tool | 0.133 | 0.000 | 0.067 | 0.118 | n/a | 0.615 | 0.593 | 0.882 | 0.000 | 1 | 0 |
| C027 | clean | baseline | 1.000 | 1.000 | — | 0.059 | n/a | — | — | 0.000 | — | — | 0 |
| C028 | clean | tool | 0.121 | 0.000 | 0.061 | 0.100 | n/a | 0.618 | 0.600 | 0.900 | 0.000 | 1 | 0 |
| C028 | clean | baseline | 1.000 | 1.000 | — | 0.050 | n/a | — | — | 0.000 | — | — | 0 |
| C029 | hard:ambiguous_horizon | tool | 0.212 | 0.000 | 0.000 | 0.176 | n/a | 0.621 | 0.600 | 0.875 | 0.000 | 1 | 0 |
| C029 | hard:ambiguous_horizon | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C030 | hard:missing_risk | tool | 0.074 | 0.000 | 0.074 | 0.235 | n/a | 0.533 | 0.516 | 0.875 | 0.000 | 0 | 1 |
| C030 | hard:missing_risk | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C031 | clean | tool | 0.029 | 0.000 | 0.029 | 0.150 | n/a | 0.567 | 0.548 | 0.800 | 0.000 | 0 | 1 |
| C031 | clean | baseline | 1.000 | 1.000 | — | 0.200 | n/a | — | — | 0.000 | — | — | 0 |
| C032 | clean | tool | 0.091 | 0.000 | 0.000 | 0.176 | n/a | 0.593 | 0.571 | 0.882 | 0.000 | 2 | 0 |
| C032 | clean | baseline | 1.000 | 1.000 | — | 0.176 | n/a | — | — | 0.000 | — | — | 0 |
| C033 | hard:contradiction | tool | 0.083 | 0.000 | 0.000 | 0.059 | 0/1 | 0.613 | 0.594 | 1.000 | 0.000 | 1 | 1 |
| C033 | hard:contradiction | baseline | 1.000 | 1.000 | — | 0.118 | 0/1 | — | — | 0.000 | — | — | 0 |
| C034 | hard:ambiguous_horizon | tool | 0.036 | 0.000 | 0.000 | 0.235 | n/a | 0.667 | 0.645 | 0.875 | 0.000 | 2 | 0 |
| C034 | hard:ambiguous_horizon | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C035 | hard:missing_risk | tool | 0.069 | 0.000 | 0.000 | 0.125 | n/a | 0.519 | 0.500 | 0.867 | 0.000 | 2 | 0 |
| C035 | hard:missing_risk | baseline | 1.000 | 1.000 | — | 0.125 | n/a | — | — | 0.000 | — | — | 0 |
| C036 | clean | tool | 0.037 | 0.000 | 0.000 | 0.118 | n/a | 0.571 | 0.552 | 0.882 | 0.000 | 2 | 1 |
| C036 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C037 | clean | tool | 0.037 | 0.000 | 0.000 | 0.150 | n/a | 0.679 | 0.655 | 0.850 | 0.000 | 2 | 0 |
| C037 | clean | baseline | 1.000 | 1.000 | — | 0.100 | n/a | — | — | 0.000 | — | — | 0 |
| C038 | clean | tool | 0.143 | 0.000 | 0.000 | 0.118 | n/a | 0.536 | 0.517 | 0.765 | 0.000 | 2 | 0 |
| C038 | clean | baseline | 1.000 | 1.000 | — | 0.118 | n/a | — | — | 0.000 | — | — | 0 |
| C039 | hard:contradiction | tool | 0.160 | 0.120 | 0.000 | 0.062 | 1/1 | 0.615 | 0.593 | 0.867 | 0.000 | 1 | 1 |
| C039 | hard:contradiction | baseline | 1.000 | 1.000 | — | 0.062 | 0/1 | — | — | 0.000 | — | — | 0 |
| C040 | hard:absent_capacity | tool | 0.172 | 0.138 | 0.000 | 0.235 | n/a | 0.654 | 0.630 | 0.875 | 0.000 | 0 | 1 |
| C040 | hard:absent_capacity | baseline | 1.000 | 1.000 | — | 0.235 | n/a | — | — | 0.000 | — | — | 0 |

## 2. Aggregate (mean of per-case rates; catch = pooled)

| pipeline | unsup (strict) | insuff | omission | catch | prec-fact | prec-all | recall | invalid | flags |
|---|---|---|---|---|---|---|---|---|---|
| tool | 0.079 | 0.012 | 0.130 | 2/3 | 0.596 | 0.574 | 0.885 | 0.001 | 11 |
| baseline | 1.000 | — | 0.122 | 0/3 | — | — | 0.000 | — | 0 |

## 3. Per-condition breakdown (tool | baseline)

| condition | n | unsup strict T/B | omission T/B | catch T/B | prec-fact T | recall T | invalid T | flags T/B |
|---|---|---|---|---|---|---|---|---|
| clean | 28 | 0.075 / 1.000 | 0.117 / 0.113 | n/a / n/a | 0.595 | 0.883 | 0.001 | 5 / 0 |
| hard:missing_risk | 3 | 0.062 / 1.000 | 0.179 / 0.159 | n/a / n/a | 0.558 | 0.893 | 0.000 | 2 / 0 |
| hard:absent_capacity | 3 | 0.086 / 1.000 | 0.207 / 0.171 | n/a / n/a | 0.591 | 0.882 | 0.000 | 1 / 0 |
| hard:ambiguous_horizon | 3 | 0.114 / 1.000 | 0.179 / 0.140 | n/a / n/a | 0.637 | 0.872 | 0.000 | 0 / 0 |
| hard:contradiction | 3 | 0.092 / 1.000 | 0.080 / 0.099 | 2/3 / 0/3 | 0.603 | 0.914 | 0.000 | 3 / 0 |

## 4. Sentence-strict vs block-level sensitivity (tool)

| scoring unit | mean unsupported rate |
|---|---|
| sentence-strict (PRIMARY) | 0.079 |
| block-level (sensitivity) | 0.009 |

**Inventory-shape footnote (ruling 21).** Omission denominator = each case's own label inventory: ss_isa 17 keys (27 cases) · gia 16 keys (5 cases; isa_allowance_used absent by construction) · both 20 keys (8 cases; product triplet once per FS:ISA/FS:GIA family). Observed mix: {16: 5, 17: 27, 20: 8}. Aggregate = mean of per-case proportions, identical for both pipelines. Granularity limitation: presence detection is text-based and pipeline-symmetric; in 'both' cases each duplicated product pair shares one detector, so the pair moves together. Keys with label status 'missing' have no value to state and count as absent for BOTH pipelines symmetrically. Block-coverage note: a block counts as cited if any of its lines physically contains a span citation; the batch's single invalid citation (1/1,689, C021) cannot materially shift the block-level sensitivity figure.


**Stub footnote.** 47 boilerplate stubs (lead-ins/'None identified.' fillers) excluded from statement denominators across the 40 tool drafts (1186 raw statements → 1139 scored). Per-case stub counts in column 'stubs'. Omission-rate note: label keys with status 'missing' have no value to state and count as absent for BOTH pipelines symmetrically.

**Contradiction-catch source footnote (ratified — ruling 22, 2026-08-18).** Primary catch figure reads flag-line citations from the FROZEN PARSER's evidence map (the citation authority for all other metrics; it normalises non-ASCII citation brackets — C039's flag cites both correct spans via fullwidth brackets). Strict ASCII draft-text variant (CSV column contradiction_caught_textstrict): tool 1/3 (C039 not counted). C033: flag raised but addresses ATR-vs-capacity, not the labelled horizon contradiction — genuine miss under both variants. Baseline catch is draft-text based (no evidence map exists).

## 5. Variance delta — C004/C001 run1 (frozen batch) vs run2 (variance_check)

Same harness, same labels; run2 = mother-commissioned re-run, identical params (temp 0, seed 42). Deltas quantify provider-side non-determinism (Ch4 footnote).

| case | metric | run1 (batch) | run2 | delta |
|---|---|---|---|---|
| C004 | n_statements | 34 | 31 | CHANGED |
| C004 | n_stubs | 2 | 0 | CHANGED |
| C004 | unsupported_rate | 0.031 | 0.032 | 0.001 |
| C004 | insufficient_rate | 0.000 | 0.097 | 0.097 |
| C004 | omission_rate | 0.118 | 0.059 | -0.059 |
| C004 | em_precision_fact | 0.515 | 0.577 | 0.062 |
| C004 | em_precision_all | 0.500 | 0.556 | 0.056 |
| C004 | em_recall | 0.882 | 0.824 | -0.059 |
| C004 | invalid_span_rate | 0.000 | 0.000 | 0.000 |
| C004 | n_flags | 0 | 1 | CHANGED |
| C004 | contradiction_catch | n/a | n/a |  |
| C001 | n_statements | 32 | 39 | CHANGED |
| C001 | n_stubs | 2 | 1 | CHANGED |
| C001 | unsupported_rate | 0.033 | 0.026 | -0.007 |
| C001 | insufficient_rate | 0.000 | 0.000 | 0.000 |
| C001 | omission_rate | 0.118 | 0.118 | 0.000 |
| C001 | em_precision_fact | 0.581 | 0.545 | -0.035 |
| C001 | em_precision_all | 0.562 | 0.529 | -0.033 |
| C001 | em_recall | 0.875 | 0.938 | 0.062 |
| C001 | invalid_span_rate | 0.000 | 0.000 | 0.000 |
| C001 | n_flags | 1 | 1 |  |
| C001 | contradiction_catch | 1/1 | 1/1 |  |


**Cross-check vs mother-verified batch counts:** statuses 1036 supported / 14 insufficient / 136 unsupported; invalid citations 1/1689. Expected: 1,036 / 14 / 136; 1/1,689.


*Generated deterministically; eval-harness v1.2.1 (2026-08-18); task2-runner v1.1.0 (2026-08-18, ruling 21).*

## 6. T2b micro-analysis — omission disclosure, decomposition, paired sign test

Computed by t2b v1.1.0 (2026-08-19, in-situ paths) on T2 scores (eval-harness v1.2.1 (2026-08-18)); labels read-only; no API calls.

### 6.1 Omission-disclosure rate (tool)

A tool-omitted key counts as DISCLOSED if it is named in that case's row-14 'Missing information' section or an [INSUFFICIENT EVIDENCE: …] tag (deterministic term match per key; term table in t2b.py). Baseline = 0 by construction — it has no disclosure surface.

- Pooled: **9/91 omitted key-instances disclosed (0.099)** across the 40 tool drafts.
- Cases with ≥1 tool omission: 40; fully disclosed: 0; zero disclosed: 33; partial: 7.

### 6.2 Omission decomposition by key (cases omitting the key)

| key | tool | baseline | both (same case) | tool disclosed |
|---|---|---|---|---|
| capacity_for_loss | 3 | 3 | 3 | 3 |
| client_identity | 40 | 40 | 40 | 0 |
| contribution_type | 6 | 4 | 3 | 0 |
| emergency_fund | 0 | 4 | 0 | 0 |
| investment_horizon | 8 | 8 | 5 | 2 |
| isa_allowance_used | 25 | 20 | 17 | 2 |
| liabilities | 4 | 0 | 0 | 0 |
| primary_objective | 1 | 2 | 1 | 0 |
| product_tax_treatment | 0 | 1 | 0 | 0 |
| risk_tolerance_atr | 4 | 3 | 3 | 2 |

Overlap: 72 of 91 tool-omitted key-instances are also omitted by the baseline in the same case (shared, largely structural/'missing'-status omissions rather than tool-specific losses).

### 6.3 Paired direction + sign test (per-case omission rate)

- tool < baseline: **7** · tool > baseline: **14** · ties: **19** (n=40 pairs)
- Exact two-sided sign test on the 21 non-tied pairs: p = 0.189 (binomial, p₀=0.5, ties dropped). Descriptive only — n small, single frozen run.

*t2b v1.1.0 (2026-08-19, in-situ paths); deterministic.*
