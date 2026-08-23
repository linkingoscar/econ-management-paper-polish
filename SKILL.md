---
name: econ-management-paper-polish
description: >
  Writing, revision, review, evidence, journal adaptation, and method-safety
  support for economics, management, finance, accounting, marketing, information
  systems, public administration, and related business-school papers. Routes by
  discipline, subfield, language, method, outlet, section, and task mode while
  preserving claims, numbers, variables, equations, and citations. Use for
  经管/经济学/管理学论文润色、改写、审稿回复、论点诊断、文献与方法背书、
  期刊适配、返修跟踪、LaTeX、证据核验、paper spine、RAG 和研究工作区。
---

# Econ and Management Paper Polish

Use this skill for econ/management paper writing, revision, and polishing.
First identify the paper's disciplinary paradigm and target writing context;
then keep the user's claims, numbers, variables, model notation, citations,
and intended contribution intact unless the user explicitly asks for substantive rewriting.

## Compatibility

This skill is designed to work with any coding agent that supports skill/system-prompt
loading, including but not limited to:

- **OpenCode** — place under `.opencode/skills/` or reference via `skill` tool
- **Claude Code** — place under `.claude/skills/` or reference via `skill` tool
- **Codex (OpenAI)** — place under `.codex/skills/`
- **Cursor** — place under `.cursor/rules/` or reference as project rules
- **Windsurf** — place under `.windsurf/rules/`
- **Cline** — place under `.clinerules/`
- **GitHub Copilot** — reference as custom instructions
- **Aider** — place in repo root or reference via `/add`

See `README.md` for agent-specific installation instructions.

## v3.0 Runtime Contract (reliability core)

The current implementation is **v3.1.0-alpha.5** on top of the v3.0 reliability
core. The 41 v2 reference modules remain available for backward-compatible loading;
the v3 core adds explicit
contracts around routing, evidence, deterministic audits, and capability limits.
For any non-trivial task:

1. Create a routing card and state why non-obvious discipline, method, language,
   outlet, and task choices were made. Let the user override the card and record
   the override rather than silently re-routing later.
2. Declare the actual capability mode: **Verified** (a script/source check ran),
   **Documented** (the workflow is described but not executed), or
   **Conceptual** (required infrastructure, data, or connector is unavailable).
   A text audit is never a claim of data or code replication.
3. Read `references/v3/README.md` and load only the relevant v3 responsibility packs
   (`01`–`14`) before acting. The four root contracts
   (`references/v3-runtime-contract.md`, `references/v3-evidence-ledger.md`,
   `references/v3-method-safety.md`, `references/v3-audit-contract.md`) remain the
   cross-cutting red lines.
4. Run deterministic checks before asserting that numbers, variables, citations,
   cross-references, or LaTeX are consistent. The model explains findings and
   proposes repairs; it does not replace the check.

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

The v3 method-safety red lines are mandatory: an event study is not by itself a
proof of parallel trends; staggered adoption and heterogeneous effects need an
estimator-specific design; matching, controls, Heckman, or mediation are not
automatic cures for endogeneity; and survey, experimental, qualitative, and
review designs use their own quality gates. Follow the chain
`data structure → source of variation → estimand → assumptions → diagnostics →
estimator → unresolved threats → reporting` and bind method claims to traceable
sources. Use `assets/evidence-pack.schema.json`, `assets/journal-card.schema.json`,
and `assets/paper-state.schema.json` when state must persist across turns.

## v3.1 Writing Foundation (P0)

The v3.1 upgrade remains writing-first. In alpha.5 the orchestration surface is a
**pure AI-Agent control plane**: independent writer candidates, anonymous isolated
judge profiles, deterministic adjudication, and adversarial regression generation can
run without a human reviewer for low- and medium-risk work. Deterministic safety gates
remain outside model preference so Agents cannot vote away changed numbers, citations,
meaning markers, method regressions, or broken LaTeX. High-risk scholarly meaning has a
terminal `blocked` result; Agent consensus is evaluation evidence, never authorization.

For a substantive writing task, create or update these artifacts as applicable:

1. paper-spine.json: research question, contribution chain, section, evidence,
   method dependency, and risk for each author-supplied claim.
2. corpus-manifest.json and style-card.json: file identity, role, hash,
   extraction level, structural observations, confidence, and structural-only
   copy boundary.
