# Revision Matrix (修订矩阵)

Use this file when tracking revision actions during major revision, reviewer response, or manuscript restructuring. The revision matrix maps each required change to a specific action, evidence, and location.

## When To Use

- User is responding to reviewer comments.
- User is doing a major revision after diagnosis.
- User asks to track what changed between versions.
- User asks "这篇返修改了哪些地方？"

## Matrix Structure

### Standard Revision Matrix

| ID | Source | Concern/Requirement | Action Taken | Evidence Added | New Location | Status |
|----|--------|--------------------|--------------| ---------------|--------------|--------|
| R1 | Reviewer 1 | Weak identification | Added IV approach | Table A5 | Section 4.2 | ✅ Done |
| R2 | Reviewer 2 | Missing mechanism | Added channel test | Table 6 | Section 5.3 | ✅ Done |
| R3 | Editor | Contribution unclear | Rewrote intro | — | Section 1 | ✅ Done |
| R4 | Self | Robustness concern | Added placebo test | Table A8 | Appendix | 🔄 Pending |

### Column Definitions

- **ID**: Unique identifier for each revision item.
- **Source**: Where the concern came from (Reviewer 1/2/3, Editor, Self, Coauthor).
- **Concern/Requirement**: Exact or paraphrased concern from the source.
- **Action Taken**: What was changed in the manuscript.
- **Evidence Added**: New tables, figures, analyses, or citations added.
- **New Location**: Section, table, or page where the change appears.
- **Status**: ✅ Done, 🔄 Pending, ❌ Not Addressed, ⚠️ Partially Addressed.

## Reviewer Response Integration

When building a response letter, each matrix row maps to:

```markdown
**[R1] Reviewer 1, Comment 1:**
> [Original concern quoted or paraphrased]

**Response:** We thank the reviewer for this insightful comment. [Action taken]. Specifically, [evidence added]. This can be found in [new location]. [Explanation of how this addresses the concern].

**Changes in manuscript:**
- Section 4.2: [Description of change]
- Table A5: [New analysis]
```

## Revision Severity Classification

| Severity | Description | Response Strategy |
|----------|-------------|-------------------|
| **Fatal** | Methodology flaw, data error, or core claim unsupported | Must fix; may require new analysis |
| **Major** | Missing mechanism, weak identification, or contribution gap | Should fix with evidence |
| **Minor** | Clarity, presentation, or formatting issues | Fix in revision |
| **Optional** | Nice-to-have improvements | Acknowledge or explain why not addressed |

## Tracking Rules

1. Every reviewer comment gets a matrix row, even if not addressed.
2. If a concern is not addressed, explain why in the response letter.
3. Evidence additions must be traceable to specific table/figure numbers.
4. Status must reflect actual manuscript state, not intent.
5. When a single comment requires multiple actions, use sub-IDs (R1a, R1b, R1c).

## Output Template

When the user provides reviewer comments, output:

```markdown
## 修订矩阵 (Revision Matrix)

### 汇总统计
- 总意见数: [N]
- 已完成: [X]
- 进行中: [Y]
- 未处理: [Z]

### 详细矩阵
[Table as above]

### 优先级排序
1. [Most critical item]
2. [Second priority]
3. ...

### 建议的返修路线
[Ordered list of actions with dependencies]
```

## Common Patterns

### Endogeneity Concern

```
| R1 | R2 | 内生性问题未充分讨论 | 新增工具变量回归 + 讨论局限性 | Table A5 + Section 4.3 | ✅ |
```

### Missing Literature

```
| R2 | R1 | 未引用关键文献 Author (Year) | 添加引用并定位与本文差异 | Section 2.2 + References | ✅ |
```

### Contribution Clarity

```
| R3 | Editor | 贡献定位不清晰 | 重写引言贡献段落，映射到具体文献流 | Section 1, ¶3-5 | ✅ |
```

## Integration With Paper Spine

The revision matrix should be consistent with the paper spine:

- Each revision action should strengthen a spine link.
- Risks identified in the spine should appear in the matrix if reviewers flagged them.
- After revision, re-run the spine diagnosis to check if the argument is now stronger.
