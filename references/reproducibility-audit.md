# Transparency, consistency, and actual reproduction

Use for requests about transparency, replication materials or reproducibility.
State which of the following scopes the available artifacts support.

| Scope | Material inspected / work performed | Permitted conclusion |
|---|---|---|
| Reporting and internal consistency | Manuscript, table notes, supplied outputs | What is documented, conflicting or missing |
| Code/data inspection | Actual scripts, data documentation and permitted data | What the implementation appears to do; unresolved execution dependencies |
| Computational reproduction | Executed relevant code with permitted data; inspected results against claimed quantities | Which results were or were not reproduced, under what environment and tolerances |

Do not collapse these scopes into a "reproducible" verdict. A script's zero exit
status, matching hash or complete checklist cannot establish semantic correctness.
Do not request all data/code for a task that only needs a reporting audit.

## Proportional audit

1. Identify the central quantities/claims whose verification matters.
2. Locate their data definitions, sample, model, actual output and manuscript uses.
3. Check agreement under comparable conditions.
4. Distinguish error, missing reporting, unavailable evidence and not applicable.
5. Explain consequences and the smallest feasible correction.

Use [data checks](data-reproducibility.md),
[method checks](method-reproducibility.md) and
[results-to-text](results-to-text.md) only for the relevant issues.

Different samples, controls, estimands or outcomes can yield different N, signs and
magnitudes. Compare like with like before reporting inconsistency.
Read stars against the actual table legend; there is no universal symbol scheme.
A correctly stated limitation is not a reporting failure.

## If actual reproduction is requested

Inspect instructions and code before execution; preserve raw data and existing
outputs, use a separate output location, and respect access restrictions.
Resolve feasible dependencies using available tools. If necessary materials are
absent, report the specific blocker and finish the inspection possible.
Compare meaningful target quantities, samples, definitions and uncertainty, allowing
justified numerical tolerance. Record actual execution scope and discrepancies.
Do not silently overwrite a reported result to make it match a run.

## Delivery

Report findings in order of consequence, with artifact/section/table locations,
evidence and suggested action. State which outputs were actually checked or run.
Avoid a simulated quality score, a universal robustness list, or a full-replication
claim from reading the manuscript alone.
