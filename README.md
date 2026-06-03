# Econ-Management Paper Polish

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Compatible](https://img.shields.io/badge/Agents-Universal-green.svg)](#compatibility)

**A universal academic paper skill for economics, management, and business-school disciplines.**

Polishing, rewriting, literature augmentation, method diagnosis, topic advisory, and reviewer response — with discipline-aware routing and traceable citations.

> **适用领域**：经济学、管理学、金融、会计、营销、信息系统、公共管理、旅游/服务管理、创新创业等经管类学术论文。

---

## Features

| 能力 | 说明 |
|---|---|
| **论文润色** | 轻润色、同行化改写、降 AI 味、中英文风格适配 |
| **结构改写** | 引言→文献综述→理论→假设→实证→结果→稳健性→异质性→讨论→结论 |
| **四象限路由** | 中文经济学 / 英文经济学 / 中文管理学 / 英文管理学 |
| **细分方向路由** | 应用微观、劳动、环境、产业组织、战略、OB/HR、IS、营销等 |
| **目标期刊适配** | 基于作者指南和近期样刊生成 journal style card |
| **文献补强** | 政策背景、理论机制、方法背书、变量测量、替代参考文献 |
| **证据分级** | Grade A/B/C/D 区分可直接引用→不建议引用 |
| **方法诊断** | DID、事件研究、IV、RD、SCM、匹配、中介、文本/ML、DML 等 |
| **选题与改稿** | 贡献诊断、变量建议、保守改稿/激进转向路径 |
| **返修回复** | 审稿意见拆解、回应语气、修改动作和证据补充 |

## Quick Start

### OpenCode

```bash
# Clone into OpenCode skills directory
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.opencode/skills/econ-management-paper-polish
```

Then use in conversation:

```text
用 econ-management-paper-polish 帮我润色这段中文管理学论文引言，保留原意和引用。
```

### Claude Code

```bash
# Clone into Claude Code skills directory
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.claude/skills/econ-management-paper-polish
```

Or use the `skill` tool to load it dynamically.

### Codex (OpenAI)

```bash
# Clone into Codex skills directory
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  ~/.codex/skills/econ-management-paper-polish
```

### Cursor

```bash
# Clone into project rules directory
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  .cursor/rules/econ-management-paper-polish
```

Then reference the rules in your `.cursorrules` file or project settings.

### Windsurf

```bash
git clone https://github.com/YOUR_USERNAME/econ-management-paper-polish.git \
  .windsurf/rules/econ-management-paper-polish
```

### Cline / GitHub Copilot / Aider

Place the cloned directory in the agent's rules or instructions path, or reference
`SKILL.md` as custom instructions. See your agent's documentation for custom skill
loading.

## Usage Examples

### Light Polish (轻润色)

```text
用 econ-management-paper-polish 帮我润色这段中文管理学论文引言，保留原意和引用。
```

### English Economics Rewrite

```text
按英文应用微观经济学 field journal 风格，帮我重写这段 introduction，
突出 identification 和 economic magnitude。
```

### Theory Backing (理论背书)

```text
这段理论机制太弱，帮我诊断需要哪些理论背书，并检索可追溯文献，默认 APA。
```

### Method Diagnosis (方法诊断)

```text
我现在用双向固定效应 DID，帮我判断这个实证策略是否合适，
需要哪些稳健性和方法文献支持。
```

### Topic & Revision Advisory (选题与改稿)

```text
这篇文章创新性不足。基于当前题目、数据和目标 CSSCI 管理类期刊，
帮我给出保守改稿方向和激进转向方向，并提供必要文献支持。
```

### Reviewer Response (返修回复)

```text
根据这些审稿意见，帮我制定返修路线和 response letter，
要求语气克制，不夸大修改效果。
```

## How It Works

```
用户请求
  → 识别任务模式（润色/改写/诊断/建议/返修…）
    → 四象限路由（中文经济学 / 英文经济学 / 中文管理学 / 英文管理学）
      → 细分方向叠加（劳动经济学 / 战略管理 / IS / …）
        → 目标期刊适配
          → 检查来源访问层级
            → 执行输出 + 证据包
```

## File Structure

```
econ-management-paper-polish/
├── SKILL.md                           # Core skill definition and rules
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore rules
└── references/                        # 23 reference modules
    ├── intake-and-modes.md            # Task mode selection
    ├── discipline-router.md           # Discipline routing
    ├── cn-economics-style.md          # Chinese economics style
    ├── en-economics-style.md          # English economics style
    ├── cn-management-style.md         # Chinese management style
    ├── en-management-style.md         # English management style
    ├── subfields-economics.md         # Economics subfield router
    ├── subfields-management.md        # Management subfield router
    ├── journal-families-econ.md       # Economics journal families
    ├── journal-families-management.md # Management journal families
    ├── journal-style-adaptation.md    # Journal style adaptation
    ├── journal-style-card.md          # Journal style card generation
    ├── field-style-packs.md           # Adjacent field style packs
    ├── source-access-policy.md        # Source access tiers
    ├── evidence-citation-workflow.md  # Citation search/verify/format
    ├── evidence-grading.md            # Evidence grading (A/B/C/D)
    ├── theory-backing-router.md       # Theory backing router
    ├── empirical-method-router.md     # Empirical method router
    ├── method-decision-tree.md        # Method decision tree
    ├── section-patterns.md            # Section structure templates
    ├── style-and-polish.md            # Style and polish rules
    ├── quality-gates.md               # Quality gates
    └── topic-revision-advisor.md      # Topic/revision advisory
```

## Core Principles

1. **No fabrication** — Never invent citations, DOI, data, regression results, or journal requirements.
2. **Traceable sources** — Every new reference must come from a verifiable source in the current session.
3. **Discipline-aware** — Economics ≠ management ≠ finance. Respect paradigm differences.
4. **Evidence grading** — Grade A (full-text verified) to Grade D (unverifiable). Never overclaim.
5. **Preserve intent** — Keep the user's claims, numbers, variables, and contribution intact unless asked to change.
6. **Flag, don't smooth** — If a claim is unsupported or overcausal, flag it instead of silently rewriting.

## What This Skill Will NOT Do

- ❌ Fabricate references, DOI, journal requirements, or regression results
- ❌ Treat search snippets as complete literature
- ❌ Recommend advanced methods without data support
- ❌ Write correlation as causation
- ❌ Claim systematic literature coverage without actual retrieval
- ❌ Bypass database access restrictions or terms of use

## License

[MIT](LICENSE) — free to use, modify, and distribute.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding subfield modules,
improving style rules, and submitting pull requests.

## Acknowledgments

Built for the academic community in economics, management, and business research.
Designed to work with any AI coding agent that supports skill or system-prompt loading.
