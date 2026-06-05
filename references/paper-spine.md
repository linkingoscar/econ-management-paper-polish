# Paper Spine: 论点骨架系统

Use this file when the user asks to build, diagnose, or revise the argument structure of a paper. The spine is the backbone of a manuscript — the chain of claims, evidence, and contributions that holds the paper together.

## When To Use

- User asks to diagnose the paper's argument structure before major revision.
- User asks to build a "spine" or "skeleton" before writing.
- User provides a full draft and wants to check if the argument holds.
- Reviewer comments suggest the paper lacks focus or coherence.
- User asks "这篇文章的核心论点是什么？" or similar.

## What Is A Paper Spine

A paper spine is a structured representation of the manuscript's argument chain:

```
研究问题 → 文献缺口 → 理论主张 → 假说推导 → 实证设计 → 结果解读 → 贡献定位
```

Each link must be traceable to specific text, tables, or citations in the manuscript.

## Spine Structure

### 1. Central Claim (核心主张)

One sentence answering: "After reading this paper, the reader should believe that..."

- Must be specific, not generic.
- Must be falsifiable or empirically testable.
- Must connect to a research question.

Example:
- ✅ "Digital financial inclusion reduces rural household poverty by expanding credit access, not by increasing savings."
- ❌ "This paper studies the impact of digital finance on poverty."

### 2. Research Gap (文献缺口)

Identify the specific gap the paper claims to fill:

- **Empirical gap**: no evidence on X, conflicting evidence, limited setting.
- **Theoretical gap**: missing mechanism, untested boundary condition.
- **Methodological gap**: identification problem, measurement issue.

Rules:
- The gap must be meaningful, not trivial.
- The gap must be supported by cited literature.
- Avoid "scholars have not studied X" without search evidence.

### 3. Contribution Chain (贡献链)

Map each contribution to a specific literature stream:

| Contribution | Literature Stream | What This Paper Adds |
|-------------|-------------------|---------------------|
| C1: Empirical finding | [Stream A] | First evidence in [setting] |
| C2: Mechanism | [Stream B] | Tests [specific channel] |
| C3: Method | [Stream C] | Applies [method] to [problem] |

Rules:
- Each contribution must answer: "What do readers know after this paper that they did not know before?"
- Avoid generic contributions like "enriches the literature" or "provides practical implications."
- Contributions should be verifiable against the paper's actual content.

### 4. Hypothesis Chain (假说链)

For each hypothesis H1, H2, ...:

```
H1: [Directional statement]
  ├── Mechanism: [Channel name]
  │   └── Theory source: [Author (Year)]
  ├── Boundary condition: [When/where this should hold]
  ├── Testable implication: [Observable pattern in data]
  └── Empirical test: [Table X, Column Y, Specification Z]
```

Rules:
- Each hypothesis must follow from a stated mechanism.
- Competing mechanisms should be acknowledged.
- Hypotheses should be directional when theory supports direction.

### 5. Evidence Map (证据地图)

Map each major claim to its evidence:

| Claim | Evidence Location | Direction | Magnitude | Confidence |
|-------|------------------|-----------|-----------|------------|
| H1 supported | Table 3, Col 2 | Positive | 0.15*** | High |
| Mechanism A | Table 5, Col 1 | Positive | 0.08** | Medium |
| Robustness | Table A3 | Consistent | Similar | High |

Rules:
- Every claim in the spine must have a traceable evidence location.
- If evidence is missing, mark as `[需补充]`.
- Distinguish statistical significance from economic significance.

### 6. Risk Register (风险清单)

Identify threats to the paper's argument:

| Risk Type | Description | Severity | Mitigation |
|-----------|-------------|----------|------------|
| Endogeneity | Reverse causality concern | High | IV approach |
| Measurement | Proxy validity | Medium | Alternative measure |
| External validity | Limited sample | Medium | Acknowledge scope |
| Literature | Missing seminal work | High | Add citation |

See `risk-register.md` for detailed risk categories.

## Output Format

When building or diagnosing a spine, output:

```markdown
## 论点骨架 (Paper Spine)

### 核心主张
[One sentence]

### 研究问题
[Direct question]

### 文献缺口
- [Gap type]: [Description] (Source: Author Year)

### 贡献链
1. [Contribution] → [Literature stream] → [What's new]
2. ...

### 假说链
H1: [Statement]
  - 机制: [Channel]
  - 理论来源: [Citation]
  - 检验位置: [Table/Column]

### 证据地图
| 主张 | 证据位置 | 方向 | 幅度 | 置信度 |
|------|---------|------|------|--------|
| ... | ... | ... | ... | ... |

### 风险清单
| 风险类型 | 描述 | 严重度 | 应对措施 |
|---------|------|--------|---------|
| ... | ... | ... | ... |
```

## Integration With Other Modules

- **quality-gates.md**: Use spine to run Claim-Evidence Gate and Reviewer-Risk Gate.
- **section-patterns.md**: Ensure each section's structure supports the spine.
- **revision-matrix.md**: Track how revision actions address spine risks.
- **topic-revision-advisor.md**: Use spine diagnosis to recommend revision directions.

## Common Problems

### Weak Spine Symptoms

- Central claim is too broad or generic.
- Hypotheses do not follow from mechanisms.
- Evidence map has gaps (claims without data).
- Contributions are not literature-linked.
- Risk register is empty despite known threats.

### Repair Strategies

1. **Central claim too broad**: Ask "What specific result would surprise a reader in this field?"
2. **Missing mechanism**: Ask "Why would X affect Y? Through what channel?"
3. **Evidence gaps**: Flag `[需补充数据/检验]` and recommend additional tests.
4. **Generic contributions**: Map each claim to a named literature stream and state the increment.
5. **Empty risk register**: Run through the Reviewer-Risk Gate checklist.
