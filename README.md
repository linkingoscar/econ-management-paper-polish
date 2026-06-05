# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#compatibility)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](#version-history)

**经管类学术论文全流程智能写作助手**

从选题到投稿，覆盖论文写作全生命周期的AI Skill。

> **适用领域**：经济学、管理学、金融、会计、营销、信息系统、公共管理、旅游/服务管理、创新创业等经管类学术论文。

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

---

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

## 文件结构

```
econ-management-paper-polish/
├── SKILL.md                           # 核心技能定义和规则 (v2.0)
├── README.md                          # 项目说明文档
├── LICENSE                            # MIT许可证
├── CONTRIBUTING.md                    # 贡献指南
├── .gitignore                         # Git忽略规则
└── references/                        # 41个参考模块
    │
    ├── 【核心路由】 (6个)
    │   ├── intake-and-modes.md            # 任务模式选择
    │   ├── discipline-router.md           # 学科路由
    │   ├── subfields-economics.md         # 经济学细分方向
    │   ├── subfields-management.md        # 管理学细分方向
    │   ├── field-style-packs.md           # 相邻领域风格包
    │   └── source-access-policy.md        # 来源访问层级
    │
    ├──【写作风格】 (6个)
    │   ├── cn-economics-style.md          # 中文经济学风格
    │   ├── en-economics-style.md          # 英文经济学风格
    │   ├── cn-management-style.md         # 中文管理学风格
    │   ├── en-management-style.md         # 英文管理学风格
    │   ├── style-and-polish.md            # 风格润色规则
    │   └── section-patterns.md            # 章节结构模板
    │
    ├── 【期刊适配】 (4个)
    │   ├── journal-families-econ.md       # 经济学期刊家族
    │   ├── journal-families-management.md # 管理学期刊家族
    │   ├── journal-style-adaptation.md    # 期刊风格适配
    │   └── journal-style-card.md          # 期刊风格卡生成
    │
    ├── 【文献引用】 (4个)
    │   ├── evidence-citation-workflow.md  # 引用搜索/验证/格式化
    │   ├── evidence-grading.md            # 证据分级 (A/B/C/D)
    │   ├── theory-backing-router.md       # 理论背书路由
    │   └── topic-revision-advisor.md      # 选题/改稿建议
    │
    ├── 【方法诊断】 (2个)
    │   ├── empirical-method-router.md     # 实证方法路由
    │   └── method-decision-tree.md        # 方法决策树
    │
    ├── 【质量门控】 (1个)
    │   └── quality-gates.md               # 质量门控检查
    │
    ├── 【v2.0新增：论点骨架】 (3个) ★
    │   ├── paper-spine.md                 # 论点骨架系统
    │   ├── revision-matrix.md             # 修订矩阵
    │   └── risk-register.md               # 风险清单
    │
    ├── 【v2.0新增：可复现性审计】 (3个) ★
    │   ├── reproducibility-audit.md       # 可复现性审计
    │   ├── data-reproducibility.md        # 数据可复现性
    │   └── method-reproducibility.md      # 方法可复现性
    │
    ├── 【v2.0新增：研究流水线】 (3个) ★
    │   ├── research-pipeline.md           # 研究流水线
    │   ├── pipeline-stage-gates.md        # 阶段门控
    │   └── pipeline-delegation.md         # 子代理委派
    │
    ├── 【v2.0新增：LaTeX支持】 (3个) ★
    │   ├── latex-support.md               # LaTeX写作支持
    │   ├── latex-templates.md             # 期刊LaTeX模板
    │   └── latex-audit.md                 # LaTeX质量审计
    │
    ├── 【v2.0新增：RAG知识库】 (3个) ★
    │   ├── rag-workflow.md                # RAG工作流
    │   ├── rag-retrieval.md               # RAG检索策略
    │   └── rag-verification.md            # RAG引用验证
    │
    └── 【v2.0新增：调研工作区】 (3个) ★
        ├── survey-workspace.md            # 调研工作区
        ├── paper-pool.md                  # 论文池管理
        └── close-reading.md               # 逐文精读
```

