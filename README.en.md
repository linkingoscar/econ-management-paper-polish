# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#compatibility)
[![Version](https://img.shields.io/badge/Version-3.1.0--alpha.4-orange.svg)](#v31-writing-reliability-foundation-alpha)
[![Academic](https://img.shields.io/badge/Academic-Writing-005A9C?logo=google&logoColor=white)](#)
[![Multi-Agent](https://img.shields.io/badge/MultiAgent-Supported-FF6F00?logo=javascript&logoColor=white)](#)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-000000?logo=opencode&logoColor=white)](#)
[![Claude Code](https://img.shields.io/badge/Claude-Code-CC0000?logo=anthropic&logoColor=white)](#)
[![Codex](https://img.shields.io/badge/Codex-OpenAI-000000?logo=openai&logoColor=white)](#)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000?logo=cursor&logoColor=white)](#)
[![RAG](https://img.shields.io/badge/RAG-Knowledge-4CAF50?logo=google&logoColor=white)](#)
[![LaTeX](https://img.shields.io/badge/LaTeX-Supported-008080?logo=latex&logoColor=white)](#)

**Full-lifecycle AI writing assistant for economics and management academic papers**

An AI Skill covering the entire paper-writing pipeline — from topic selection to journal submission.

> **Domains**: Economics, Management, Finance, Accounting, Marketing, Information Systems, Public Administration, Tourism/Service Management, Innovation & Entrepreneurship, and other business-related academic papers.

> **[中文文档](README.md)**

---

## Overview

Econ-Management Paper Polish is an AI Skill designed specifically for academic papers in economics and management. It supports multiple AI coding agents (OpenCode, Claude Code, Codex, Cursor, etc.).

### Core Objectives

| Objective | Description |
|-----------|-------------|
| **Writing Quality** | Chinese/English academic writing standardization, de-AI-ification, journal adaptation |
| **Argument Quality** | Clear claims, sufficient evidence, sound methods, accurate causal language |
| **Citation Quality** | Traceable, no fabrication, evidence grading |
| **Revision Quality** | Effective reviewer response, trackable revisions |
| **Research Efficiency** | Literature management, survey organization, pipeline collaboration |

### Design Principles

1. **No Fabrication** — Never invent citations, data, regression results, or journal requirements
2. **Traceable** — Every new citation must have a verifiable source in the current session
3. **Discipline-Aware** — Economics ≠ Management ≠ Finance — respect paradigm differences
4. **Evidence Grading** — Grade A (full-text verified) to Grade D (unverifiable), never overclaim
5. **Preserve Intent** — Unless requested, retain the user's claims, numbers, variables, and contribution positioning

### De-AI Tone Reduction & Academic Integrity

This project provides "de-AI" tone reduction with an explicit stance:

1. **Definition** — De-AI means removing template-like academic filler (vague openings, empty signifiers such as "significant importance", mechanical parallel structure) and restoring discipline-specific substance (mechanisms, institutional context, sample details, table references) — text the way a field insider would naturally write it.
2. **What we do not do** — We do not provide evasive rewriting aimed at AI-detection tools, and we do not optimize for detector scores. If a user asks to rewrite text so that it cannot be identified as AI-generated, decline and explain why.
3. **Author responsibility** — All output must be verified by the author. If the target journal, institution, or publisher requires disclosure of AI assistance, disclose it. This follows from the same integrity framework as our no-fabricated-citations and no-overclaiming rules.
4. **Stance** — Norms around AI use in academia are still evolving. This project takes the conservative position: better to decline than to help evade detection.

## Features

### v1.0 Core Capabilities (23 Modules)

| Capability | Description | Example Triggers |
|------------|-------------|------------------|
| **Paper Polish** | Light polish, peer-style rewrite, de-AI, Chinese/English style adaptation | Paper polish, de-AI, paper polish |
| **Structural Rewrite** | Intro → Lit Review → Theory → Hypotheses → Empirics → Results → Robustness → Heterogeneity → Discussion → Conclusion | Structural rewrite, reorganize paragraphs |
| **4-Quadrant Routing** | Chinese Economics / English Economics / Chinese Management / English Management | Auto-detect |
| **Subfield Routing** | Applied Micro, Labor, Environment, IO, Strategy, OB/HR, IS, Marketing, etc. | Auto-detect |
| **Journal Adaptation** | Generate journal style card based on author guidelines and recent issues | Adapt to AER, adapt to Management World |
| **Literature Augmentation** | Policy background, theory backing, method endorsement, variable measurement, alternative references | Augment literature, literature endorsement |
| **Evidence Grading** | Grade A/B/C/D to distinguish citable → not recommended | Auto-grade |
| **Method Diagnosis** | DID, Event Study, IV, RD, SCM, Matching, Mediation, Text/ML, DML, etc. | Method diagnosis, is method appropriate |
| **Topic & Revision** | Contribution diagnosis, variable suggestions, conservative revision / aggressive pivot paths | Topic adjustment, revision direction |
| **Reviewer Response** | Reviewer comment decomposition, response tone, revision actions and evidence supplement | Reviewer response, response letter |

### v2.0 New Capabilities (18 Modules)

| Capability | Description | Example Triggers | Inspired By |
|------------|-------------|------------------|-------------|
| **Paper Spine** | Core claims, contribution chain, hypothesis chain, evidence map, risk register | Paper spine, core argument | PaperSpine |
| **Revision Matrix** | Revision tracking, modification action log, status management | Revision matrix, revision tracking | PaperSpine |
| **Risk Register** | Method risk, theory risk, evidence risk, expression risk, publication risk | Risk register, reviewer concerns | PaperSpine |
| **Reproducibility Audit** | Data transparency, method transparency, result consistency check | Reproducibility, replication check | Repro Pack |
| **Research Pipeline** | 8-stage end-to-end workflow | Research pipeline, topic to submission | academic-research-skills |
| **Stage Gates** | Quality checkpoints at each stage | Stage gates | academic-research-skills |
| **Sub-agent Delegation** | Parallel / sequential / step-by-step execution modes | Full review, systematic analysis | academic-research-skills |
| **LaTeX Support** | LaTeX writing standards, journal templates, format audit | LaTeX, three-line table, BibTeX | LaTeX Writer |
| **RAG Knowledge Base** | Local PDF retrieval, semantic search, cross-paper QA, citation verification | RAG, knowledge base, cross-paper QA | PaperRAG / Cite Verity |
| **Survey Workspace** | Literature pool management, main thread梳理, close reading, gap analysis | Survey workspace, literature organization | Survey Builder |

---

## v3.0 Reliability Core (alpha)

v3.0.0-alpha.1 focuses on whether an edit can be trusted and re-checked. It keeps
the 41 legacy `references/` modules loadable while adding a small executable core:

| Capability | Deliverable |
|------------|-------------|
| Routing and capability declaration | `references/v3-runtime-contract.md`; Verified / Documented / Conceptual modes |
| Evidence ledger | `assets/evidence-pack.schema.json`, `scripts/build_evidence_pack.py` |
| Deterministic audits | Numeric, citation, LaTeX, and before/after version checks |
| Method safety layer | `references/v3-method-safety.md` with design-specific causal red lines |
| Responsibility packs | 14 aggregated packs in `references/v3/`, with a 41-file legacy migration index |
| Pluggable integrations | Crossref/OpenAlex search, persistent local RAG, serial/HTTP agent adapters |
| Persistent validation | State schemas, evaluation fixtures, and GitHub Actions CI |

From the repository root:

```bash
python scripts/validate_v3.py .
python evals/run_smoke_tests.py
python evals/run_extended_tests.py
python evals/run_v31_writing_tests.py
python scripts/run_writing_benchmark.py --output writing-benchmark.json --json
python scripts/validate_skill_package.py . --json
python scripts/validate_repro_lock.py . --json
```

These checks cover manuscript text, citations, and structure. Without original
data, code, or a licensed database, the skill reports a transparency audit rather
than claiming a replication. RAG and multi-agent execution remain documented
capabilities with optional adapters. Live retrieval and model calls still require
network access, credentials, and separate evidence verification.

---

## v3.1 Writing Reliability Foundation (alpha)

v3.1 keeps the project centered on economics/management paper writing and revision,
not on becoming a general autonomous research platform. The consolidated alpha.1–alpha.4
release connects the checks
into a recoverable writing loop: workspace/intake/route cards, candidate paper spine,
protected snapshots, checkpoints and a JSONL revision journal; many-to-many evidence
ledger and source-impact checks; corpus authorization/freshness/sample gates; role-
weighted section style profiles, overlap screening and structural revision plans;
method risk cards with conservative rewrites; bounded apply/rollback, issue transitions,
response-letter scaffolds, evidence/journal freshness gates, revision-matrix and
submission-ready response validation, a local synthetic dogfood harness, portable
platform/LaTeX capability reporting, 32 writing-contract checks, gold/mutation metrics,
package validation, a unified contract suite, an adapter repro lock, and hash-bound AI
confirmation gates for low- and medium-risk artifacts. Retrieval, RAG,
and multi-agent features remain supporting layers.

* [v3.1 landscape research report](docs/v3.1-landscape-research.md)
* [v3.1 detailed upgrade plan](docs/v3.1-upgrade-plan.md)

The implemented capabilities are still alpha: scripts perform deterministic scans,
contract validation, and candidate diffs; they do not decide theory, identification,
results, or contribution for the author. A style profile is `draft` by default and may
be used for structural diagnosis after author confirmation or two isolated AI reviews
reach a hash-bound consensus. Numbers, citations, identification, causal direction,
results, and contribution claims remain author-controlled. When no TeX compiler is installed, the report is
`Documented` rather than a claimed compile. The 32 checks, ten synthetic dogfood cases,
and gold/mutation metrics are repository-owned fixtures; they verify workflow wiring and
deterministic gates rather than author voice, causal adjudication, or journal effectiveness.
Real/anonymous-paper dogfooding and a human journal-effectiveness rubric remain beta
prerequisites.

---

## File Structure

```
econ-management-paper-polish/
├── SKILL.md                           # Core skill definition and routing
├── README.md / README.en.md           # Chinese and English documentation
├── LICENSE / CONTRIBUTING.md          # License and contribution guide
├── .github/workflows/ci.yml           # CI, contract tests, and Pages checks
├── agents/openai.yaml                 # Agent display metadata
├── adapters/                          # Search, local RAG, and agent adapters
│   ├── providers/                     # Crossref and OpenAlex
│   ├── rag/                           # Local markdown index
│   └── agents/                        # Serial and OpenAI-compatible agents
├── assets/                            # JSON schemas and report templates
├── scripts/                           # Deterministic writing and audit commands
├── evals/                             # Smoke, benchmark, writing tests, and dogfood harness
├── docs/                              # GitHub Pages and v3.1 research/upgrade documents
└── references/                        # 41 legacy modules plus v3 contracts and packs
    ├── v3-*.md                        # Runtime, audit, evidence, method, and writing contracts
    └── v3/                             # 14 progressive-loading responsibility packs
```

---

## Quick Start

### Installation

#### OpenCode

```bash
git clone https://github.com/linkingoscar/econ-management-paper-polish.git \
  ~/.opencode/skills/econ-management-paper-polish
```

#### Claude Code

```bash
git clone https://github.com/linkingoscar/econ-management-paper-polish.git \
  ~/.claude/skills/econ-management-paper-polish
```

#### Codex (OpenAI)

```bash
git clone https://github.com/linkingoscar/econ-management-paper-polish.git \
  ~/.codex/skills/econ-management-paper-polish
```

#### Cursor

```bash
git clone https://github.com/linkingoscar/econ-management-paper-polish.git \
  .cursor/rules/econ-management-paper-polish
```

### Basic Usage

```text
Use econ-management-paper-polish to polish this Chinese management paper introduction, preserving the original meaning and citations.
```

To verify that a polish did not change protected tokens:

```bash
python scripts/check_numeric_consistency.py original.md revised.md --json
python scripts/compare_manuscript_versions.py original.md revised.md --variable Treatment --json
```

The normal v3.1 experience is still a conversation, not a requirement to hand-chain
dozens of scripts. Give the Skill the manuscript, target outlet, reviewer comments, or
revision, and it orchestrates routing, evidence, style, method safety, and revision audits
as needed.

If you want to explicitly start a recoverable writing workspace, use the two entry points:

```bash
python scripts/init_writing_workspace.py paper-workspace --paper-id paper-001 --json
python scripts/run_writing_workflow.py paper-workspace --variable Treatment --json
```

Protected numbers and variables can be checked independently:

```bash
python scripts/check_numeric_consistency.py original.md revised.md --json
python scripts/compare_manuscript_versions.py original.md revised.md --variable Treatment --json
```

The remaining scripts are internal implementation and CI/developer tools, not a user-facing
control panel. See [`scripts/`](scripts/), each command's `--help`, and the [v3.1 upgrade plan](docs/v3.1-upgrade-plan.md).
All entry points produce inspectable state, reports, or candidate diffs; they do not overwrite
the manuscript automatically.

---

## Usage Scenarios

### Scenario 1: Paper Polish

```text
Rewrite this introduction in the style of an English applied microeconomics field journal, emphasizing identification and economic magnitude.
```

### Scenario 2: Method Diagnosis

```text
I'm using a two-way fixed effects DID. Help me determine if this empirical strategy is appropriate, and what robustness checks and methodological references I need.
```

### Scenario 3: Topic Suggestions

```text
This paper lacks innovation. Based on the current topic, data, and target CSSCI management journal, suggest conservative revision directions and aggressive pivot paths with necessary literature support.
```

### Scenario 4: Reviewer Response

```text
Based on these reviewer comments, help me制定 a revision plan and response letter, with a restrained tone and no exaggeration of revisions.
```

### Scenario 5: Paper Spine Diagnosis (v2.0)

```text
Diagnose this paper's argument spine — check if the core claims, contribution chain, and hypothesis chain are clear, and identify evidence gaps and risk points.
```

### Scenario 6: Reproducibility Audit (v2.0)

```text
Check this paper's reproducibility, including data transparency, method transparency, result consistency, identification logic, and robustness completeness.
```

### Scenario 7: Research Pipeline (v2.0)

```text
I want to go through the full pipeline from topic selection to submission. I have a preliminary research direction — help me diagnose the current stage and plan next steps.
```

### Scenario 8: LaTeX Support (v2.0)

```text
Check this .tex file for formatting issues, including three-line tables, equation numbering, cross-references, and BibTeX entry completeness.
```

### Scenario 9: RAG Knowledge Base (v2.0)

```text
I have a PDF literature library. Help me检索 which papers support the claim that "digital finance reduces poverty," and verify citation accuracy.
```

### Scenario 10: Survey Workspace (v2.0)

```text
Help me organize literature on "digital finance and rural development" — build a literature pool, trace the research lineage, and analyze literature gaps.
```

---

## Workflow

### Overall Flow

```
User Request
  → Identify task mode (polish/rewrite/diagnose/suggest/respond/pipeline...)
    → 4-quadrant routing (Chinese Econ / English Econ / Chinese Mgmt / English Mgmt)
      → Subfield overlay (Labor Econ / Strategic Mgmt / IS / ...)
        → Target journal adaptation
          → Check source access level
            → Execute output + evidence pack
```

### Research Pipeline (v2.0)

```
Stage 1: Topic Diagnosis
    ↓
Stage 2: Literature Review
    ↓
Stage 3: Theory Construction
    ↓
Stage 4: Research Design
    ↓
Stage 5: Writing Execution
    ↓
Stage 6: Self-Review
    ↓
Stage 7: Simulated Peer Review
    ↓
Stage 8: Iterative Refinement
```

---

## Degradation Modes

### RAG Knowledge Base Degradation

When vector database infrastructure is unavailable, 4 degradation modes are supported:

| Mode | Requirements | Capabilities | Use Case |
|------|-------------|--------------|----------|
| **Full RAG** | Vector DB + PDF parsing + embedding model | Semantic search, cross-paper QA | With tech infrastructure |
| **Manual Index** | User provides structured index | Keyword search | Have PDFs but no vector DB |
| **BibTeX Search** | BibTeX file | Metadata search | Only have reference list |
| **User-Guided** | User provides citations | Citation verification | No infrastructure |

### Sub-agent Delegation Degradation

When parallel execution is unavailable, 4 execution modes are supported:

| Mode | Requirements | Speed | Use Case |
|------|-------------|-------|----------|
| **Parallel** | Supports parallel sub-agents | Fast | Large manuscripts, time-sensitive |
| **Sequential** | Supports sequential sub-agents | Medium | General review |
| **Step-by-Step** | Single-threaded agent | Slow | Most scenarios |
| **Integrated** | No sub-agent support | Medium | Small manuscripts |

---

## Trigger Words

### English Triggers

```
paper polish, paper review, citation help, methodology diagnosis,
reviewer response, literature augmentation,
research pipeline, end-to-end, paper spine, argument structure,
RAG knowledge base, cross-paper QA, citation verification,
survey workspace, paper pool, close reading,
LaTeX writing, BibTeX management, reproducibility audit,
revision matrix, risk register
```

### Chinese Triggers

```
经管论文, 经济学论文, 管理论文, 实证论文, 论文润色, 学术润色,
降AI味, 选题调整, 变量建议, 改稿方向, 研究前沿, 主流研究, 贡献定位,
文献背书, 理论背书, 方法背书, 补充参考文献, 替代参考文献, APA格式, 返修回复,
研究流水线, 端到端, 从选题到投稿, 完整论文流程,
论点骨架, 核心论点, 论证链, 论点诊断,
RAG, 知识库, 文献库, 跨论文问答, 引用验证,
调研工作区, 文献池, 逐文精读, 文献整理,
LaTeX, tex, BibTeX, 期刊模板, 三线表,
可复现性, 复现检查, 数据透明度, 方法透明度,
修订矩阵, 返修跟踪, 风险清单
```

---

## Compatibility

This Skill supports all AI coding agents that support skill/system-prompt loading:

| Agent | Install Path | Status |
|-------|-------------|--------|
| **Codex (OpenAI)** | `.codex/skills/` | **Verified (local package contract + Windows 32-check suite + synthetic dogfood)** |
| **OpenCode** | `.opencode/skills/` | **Documented (installation path; no host smoke in this repo)** |
| **Claude Code** | `.claude/skills/` | **Documented (installation path; no host smoke in this repo)** |
| **Cursor** | `.cursor/rules/` | **Documented (installation path; no host smoke in this repo)** |
| **Windsurf** | `.windsurf/rules/` | **Documented (installation path; no host smoke in this repo)** |
| **Cline** | `.clinerules/` | **Documented (installation path; no host smoke in this repo)** |
| **GitHub Copilot** | Custom instructions | **Conceptual (requires host-specific conversion)** |
| **Aider** | Repo root | **Conceptual (requires host-specific conversion)** |

---

## Version History

### v3.1.0 (Writing Reliability Core, alpha.1–alpha.4) (2026-08-04)

This is the consolidated v3.1 alpha history. On top of the v3.0 reliability contracts,
it added the writing workspace/intake/route/checkpoint/journal, candidate paper spine,
protected snapshot/hash/anchor, many-to-many evidence ledger, corpus/style authorization
and freshness/overlap gates, section style revision plans, method risk cards and
conservative rewrites, bounded apply/rollback, issue transitions, response-letter
scaffolding, gold/mutation benchmarks, synthetic dogfooding, cross-platform/LaTeX
capability smoke, a unified contract suite, and hash-bound AI review packets with
isolated review and deterministic adjudication. The installable GitHub tag is
`v3.1.0-alpha.4`; the 32-check writing suite passes, while real-paper dogfooding, live
providers, real TeX, and high-risk scholarly decisions remain author-controlled, so the
release remains an alpha.

### v3.0.0-alpha.1 (2026-08-03)

Reliability core: routing and capability contracts, evidence-pack and journal-card
schemas, deterministic manuscript/citation/LaTeX audits, method-safety guidance,
fixtures, smoke tests, and CI. Legacy v2 references remain backward compatible.

### v2.0.0 (2026-06-05)

**18 new modules** for full-lifecycle coverage:

- **Paper Spine**: Inspired by PaperSpine — argument spine, revision matrix, risk register
- **Reproducibility Audit**: Inspired by Repro Pack — data/method reproducibility checks
- **Research Pipeline**: Inspired by academic-research-skills — 8-stage end-to-end workflow
- **LaTeX Support**: Inspired by LaTeX Writer — LaTeX writing, templates, audit
- **RAG Knowledge Base**: Inspired by PaperRAG/Cite Verity — RAG workflow (with degradation modes)
- **Survey Workspace**: Inspired by Survey Builder — survey workspace, paper pool, close reading

### v1.0.0 (2026-05-01)

**Initial release**, 23 core modules:

- 4-quadrant routing (CN/EN × Economics/Management)
- Subfield routing (20+ sub-disciplines)
- Target journal adaptation
- Citation workflow
- Evidence grading system
- Method diagnosis decision tree
- Quality gate checks

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to add subfield modules
- How to improve style rules
- How to submit Pull Requests

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

## Acknowledgments

The v2.0 upgrade was inspired by the following open-source academic research skill projects:

| Project | Stars | What We Learned |
|---------|-------|-----------------|
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | 32.9k | Journal-specific writing standards |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | 7.7k | End-to-end research pipeline |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) | 4.6k | Paper spine, revision matrix |
| [PaperRAG](https://github.com/GeederX/paper-rag-skill) | 0 | RAG knowledge base |
| [Cite Verity](https://github.com/kronzie/verity) | 0 | Cross-paper QA, citation verification |
| [LaTeX Writer](https://github.com/Listen-Sun/ieee-latex-writer) | 14 | LaTeX writing standards |
| [Survey Builder](https://github.com/zane-gao/paper-survey-builder) | 12 | Survey workspace organization |

*Star counts as of 2026-08-03.*

Thanks to all open-source contributors for their innovation!

---

**Built for the academic community in economics, management, and business research.**
