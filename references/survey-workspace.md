# Survey Workspace (调研工作区)

Use this file when the user wants to organize research on a specific topic into a structured, long-term workspace. This is for topics that are still fuzzy and need systematic exploration before writing.

## When To Use

- User asks to organize research on a topic.
- User has many papers but no clear structure.
- User says "帮我整理一下这个方向的文献".
- User is starting a new research direction.
- User wants a systematic literature survey.

## Workspace Structure

```
research-[topic]/
├── 00-研究问题.md
│   └── 初始问题 + 关键词 + 子问题
├── 01-文献池/
│   ├── 核心文献.md          # 必读，与研究问题直接相关
│   ├── 扩展文献.md          # 选读，间接相关
│   ├── 边缘文献.md          # 参考，可能有用
│   └── 已排除.md            # 读过但不相关
├── 02-主脉络.md
│   └── 研究演进时间线
├── 03-逐文精读/
│   ├── author1-year.md      # 每篇论文一个文件
│   ├── author2-year.md
│   └── ...
├── 04-方法图.md
│   └── 方法演进和比较
├── 05-可比组.md
│   └── 相似研究的对比表
├── 06-缺口分析.md
│   └── 文献缺口 + 研究机会
├── 07-研究设计.md
│   └── 基于调研的初步设计
└── 08-调研日志.md
    └── 每次调研的记录
```

## Step 1: Define Research Question (研究问题)

### Template

```markdown
# 研究问题: [Topic]

## 核心问题
[One clear sentence stating the research question]

## 子问题
1. [Sub-question 1]
2. [Sub-question 2]
3. ...

## 关键词
- 中文: [keyword1], [keyword2], [keyword3]
- 英文: [keyword1], [keyword2], [keyword3]

## 相关概念
| 概念 | 定义 | 相关性 |
|------|------|--------|
| [Concept 1] | [Definition] | 核心 |
| [Concept 2] | [Definition] | 相关 |
| ... | ... | ... |

## 初始假设
- [Preliminary hypothesis 1]
- [Preliminary hypothesis 2]

## 调研目标
- [ ] 明确研究问题的具体边界
- [ ] 识别主要文献流
- [ ] 找到理论基础
- [ ] 确定可行的方法
- [ ] 识别数据来源
```

## Step 2: Build Paper Pool (文献池)

For detailed paper pool management, see `paper-pool.md`. Below is a summary of the workflow.

### Quick Classification

| Category | Criteria | Action |
|----------|----------|--------|
| 核心文献 | Directly addresses the research question | Must read thoroughly |
| 扩展文献 | Related topic, different angle | Read abstract + key sections |
| 边缘文献 | Tangentially related | Skim for relevant parts |
| 已排除 | Read but not relevant | Record reason for exclusion |

### Pool Structure

```
01-文献池/
├── 核心文献.md          # 必读，与研究问题直接相关
├── 扩展文献.md          # 选读，间接相关
├── 边缘文献.md          # 参考，可能有用
└── 已排除.md            # 读过但不相关
```

### Entry Format

For each paper, record:

```markdown
### [Author (Year)]
- **标题**: [Full title]
- **期刊**: [Journal name]
- **主题**: [Main topic]
- **方法**: [Method used]
- **相关性**: [Why relevant to research question]
- **状态**: [未读/已读/精读]
- **笔记**: [Brief notes if read]
```

For detailed entry templates, management rules, and statistics, see `paper-pool.md`.

## Step 3: Map Research Timeline (主脉络)

### Template