---

## 快速开始

### 安装

#### OpenCode

```bash
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.opencode/skills/econ-management-paper-polish
```

#### Claude Code

```bash
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.claude/skills/econ-management-paper-polish
```

#### Codex (OpenAI)

```bash
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.codex/skills/econ-management-paper-polish
```

#### Cursor

```bash
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  .cursor/rules/econ-management-paper-polish
```

### 基本使用

```text
用 econ-management-paper-polish 帮我润色这段中文管理学论文引言，保留原意和引用。
```

---

## 使用场景

### 场景1：论文润色

```text
按英文应用微观经济学field journal风格，帮我重写这段introduction，
突出identification和economic magnitude。
```

### 场景2：方法诊断

```text
我现在用双向固定效应DID，帮我判断这个实证策略是否合适，
需要哪些稳健性和方法文献支持。
```

### 场景3：选题建议

```text
这篇文章创新性不足。基于当前题目、数据和目标CSSCI管理类期刊，
帮我给出保守改稿方向和激进转向方向，并提供必要文献支持。
```

### 场景4：返修回复

```text
根据这些审稿意见，帮我制定返修路线和response letter，
要求语气克制，不夸大修改效果。
```

### 场景5：论点骨架诊断（v2.0）

```text
帮我诊断这篇论文的论点骨架，检查核心主张、贡献链、假说链是否清晰，
识别证据缺口和风险点。
```

### 场景6：可复现性审计（v2.0）

```text
帮我检查这篇论文的可复现性，包括数据透明度、方法透明度、
结果一致性、识别逻辑和稳健性完整性。
```

### 场景7：研究流水线（v2.0）

```text
我想从选题到投稿走一遍完整流程，现在有一个初步的研究方向，
帮我诊断当前阶段并规划下一步。
```

### 场景8：LaTeX支持（v2.0）

```text
帮我检查这个.tex文件的格式问题，包括三线表、公式编号、
交叉引用、BibTeX条目是否完整。
```

### 场景9：RAG知识库（v2.0）

```text
我有一个PDF文献库，帮我检索哪些文献支持"数字金融减少贫困"这个观点，
并验证引用的准确性。
```

### 场景10：调研工作区（v2.0）

```text
帮我整理"数字金融与农村发展"这个方向的文献，
建立文献池、梳理研究脉络、分析文献缺口。
```

---

## 工作流程

### 整体流程

```
用户请求
  → 识别任务模式（润色/改写/诊断/建议/返修/流水线...）
    → 四象限路由（中文经济学 / 英文经济学 / 中文管理学 / 英文管理学）
      → 细分方向叠加（劳动经济学 / 战略管理 / IS / ...）
        → 目标期刊适配
          → 检查来源访问层级
            → 执行输出 + 证据包
```

### 研究流水线（v2.0）

```
Stage 1: 选题诊断
    ↓
Stage 2: 文献综述
    ↓
Stage 3: 理论构建
    ↓
Stage 4: 研究设计
    ↓
Stage 5: 写作执行
    ↓
Stage 6: 自审自查
    ↓
Stage 7: 同行模拟审稿
    ↓
Stage 8: 迭代完善
```

---

## 降级方案

### RAG知识库降级

当没有向量数据库等基础设施时，支持4种降级模式：

| 模式 | 要求 | 能力 | 适用场景 |
|------|------|------|---------|
| **Full RAG** | 向量数据库+PDF解析+嵌入模型 | 语义搜索、跨论文QA | 有技术基础设施 |
| **Manual Index** | 用户提供结构化索引 | 关键词搜索 | 有PDF但无向量DB |
| **BibTeX Search** | BibTeX文件 | 元数据搜索 | 只有参考文献列表 |
| **User-Guided** | 用户提供引文 | 引用验证 | 无任何基础设施 |

### 子代理委派降级

当不支持并行执行时，支持4种执行模式：