3. style-profile.json: observed rhetorical/paragraph/citation patterns, conflicts,
   P1 preservation priority, and recheck date. It starts as `draft`; use it only
   after either explicit human confirmation or a hash-bound two-pass AI gate.
4. review-ledger.json: reviewer issue, severity, decision, protected fields,
   status history, and unresolved limitation.
5. A bounded diff plus deterministic audit before proposing a manuscript change.
6. A meaning gate, method-language gate, LaTeX compile guard, and review-issue
   recall report for any revision cycle that changes prose or structure.

Use scripts/prepare_corpus.py, scripts/extract_style_card.py,
scripts/build_style_profile.py, scripts/build_paper_spine.py,
scripts/build_issue_ledger.py, scripts/route_review_issues.py,
scripts/check_local_bindings.py, scripts/propose_bounded_patch.py,
scripts/verify_bounded_patch.py,
scripts/meaning_audit.py, scripts/check_method_language.py,
scripts/compile_guard.py, scripts/check_issue_recall.py,
scripts/validate_style_profile_gate.py, scripts/check_claim_evidence.py, and
scripts/validate_writing_contract.py for deterministic scaffolding and checks.
Use `build_ai_review_packet.py → run_ai_reviews.py → adjudicate_ai_reviews.py`
for replaceable confirmations. Low risk needs one isolated review, medium risk
needs two unanimous reviews, and high-risk scholarly meaning remains author-required.
For comparative Agent evaluation, use
`run_agentic_candidates.py → build_agentic_review_packet.py → run_agentic_judges.py →
adjudicate_agentic_benchmark.py`. It requires at least three declared, isolated judge
profiles, hides candidate identities and hard-audit results until adjudication, binds
all content and responses by hash, and labels same-model panels low-confidence. Use
`generate_adversarial_mutations.py` to run deterministic detector regressions; generated
cases are admitted only when an independent oracle rejects the mutation.
These scripts do not decide whether a claim is true and do not apply prose patches
automatically. Freshness gates block stale direct evidence and journal profiles;
`run_dogfood_suite.py` exercises only repository-owned synthetic fixtures in temporary
workspaces and is not real-paper quality evidence. Read references/v3-writing-contract.md,
references/v3-corpus-and-style.md, references/v3-argument-evidence.md,
references/v3-review-ledger.md, and
references/v3-capability-and-provenance.md when the corresponding mode is used.
Read `references/v3-agentic-benchmark.md` before running comparative Agent evaluation.

Dynamic journal adaptation has two gates: first build and inspect a structural
style profile from supplied/verified materials, then pass explicit human review
or the hash-bound two-pass AI gate; only then revise a specified section. The profile never
authorizes copying source sentences or a target author's distinctive voice.
P1 facts, citations, equations, variables, numbers, results, contribution claims,
and limitations override every style preference. Methodological, theoretical,
causal, result, or contribution changes remain author-required by default.

The v3.1 corpus gate now checks license status, full-text availability, sample
roles, freshness, and exact n-gram overlap. Profile rules keep role weights,
section-specific locators, and a `structural-only` copy boundary. A confirmed
profile can produce a diagnostic revision plan, but the plan never edits prose.

For methods, use the risk-card catalog in `assets/method-safety-cards.json` and
`build_method_safety_report.py`: every flagged phrase should be explained through
data structure, variation, estimand, assumptions, diagnostics, remaining threats,
and a conservative rewrite. A method name alone is never an identification claim.

For a real manuscript, initialize a workspace first. The serial workflow persists
`intake.json`, `route-card.json`, `paper-spine.json` (unconfirmed candidate map),
`protected-snapshot.json`, `capability-report.json`, `checkpoint.json`, and a
JSONL revision journal. It does not overwrite the manuscript. Apply/rollback and
issue-transition commands require separate output paths and auditable confirmation.

For revision safety, the default order is: protected token audit → lexical meaning
gate → method-language screen → LaTeX structural/compile guard → issue-ID recall →
author confirmation for any meaning, method, theory, result, or contribution change.
An unavailable TeX compiler is reported as `Documented`; it is never silently
reported as a successful compilation.

## Core Rules

1. Do not invent citations, data, regression results, mechanisms, institutions,
   journal requirements, or author claims.
