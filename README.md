# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#兼容性)
[![Version](https://img.shields.io/badge/Version-3.1.0--alpha.3-orange.svg)](#v31-写作可靠性基础alpha)
[![Academic](https://img.shields.io/badge/Academic-Writing-005A9C?logo=google&logoColor=white)](#)
[![Multi-Agent](https://img.shields.io/badge/MultiAgent-Supported-FF6F00?logo=javascript&logoColor=white)](#)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-000000?logo=opencode&logoColor=white)](#)
[![Claude Code](https://img.shields.io/badge/Claude-Code-CC0000?logo=anthropic&logoColor=white)](#)
[![Codex](https://img.shields.io/badge/Codex-OpenAI-000000?logo=openai&logoColor=white)](#)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000?logo=cursor&logoColor=white)](#)
[![RAG](https://img.shields.io/badge/RAG-Knowledge-4CAF50?logo=google&logoColor=white)](#)
[![LaTeX](https://img.shields.io/badge/LaTeX-Supported-008080?logo=latex&logoColor=white)](#)

**经管类学术论文全流程智能写作助手**

从选题到投稿,覆盖论文写作全生命周期的AI Skill。

> **适用领域**：经济学、管理学、金融、会计、营销、信息系统、公共管理、旅游/服务管理、创新创业等经管类学术论文。

> **[English](README.en.md)**

---

## 项目简介

Econ-Management Paper Polish 是一个专为经管类学术论文设计的AI Skill，支持多种AI编程代理（OpenCode、Claude Code、Codex、Cursor等）。

### 核心目标

| 目标 | 说明 |
|------|------|
| **写作质量** | 中英文学术写作规范化、降AI味、期刊适配 |
| **论证质量** | 论点清晰、证据充分、方法合理、因果语言准确 |
| **引用质量** | 可追溯、不造假、证据分级 |
| **返修质量** | 审稿意见有效回应、修订可追踪 |
| **研究效率** | 文献管理、调研组织、流水线协作 |

### 设计原则

1. **不造假** — 绝不虚构引用、数据、回归结果或期刊要求
2. **可追溯** — 每个新引用必须有当前会话中的可验证来源
3. **学科感知** — 经济学 ≠ 管理学 ≠ 金融学，尊重范式差异
4. **证据分级** — Grade A（全文验证）到 Grade D（不可验证），绝不过度宣称
5. **保留意图** — 除非用户要求，保留用户的主张、数字、变量和贡献定位

### 降AI味与学术诚信

本项目提供"降AI味"能力，立场明确：

1. **定义** — 降AI味指消除模板化套话（空泛开头、"具有重要意义"式表态、机械排比），恢复学科具体性（机制、制度背景、样本细节、表列引用），让文本回到领域内行家自然写作的样态。
2. **不做什么** — 不提供任何针对 AI 检测器的规避手段，不以"通过检测"为优化目标。若用户要求改写至无法被识别为 AI 生成，应拒绝并说明理由。
3. **作者责任** — 所有输出需作者自行核实；若目标期刊、学校或出版社要求披露 AI 辅助，应如实披露。这与本项目"不造假引用、不夸大证据"的原则同属一套诚信框架。
4. **立场** — 学术机构对 AI 使用的规范仍在演进，本项目选择保守立场：宁可不帮，不帮规避。

## 功能特性

### v1.0 核心能力（23个模块）

| 能力 | 说明 | 触发词示例 |
|------|------|-----------|
| **论文润色** | 轻润色、同行化改写、降AI味、中英文风格适配 | 论文润色, 降AI味, paper polish |
| **结构改写** | 引言→文献综述→理论→假设→实证→结果→稳健性→异质性→讨论→结论 | 结构改写, 重组段落 |
| **四象限路由** | 中文经济学 / 英文经济学 / 中文管理学 / 英文管理学 | 自动识别 |
| **细分方向路由** | 应用微观、劳动、环境、产业组织、战略、OB/HR、IS、营销等 | 自动识别 |
| **目标期刊适配** | 基于作者指南和近期样刊生成journal style card | 适配AER, 适配管理世界 |
| **文献补强** | 政策背景、理论机制、方法背书、变量测量、替代参考文献 | 补充文献, 文献背书 |
| **证据分级** | Grade A/B/C/D 区分可直接引用→不建议引用 | 自动分级 |
| **方法诊断** | DID、事件研究、IV、RD、SCM、匹配、中介、文本/ML、DML等 | 方法诊断, 方法是否合适 |
| **选题与改稿** | 贡献诊断、变量建议、保守改稿/激进转向路径 | 选题调整, 改稿方向 |
| **返修回复** | 审稿意见拆解、回应语气、修改动作和证据补充 | 返修回复, response letter |

### v2.0 新增能力（18个模块）

| 能力 | 说明 | 触发词示例 | 对标项目 |
|------|------|-----------|---------|
| **论点骨架** | 核心主张、贡献链、假说链、证据地图、风险清单 | 论点骨架, 核心论点 | PaperSpine |
| **修订矩阵** | 返修跟踪、修改动作记录、状态管理 | 修订矩阵, 返修跟踪 | PaperSpine |
| **风险清单** | 方法风险、理论风险、证据风险、表述风险、发表风险 | 风险清单, 审稿人可能的问题 | PaperSpine |
| **可复现性审计** | 数据透明度、方法透明度、结果一致性检查 | 可复现性, 复现检查 | Repro Pack |
| **研究流水线** | 8阶段端到端流程 | 研究流水线, 从选题到投稿 | academic-research-skills |
| **阶段门控** | 每个阶段的质量检查点 | 阶段门控 | academic-research-skills |
| **子代理委派** | 并行/顺序/分步执行模式 | 全面审查, 系统分析 | academic-research-skills |
| **LaTeX支持** | LaTeX写作规范、期刊模板、格式审计 | LaTeX, 三线表, BibTeX | LaTeX Writer |
| **RAG知识库** | 本地PDF检索、语义搜索、跨论文问答、引用验证 | RAG, 知识库, 跨论文问答 | PaperRAG / Cite Verity |
| **调研工作区** | 文献池管理、主脉络梳理、逐文精读、缺口分析 | 调研工作区, 文献整理 | Survey Builder |

---

## v3.0 可靠性核心（alpha）

v3.0.0-alpha.1 先解决“能不能信、能不能复核”，不假装把 41 个旧参考模块
变成可执行系统。本次升级保持旧版 `references/` 兼容，同时加入：

| 能力 | 可交付物 |
|------|----------|
| 路由与能力声明 | `references/v3-runtime-contract.md`；Verified / Documented / Conceptual 三档 |
| 证据账本 | `assets/evidence-pack.schema.json`、`scripts/build_evidence_pack.py` |
| 确定性审计 | 数字、引用、LaTeX、修订前后变量/数字检查脚本 |
| 方法安全层 | `references/v3-method-safety.md`，明确 DID、IV、RD、面板、调查、实验、定性研究的边界 |
| 职责化知识层 | `references/v3/` 下 14 个聚合包；41 个旧模块由 `legacy-index.md` 映射并保留兼容 |
| 可插拔集成 | Crossref/OpenAlex 检索、可持久化本地 RAG、串行/HTTP 多代理适配器 |
| 可持续验证 | `assets/` 状态 schema、`evals/` fixtures、GitHub Actions CI |

从仓库根目录运行：

```bash
py scripts/validate_v3.py .
py evals/run_smoke_tests.py
py evals/run_extended_tests.py
py evals/run_v31_writing_tests.py
py scripts/run_writing_benchmark.py --output writing-benchmark.json --json
py scripts/validate_skill_package.py . --json
py scripts/validate_repro_lock.py . --json
```

脚本能验证的是文本、引用和结构一致性；没有原始数据、代码或付费数据库时，
不会把“审计”包装成真实复现。RAG 和多代理已经提供可选适配器，但真实检索
和模型调用仍需网络、凭据和独立的证据核验。

---

## v3.1 写作可靠性基础（alpha）

v3.1 仍以“经管论文写作与返修 Skill”为核心，不把项目扩张为通用自主科研平台。
本次 alpha.2 已把检查器串成可恢复的写作闭环：workspace/intake/route card、候选
paper spine、protected snapshot、checkpoint 和 JSONL revision journal；many-to-many
evidence ledger、source withdrawal impact、corpus license/freshness/sample gate、
加权且带 locator 的 section style profile、原句重合审计和结构化 revision plan；方法
风险卡与保守改写报告；bounded apply/rollback、hash/anchor 校验、issue 状态迁移和
response-letter scaffold；证据/期刊新鲜度门、返修矩阵与 response-letter 提交前校验；
本地 synthetic dogfood、跨平台/LaTeX 能力报告、26 项写作契约测试、gold/mutation
benchmark、统一 contract suite、Skill 包装校验和 adapter repro lock。
检索、RAG 与多代理仍只作为这些写作能力的支撑。

* [v3.1 外部项目调研报告](docs/v3.1-landscape-research.md)
* [v3.1 超详细升级计划](docs/v3.1-upgrade-plan.md)

已实现能力仍属于 alpha：脚本负责确定性扫描、契约校验和候选 diff，不自动替作者
决定理论、识别、结果或贡献。style profile 默认是 draft，必须人工确认；TeX 编译器
缺失时只报告 Documented，不把结构审计冒充真实编译。当前 benchmark 的 26 项检查、
10 个本地 synthetic dogfood case 和 gold/mutation 指标均为公开 fixture；它们验证的是
工作流接线与确定性闸门，不是作者声音、因果裁决或期刊效果。真实/匿名论文与期刊效果
人工 rubric 仍是进入 beta 前的工作。

---

## 快速开始

### 安装

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

### 基本使用

```text
用 econ-management-paper-polish 帮我润色这段中文管理学论文引言，保留原意和引用。
```

如需检查润色是否意外改动数字或变量，可在论文文件旁运行：

```bash
py scripts/check_numeric_consistency.py original.md revised.md --json
py scripts/compare_manuscript_versions.py original.md revised.md --variable Treatment --json
```

v3.1 写作基础可以按需运行：

```bash
py scripts/prepare_corpus.py corpus --role target-journal --output corpus-manifest.json --json
py scripts/extract_style_card.py corpus/paper.md --source-id SRC-0001 --output style-card.json --json
py scripts/build_style_profile.py style-cards --output style-profile.json --json
py scripts/check_claim_evidence.py paper-spine.json --evidence-pack evidence-pack.json --json
py scripts/build_evidence_ledger.py evidence-ledger-input.json --output evidence-ledger.json --json
py scripts/check_evidence_impact.py evidence-ledger.json SRC-0001 --json
py scripts/audit_evidence_freshness.py evidence-ledger.json --max-age-days 365 --json
py scripts/audit_journal_freshness.py journal-card.json --max-age-days 365 --json
py scripts/build_issue_ledger.py reviewer-issues.json --output review-ledger.json --json
py scripts/propose_bounded_patch.py original.md revised.md --output patch-report.json --json
py scripts/verify_bounded_patch.py original.md revised.md --variable Treatment --json
py scripts/apply_bounded_patch.py original.md revised.md --output applied.md --variable Treatment --json
py scripts/rollback_bounded_patch.py original.md --output rollback.md --json
py scripts/transition_issue.py review-ledger.json ISS-001 proposed --output review-ledger-proposed.json --actor author --rationale "..." --json
py scripts/build_response_letter.py review-ledger.json --output response-letter.md --json
py scripts/build_revision_matrix.py review-ledger.json --output revision-matrix.csv --json
py scripts/validate_response_letter.py review-ledger-closed.json response-letter-submission.md --json
py scripts/meaning_audit.py original.md revised.md --json
py scripts/check_method_language.py manuscript.md --json
py scripts/build_method_safety_report.py manuscript.md --json
py scripts/compile_guard.py manuscript.tex --strict --json
py scripts/check_issue_recall.py review-ledger-before.json review-ledger-after.json --json
py scripts/validate_style_profile_gate.py style-profile.json --json
py scripts/plan_style_revision.py manuscript.md style-profile-confirmed.json --section method --output style-revision-plan.json --json
py scripts/init_writing_workspace.py paper-workspace --paper-id paper-001 --json
py scripts/run_writing_workflow.py paper-workspace --variable Treatment --json
py scripts/run_dogfood_suite.py --json
py scripts/run_platform_smoke.py --json
py scripts/run_contract_suite.py --json
```

这些命令只生成可检查的状态和候选 diff，不会自动覆盖论文正文。`run_dogfood_suite.py`
只把仓库内的 synthetic fixture 复制到临时工作区，用于回归工作流接线，不等同于真实
论文 dogfooding；如需保存机器可读报告，请显式传入 `--output` 并放在仓库外。

---

## 兼容性

本Skill支持所有支持skill/系统提示加载的AI编程代理：

| 代理 | 安装路径 | 状态 |
|------|---------|------|
| **Codex (OpenAI)** | `.codex/skills/` | **Verified（本地包契约 + Windows 26 项写作测试 + synthetic dogfood）** |
| **OpenCode** | `.opencode/skills/` | **Documented（安装路径已记录，未在本仓库 smoke）** |
| **Claude Code** | `.claude/skills/` | **Documented（安装路径已记录，未在本仓库 smoke）** |
| **Cursor** | `.cursor/rules/` | **Documented（安装路径已记录，未在本仓库 smoke）** |
| **Windsurf** | `.windsurf/rules/` | **Documented（安装路径已记录，未在本仓库 smoke）** |
| **Cline** | `.clinerules/` | **Documented（安装路径已记录，未在本仓库 smoke）** |
| **GitHub Copilot** | 自定义指令 | **Conceptual（需按宿主产品规则转换）** |
| **Aider** | 仓库根目录 | **Conceptual（需按宿主产品规则转换）** |

---

## 版本历史

### v3.1.0-alpha.3 (2026-08-04)

在 alpha.2 之上完成非人工可自动化收口：证据与期刊卡 freshness gate、revision matrix
CSV/JSON、response-letter 提交前 placeholder/issue/evidence 校验、10 个临时工作区
synthetic dogfood case、跨平台 UTF-8/路径/LaTeX capability smoke、26 项 v3.1 writing
测试和统一 contract suite。真实论文、作者语义确认、人工 rubric 和外部 TeX/数据库
仍不宣称已完成。

### v3.1.0-alpha.2 (2026-08-04)

按 v3.1-upgrade-plan 完成 alpha 闭环：workspace/intake/route/checkpoint/journal、
候选 paper spine、protected snapshot/hash/anchor、many-to-many evidence ledger 与
impact、corpus/style license/freshness/overlap gates、section style revision plan、
方法风险卡与保守改写报告、bounded apply/rollback、issue transition、response-letter
scaffold、gold/mutation benchmark、Skill 包装子集和 adapter repro lock。
该版本仍不自动决定理论/识别/贡献，不把合成测试或文本审计包装成真实复现。

### v3.1.0-alpha.1 (2026-08-04)

写作可靠性基础：corpus manifest、style card/profile、paper spine、claim–evidence
检查、review ledger、风险预路由、受保护 patch 验证、语义/方法语言闸门、LaTeX
compile guard、issue recall、provenance 扫描、契约 schema 和离线 fixture。

### v3.0.0-alpha.1 (2026-08-03)

可靠性核心：新增路由与能力声明、证据账本与 journal card schema、数字/引用/LaTeX
确定性审计、方法安全层、14 个职责化 reference 包、Crossref/OpenAlex 检索、本地
RAG、多代理适配器、扩展评测和 CI。旧版 41 个 reference 模块继续兼容。

### v2.0.0 (2026-06-05)

新增 18 个模块：论点骨架、修订矩阵、风险清单、可复现性审计、研究流水线、阶段门控、子代理委派、LaTeX 支持、RAG 知识库、调研工作区等（详见上方功能表）。

### v1.0.0 (2026-05-01)

首发 23 个核心模块：四象限路由、细分方向路由、目标期刊适配、引用工作流、证据分级、方法诊断决策树、质量门控检查。

---

## 许可证

[MIT](LICENSE) — 免费使用、修改和分发。

---

**Built for the academic community in economics, management, and business research.**
