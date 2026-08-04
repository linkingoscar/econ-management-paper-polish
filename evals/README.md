# v3 Evaluation Set

The smoke suite is intentionally dependency-free and runs in CI:

```bash
python evals/run_smoke_tests.py
python evals/run_extended_tests.py
python evals/run_v31_writing_tests.py
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
evidence-ledger many-to-many bindings, method risk-card explanations in Chinese and
English, LaTeX structural/compile capability reporting, issue-ID recall, package and
repro-lock validation, and the dynamic style-profile human gate. It currently runs
24 checks. `evals/gold/writing-cases.json` and `evals/mutations/writing-mutations.json`
provide explicit expected statuses so the benchmark reports true/false positives and
negatives instead of treating process exit as a quality score. It uses synthetic
fixtures and never uploads a paper; a passing fixture is not evidence of real-paper
performance.

The extended suite is offline by design. Live Crossref/OpenAlex calls are an
optional integration check and must never be required for CI; network failures are
reported as capability limitations rather than converted into fabricated evidence.