2. Preserve coefficient signs, p-values, sample sizes, variable names, equation
   notation, table numbers, and citation keys exactly unless correcting an explicit
   inconsistency.
3. Separate polishing from substantive risk. If a claim is unsupported, overcausal,
   vague, or inconsistent with evidence, flag it instead of silently smoothing it.
4. Match the target language. For Chinese drafts, use precise mainland academic
   Chinese. For English drafts, use journal-style academic English without inflated
   adjectives.
5. Do not impose one paradigm on all papers. Economics, management, finance,
   accounting, marketing, information systems, and other fields differ in contribution
   logic, theory density, methods language, and implication style.
6. For empirical papers, prioritize claim-evidence alignment: every theoretical claim
   should connect to an empirical test, and every empirical result paragraph should
   state economic meaning, not only statistical significance.
7. Any new, replaced, or corrected reference must be based on a traceable source found
   in the current session, an accessible Zotero/library record, a user-provided source,
   or a verified bibliographic database/API result. Never add references from memory.
8. Default citation output is APA 7 for English references and APA-compatible
   translated bibliographic details for Chinese references unless the user requests
   GB/T 7714, Chicago, journal style, or another format.
9. If required context is missing, write the best revision using placeholders such as
   `[需补充数据来源]`, `[check table number]`, or `[citation needed]`.
10. De-AI policy: "De-AI" means removing template-like academic filler and
    restoring discipline-specific substance (mechanisms, institutional context,
    sample details, table references). It does not mean disguising AI-written
    text to evade AI-detection tools. Do not provide rewrites whose purpose is
    to pass an AI detector, and never optimize for detector scores. If a user
    explicitly asks to make text undetectable as AI-generated, decline and
    explain why. Authors remain responsible for verifying output and for
    disclosing AI assistance when their institution or target journal requires it.

## First Step

Before editing, read `references/intake-and-modes.md` for any non-trivial request.
Build a short intake/routing card. Infer from the supplied text when possible;
ask concise questions only when missing context would change the style or risk
fabricating requirements.

Routing card:

- **Discipline family**: economics, finance, accounting, management, marketing,
  strategy, OB/HR, information systems, public administration, tourism,
  innovation/entrepreneurship, or mixed.
- **Specific direction**: e.g., labor economics, environmental economics,
  corporate finance, corporate governance, archival accounting, consumer behavior,
  strategic management, platform economy, digital transformation.
- **Method/paradigm**: theory/model, archival empirical, survey, experiment,
  qualitative case, mixed methods, review, meta-analysis, or policy evaluation.
- **Language context**: Chinese CSSCI-style, English international journal-style,
  translation polish, or bilingual manuscript.
- **Target outlet**: specific journal if known; otherwise Chinese CSSCI-compatible
  or English field-journal-compatible.
- **Section type**: introduction, literature review, theory/hypotheses, empirical
  strategy, results, mechanism, robustness, heterogeneity, discussion, abstract,
  reviewer response, or full manuscript.
- **Evidence need**: no new references, policy/background support, theory support,
  method support, topic/frontier support, replacement references, or full reference audit.

Style route:

- Chinese economics -> `cn-economics-style.md` + `subfields-economics.md`
  + `journal-families-econ.md` when relevant.
- English economics -> `en-economics-style.md` + `subfields-economics.md`
  + `journal-families-econ.md` when relevant.
- Chinese management -> `cn-management-style.md` + `subfields-management.md`
  + `journal-families-management.md` when relevant.
- English management -> `en-management-style.md` + `subfields-management.md`
  + `journal-families-management.md` when relevant.
- Finance, accounting, marketing, IS, public management, tourism, operations,
  and mixed papers -> start from the closest economics/management route, then
  refine with `field-style-packs.md` and subfield files.

If the user provides a specific target journal, use the journal's current author
instructions and recent accepted papers when available before enforcing journal-specific
style. If browsing is unavailable, say the journal-specific adaptation is based on
general field conventions, not verified current requirements.

Then identify the task type:

- **Line polish**: improve clarity, concision, academic tone, and flow while
  keeping meaning fixed.
- **Structural rewrite**: reorganize the paragraph or section to improve argument order.
- **Section drafting**: produce or expand a section from notes, tables, or bullet points.
- **Reviewer-style audit**: find weaknesses, unsupported claims, causal overreach,
  citation gaps, and readability problems.
