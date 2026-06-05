# LaTeX Templates (LaTeX期刊模板库)

Use this file for journal-specific LaTeX template guidance. This covers major journals in economics, management, finance, and related fields.

## Economics Journals

### Top 5 General Economics

| Journal | Template | Class | Citation | Notes |
|---------|----------|-------|----------|-------|
| AER | `aer.cls` | Custom | `natbib` | Strict formatting |
| Econometrica | `econometrica.cls` | Custom | `natbib` | Math-heavy |
| JPE | Standard `article` | Standard | `natbib` | Simple format |
| QJE | Standard `article` | Standard | `natbib` | OUP style |
| ReStud | `restud.cls` | Custom | `natbib` | Specific margins |

### Applied/Field Economics

| Journal | Template | Citation | Notes |
|---------|----------|----------|-------|
| AEJ:Applied | AER template | `natbib` | Same as AER |
| AEJ:Policy | AER template | `natbib` | Same as AER |
| JOLE | Standard | `natbib` | Labor focus |
| JEEA | Standard | `natbib` | European |
| AEJ:Macro | AER template | `natbib` | Same as AER |
| JDE | Standard | `natbib` | Development |
| JEEM | Standard | `natbib` | Environment |

### Chinese Economics (CSSCI)

| Journal | Format | Notes |
|---------|--------|-------|
| 经济研究 | Word preferred | LaTeX accepted but rare |
| 管理世界 | Word preferred | LaTeX accepted but rare |
| 中国工业经济 | Word preferred | LaTeX accepted |
| 经济学(季刊) | LaTeX accepted | More LaTeX-friendly |
| 世界经济 | Word preferred | LaTeX rare |

**Note**: Most Chinese CSSCI journals prefer Word. LaTeX is more common for English submissions.

## Management Journals

### Top Management

| Journal | Template | Citation | Notes |
|---------|----------|----------|-------|
| AMJ | Standard | APA style | Word preferred |
| AMR | Standard | APA style | Theory focus |
| SMJ | Standard | APA style | Strategy |
| ASQ | Standard | APA style | Org theory |
| OrgSci | Standard | APA style | OB/OT |
| MS | Standard | `natbib` | Operations |
| ISR | Standard | `natbib` | IS |

### Finance

| Journal | Template | Citation | Notes |
|---------|----------|----------|-------|
| JF | `jF.cls` | Custom | Strict format |
| JFE | Standard | `natbib` | Econometrics |
| RFS | Standard | `natbib` | Asset pricing |
| JFQA | Standard | `natbib` | Quantitative |
| JAR | Standard | APA | Accounting |
| TAR | Standard | APA | Accounting |

## Template Usage Guide

### AER Template Example

```latex
\documentclass[12pt]{article}
% AER specific packages
\usepackage{aer}           % AER style
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{natbib}

\begin{document}

\title{Paper Title}
\author{Author Name\thanks{Affiliation. Email: email@university.edu.}}
\date{}
\maketitle

\begin{abstract}
Abstract text (150-200 words)...
\end{abstract}

\newpage
\section{Introduction}
...

\bibliographystyle{aer}
\bibliography{references}
\end{document}
```

### Standard Article Template

```latex
\documentclass[12pt, a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage[margin=1in]{geometry}
\usepackage{natbib}
\usepackage{hyperref}

\title{Paper Title}
\author{Author Name\\ \small{University}}
\date{}

\begin{document}
\maketitle

\begin{abstract}
Abstract text...
\end{abstract}

\textbf{Keywords:} keyword1, keyword2, keyword3

\section{Introduction}
...

\bibliographystyle{apalike}
\bibliography{references}
\end{document}
```

## Journal-Specific Requirements

### AER Requirements

- Max 45 pages (including references)
- Double-spaced, 12pt font
- Abstract ≤ 150 words
- JEL codes required
- Acknowledgments at end

### QJE Requirements

- Max 50 pages
- 12pt font, double-spaced
- Abstract ≤ 200 words
- Footnotes, not endnotes

### Management Journal Requirements

- Varies significantly
- Most accept APA or journal-specific style
- Check author guidelines carefully
- Word often preferred for initial submission

## BibTeX Style Files

### Common Styles

| Style | Usage | Output |
|-------|-------|--------|
| `apalike` | APA-like format | (Author, Year) |
| `natbib` | Flexible | `\citet` and `\citep` |
| `aer` | AER specific | AER format |
| `econometrica` | Econometrica | Specific format |
| `plain` | Basic | Numbered |

### Custom BibTeX Fields

Some journals require custom fields:

```bibtex
@article{key,
    ...
    doi = {10.1234/example},
    issn = {1234-5678},
    publisher = {Publisher Name}
}
```

## Converting Between Templates

### General Process

1. Change `\documentclass`
2. Update packages (add/remove)
3. Adjust citation style
4. Reformat tables if needed
5. Check page limits
6. Update bibliography style

### Common Adjustments

| From | To | Changes Needed |
|------|-----|----------------|
| Standard → AER | Use `aer` class | Bibliography, margins |
| AER → Standard | Remove `aer` | Bibliography style |
| Natbib → APA | Change style | Citation commands |
| APA → Natbib | Change style | Citation commands |

## Integration With Other Modules

- **latex-support.md**: General LaTeX guidance.
- **latex-audit.md**: Template compliance checks.
- **journal-style-card.md**: Journal requirements (non-LaTeX).
- **journal-families-econ.md**: Economics journal families.
- **journal-families-management.md**: Management journal families.
