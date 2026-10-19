# From actual results to accurate prose

Use when drafting or checking results, abstracts, discussions, tables, or a changed
estimate. This module interprets supplied evidence; it does not imply replication.

## Establish the comparison

Read the table/figure and notes before interpreting a coefficient. Find the focal
question, outcome and unit/transformation, treatment/exposure contrast, model,
sample/period, estimator and uncertainty. Keep table/column or file locators.

Distinguish what is absent from what was not done. Ask for a missing unit or
denominator only if it changes interpretation; write the supported parts meanwhile.
If text and table conflict, flag both locations and avoid guessing which is current.

For long work, retain a compact record of key numbers and their meanings:
claim; locator; estimate; uncertainty; outcome/exposure units; comparison; model;
sample; interpretation limit. Do not require a new file for a paragraph.

## Interpret on the reported scale

| Given information | Permitted interpretation |
|---|---|
| Linear level-on-level coefficient | Change in outcome units per exposure unit, conditional on the specification |
| Outcome is a proportion from 0 to 1 | A coefficient of 0.03 is 3 percentage points for a one-unit contrast; not automatically a 3% relative change |
| Outcome is already in percent units | A coefficient of 0.03 is 0.03 percentage points; do not multiply by 100 again |
| Natural-log outcome, level exposure, suitable linear log model | beta × delta is a change in modeled log outcome; 100 × (exp(beta × delta) − 1) transforms that contrast to percent on the multiplicative scale |
| Standardized variables | State which variables were standardized and against which sample/SD; do not assume both |
| Logit/probit or nonlinear interaction | Coefficients are not probability changes; use actual marginal effects or predicted contrasts with their conditions |
| Group/event-time treatment effects | Report the cohort/time target and actual aggregation; do not reinterpret as a single two-period coefficient |
| Structural counterfactual | State the modeled comparison and assumptions; do not call it an observed causal estimate |

A transformed log contrast is not automatically the change in the arithmetic mean
of the outcome; retransformation and distributional assumptions can matter.
Check log base, log(1 + y), zeros, offsets and model family before using a formula.
Relative changes need a relevant supplied baseline. Report any calculation and
its inputs transparently; use a calculator/runtime for nontrivial arithmetic.

When combining an interaction with reported simple slopes or conditional effects,
check the model, coefficient scale, moderator centering and probe values. If these
are available for a linear interaction, compare the slopes with
`b_X + b_XW × W` on that same scale. Do not mistake different scaling or models for
an error. If the reported values cannot be reconciled from the available details,
identify the discrepancy and needed clarification; attribute them as reported or
omit the unresolved derived values from the reusable paragraph. Do not present a
collection of faithfully copied numbers as an internally verified model, or
silently replace reported estimates with your diagnostic calculation.

## Judge uncertainty without overstating it

- Read significance symbols from this table's legend. Thresholds differ across
  software and author settings. A missing legend is an ambiguity, not a universal error.
- Distinguish SE, SD, t/z statistic, p-value and confidence/credible interval.
  Do not reconstruct inferential claims from rounded displays when precision matters.
- A non-significant result does not establish no effect. Discuss the range of
  effects compatible with the reported uncertainty when available.
- Significant in one subgroup and not another does not establish a between-group
  difference. Use an actual comparison and its uncertainty.
- A changed N or coefficient across models is not automatically inconsistent.
  Check samples, missingness, controls, outcomes and estimands before comparing.
- Stability across selected specifications does not eliminate all confounding.
  A mediator regression, interaction, or coefficient attenuation alone does not
  identify a causal mechanism.

## Write the result's role in the argument

Explain what question this result answers, where it appears, what the estimate
means on its scale, how uncertain it is, and what conclusion it supports.
Include only relevant elements; descriptive, theory and qualitative papers do not
need a significance sentence. Report nulls and conflicting specifications when
they affect the answer.

Use causal language only to the extent justified by the design and assumptions.
Neither the name "DID" nor a small p-value is sufficient. Do not automatically
weaken a supported causal interpretation to association either.

Example (synthetic; not manuscript evidence):
Table 3, column 2 estimates beta = 0.03 with 95% CI [−0.01, 0.07] for a binary
exposure in a linear model whose outcome is a 0–1 employment indicator.
A defensible description is a 3-percentage-point estimate with an interval from
−1 to 7 percentage points, not a definitive increase or proof of no effect.
Whether it is a causal estimate depends on the design.

## Check downstream text

For a changed result, inspect its uses in the abstract, introduction, discussion,
conclusion and response letter. Update the affected claims, not every number with
the same variable name. Preserve author notes on unresolved conflicts.

If no actual result is available, draft a labeled plan or prose skeleton and
identify the exact evidence needed. Never supply a "plausible" effect size, invented
standard error, or successful robustness test.