- **Bilingual translation/polish**: translate and then adapt to academic convention
  rather than literal word order.
- **Evidence-backed expansion**: add policy background, theoretical support, method
  support, or alternative references using only verified sources.
- **Topic/revision advisory**: diagnose topic contribution, suggest new directions,
  variable designs, manuscript repositioning, or revision roadmaps with literature support.

Ask for missing context only when it is necessary to avoid changing meaning or
fabricating evidence. Otherwise proceed and mark assumptions.

## Literature and Evidence Rule

When the user asks to add, replace, verify, or strengthen references, or when the
draft clearly needs new support:

1. Identify the claim type: policy/background, stylized fact, theory/mechanism,
   method/identification, measurement/proxy, empirical benchmark, or implication.
2. Search or inspect available sources before writing the citation. Prefer the user's
   Zotero/library sources, school-authorized databases, CNKI/publisher pages, DOI
   landing pages, Crossref/OpenAlex metadata, journal pages, working-paper
   repositories, and official policy documents.
3. Build an evidence pack with source title, authors, year, venue, DOI/URL/CNKI/
   source link, claim supported, and confidence.
4. Add only sources that actually support the sentence. If a source is adjacent but
   not supportive, label it as an alternative candidate rather than citing it.
5. Output the added or modified references in complete APA format by default.
   Include DOI URLs when available.
6. If no reliable source is found, do not fill the gap; write `[citation needed]`
   or ask the user for database access/Zotero material.

Do not use secondary summaries when the primary paper, official policy, or journal
page is available.

## Output Pattern

For a polishing request, default to:

1. **Revised text** first.
2. **Key changes** in 3-6 bullets, only if useful.
3. **Risks to check** when there are unsupported claims, missing citations,
   inconsistent numbers, or causal language issues.

For a review request, lead with issues ordered by severity. Include exact quoted
fragments only when short and necessary.

## v3 Default Reference Packs

Load from `references/v3/` rather than loading every legacy file:

- `01-intake-routing.md`: routing card, discipline/subfield, language, and task mode.
- `02-writing-style.md`: Chinese/English economics/management and adjacent-field style.
- `03-journal-adaptation.md`: source-backed outlet adaptation and journal cards.
- `04-evidence-sources.md`: source tiers, claim IDs, evidence grading, and theory support.
- `05-methods-identification.md`: data structure, estimand, identification, and safety gates.
- `06-argument-structure.md`: paper spine, contribution chain, and section patterns.
- `07-results-quality.md`: claim-evidence, numbers, causal language, and audit gates.
- `08-revision-risk.md`: reviewer response, risk register, and revision lifecycle.
- `09-research-pipeline.md`: eight stages, gates, and bounded delegation.
- `10-latex-typesetting.md`: LaTeX structure, templates, and structural audit boundaries.
- `11-rag-retrieval.md`: retrieval, chunk provenance, verification, and degradation modes.
- `12-literature-workspace.md`: survey, paper pool, and close-reading artifacts.
- `13-reproducibility-data.md`: data/method/result transparency and replication ceilings.
- `14-integrations-and-capability.md`: source, RAG, and agent adapter contracts.

The old 41 modules are mapped in `references/v3/legacy-index.md` and remain
loadable for compatibility; do not add new v3 rules only to a legacy file.

## v3.1 Contract References

The v3.1 writing contracts live at the reference root because they extend the
cross-cutting runtime without creating a fifteenth default pack:

- v3-writing-contract.md: writing modes, output contract, and protected fields.
- v3-corpus-and-style.md: corpus manifest, style cards, profile, and copy boundary.
- v3-argument-evidence.md: paper spine and claim-evidence map.
- v3-review-ledger.md: reviewer issue lifecycle and bounded revision.
- v3-capability-and-provenance.md: capability modes and component provenance.

## Compatibility Layer

The original 41 files remain available at `references/*.md` for existing installs.
Their migration map is `references/v3/legacy-index.md`; new guidance belongs in the
14 v3 packs and should not fork rules in a legacy file. The root contracts, schemas,
adapters, scripts, and tests are the executable reliability surface. Run
`py scripts/validate_v3.py .`, `py evals/run_smoke_tests.py`, and
`py evals/run_extended_tests.py` before distributing a modified skill.