```markdown
# 研究脉络: [Topic]

## 时间线

### 起源期 (Year - Year)
- **代表文献**: Author1 (Year), Author2 (Year)
- **核心观点**: [Main idea of this period]
- **方法特征**: [Typical methods]
- **局限**: [What was missing]

### 发展期 (Year - Year)
- **代表文献**: Author3 (Year), Author4 (Year)
- **核心进展**: [What was established]
- **方法演进**: [New methods introduced]
- **争论**: [Key debates]

### 前沿期 (Year - Present)
- **代表文献**: Author5 (Year), Author6 (Year)
- **当前热点**: [Current hot topics]
- **最新方法**: [State-of-art methods]
- **未解决问题**: [Open questions]

## 脉络图

```
[Topic Origin]
    │
    ├──→ [Stream A: Author1 → Author3 → Author5]
    │
    ├──→ [Stream B: Author2 → Author4 → Author6]
    │
    └──→ [Stream C: Author7 → Author8]
```

## 关键转折点
1. **Year**: [What changed and why]
2. **Year**: [What changed and why]
```

## Step 4: Method Map (方法图)

### Template

```markdown
# 方法图: [Topic]

## 方法演进

### 早期方法
| 方法 | 代表文献 | 优点 | 缺点 |
|------|---------|------|------|
| [Method 1] | Author1 (Year) | [Pros] | [Cons] |

### 主流方法
| 方法 | 代表文献 | 优点 | 缺点 |
|------|---------|------|------|
| [Method 2] | Author3 (Year) | [Pros] | [Cons] |

### 前沿方法
| 方法 | 代表文献 | 优点 | 缺点 |
|------|---------|------|------|
| [Method 3] | Author5 (Year) | [Pros] | [Cons] |

## 方法选择指南

### 数据要求
| 方法 | 数据要求 | 适用场景 |
|------|---------|---------|
| [Method 1] | [Requirements] | [When to use] |

### 识别策略
| 方法 | 识别假设 | 检验方法 |
|------|---------|---------|
| [Method 1] | [Assumptions] | [How to test] |
```

## Step 5: Comparable Group (可比组)

### Template

```markdown
# 可比组: [Topic]

## 相似研究对比

| 维度 | Paper A | Paper B | Paper C | 本文计划 |
|------|---------|---------|---------|---------|
| 研究问题 | [Q] | [Q] | [Q] | [Q] |
| 样本 | [Sample] | [Sample] | [Sample] | [Sample] |
| 方法 | [Method] | [Method] | [Method] | [Method] |
| 数据 | [Data] | [Data] | [Data] | [Data] |
| 主发现 | [Finding] | [Finding] | [Finding] | — |
| 期刊 | [Journal] | [Journal] | [Journal] | [Target] |

## 差异化分析
- Paper A 的优势: [Strength]
- Paper B 的局限: [Weakness]
- 本文的机会: [How to differentiate]
```

## Step 6: Gap Analysis (缺口分析)

### Template

```markdown
# 缺口分析: [Topic]

## 文献缺口

### 实证缺口
| 缺口 | 描述 | 机会 | 难度 |
|------|------|------|------|
| [Gap 1] | [Description] | [Opportunity] | [H/M/L] |

### 理论缺口
| 缺口 | 描述 | 机会 | 难度 |
|------|------|------|------|
| [Gap 2] | [Description] | [Opportunity] | [H/M/L] |

### 方法缺口
| 缺口 | 描述 | 机会 | 难度 |
|------|------|------|------|
| [Gap 3] | [Description] | [Opportunity] | [H/M/L] |

## 研究机会排序

| 排名 | 机会 | 新颖性 | 可行性 | 贡献潜力 | 综合评分 |
|------|------|--------|--------|---------|---------|
| 1 | [Opportunity] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | [Score] |
| 2 | [Opportunity] | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | [Score] |
| ... | ... | ... | ... | ... | ... |

## 建议
1. **首选方向**: [Direction] - 理由: [Reason]
2. **备选方向**: [Direction] - 理由: [Reason]
```

## Integration With Other Modules

- **paper-pool.md**: Detailed paper pool management.
- **close-reading.md**: Templates for close reading.
- **topic-revision-advisor.md**: Uses survey results for advice.
- **evidence-citation-workflow.md**: Survey feeds into citation system.
- **research-pipeline.md**: Survey is part of Stage 1-2.
