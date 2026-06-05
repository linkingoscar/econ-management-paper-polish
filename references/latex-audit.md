# LaTeX Audit (LaTeX质量审计)

Use this file when reviewing .tex files for quality, consistency, and compliance. This audit catches common LaTeX issues before compilation.

## When To Use

- User provides a .tex file for review.
- User reports compilation errors.
- User asks to check LaTeX formatting.
- Before submission to a journal.

## Audit Checklist

### 1. Document Structure

| Check | Description | Status |
|-------|-------------|--------|
| `\documentclass` | Appropriate class for journal | ☐ |
| Packages | All needed packages loaded | ☐ |
| Preamble | No content before `\begin{document}` | ☐ |
| Title/Author | Properly formatted | ☐ |
| Abstract | Within word limit | ☐ |
| Keywords | Present if required | ☐ |
| JEL codes | Present if required | ☐ |

### 2. Cross-References

| Check | Description | Status |
|-------|-------------|--------|
| Labels defined | Every figure, table, equation has `\label` | ☐ |
| References used | No unused labels | ☐ |
| References correct | `\ref` matches `\label` | ☐ |
| No undefined refs | All `\ref` have corresponding `\label` | ☐ |

**Common issues:**
- `\ref{tab:results}` but label is `\label{tab:result}` (typo)
- Figure referenced but not yet defined
- Unused labels (warnings only)

### 3. Citations

| Check | Description | Status |
|-------|-------------|--------|
| BibTeX file exists | `references.bib` present | ☐ |
| All cited | Every `\cite` has BibTeX entry | ☐ |
| No unused entries | Every BibTeX entry is cited | ☐ |
| Format correct | Author, title, journal, year complete | ☐ |
| DOI included | When available | ☐ |
| Style consistent | Same citation style throughout | ☐ |

**Common issues:**
- Citing `author2024` but BibTeX has `Author2024` (case-sensitive)
- Missing required fields (journal, year)
- Inconsistent author name format

### 4. Tables

| Check | Description | Status |
|-------|-------------|--------|
| Booktabs used | `\toprule`, `\midrule`, `\bottomrule` | ☐ |
| No `\hline` | Avoided horizontal lines | ☐ |
| No vertical lines | `\|` not used in tabular | ☐ |
| Caption above | Table caption before table | ☐ |
| Label below | `\label` after caption | ☐ |
| SE in parentheses | Standard errors formatted correctly | ☐ |
| Stars correct | Significance stars in superscript | ☐ |
| N reported | Sample size included | ☐ |
| R² reported | If applicable | ☐ |
| Notes included | SE explanation and variable definitions | ☐ |

**Common issues:**
- Using `\hline` instead of booktabs
- Vertical lines in table
- Missing significance stars explanation
- Inconsistent decimal places

### 5. Figures

| Check | Description | Status |
|-------|-------------|--------|
| File exists | All `\includegraphics` files present | ☐ |
| Format correct | PDF for vector, PNG for raster | ☐ |
| Resolution | ≥ 300 DPI for print | ☐ |
| Size appropriate | Not too large or small | ☐ |
| Caption below | Figure caption after figure | ☐ |
| Label present | Every figure has label | ☐ |
| Source noted | Data source in caption if needed | ☐ |

### 6. Equations

| Check | Description | Status |
|-------|-------------|--------|
| Math mode correct | All math in `$...$` or `equation` | ☐ |
| Subscripts correct | `Y_{it}` not `Y_it` | ☐ |
| Superscripts correct | `\hat{\beta}` not `\hat beta` | ☐ |
| Numbering | Important equations numbered | ☐ |
| References | Numbered equations referenced | ☐ |
| Alignment | Multi-line equations aligned | ☐ |

### 7. Bibliography

| Check | Description | Status |
|-------|-------------|--------|
| Style file exists | `.bst` file present or built-in | ☐ |
| Compilation | BibTeX runs without errors | ☐ |
| All entries formatted | Consistent style | ☐ |
| No missing fields | Required fields present | ☐ |
| URLs formatted | DOIs as URLs, not raw | ☐ |
| Special characters | Accents properly encoded | ☐ |

## Automated Checks

### Check for Common Errors

```latex
% Check for \hline in tables (should be booktabs)
% Search: \hline
% Fix: Replace with \toprule, \midrule, \bottomrule

% Check for vertical lines in tables
% Search: |l|c|r|
% Fix: Remove | characters

% Check for missing labels
% Search: \begin{table} ... \end{table} without \label
% Fix: Add \label{tab:name}

% Check for undefined references
% Look for: LaTeX Warning: Reference `xxx' on page y undefined
% Fix: Add \label{xxx} or fix typo
```

### Compilation Checklist

1. Run LaTeX: `pdflatex paper.tex`
2. Run BibTeX: `bibtex paper`
3. Run LaTeX twice: `pdflatex paper.tex` (twice)
4. Check for warnings in `.log` file
5. Check for undefined references
6. Check for missing figures

## Output Template

```markdown
## LaTeX审计报告

### 总体评估
- 文档结构: [✅/⚠️/❌]
- 交叉引用: [✅/⚠️/❌]
- 引用管理: [✅/⚠️/❌]
- 表格格式: [✅/⚠️/❌]
- 图片质量: [✅/⚠️/❌]
- 公式排版: [✅/⚠️/❌]
- 参考文献: [✅/⚠️/❌]

### 详细检查

#### 文档结构
| 检查项 | 状态 | 位置 | 问题 |
|--------|------|------|------|
| Document class | ✅ | Line 1 | — |
| Abstract length | ⚠️ | Line 15 | 超过200词 |
| ... | ... | ... | ... |

#### 表格
| 检查项 | 状态 | 位置 | 问题 |
|--------|------|------|------|
| Table 1 | ⚠️ | Line 45 | 使用了\hline |
| Table 2 | ✅ | Line 80 | — |
| ... | ... | ... | ... |

### 问题清单
1. [Critical issue 1]
2. [Major issue 2]
3. [Minor issue 3]

### 修改建议
1. [Specific fix with line number]
2. ...
```

## Common Fixes

### Replace \hline with Booktabs

**Before:**
```latex
\begin{tabular}{|l|c|c|}
\hline
Variable & Coef. & SE \\
\hline
X1 & 0.15 & 0.04 \\
\hline
\end{tabular}
```

**After:**
```latex
\begin{tabular}{lcc}
\toprule
Variable & Coef. & SE \\
\midrule
X1 & 0.15 & 0.04 \\
\bottomrule
\end{tabular}
```

### Fix Undefined References

**Error:** `LaTeX Warning: Reference 'tab:result' on page 5 undefined`

**Fix:** Check if label exists:
- If missing: Add `\label{tab:result}` after `\caption{}`
- If typo: Fix the `\ref{tab:result}` to match actual label

### Fix Missing Packages

**Error:** `! LaTeX Error: Unknown graphics extension: .eps`

**Fix:** Add `\usepackage{epstopdf}` or convert EPS to PDF

## Integration With Other Modules

- **latex-support.md**: General LaTeX guidance.
- **latex-templates.md**: Journal-specific templates.
- **quality-gates.md**: Content quality checks (format-independent).
- **reproducibility-audit.md**: Number and table consistency checks.
