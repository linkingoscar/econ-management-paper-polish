# Manuscript files and LaTeX editing

Use when the requested writing task involves TeX, bibliography files, conversion,
or an editable manuscript. The skill owns content accuracy; available file tools
handle editing, conversion, compilation and rendering.

## Inspect the existing artifact

Identify the main document, included sections, figures/tables, bibliography backend,
class/engine and any project instructions. Reuse working conventions.
Do not replace a functioning project with generic boilerplate for a prose edit.
For new projects use the host's available document facilities; do not assume
Pandoc, TeX, Word or a particular external skill is installed.

## Preserve scientific and document meaning

- Keep citation keys, labels, macros, equation symbols, units and numeric values.
- Do not translate macro names or variable identifiers while translating prose.
- Keep table/figure notes, sample definitions, model conditions and uncertainty
  attached to the relevant results.
- Retain legitimate precision. Do not round every coefficient to three decimals.
- Use the table's stated significance legend. Different symbol conventions can be valid.
- Match the established or verified target style; booktabs is a common option,
  not a reason to reject every table using horizontal or vertical rules.
- Treat numeric/layout examples as illustrations, never manuscript data.

For result interpretation follow [results-to-text](results-to-text.md);
for bibliography support follow [evidence-citation-workflow](evidence-citation-workflow.md).

## Conversion and delivery

Use available document tools for Word/LaTeX/PDF as requested. Conversion may alter
equations, citations, tracked changes, links or table layout; inspect the result.
Preserve editable sources and source assets. Do not deliver a PDF as if it were
the requested editable Word/TeX manuscript.

For a TeX project, compile with its actual engine/backend when available and
appropriate, then inspect rendered output through [latex-audit](latex-audit.md).
For other formats inspect final pages, tables, equations and bibliography through
the available viewer/rendering tools.

If generation/compilation is unavailable, provide the usable source or text that
can be completed and state the missing capability. Do not claim a file was created,
rendered or checked when it was not.
