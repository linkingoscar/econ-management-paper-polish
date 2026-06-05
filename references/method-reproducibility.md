# Method Reproducibility (方法可复现性)

Use this file for detailed method-level reproducibility checks. This is a sub-module of `reproducibility-audit.md`.

## General Method Reporting

### Required Information

| Item | Required | Location | Status |
|------|----------|----------|--------|
| Estimation method | Yes | Section/equation | ☐ |
| Model specification | Yes | Equation | ☐ |
| Fixed effects | Yes | Section/table notes | ☐ |
| Control variables | Yes | Section/table notes | ☐ |
| Standard errors | Yes | Table notes | ☐ |
| Cluster level | If applicable | Table notes | ☐ |
| Weighting | If applicable | Section | ☐ |
| Software | Recommended | Footnote | ☐ |

## Method-Specific Checks

### OLS / Panel FE

| Check | Description | Status |
|-------|-------------|--------|
| Model equation | Full equation with subscripts | ☐ |
| Fixed effects | Entity, time, or both | ☐ |
| Controls | List of control variables | ☐ |
| SE type | Robust, clustered, heteroskedastic | ☐ |
| Cluster level | Firm, industry, state, etc. | ☐ |

**Standard reporting:**
```
Y_it = α + β X_it + γ Z_it + μ_i + λ_t + ε_it

Where μ_i are firm fixed effects, λ_t are year fixed effects.
Standard errors are clustered at the firm level.
```

### Difference-in-Differences (DID)

| Check | Description | Status |
|-------|-------------|--------|
| Treatment definition | What constitutes treatment | ☐ |
| Treatment timing | When treatment occurs | ☐ |
| Control group | Who is in the control group | ☐ |
| Parallel trends | Assumption discussed/tested | ☐ |
| Pre-treatment period | How many pre-treatment periods | ☐ |
| Event study | Pre-trends shown | ☐ |
| Anticipation effects | Addressed or ruled out | ☐ |

**Required specifications:**
```
Y_it = α + β (Post_t × Treat_i) + γ Z_it + μ_i + λ_t + ε_it

Parallel trends test: Event study with leads and lags
```

### Instrumental Variable (IV)

| Check | Description | Status |
|-------|-------------|--------|
| Instrument | What is the instrument | ☐ |
| First stage | First-stage equation reported | ☐ |
| First-stage F | F-statistic reported | ☐ |
| Exclusion restriction | Why instrument is valid | ☐ |
| Overidentification | Test if multiple instruments | ☐ |
| LATE interpretation | Acknowledged if applicable | ☐ |

**Required reporting:**
```
First stage: X_it = α + π Z_it + γ W_it + μ_i + λ_t + ν_it
Second stage: Y_it = α + β X̂_it + γ W_it + μ_i + λ_t + ε_it

First-stage F-statistic: [value]
```

### Regression Discontinuity (RD)

| Check | Description | Status |
|-------|-------------|--------|
| Running variable | What determines treatment | ☐ |
| Cutoff | Where is the cutoff | ☐ |
| Bandwidth | How is bandwidth chosen | ☐ |
| Manipulation test | McCrary density test | ☐ |
| Functional form | Polynomial order | ☐ |
| Robustness | Different bandwidths | ☐ |

**Required reporting:**
```
Y_i = α + β D_i + f(X_i - c) + ε_i

Where D_i = 1[X_i ≥ c], c is the cutoff.
Bandwidth: [value], chosen by [method].
```

### Matching / PSM

| Check | Description | Status |
|-------|-------------|--------|
| Matching variables | What variables are used | ☐ |
| Matching method | Nearest neighbor, caliper, etc. | ☐ |
| Balance tests | SMD reported | ☐ |
| Common support | Overlap discussed | ☐ |
| Sensitivity | Rosenbaum bounds or similar | ☐ |

**Required reporting:**
```
Matching variables: [list]
Method: [nearest neighbor/caliper/kernel]
Caliper: [value if applicable]
Balance: SMD < 0.1 for all covariates
```

### Mediation / Mechanism

| Check | Description | Status |
|-------|-------------|--------|
| Mediator variable | What is the mediator | ☐ |
| Causal steps | Baron-Kenny or similar | ☐ |
| Indirect effect | Sobel test or bootstrap | ☐ |
| Direct effect | After controlling for mediator | ☐ |
| Exclusion restriction | No direct path from IV to DV | ☐ |

**Caution:** Standard mediation analysis has limitations. Acknowledge that mediation does not prove causation of the mechanism.

### Heterogeneity Analysis

| Check | Description | Status |
|-------|-------------|--------|
| Subgroups | How are subgroups defined | ☐ |
| Theoretical motivation | Why these subgroups | ☐ |
| Coefficient comparison | How is difference tested | ☐ |
| Multiple testing | Corrections if many subgroups | ☐ |

## Standard Error Reporting

### Required Information

| SE Type | When to Use | Report As |
|---------|-------------|-----------|
| Robust | Default for cross-section | "Robust standard errors" |
| Clustered | Panel data, grouped data | "Standard errors clustered at [level]" |
| HC2/HC3 | Small samples | "HC3 standard errors" |
| Bootstrapped | Complex statistics | "Bootstrap standard errors (B=1000)" |

### Common Errors

- Reporting "standard errors in parentheses" without type.
- Clustering at wrong level (e.g., individual when treatment varies at state level).
- Not clustering when using clustered treatment.

## Software and Version Reporting

### Recommended Reporting

```
All analyses are conducted in [Stata 17 / R 4.3 / Python 3.11].
[Package/version] is used for [specific method].
Code is available at [repository URL] upon request.
```

## Output Template

```markdown
## 方法可复现性检查

### 总体评估
- 方法描述清晰度: [⭐⭐⭐⭐⭐]
- 参数报告完整性: [⭐⭐⭐⭐⭐]
- 识别策略论证: [强/中/弱]
- 标准误报告: [✅/⚠️/❌]

### 详细检查

#### 模型设定
- 模型类型: [OLS/FE/IV/DID/RD/...]
- 方程: [是否完整报告]
- 固定效应: [是否说明]
- 控制变量: [是否列出]

#### 识别策略
- 识别方法: [描述]
- 关键假设: [是否讨论]
- 稳健性检验: [是否充分]

#### 标准误
- 类型: [Robust/Clustered/...]
- 聚类层级: [Firm/Industry/State/...]
- 报告位置: [Table notes]

### 问题清单
1. [Method issue 1]
2. [Method issue 2]

### 改进建议
1. [Specific recommendation]
2. ...
```

## Integration With Other Modules

- **empirical-method-router.md**: Method selection guidance.
- **method-decision-tree.md**: Decision tree for method choice.
- **quality-gates.md**: Identification And Causal Language Gate.
- **reproducibility-audit.md**: Parent module for overall audit.
