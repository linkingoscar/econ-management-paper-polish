# Choose a method from the question and feasible evidence

Use for design advice, not as a prerequisite for describing a method already used.

## Identify the task

Define the target quantity or understanding, unit and population, timing,
data-generating process, available measures and constraints.
For causal work identify treatment/exposure, outcome, counterfactual and assumptions.
For descriptive, predictive, measurement or qualitative work use its own success
criteria rather than searching automatically for a policy shock.

## Consider only designs the material can support

| Evidence available | Candidate reasoning | What still needs justification |
|---|---|---|
| Random assignment | Experiment-based comparison | Assignment execution, attrition/compliance, interference, inference and target effect |
| Treated/comparison units over time | DID/event-study approach | Credible comparison trend, timing/anticipation, heterogeneous effects and aggregation |
| Genuine assignment threshold | RD-type comparison | Continuity/local design, manipulation, bandwidth and relevant target |
| Plausible instrument | Instrument-based identification | Relevance, independence, exclusion and interpretation-specific assumptions |
| Aggregate intervention and donor information | Synthetic control or related design | Donors, pre-period information, alternative shocks and inference |
| Observational covariates/time structure | Regression, adjustment, matching/weighting, sensitivity or descriptive work | Assumptions needed for the claimed interpretation; FE/controls do not automatically supply them |
| Prediction or measurement materials | Validation design | Intended use, ground truth, train/test separation, coverage and error |
| Interviews/cases/process observations | Qualitative analysis | Sampling/access, analytic logic, negative cases and evidentiary trace |

A policy date alone does not establish a natural experiment.
A threshold or instrument cannot be invented to make a method available.
Several routes may be defensible; explain the tradeoff instead of declaring one
estimator mandatory.

## Diagnose the threat before the remedy

- A lag changes timing; it does not by itself solve reverse causality.
- Controls need a role in the intended estimand. Examine post-treatment variables
  and collider risks; do not automatically add or delete variables by label.
- Measurement problems may require validation or a narrower construct claim,
  rather than another regression specification.
- Missingness and selection may change population/comparability; choose a response
  under explicit assumptions, not a universal Heckman or matching prescription.
- Cluster/dependence structure follows sampling, assignment and error processes,
  not a fixed field or a default software setting.
- A method that is fashionable or complex is not necessarily better for the question.

Distinguish a writing repair, a feasible additional analysis and a new study.
Use [method reporting](method-reproducibility.md) for the actual chosen design.
Check current primary literature/documentation before method-specific
recommendations that depend on recent developments.

## Output

State the recommended route, what it can establish, its needed conditions and
the most consequential uncertainty. Include alternatives only when useful.
Do not promise that a list of tests resolves every identification concern.

