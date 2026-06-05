# Risk Register (风险清单)

Use this file to identify, classify, and track risks to a paper's argument, methodology, evidence, and publication prospects. The risk register is part of the paper spine system.

## When To Use

- Building or diagnosing a paper spine.
- Preparing for reviewer response.
- Doing a full-manuscript audit.
- User asks "这篇文章有哪些风险？" or "审稿人可能会提什么问题？"

## Risk Categories

### 1. Methodological Risks (方法风险)

| Risk | Description | Detection | Mitigation |
|------|-------------|-----------|------------|
| Endogeneity | Omitted variables, reverse causality, selection bias | Check identification strategy | IV, DID, RD, matching, Heckman |
| Weak identification | Instrument is weak or invalid | First-stage F, overid tests | Better instrument, alternative design |
| Measurement error | Proxy does not capture construct | Validation studies, robustness | Alternative measures, measurement model |
| Sample selection | Non-random sample | Compare to population | Heckman, bounds, acknowledge scope |
| Functional form | Wrong specification | RESET test, flexible form | Polynomial, nonparametric |
| Multicollinearity | High correlation among regressors | VIF, condition number | Drop variable, combine, ridge |
| Heteroskedasticity | Non-constant variance | Breusch-Pagan, White | Robust/clustered SE |
| Clustering | Wrong cluster level | Design-based reasoning | Cluster at appropriate level |

### 2. Theoretical Risks (理论风险)

| Risk | Description | Detection | Mitigation |
|------|-------------|-----------|------------|
| Missing mechanism | No clear channel from X to Y | Check if mechanism is tested | Add mechanism test |
| Weak theory | Hypotheses not derived from theory | Check theoretical grounding | Add theory section, cite theory papers |
| Competing explanation | Alternative mechanism not addressed | Brainstorm alternatives | Acknowledge, test, or discuss |
| Over-claiming | Causal language for correlational design | Check language vs. design | Soften language |
| Boundary conditions | When/where effect should not hold | Check scope conditions | Add heterogeneity, acknowledge limits |

### 3. Evidence Risks (证据风险)

| Risk | Description | Detection | Mitigation |
|------|-------------|-----------|------------|
| Unsupported claim | Claim without citation or data | Trace each claim | Add evidence or flag |
| Weak citation | Source does not support claim | Verify citation content | Replace or remove |
| Missing seminal work | Key paper not cited | Literature check | Add citation |
| Outdated evidence | Old data or methods | Check dates, methods | Update or acknowledge |
| Cherry-picking | Only favorable results reported | Check all specifications | Report all, explain selection |

### 4. Presentation Risks (表述风险)

| Risk | Description | Detection | Mitigation |
|------|-------------|-----------|------------|
| Table-text mismatch | Numbers don't match tables | Cross-check all numbers | Correct text or table |
| Inconsistent notation | Variables named differently | Scan for consistency | Standardize |
| Poor structure | Sections don't flow logically | Check section order | Restructure |
| AI-tone | Template-like, generic prose | Check for filler phrases | Rewrite with specifics |
| Translation issues | Awkward phrasing from translation | Read for naturalness | Rewrite in target language |

### 5. Publication Risks (发表风险)

| Risk | Description | Detection | Mitigation |
|------|-------------|-----------|------------|
| Wrong journal fit | Paper doesn't match journal scope | Check aims & scope | Resubmit to better fit |
| Contribution too small | Incremental contribution | Compare to recent papers | Strengthen or pivot |
| Not novel enough | Similar paper exists | Literature search | Differentiate clearly |
| Timing issue | Data or topic is dated | Check recency | Acknowledge or update |
| Formatting issues | Wrong style, length, format | Check author guidelines | Format correctly |

## Risk Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| 🔴 **Critical** | Could lead to rejection or retraction | Must fix before submission |
| 🟠 **High** | Likely to be flagged by reviewers | Should fix; prepare response |
| 🟡 **Medium** | Might be questioned | Prepare explanation or fix |
| 🟢 **Low** | Minor concern | Acknowledge if asked |

## Risk Assessment Output

When diagnosing risks, output:

```markdown
## 风险清单 (Risk Register)

### 汇总
- 🔴 Critical: [N]
- 🟠 High: [N]
- 🟡 Medium: [N]
- 🟢 Low: [N]

### 详细清单

| ID | 类别 | 风险描述 | 严重度 | 当前应对 | 建议改进 |
|----|------|---------|--------|---------|---------|
| R1 | 方法 | 内生性：遗漏变量 | 🔴 | 控制变量 | 需要IV或讨论局限 |
| R2 | 理论 | 机制未检验 | 🟠 | 无 | 添加机制检验 |
| R3 | 证据 | 缺少关键文献 | 🟡 | 无 | 补充Author(Year) |
| ... | ... | ... | ... | ... | ... |

### 优先处理建议
1. [Most critical risk and recommended action]
2. [Second priority]
3. ...
```

## Integration With Other Modules

- **paper-spine.md**: Risks feed into the spine's risk register section.
- **revision-matrix.md**: Reviewer-identified risks become revision items.
- **quality-gates.md**: Gates detect risks automatically during review.
- **topic-revision-advisor.md**: Risk assessment informs revision strategy.

## Common Risk Patterns By Method

### DID Papers

- Parallel trends assumption
- Anticipation effects
- Treatment heterogeneity
- Spillover effects

### IV Papers

- Exclusion restriction
- Weak instrument
- Monotonicity
- LATE interpretation

### Panel FE Papers

- Time-varying omitted variables
- Selection on observables only
- Nickell bias (short T)

### Survey/Experimental Papers

- Social desirability bias
- Hawthorne effect
- External validity
- Attrition
