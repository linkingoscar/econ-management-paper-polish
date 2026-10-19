# Check the source and rendered manuscript

Use for TeX review, compilation problems, conversion or final file delivery.
Distinguish source inspection, successful compilation, rendered review and
journal compliance. None implies the others.

## Source checks relevant to the change

- Resolve actual main file, includes, figure assets, class and bibliography backend.
- Check citations and cross-references against existing keys/labels.
- An unused bibliography entry or label is not automatically an error.
- Confirm table notes describe the displayed models, units, samples and uncertainty.
- Preserve equations/macros and meaningful precision after editing.
- Check anonymization and file requirements only against the applicable stage/rules.
- Do not enforce booktabs, three decimals, stars, a particular image resolution or
  a universal abstract length without a relevant requirement.

## Compilation

Use an available compiler that matches the project; do not force pdfLaTeX/BibTeX
on a XeLaTeX or biber project. Inspect diagnostics and fix relevant source errors.
Avoid installing a new toolchain merely for a simple text edit.
If compilation is unavailable, leave valid editable work and report it as uncompiled.

## Rendered checks

Inspect the changed pages and context: clipping, table width and footnotes, equation
layout, figures/captions, page breaks, unresolved citations/references and language
glyphs. Verify data-bearing content against source after conversion.
Broaden inspection for structural changes; a local prose edit does not demand
rechecking every untouched page unless a layout dependency warrants it.

A successful process exit proves neither readability nor scientific consistency.
Conversely a source-only review must not claim rendered compliance.
Use [journal-style-card](journal-style-card.md) for requirements and
[results-to-text](results-to-text.md) for numerical meaning.

## Delivery

Provide the requested file and editable sources, plus only material unresolved
issues. Name the artifact/pages inspected and remaining gaps when they affect use.
Do not announce "submission ready" solely because it compiles.
