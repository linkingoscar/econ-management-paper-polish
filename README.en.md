# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#compatibility)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](#version-history)

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

---

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

## File Structure

```
econ-management-paper-polish/
├── SKILL.md                           # Core skill definition and rules (v2.0)
├── README.md                          # Chinese documentation
├── README.en.md                       # English documentation
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guide
├── .gitignore
└── references/                        # 41 reference modules
    ├── Core Routing (6)
    ├── Writing Style (6)
    ├── Journal Adaptation (4)
    ├── Citation & Evidence (4)
    ├── Method Diagnosis (2)
    ├── Quality Gates (1)
    ├── v2.0: Paper Spine (3)
    ├── v2.0: Reproducibility Audit (3)
    ├── v2.0: Research Pipeline (3)
    ├── v2.0: LaTeX Support (3)
    ├── v2.0: RAG Knowledge Base (3)
    └── v2.0: Survey Workspace (3)
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
| **OpenCode** | `.opencode/skills/` | Supported |
| **Claude Code** | `.claude/skills/` | Supported |
| **Codex (OpenAI)** | `.codex/skills/` | Supported |
| **Cursor** | `.cursor/rules/` | Supported |
| **Windsurf** | `.windsurf/rules/` | Supported |
| **Cline** | `.clinerules/` | Supported |
| **GitHub Copilot** | Custom instructions | Supported |
| **Aider** | Repo root | Supported |

---

## Version History

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
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | 16.7k | Journal-specific writing standards |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | 2.9k | End-to-end research pipeline |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) | 2.2k | Paper spine, revision matrix |
| [PaperRAG](https://github.com/GeederX/paper-rag-skill) | — | RAG knowledge base |
| [Cite Verity](https://github.com/kronzie/verity) | — | Cross-paper QA, citation verification |
| [LaTeX Writer](https://github.com/Listen-Sun/ieee-latex-writer) | 8 | LaTeX writing standards |
| [Survey Builder](https://github.com/zane-gao/paper-survey-builder) | 1 | Survey workspace organization |

Thanks to all open-source contributors for their innovation!

---

**Built for the academic community in economics, management, and business research.**
