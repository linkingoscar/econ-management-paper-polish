# LaTeX Support (LaTeX写作支持)

Use this file when the user provides .tex files or asks for LaTeX-specific writing help. This covers LaTeX conventions for academic papers in economics, management, and business fields.

## When To Use

- User provides a .tex file for review or polish.
- User asks about LaTeX formatting for a specific journal.
- User asks "LaTeX怎么排版三线表？" or similar.
- User needs help with BibTeX management.
- User asks to convert between LaTeX and other formats.

## LaTeX Basics For Academic Writing

### Document Structure

```latex
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}      % 三线表
\usepackage{natbib}         % 参考文献
\usepackage{hyperref}       % 超链接

\title{Paper Title}
\author{Author Name}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
Abstract text...
\end{abstract}

\section{Introduction}
...

\bibliographystyle{apalike}
\bibliography{references}
\end{document}
```

### Common Packages For Econ/Management Papers

| Package | Purpose | Usage |
|---------|---------|-------|
| `booktabs` | Three-line tables | `\toprule`, `\midrule`, `\bottomrule` |
| `natbib` | Citation management | `\citet`, `\citep` |
| `amsmath` | Math equations | `\begin{equation}` |
| `graphicx` | Figures | `\includegraphics` |
| `hyperref` | Clickable links | Auto-loaded |
| `float` | Figure/table positioning | `[H]` option |
| `caption` | Custom captions | `\captionsetup` |
| `subcaption` | Subfigures | `\subfigure` |
| `siunitx` | Number formatting | `\num{1234}` |
| `threeparttable` | Table notes | `\tablenotes` |

## Table Formatting

### Three-Line Table (三线表)

```latex
\begin{table}[htbp]
\centering
\caption{Regression Results}
\label{tab:baseline}
\begin{threeparttable}
\begin{tabular}{lccc}
\toprule
& (1) & (2) & (3) \\
& DV1 & DV2 & DV3 \\
\midrule
Treatment & 0.150*** & 0.120** & 0.180*** \\
          & (0.040)  & (0.050) & (0.035) \\
\addlinespace
Controls  & Yes      & Yes     & Yes     \\
Fixed Effects & Firm & Firm+Year & Industry \\
\midrule
N         & 3,000    & 3,000   & 3,000   \\
R²        & 0.150    & 0.200   & 0.180   \\
\bottomrule
\end{tabular}
\begin{tablenotes}
\small
\item Standard errors in parentheses. * p$<$0.10, ** p$<$0.05, *** p$<$0.01
\end{tablenotes}
\end{threeparttable}
\end{table}
```

### Key Rules

1. Use `booktabs` rules, never `\hline`.
2. No vertical lines.
3. Standard errors in parentheses below coefficients.
4. Significance stars in superscript after coefficient.
5. Notes below the table with SE explanation.

### Regression Table Conventions

| Element | Format | Example |
|---------|--------|---------|
| Coefficient | 3 decimal places | 0.150 |
| Standard error | In parentheses | (0.040) |
| Significance | Superscript stars | 0.150*** |
| N | Integer | 3,000 |
| R² | 3 decimal places | 0.150 |

## Equation Formatting

### Inline Math

```latex
The coefficient $\beta_1$ measures the treatment effect.
```

### Display Equation

```latex
\begin{equation}
Y_{it} = \alpha + \beta_1 X_{it} + \gamma Z_{it} + \mu_i + \lambda_t + \varepsilon_{it}
\label{eq:baseline}
\end{equation}
```

### Aligned Equations

```latex
\begin{align}
Y_{it} &= \alpha + \beta_1 X_{it} + \varepsilon_{it} \label{eq:short} \\
Y_{it} &= \alpha + \beta_1 X_{it} + \gamma Z_{it} + \varepsilon_{it} \label{eq:full}
\end{align}
```

### Conventions

- Use `_` for subscripts: `Y_{it}` not `Y_it`.
- Use `^` for superscripts: `\hat{\beta}` not `\hat beta`.
- Use `\mathbb{E}` for expectation, `\text{Var}` for variance.
- Number only important equations.
- Reference equations by number: Equation~\eqref{eq:baseline}.

