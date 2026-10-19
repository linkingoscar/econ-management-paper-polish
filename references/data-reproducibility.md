# Data and sample traceability

Use when data definitions, sample construction or transparency affect the claim.
This supplements [reproducibility-audit](reproducibility-audit.md); it does not
establish that the dataset or code was inspected unless that happened.

## Understand what the numbers count

Identify source/version, access and coverage, period, geography, observational
unit, repeated observations and analysis population.
For surveys distinguish sampled, responding and analyzed units and any weights.
For merged data identify keys, unmatched records, duplicate handling and resulting
coverage. Do not infer a match rate or response rate that is not supplied.

## Follow sample construction

Use an existing flow or a short sequence of exclusions when available.
Check whether counts are sequential or overlapping before adding/subtracting them.
Distinguish firms, people, transactions and firm-years.
Different outcomes, missingness, lag requirements, subgroups or specifications
can legitimately give different analysis N.

When differences are unexplained, flag a reporting gap. Do not force every table
to the same N or label explained missingness a computational error.
For confidential/proprietary data, respect access and reporting restrictions and
describe feasible verification within them.

## Construct and variable meaning

Check definitions, source fields, units, currency/base year, transformations,
timing, index/scale construction, aggregation and validation relevant to key claims.
Separate a proxy from the construct. Preserve exact variable names and explain
aliases rather than silently merging different variables.

Winsorization, trimming, imputation and normalization are choices to document if
used, not default treatments to prescribe. Do not introduce a universal 1% cutoff.
Missingness handling can affect interpretation and population; identify its role.

## Deliver

Locate the data/sample issue, show the relevant facts, distinguish documentation
from execution, and give an actionable correction. Preserve unknowns rather than
creating an apparently complete flowchart with invented counts.
