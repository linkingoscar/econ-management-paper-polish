# LaTeX And Typesetting Pack

## Safe workflow

Inspect document class, packages, tables, equations, figures, labels, references,
citations, and bibliography paths before changing format. Use journal templates as
examples, not evidence of current author requirements. Record unsupported or
unverified template assumptions in the journal card.

Common structural checks include `booktabs` for rules, `threeparttable` for notes,
`graphicx` for figures, `amsmath` for environments, and the citation package required
by the chosen commands. Check that every `\ref`/`\eqref` has a label, every citation
key exists in the bibliography, and every included figure is present.

Run `scripts/audit_latex.py`; it is a dependency-free structural audit, not a claim
that a TeX engine compiled the paper. If compilation is available, report the engine,
version, command, and log outcome separately.

Legacy sources merged: `latex-support.md`, `latex-templates.md`, `latex-audit.md`.