## Figure Formatting

### Basic Figure

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{figure1.pdf}
\caption{Treatment Effect Over Time}
\label{fig:event_study}
\end{figure}
```

### Subfigures

```latex
\begin{figure}[htbp]
\centering
\begin{subfigure}{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig_a.pdf}
    \caption{Subfigure A}
    \label{fig:a}
\end{subfigure}
\hfill
\begin{subfigure}{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig_b.pdf}
    \caption{Subfigure B}
    \label{fig:b}
\end{subfigure}
\caption{Main Caption}
\label{fig:main}
\end{figure}
```

### Conventions

- Use PDF for vector graphics (charts, diagrams).
- Use PNG/JPG for photos or screenshots.
- Minimum resolution: 300 DPI for print.
- Caption below the figure.
- Reference as Figure~\ref{fig:event_study}.

## Citation Management

### BibTeX Entry Types

```bibtex
@article{author2024,
    author = {Author, First and Author, Second},
    title = {Article Title},
    journal = {Journal Name},
    year = {2024},
    volume = {1},
    number = {1},
    pages = {1--20},
    doi = {10.1234/example}
}

@book{author2023,
    author = {Author, First},
    title = {Book Title},
    publisher = {Publisher},
    year = {2023},
    address = {City}
}

@incollection{author2022,
    author = {Author, First},
    title = {Chapter Title},
    booktitle = {Book Title},
    editor = {Editor, First},
    pages = {100--120},
    publisher = {Publisher},
    year = {2022}
}

@unpublished{author2021,
    author = {Author, First},
    title = {Working Paper Title},
    note = {Working Paper},
    year = {2021}
}
```

### Citation Commands (natbib)

| Command | Output | Usage |
|---------|--------|-------|
| `\citet{key}` | Author (Year) | Subject of sentence |
| `\citep{key}` | (Author, Year) | Parenthetical |
| `\citep[p.~10]{key}` | (Author, Year, p. 10) | With page |
| `\citep{key1,key2}` | (Author1, Year1; Author2, Year2) | Multiple |
| `\citeauthor{key}` | Author | Name only |
| `\citeyear{key}` | Year | Year only |

## Common LaTeX Issues

### Compilation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Missing package | Add `\usepackage{...}` |
| `Missing $ inserted` | Math mode issue | Check `$...$` or `\(...\)` |
| `Missing }` | Unmatched braces | Check all `{` have `}` |
| `LaTeX Warning: Reference ... undefined` | Missing `\label` or typo | Check label spelling |
| `Overfull \hbox` | Line too long | Rewrite or use `\\` |

### Formatting Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Table floats to wrong position | Float issue | Use `[htbp]` or `[H]` |
| Figure too large | Width setting | Use `width=0.8\textwidth` |
| Inconsistent spacing | Package conflict | Check package order |
| Wrong citation style | BibTeX style | Change `\bibliographystyle` |

## Converting Between Formats

### Word → LaTeX

1. Use Pandoc: `pandoc input.docx -o output.tex`
2. Manual cleanup needed for:
   - Tables (convert to booktabs format)
   - Equations (convert to LaTeX math)
   - Citations (convert to BibTeX)
   - Cross-references (convert to `\ref`)

### LaTeX → Word

1. Use Pandoc: `pandoc input.tex -o output.docx`
2. Or use LaTeX2RTF for basic conversion.
3. Manual cleanup always needed.

### Markdown → LaTeX

1. Use Pandoc: `pandoc input.md -o output.tex`
2. Good for basic structure.
3. Manual refinement for journal-specific formatting.

## Integration With Other Modules

- **latex-templates.md**: Journal-specific LaTeX templates.
- **latex-audit.md**: LaTeX quality checks.
- **section-patterns.md**: Section structure applies to LaTeX too.
- **style-and-polish.md**: Prose rules apply regardless of format.
