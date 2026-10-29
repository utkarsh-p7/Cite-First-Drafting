# Corpus statistics — synthetic corpus v1.0.1 (Ch4/Ch5 reference) · ALL DATA FICTITIOUS

## Provenance & reproducibility
| item | value |
|---|---|
| Generator | `generate.py` v1.0.1 (project store) |
| Master seed | 42 |
| Per-case seed derivation | `random.Random(f"{master_seed}:{case_id}")` — no separate seed list; all case RNG streams derive deterministically from master seed + case ID |
| Cases | 40 (C001–C040) |
| Reproduction | `python generate.py --n 40 --seed 42 --out corpus` then `python label.py --corpus corpus --out corpus/labels`; byte-identical re-runs verified (Linux container + Windows local) |
| Files | 40 fact-finds · 40 transcripts · 40 label files · manifest.json |

## Condition counts
| condition | n | case IDs |
|---|---|---|
| clean | 28 | remaining |
| hard:absent_capacity | 3 | C002, C008, C040 |
| hard:ambiguous_horizon | 3 | C003, C029, C034 |
| hard:contradiction | 3 | C001, C033, C039 |
| hard:missing_risk | 3 | C009, C030, C035 |

Hard fraction: 12/40 = 30%.

## Fact-find distributions (n=40)
| variable | min / median / max |
|---|---|
| age (years) | 28 / 48 / 68 |
| gross annual income (£) | 7,600 / 39,850 / 211,000 |
| investable amount (£) | 5,500 / 22,000 / 39,500 |
| emergency fund (months) | 2 / 13 / 62 |

| categorical | distribution |
|---|---|
| tax band | {'additional': 6, 'basic': 24, 'higher': 9, 'none': 1} |
| recommended wrapper | {'both': 8, 'gia': 5, 'ss_isa': 27} |
| capacity for loss | {'high': 15, 'low': 2, 'medium': 20, 'null(seeded)': 3} |
| ATR score | {'null(seeded)': 3, 1: 6, 2: 3, 3: 5, 4: 10, 5: 13} |
| horizon (years) | {'null(seeded)': 3, 10: 7, 15: 3, 20: 8, 3: 6, 5: 9, 7: 4} |

## Ground-truth label statistics
| metric | value |
|---|---|
| total fact labels | 699 |
| supported | 687 |
| missing | 9 (9 seeded: 3 missing_risk + 3 absent_capacity + 3 ambiguous_horizon) |
| contradictory | 3 (3 seeded) |
| facts per case | 16–20 (17-key inventory; wrapper-dependent product facts) |

Notes: distributions are generator artefacts (see `generate.py` for sampling rules), not population claims. 
Capacity-for-loss internally coherent with emergency-fund/surplus heuristic; ISA-allowance-used sampled independently. 
'null(seeded)' rows are the deliberately removed values in hard cases.
