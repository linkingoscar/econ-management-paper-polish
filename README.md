# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#兼容性)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](#版本历史)
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

新增 18 个模块：论点骨架、修订矩阵、风险清单、可复现性审计、研究流水线、阶段门控、子代理委派、LaTeX 支持、RAG 知识库、调研工作区等（详见上方功能表）。

### v1.0.0 (2026-05-01)

首发 23 个核心模块：四象限路由、细分方向路由、目标期刊适配、引用工作流、证据分级、方法诊断决策树、质量门控检查。

---

## 许可证

[MIT](LICENSE) — 免费使用、修改和分发。

---

**Built for the academic community in economics, management, and business research.**