# Paper Pool (论文池管理)

Use this file for detailed management of the paper pool — the organized collection of papers relevant to a research topic.

## Relationship to Survey Workspace

This module focuses specifically on **paper pool management** — classification, entry templates, and statistics. For the broader research organization workflow (including research question definition, timeline mapping, method maps, gap analysis), see `survey-workspace.md`.

**Quick reference**:
- `survey-workspace.md` = 整体调研工作区结构和流程
- `paper-pool.md` = 论文池的详细管理规则

## When To Use

- Building a new paper pool for a research topic.
- Adding papers to an existing pool.
- Reorganizing or cleaning a paper pool.
- User asks to categorize their papers.

## Pool Structure

### Three-Tier Classification

```
┌─────────────────────────────────────────────┐
│                 文献池 (Paper Pool)          │
├─────────────────────────────────────────────┤
│                                             │
│  Tier 1: 核心文献 (Core Papers)             │
│  └── 与研究问题直接相关，必须精读            │
│                                             │
│  Tier 2: 扩展文献 (Extended Papers)         │
│  └── 间接相关，需要了解主要内容              │
│                                             │
│  Tier 3: 边缘文献 (Peripheral Papers)       │
│  └── 可能有用，只需浏览                     │
│                                             │
└─────────────────────────────────────────────┘
```

### Classification Criteria

| Criterion | Core | Extended | Peripheral |
|-----------|------|----------|------------|
| Research question match | Direct | Indirect | Tangential |
| Sample/context match | Same | Similar | Different |
| Method relevance | High | Medium | Low |
| Theory relevance | High | Medium | Low |
| Recency | Recent preferred | Any | Recent preferred |
| Quality | Top/field journal | Any quality | Any quality |

## Paper Entry Template

### Standard Entry

```markdown
## [Author (Year)] - [Short Title]

### 基本信息
- **完整标题**: [Full title]
- **作者**: [Author list]
- **期刊**: [Journal]
- **年份**: [Year]
- **DOI**: [DOI if available]
- **分类**: [核心/扩展/边缘]

### 内容摘要
[2-3 sentence summary of the paper's main contribution]

### 与本文相关性
- **研究问题**: [How it relates to our question]
- **方法**: [Method relevance]
- **发现**: [Key findings relevant to us]
- **局限**: [What it doesn't cover]

### 可引用内容
| 用途 | 段落/页码 | 引用方式 |
|------|---------|---------|
| 理论支持 | [Location] | [How to cite] |
| 方法参考 | [Location] | [How to cite] |
| 实证基准 | [Location] | [How to cite] |

### 阅读状态
- [ ] 已读摘要
- [ ] 已读引言
- [ ] 已读方法
- [ ] 已读结果
- [ ] 已读讨论
- [ ] 已精读全文

### 笔记
[Detailed notes if close-read]
```

### Quick Entry (for initial collection)

```markdown
## [Author (Year)]
- **标题**: [Title]
- **期刊**: [Journal]
- **相关性**: [One line on why relevant]
- **分类**: [核心/扩展/边缘]
- **状态**: 待读
```

## Pool Management Rules

### Adding Papers

1. **Source**: Where did you find this paper?
   - Literature search
   - Citation tracking
   - Recommendation
   - Conference/workshop

2. **Initial classification**: Based on abstract and title.
   - Can be reclassified after reading.

3. **Deduplication**: Check if paper is already in pool.

### Reclassifying Papers

Papers may move between tiers:

| From → To | Reason |
|-----------|--------|
| Core → Extended | After reading, less relevant than expected |
| Extended → Core | Found important connection after reading |
| Peripheral → Extended | Relevant finding discovered |
| Any → Excluded | Not relevant after reading |

### Excluding Papers

When excluding a paper:

```markdown
## [Author (Year)] - 已排除

### 排除原因
- [ ] 与研究问题不相关
- [ ] 样本/情境不匹配
- [ ] 方法不适用
- [ ] 质量不达标
- [ ] 重复/已被更好文献替代
- [ ] 其他: [Specify]

### 备注
[Brief note on what was learned]
```

## Pool Statistics

Maintain statistics for the pool:

```markdown
## 文献池统计

### 数量
- 核心文献: [N] 篇
- 扩展文献: [N] 篇
- 边缘文献: [N] 篇
- 已排除: [N] 篇
- **总计**: [N] 篇

### 覆盖度
- 理论覆盖: [评估]
- 方法覆盖: [评估]
- 样本覆盖: [评估]
- 时间覆盖: [Year range]

### 阅读进度
- 已精读: [N] 篇
- 已略读: [N] 篇
- 待读: [N] 篇

### 期刊分布
| 期刊 | 数量 | 占比 |
|------|------|------|
| [Journal 1] | [N] | [%] |
| [Journal 2] | [N] | [%] |
| ... | ... | ... |
```

## Integration With Other Modules

- **close-reading.md**: Templates for detailed reading.
- **survey-workspace.md**: Paper pool is part of the workspace.
- **evidence-citation-workflow.md**: Pool feeds into citation system.
- **rag-workflow.md**: Pool can be indexed for RAG search.
