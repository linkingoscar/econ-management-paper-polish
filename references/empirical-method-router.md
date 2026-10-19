# Method description, diagnosis, and execution

Use for empirical strategy, method advice, sensitivity, mechanisms or causal claims.
For interpreting actual estimates start with [results-to-text](results-to-text.md).
For choosing a design use [method-decision-tree](method-decision-tree.md).

## Keep three tasks distinct

1. **Describe:** write what the author actually did, using supplied methods/results.
2. **Diagnose:** assess suitability and propose conditional checks or alternatives.
3. **Execute:** run an analysis only when the user requests it and the necessary
   data, tools and authorization are available; inspect actual outputs.

A method recommendation cannot be written as a completed analysis.
A supplied result can be explained without re-running its code; label that scope.
Missing tools do not prevent useful description or diagnosis.

## Understand the empirical object

Identify the research question; causal/descriptive/predictive purpose; outcome and
exposure; unit/time; comparison; data generation and measurement; estimand;
estimator; assumptions and uncertainty.
For a causal claim identify the counterfactual and why the comparison can represent it.
A method name or significant coefficient is not an identification argument.

Do not impose econometric requirements on qualitative, theoretical or review work.
Use [discipline-router](discipline-router.md) to follow those approaches.

## Conditional method concerns

| Actual approach | Concerns that may change interpretation |
|---|---|
| Observational regression / panel | Confounding, measurement, selection, timing, actual controls/FE, dependence and inference; causal interpretation requires a justified identification argument |
| DID / event study | Treatment timing, comparison groups, target effects, parallel-trend assumptions, anticipation, contamination, dynamic/heterogeneous effects and estimator compatibility |
| IV | Instrument relevance and independence, exclusion reasoning, weak identification, target population/effect; monotonicity when needed for the claimed interpretation |
| RD | Assignment rule, running variable, cutoff, continuity assumptions, manipulation, local target, bandwidth/specification and inference |
| Synthetic control | Donor suitability, pre-period fit/information, contamination, concurrent shocks and justified uncertainty |
| Matching / weighting / selection | Assignment/selection assumptions, overlap, balance, target population and sensitivity; neither balance nor matching removes all unobserved confounding |
| Mediation / moderation | Construct and timing, mediator-outcome confounding, chosen estimand, interactions, evidence discriminating mechanisms; see [method reporting](method-reproducibility.md) |
| Text / ML / prediction | Measurement validity, labels, leakage, validation target/splits, error and distribution shift; prediction is not causal identification |

These are diagnostic prompts, not a required battery of tests. Select checks
because they address a concrete threat in this study.

## Methods evidence

Verify sources before adding method citations. Use methodological work for the
estimand and assumptions; official software documentation for implementation.
An applied exemplar may show practice but does not establish validity for this study.
For claims about current estimators or package options, inspect current primary
documentation rather than citing remembered names as authoritative.

## Deliver

For a writing request, provide the method passage supported by known facts, with
local questions where needed. For a diagnosis, explain the main issue, why it
matters, a feasible response and its assumptions. Do not append an unsolicited
method upgrade or fixed robustness checklist to ordinary editing.
