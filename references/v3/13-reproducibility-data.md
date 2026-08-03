# Data And Reproducibility Pack

## Scope declaration

Separate four levels: manuscript-text consistency, method transparency, code/data
availability, and actual computational replication. A text-only session may complete
the first two partially but must not claim the last two.

## Data provenance

Record source owner, access date, coverage, license/access restriction, download or
query procedure, sample construction, merges, exclusions, missingness, and variable
construction. Survey, commercial, administrative, and merged data need different
disclosure details. If data cannot be shared, provide a reproducible access and
construction description where permitted.

## Method/result transparency

Report unit/time definitions, model equation, estimand, treatment timing, fixed
effects, clustering/inference, transformations, weights, pre-analysis decisions,
robustness rationale, and any software/version assumptions. Cross-check sample sizes,
coefficients, signs, p-values, table labels, and variable names with the scripts.

Use `assets/audit-report.md` to list skipped data/code checks and the ceiling of the
conclusion.

Legacy sources merged: `data-reproducibility.md`, `reproducibility-audit.md`,
`method-reproducibility.md`.
