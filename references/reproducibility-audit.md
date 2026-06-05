# Reproducibility Audit (可复现性审计)

Use this file when the user asks to check whether a paper's results are reproducible, or when reviewing a manuscript for transparency and replicability. This audit focuses on what can be verified from the manuscript text alone.

## When To Use

- User asks "这篇论文的实证结果能复现吗？"
- User asks to check data and method transparency.
- User is preparing replication materials.
- Reviewer asks about reproducibility.
- Full-manuscript audit includes reproducibility check.

## Audit Scope

This audit checks what is **reportable from the manuscript text**. It does not run code or access data. For code-level checks, the user must provide scripts.

## Audit Checklist

### Layer 1: Data Transparency (数据透明度)

Check whether the manuscript reports:

| Item | Required | Location | Status |
|------|----------|----------|--------|
| Data source | Yes | Section/footnote | ☐ |
| Time period | Yes | Section/footnote | ☐ |
| Sample size (N) | Yes | Table/section | ☐ |
| Sample construction | Yes | Section | ☐ |
| Exclusion criteria | Yes | Section | ☐ |
| Variable definitions | Yes | Section/table notes | ☐ |
| Variable sources | Recommended | Section/table notes | ☐ |
| Data availability | Recommended | Footnote/section | ☐ |

**Red flags:**
- Sample size varies across tables without explanation.
- Variables described differently in text vs. table notes.
- Data source mentioned only in passing.

### Layer 2: Method Transparency (方法透明度)

Check whether the manuscript reports:

| Item | Required | Location | Status |
|------|----------|----------|--------|
| Model specification | Yes | Section/equation | ☐ |
| Fixed effects | Yes | Section/table notes | ☐ |
| Control variables | Yes | Section/table notes | ☐ |
| Standard error type | Yes | Table notes | ☐ |
| Cluster level | If applicable | Table notes | ☐ |
| Estimation method | Yes | Section | ☐ |
| Software/package | Recommended | Footnote/section | ☐ |

**Red flags:**
- Table notes say "standard errors in parentheses" without specifying type.
- Cluster level not stated for panel data.
- Fixed effects mentioned but not specified which.

### Layer 3: Result Consistency (结果一致性)

Cross-check within the manuscript:

| Check | Description | Status |
|-------|-------------|--------|
| N consistency | Sample size same across tables using same sample | ☐ |
| Coefficient consistency | Same variable has consistent sign/magnitude | ☐ |
| Significance consistency | Stars match p-values if both reported | ☐ |
| Sign match | Text description matches table numbers | ☐ |
| Magnitude match | Economic interpretation matches coefficient | ☐ |

**Common errors:**
- Table says 0.15*** but text says "15%" (confusing coefficient with percentage).
- Table says p<0.01 but shows ** instead of ***.
- Sample is 3,000 in Table 2 but 2,800 in Table 3 without explanation.

### Layer 4: Identification Logic (识别逻辑)

For causal claims, check:

| Item | Required | Status |
|------|----------|--------|
| Identification strategy stated | Yes | ☐ |
| Identifying variation explained | Yes | ☐ |
| Threats acknowledged | Yes | ☐ |
| Robustness checks appropriate | Yes | ☐ |
| Causal language matches design | Yes | ☐ |

**Method-specific checks:**

#### DID (Difference-in-Differences)
- Parallel trends discussed or tested
- Pre-treatment period specified
- Treatment/control groups defined
- Anticipation effects addressed

#### IV (Instrumental Variable)
- Instrument relevance (first-stage F reported)
- Exclusion restriction argued
- Overidentification test if multiple instruments
- LATE interpretation acknowledged

#### RD (Regression Discontinuity)
- Running variable specified
- Bandwidth chosen and justified
- Manipulation test reported
- Functional form sensitivity checked

#### Matching/PSM
- Matching variables listed
- Balance tests reported
- Common support discussed
- Sensitivity to unobserved heterogeneity

### Layer 5: Robustness Completeness (稳健性完整性)

Check whether the manuscript addresses:

| Concern | Required Check | Present? |
|---------|---------------|----------|
| Omitted variables | Additional controls, Oster test, Altonji ratio | ☐ |
| Alternative measures | Different proxy for key variables | ☐ |
| Sample sensitivity | Different sample restrictions | ☐ |
| Functional form | Log, polynomial, nonparametric | ☐ |
| Placebo test | Falsification test | ☐ |
| Timing sensitivity | Different event windows, leads/lags | ☐ |

## Audit Output Format

```markdown
## 可复现性审计报告

### 总体评估
- 数据透明度: [⭐⭐⭐⭐⭐] / [需改进项数]
- 方法透明度: [⭐⭐⭐⭐⭐] / [需改进项数]
- 结果一致性: [通过/有疑问/有错误]
- 识别逻辑: [强/中/弱]
- 稳健性完整性: [完整/部分/不足]

### 详细检查

#### 数据层
| 检查项 | 状态 | 位置 | 备注 |
|--------|------|------|------|
| 数据来源 | ✅ | Section 3.1 | 清晰 |
| 样本量 | ⚠️ | Table 2 vs Table 4 | 不一致，需核实 |
| ... | ... | ... | ... |

#### 方法层
| 检查项 | 状态 | 位置 | 备注 |
|--------|------|------|------|
| 模型设定 | ✅ | Equation (1) | 清晰 |
| 标准误类型 | ❌ | 未说明 | 需补充 |
| ... | ... | ... | ... |

#### 结果一致性
| 检查项 | 状态 | 详情 |
|--------|------|------|
| 系数-文字匹配 | ⚠️ | Table 3: 0.15, 文字说"15%" |
| 显著性星号 | ✅ | 一致 |
| ... | ... | ... |

### 关键风险
1. [Most critical reproducibility risk]
2. [Second priority]

### 改进建议
1. [Specific recommendation with location]
2. ...
```

## Limitations

This audit checks reporting quality, not actual reproducibility. True replication requires:

1. Access to the original data.
2. Original code/programs.
3. Same software version and packages.
4. Same random seeds (if applicable).

If the user provides code or data, use more specific checks.

## Integration With Other Modules

- **quality-gates.md**: Numbers And Tables Gate and Identification Gate overlap with this audit.
- **paper-spine.md**: Evidence map should be consistent with reproducibility findings.
- **revision-matrix.md**: Reproducibility issues become revision items.
- **method-reproducibility.md**: Method-specific detailed checks.
- **data-reproducibility.md**: Data-specific detailed checks.