| 模式 | 要求 | 速度 | 适用场景 |
|------|------|------|---------|
| **Parallel** | 支持并行子代理 | 快 | 大型文稿、时间紧迫 |
| **Sequential** | 支持顺序子代理 | 中 | 一般审查 |
| **Step-by-Step** | 单线程代理 | 慢 | 大多数场景 |
| **Integrated** | 无子代理支持 | 中 | 小型文稿 |

---

## 触发词参考

### 中文触发词

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

### 英文触发词

```
paper polish, paper review, citation help, methodology diagnosis,
reviewer response, literature augmentation,
research pipeline, end-to-end, paper spine, argument structure,
RAG knowledge base, cross-paper QA, citation verification,
survey workspace, paper pool, close reading,
LaTeX writing, BibTeX management, reproducibility audit,
revision matrix, risk register
```

---

## 兼容性

本Skill支持所有支持skill/系统提示加载的AI编程代理：

| 代理 | 安装路径 | 状态 |
|------|---------|------|
| **OpenCode** | `.opencode/skills/` | ✅ 支持 |
| **Claude Code** | `.claude/skills/` | ✅ 支持 |
| **Codex (OpenAI)** | `.codex/skills/` | ✅ 支持 |
| **Cursor** | `.cursor/rules/` | ✅ 支持 |
| **Windsurf** | `.windsurf/rules/` | ✅ 支持 |
| **Cline** | `.clinerules/` | ✅ 支持 |
| **GitHub Copilot** | 自定义指令 | ✅ 支持 |
| **Aider** | 仓库根目录 | ✅ 支持 |

---

## 版本历史

### v2.0.0 (2026-06-05)

**新增18个模块**，实现经管论文全流程覆盖：

- **论点骨架系统**：借鉴PaperSpine，新增论点骨架、修订矩阵、风险清单
- **可复现性审计**：借鉴Repro Pack概念，新增数据/方法可复现性检查
- **研究流水线**：借鉴academic-research-skills，新增8阶段端到端流程
- **LaTeX支持**：借鉴LaTeX Writer，新增LaTeX写作、模板、审计
- **RAG知识库**：借鉴PaperRAG/Cite Verity，新增RAG工作流（含降级方案）
- **调研工作区**：借鉴Survey Builder，新增调研工作区、论文池、逐文精读

### v1.0.0 (2026-05-01)

**初始版本**，23个核心模块：

- 四象限路由（中/英 × 经济/管理）
- 细分方向路由（20+子领域）
- 目标期刊适配
- 文献引用工作流
- 证据分级系统
- 方法诊断决策树
- 质量门控检查

---

## 贡献指南

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解：

- 如何添加子领域模块
- 如何改进风格规则
- 如何提交Pull Request

---

## 许可证

[MIT](LICENSE) — 免费使用、修改和分发。

---

## 致谢

v2.0升级受到以下开源学术研究技能项目的启发：

| 项目 | Stars | 借鉴内容 |
|------|-------|---------|
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | 16.7k | 期刊特定写作规范 |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | 2.9k | 端到端研究流水线 |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) | 2.2k | 论点骨架、修订矩阵 |
| [PaperRAG](https://github.com/GeederX/paper-rag-skill) | — | RAG知识库 |
| [Cite Verity](https://github.com/kronzie/verity) | — | 跨论文问答、引用验证 |
| [LaTeX Writer](https://github.com/Listen-Sun/ieee-latex-writer) | 8 | LaTeX写作规范 |
| [Survey Builder](https://github.com/zane-gao/paper-survey-builder) | 1 | 调研工作区组织 |

感谢所有开源贡献者的创新！

---

## 联系方式

- 问题反馈：[GitHub Issues](https://github.com/YOUR_USERNAME/econ-management-paper-polish/issues)
- 功能建议：[GitHub Discussions](https://github.com/YOUR_USERNAME/econ-management-paper-polish/discussions)

---

**Built for the academic community in economics, management, and business research.**
