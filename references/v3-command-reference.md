# v3 Command Reference

Read only when selecting a script for the current task. This is a command catalog,
not a sequence to run for every request. See [the writing contract](v3-writing-contract.md)
for light-polish versus workspace scope.

For a short same-language polish, use `verify_bounded_patch.py original.md revised.md --json`.
For a faithful translation with established CNY currency context, the optional
`check_numeric_consistency.py original.md translated.md --economic-units --json`
checks covered quantity equivalence and shows the strict numeric result too.
Inspect local claim attachment, citations, and meaning separately; this option
does not relax the bounded verifier or apply protections.

`check_method_language.py` and `build_method_safety_report.py` distinguish
failing known overclaim patterns from nonblocking contextual advisories.
`no-known-overclaim` is a limited screen result, not a declaration of valid methods.

Useful commands (run from the skill root) are:

```text
py scripts/check_numeric_consistency.py original.md revised.md --json
py scripts/compare_manuscript_versions.py original.md revised.md --variable Treatment --json
py scripts/check_citations.py manuscript.tex --bib references.bib --strict --json
py scripts/audit_latex.py manuscript.tex --strict --json
py scripts/build_evidence_pack.py evidence-input.json --output evidence-pack.json --json
py scripts/validate_journal_card.py journal-card.json --max-age-days 365 --json
py scripts/search_literature.py "staggered difference in differences" --provider both --json
py scripts/rag_search.py --index .rag/index.json --ingest references --query "parallel trends" --json
py scripts/run_agent_pipeline.py tasks.json --dry-run --json
py scripts/run_agentic_candidates.py evals/agentic/manifest.json results-low-risk --output-dir candidate-runs --dry-run --json
py scripts/build_agentic_review_packet.py evals/agentic/manifest.json results-low-risk --variant candidate-a=output-a.md --variant candidate-b=output-b.md --output packet.json --mapping-output private-mapping.json --json
py scripts/run_agentic_judges.py packet.json --output-dir agentic-runs --dry-run --json
py scripts/adjudicate_agentic_benchmark.py packet.json private-mapping.json agentic-runs/ABP-*/journal-editor.json agentic-runs/ABP-*/methods-reviewer.json agentic-runs/ABP-*/copy-editor.json --output decision.json --json
py scripts/generate_adversarial_mutations.py evals/adversarial/manifest.json --output-dir generated-mutations --manifest-output mutation-report.json --json
py scripts/prepare_corpus.py corpus --role target-journal --output corpus-manifest.json --json
py scripts/extract_style_card.py corpus/paper.md --source-id SRC-0001 --output style-cards/STY-0001.json --json
py scripts/build_style_profile.py style-cards --output style-profile.json --json
py scripts/build_ai_review_packet.py style-profile.json --kind style-profile --output style-review-packet.json --json
py scripts/run_ai_reviews.py style-review-packet.json --output-dir ai-reviews --json
py scripts/adjudicate_ai_reviews.py style-review-packet.json ai-reviews/ai-review-1.json ai-reviews/ai-review-2.json --output style-decision.json --json
py scripts/build_writing_review_bundle.py original.md revised.md --style-profile style-profile.json --output writing-review-bundle.json --json
py scripts/build_paper_spine.py --paper-id paper-001 --output paper-spine.json --json
py scripts/build_paper_spine.py --manuscript manuscript.md --paper-id paper-001 --output paper-spine.json --json
py scripts/approve_paper_spine.py paper-spine.json spine-decision.json --output paper-spine-reviewed.json --json
py scripts/check_claim_evidence.py paper-spine.json --evidence-pack evidence-pack.json --json
py scripts/build_evidence_ledger.py evidence-ledger-input.json --output evidence-ledger.json --json
py scripts/check_evidence_impact.py evidence-ledger.json SRC-0001 --json
py scripts/audit_evidence_freshness.py evidence-ledger.json --max-age-days 365 --json
py scripts/audit_journal_freshness.py journal-card.json --max-age-days 365 --json
py scripts/build_issue_ledger.py reviewer-issues.json --output review-ledger.json --json
py scripts/route_review_issues.py review-ledger.json --output review-ledger-routed.json --json
py scripts/check_local_bindings.py original.md revised.md --json
py scripts/propose_bounded_patch.py original.md revised.md --output patch-report.json --json
py scripts/verify_bounded_patch.py original.md revised.md --variable Treatment --json
py scripts/apply_bounded_patch.py original.md revised.md --output manuscript.applied.md --variable Treatment --json
py scripts/rollback_bounded_patch.py original.md --output manuscript.rollback.md --json
py scripts/transition_issue.py review-ledger.json ISS-001 proposed --output review-ledger-proposed.json --actor author --rationale "..." --json
py scripts/build_response_letter.py review-ledger.json --output response-letter.md --json
py scripts/build_revision_matrix.py review-ledger.json --output revision-matrix.csv --json
py scripts/validate_response_letter.py review-ledger-closed.json response-letter-submission.md --json
py scripts/meaning_audit.py original.md revised.md --json
py scripts/check_method_language.py manuscript.md --json
py scripts/build_method_safety_report.py manuscript.md --json
py scripts/compile_guard.py manuscript.tex --strict --json
py scripts/check_issue_recall.py review-ledger-before.json review-ledger-after.json --json
py scripts/validate_style_profile_gate.py style-profile.json --ai-decision style-decision.json --json
py scripts/plan_style_revision.py manuscript.md style-profile.json --ai-decision style-decision.json --section method --output style-revision-plan.json --json
py scripts/init_writing_workspace.py paper-workspace --paper-id paper-001 --json
py scripts/run_writing_workflow.py paper-workspace --variable Treatment --json
py scripts/validate_revision_journal.py paper-workspace/revision-journal.jsonl --json
py scripts/run_writing_benchmark.py --output writing-benchmark.json --json
py scripts/run_dogfood_suite.py --json
py scripts/run_platform_smoke.py --json
py scripts/run_contract_suite.py --json
py scripts/scan_skill_provenance.py provenance-manifest.json --json
py scripts/validate_skill_package.py . --json
py scripts/validate_repro_lock.py . --json
py scripts/validate_v3.py .
```
