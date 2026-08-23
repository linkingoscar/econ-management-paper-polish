# v3 Evaluation Set

The smoke suite is intentionally dependency-free and runs in CI:

```bash
python evals/run_smoke_tests.py
python evals/run_extended_tests.py
python evals/run_v31_writing_tests.py
python evals/run_agentic_tests.py
python scripts/run_writing_benchmark.py --output writing-benchmark.json --json
```

Current fixtures cover Chinese/English-compatible manuscript text, a citation
key and BibTeX record, numeric-preservation pass/fail cases, a LaTeX package and
cross-reference failure, an evidence pack, and a journal card. The release gates
are designed for later expansion:

| Gate | Alpha target |
|---|---:|
| Protected numeric/variable preservation on light polish | 100% |
| Virtual or fabricated citations in fixtures | 0 |
| Added claim IDs with source provenance | 100% |
| Known table/text/LaTeX consistency errors detected | 95%+ |
| Repository contract and internal links | 100% pass |

Add a normal (non-error) case whenever adding a new detector so that stricter
checks do not turn into false-positive generators.

The v3.1 writing suite covers corpus manifest rejection logging, authorization and
overlap gates, deterministic style-card/profile extraction, section revision planning,
paper-spine IDs and reverse-outline candidates, reviewer issue routing and state
transitions, protected bounded patches with apply/rollback, lexical meaning changes,
local number/citation binding swaps,
evidence-ledger many-to-many bindings, method risk-card explanations in Chinese and
English, LaTeX structural/compile capability reporting, issue-ID recall, package and
repro-lock validation, freshness gates, response-letter validation, and the dynamic
style-profile human gate. It currently runs 34 checks. The local
`evals/dogfood/manifest.json` drives ten temporary-workspace workflow cases (eight
expected complete and two expected author-required blocks). `evals/gold/writing-cases.json` and `evals/mutations/writing-mutations.json`
provide explicit expected statuses so the benchmark reports true/false positives and
negatives instead of treating process exit as a quality score. Invalid JSON, malformed
detector output, and detector crashes are counted as invalid cases and fail the benchmark.
The mutation set includes safe local bindings plus number and citation swaps. It uses synthetic
fixtures and never uploads a paper; a passing fixture is not evidence of real-paper
performance. `scripts/run_contract_suite.py` is the single serial entry point for the
repository/package/repro/smoke/benchmark/platform/dogfood gates.

`evals/run_agentic_tests.py` adds 12 offline pure-Agent benchmark checks. They verify
public/private blind separation, content-hash binding, hard-gate precedence over unanimous
Agent votes, single-model and cross-model labels, fail-closed invalid reviews, the high-risk
authorization boundary, no-call dry runs, duplicate LaTeX labels, and eight deterministic
adversarial operators with independent oracle evidence. These are synthetic protocol tests;
they do not claim live-provider, cross-model quality, or real-manuscript effectiveness.

The extended suite is offline by design. Live Crossref/OpenAlex calls are an
optional integration check and must never be required for CI; network failures are
reported as capability limitations rather than converted into fabricated evidence.
