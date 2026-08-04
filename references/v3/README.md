# v3 Reference Packs

These 14 packs are the default knowledge layer for v3.0. They replace the old
41-file loading pattern with one responsibility per pack. Each pack contains the
operational rules needed for its route and names the legacy modules that supplied
the migration. The legacy files remain available, but should be opened only when
the pack explicitly points to a detail that has not yet been migrated.

## Load matrix

| Pack | Use when | Legacy sources consolidated |
|---|---|---|
| `01-intake-routing.md` | route discipline, subfield, language, method, task | intake, discipline, economics/management subfields |
| `02-writing-style.md` | polish, rewrite, translation, adjacent business fields | CN/EN style packs, field styles, style-and-polish |
| `03-journal-adaptation.md` | outlet fit, author instructions, journal card | journal families, style adaptation, style card |
| `04-evidence-sources.md` | source search, citation, theory, replacement references | source policy, evidence workflow/grading, theory backing |
| `05-methods-identification.md` | method diagnosis and causal claims | method router, decision tree, method reproducibility |
| `06-argument-structure.md` | paper spine, sections, contribution chain | paper spine, section patterns |
| `07-results-quality.md` | quality gates, result interpretation, audit triage | quality gates |
| `08-revision-risk.md` | reviewer response, risk register, revision tracking | revision matrix, risk register, topic/revision advisor |
| `09-research-pipeline.md` | end-to-end stages and handoffs | research pipeline, stage gates, delegation |
| `10-latex-typesetting.md` | LaTeX writing, templates, structural audit | LaTeX support/templates/audit |
| `11-rag-retrieval.md` | local literature retrieval and evidence verification | RAG workflow/retrieval/verification |
| `12-literature-workspace.md` | survey, paper pool, close reading | survey workspace, paper pool, close reading |
| `13-reproducibility-data.md` | data/method/result transparency | reproducibility audit, data reproducibility |
| `14-integrations-and-capability.md` | source/RAG/agent adapters and degradation | v3 runtime and adapter contracts |

The normal load order is `01` → one or more task packs → `04`/`05` when evidence or
methods are involved → `07`/`13` before a final audit. Do not load every pack for a
line-polish request.

## v3.1 writing contracts

The writing-first alpha extends these packs with root-level contracts:

- `../v3-writing-contract.md`: writing modes, protected fields, and output contract.
- `../v3-corpus-and-style.md`: corpus manifest, style cards, profiles, and copy boundary.
- `../v3-argument-evidence.md`: paper spine and claim-evidence checks.
- `../v3-review-ledger.md`: reviewer issue lifecycle and bounded revision.
- `../v3-capability-and-provenance.md`: capability and provenance boundaries.

The writing safety gates are exposed as deterministic scripts:

- `../../scripts/meaning_audit.py` and `../../scripts/check_method_language.py` for
  lexical meaning and method-language overclaims;
- `../../scripts/compile_guard.py` for structural LaTeX checks plus an optional
  isolated compiler run;
- `../../scripts/check_issue_recall.py` for issue-ID lifecycle recall; and
- `../../scripts/validate_style_profile_gate.py` for author or hash-bound AI
  confirmation of a dynamic style profile; and
- `../../scripts/build_ai_review_packet.py` plus `../../scripts/adjudicate_ai_reviews.py`
  for fixed-risk, isolated AI review gates.
