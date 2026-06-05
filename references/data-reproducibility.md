# Data Reproducibility (数据可复现性)

Use this file for detailed data-level reproducibility checks. This is a sub-module of `reproducibility-audit.md`.

## Data Source Verification

### Required Information

| Item | Description | Check |
|------|-------------|-------|
| Primary source | Database, survey, administrative records | Is it named? |
| Access method | How was data obtained? | Is it stated? |
| Time period | Start and end dates | Is it specific? |
| Geographic scope | Countries, regions, firms | Is it defined? |
| Unit of observation | Individual, firm, country, transaction | Is it clear? |

### Source-Specific Checks

#### Administrative Data
- Government agency or registry named
- Data access procedure described
- Any restrictions acknowledged

#### Survey Data
- Survey name and year stated
- Sampling design described
- Response rate reported
- Weights used specified

#### Commercial/Proprietary Data
- Provider named
- Coverage described
- Known limitations acknowledged

#### Merged/Combined Data
- Each source listed
- Merge key described
- Match rate reported

## Sample Construction

### Required Documentation

```
原始样本: [N observations]
  - 排除标准1: [Criterion] → 排除 [n] 个观测
  - 排除标准2: [Criterion] → 排除 [n] 个观测
  - ...
最终样本: [N observations]
```

### Checks

| Check | Description | Status |
|-------|-------------|--------|
| Starting sample | Total available observations stated | ☐ |
| Each exclusion | Each exclusion criterion listed | ☐ |
| Exclusion count | Number excluded at each step | ☐ |
| Final sample | Total observations in analysis | ☐ |
| Consistency | Final N matches tables | ☐ |

### Common Problems

- Exclusions described in text but N doesn't add up.
- Different tables use different samples without explanation.
- "After removing outliers" without specifying the rule.

## Variable Construction

### Required Documentation

For each key variable:

| Item | Required | Example |
|------|----------|---------|
| Variable name | Yes | "TFP" |
| Definition | Yes | "Total factor productivity estimated by LP method" |
| Source | Yes | "Compustat, item AT" |
| Construction | Yes | "Revenue/Assets, winsorized at 1%/99%" |
| Time period | Yes | "2000-2020" |
| Missing handling | If applicable | "Dropped if missing" |

### Checks

| Check | Description | Status |
|-------|-------------|--------|
| DV definition | Dependent variable clearly defined | ☐ |
| IV definition | Key independent variable clearly defined | ☐ |
| Control definitions | Control variables defined | ☐ |
| Interaction terms | How interactions are constructed | ☐ |
| Index/scale | How indices are built | ☐ |
| Normalization | Any normalization applied | ☐ |

## Sample Size Consistency

### Cross-Table Check

| Table | N | Sample Description | Consistent? |
|-------|---|-------------------|-------------|
| Table 2 (baseline) | 3,000 | Full sample | — |
| Table 3 (mechanism) | 3,000 | Full sample | ✅ |
| Table 4 (heterogeneity) | 2,800 | Subsample: SOEs | ✅ (if stated) |
| Table 5 (robustness) | 3,000 | Full sample | ✅ |

### Common Inconsistencies

- Baseline N = 3,000 but robustness N = 2,950 without explanation.
- Mechanism test has different N because of additional variable missingness.
- Subsample N doesn't match stated restriction.

## Outlier and Winsorization Treatment

### Required Documentation

| Item | Required | Example |
|------|----------|---------|
| Outlier definition | Yes | "Top and bottom 1%" |
| Treatment method | Yes | "Winsorized" or "Dropped" |
| Variables affected | Yes | "ROA, Size, Leverage" |
| Sensitivity check | Recommended | "Results hold without winsorization" |

## Missing Data Handling

### Required Documentation

| Item | Required | Example |
|------|----------|---------|
| Missing pattern | Recommended | "Listwise deletion" |
| Missing rate | Recommended | "Less than 5% for all variables" |
| Sensitivity | Recommended | "Results hold with multiple imputation" |

## Output Template

```markdown
## 数据可复现性检查

### 数据来源
- 来源: [Database/Survey/Administrative]
- 时间: [Period]
- 范围: [Geographic/Unit]
- 获取方式: [Method]

### 样本构建
| 步骤 | 标准 | 排除数 | 剩余数 |
|------|------|--------|--------|
| 原始 | — | — | [N] |
| 1 | [Criterion] | [n] | [N-n] |
| 2 | [Criterion] | [n] | [N-n] |
| 最终 | — | — | [N] |

### 变量构造
| 变量 | 定义 | 来源 | 构造方法 |
|------|------|------|---------|
| DV | [Definition] | [Source] | [Method] |
| IV | [Definition] | [Source] | [Method] |
| Controls | ... | ... | ... |

### 一致性检查
- 样本量一致性: [✅/⚠️/❌]
- 变量定义一致性: [✅/⚠️/❌]
- 异常值处理: [✅/⚠️/❌]

### 问题清单
1. [Issue 1]
2. [Issue 2]
```
