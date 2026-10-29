# Task 3 — RQ2: machine-timed time-to-first-draft (frozen batch, n=40)

Source: batch `outputs/{baseline,tool}/run_log.jsonl` only (ruling 13). Per-draft wall-clock, model openai/gpt-oss-120b via Groq free tier, temp 0, seed 42; all stop_reason 'stop'. t3 v1.0.0 (2026-08-19).

## Wall-clock per draft (seconds)

| pipeline | n | mean | median | min | max | stdev |
|---|---|---|---|---|---|---|
| baseline | 40 | 2.45 | 2.37 | 1.89 | 3.78 | 0.41 |
| tool | 40 | 3.46 | 3.37 | 2.62 | 5.28 | 0.49 |

Per-case pairs in `timing_per_case.csv`. Distribution note: Groq free-tier queueing makes wall-clock volatile between calls (Build Task 2 observed 2.5s vs 39.2s for identical params), so the distribution — not any single draft — is the reportable quantity; timings include network/queue time, not pure inference.

## Published industry context — explicitly indicative, NO like-for-like claim

These figures describe the full human drafting task (fact-find review, analysis, writing, compliance checking) by qualified staff; the machine timing above covers only automated first-draft generation from pre-assembled context. They are vendor/trade sources of limited evidential weight (per Ch3 §3.6) and are click-verifiable:

| figure | source |
|---|---|
| 4–6 hours of active paraplanner time to write one suitability report from scratch | AdvisoryAI (vendor), https://advisoryai.com/blog/ai-vs-traditional-documentation-financial-advisers |
| 10–15 hours per week spent on suitability reports per adviser (attributed to Money Marketing) | Aveni (vendor blog), https://aveni.ai/blog/how-to-fix-the-suitability-report-bottleneck-in-financial-advice/ |
| Vendor case study: VCT suitability report time cut from ~6 hours to ~1 hour with AI tooling | AdvisoryAI 2026 buyer's guide, https://advisoryai.com/blog/ai-suitability-report-generators-uk-buyers-guide-2026 |

Contrast (indicative only): mean machine time-to-first-draft here is 3.5s (tool) / 2.4s (baseline) — minutes-vs-hours order-of-magnitude context, not a controlled comparison: human review and approval of every draft remains mandatory (ethical boundary), and no human review time was measured (PIVOT 2026-08-04: no participants).

*t3 v1.0.0 (2026-08-19); deterministic; timing data untouched.*
