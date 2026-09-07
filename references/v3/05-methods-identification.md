# Methods And Identification Pack

## Required chain

```text
data structure → source of variation → target estimand → assumptions
→ observable diagnostics → estimator/design → remaining threats → reporting
```

If variation or estimand is unclear, diagnose the design and use association
language. A method label is not an identification argument.

Use the supplied model, table, or methods paragraph before asking for more data.
Read [the decision tree](../method-decision-tree.md) when selecting a design and
[the method router](../empirical-method-router.md) for the relevant method family.
Do not request an entire dataset to improve a methods paragraph.

## Match the check to the material

| Material supplied | Useful output | What remains unverified |
|---|---|---|
| Manuscript only | Located reporting gaps, design questions, defensible wording | Estimates, data quality, execution, and unreported diagnostics |
| Tables, equations, or logs | Cross-check estimates, samples, inference, model labels, and reported tests | Unreported steps and calculations not independently rerun |
| Data, code, and a usable runtime | Execute the requested analysis or replication and inspect outputs | Identification assumptions and generalizability do not become proven by execution |

For a routine question, give a short diagnosis, the proposed paragraph or reporting
fix, and only the missing inputs that affect it. Existing information should
answer a question once; do not demand a completed risk card from the user.

## Design gates

- Panel/archival regression: define unit/time effects, clustering, functional form,
  and what variation identifies the coefficient.
- DID/event study: inspect timing, comparison groups, treatment-effect heterogeneity,
  anticipation, and the target estimand. Event-study leads are diagnostics, not a
  proof of parallel trends.
- IV: explain relevance, exclusion, monotonicity where needed, and the local
  estimand; first-stage strength alone is insufficient.
- RD: establish cutoff validity, continuity, bandwidth sensitivity, manipulation
  checks, and the local nature of the effect.
- Matching/controls/Heckman: describe selection assumptions; none is an automatic
  cure for endogeneity.
- Mediation/mechanism: distinguish descriptive decomposition from causal mediation;
  post-treatment or endogenous mediators require stronger assumptions.
- Survey, experiment, qualitative, and review designs use separate quality gates;
  do not force archival-empirical standards onto them.

## Frequent reporting decisions

Use only the applicable row; this is not a checklist to impose on every paper.

| Design | Inspect in the supplied material | Writing decision |
|---|---|---|
| Panel/archival FE | Observation unit, transformations, fixed effects, inference/clustering, identifying variation | Explain what the specification absorbs and what threats remain; do not promise all endogeneity is removed |
| DID/event study | Adoption cohorts, comparison group, target ATT/aggregation, anticipation, support, inference | Describe pre-trends as diagnostics; name the actual estimator rather than replacing every DID with a fashionable method |
| IV/Bartik | First stage, exclusion argument, source of variation, weak-IV inference, target population | Strength is not validity; distinguish share-based and shock-based justification for shift-share designs |
| RD | Cutoff/assignment, sharp or fuzzy design, bandwidth, local sample, manipulation/continuity evidence | Keep the interpretation local and tied to the reported specification |
| Synthetic control | Donor pool, pre-treatment fit, post-treatment contamination, placebo/inference procedure | Explain which comparison supports the result instead of calling fit a proof |
| Logit/probit and interactions | Coefficient versus marginal/discrete effect, evaluation population, uncertainty | Do not translate a raw coefficient or interaction directly into percentage-point changes |
| Survey/CFA/SEM | Construct definitions, item source, measurement model, estimator, reliability versus validity | Report the actual evidence for each claim; fit or reliability alone is not causal identification |
| Group comparisons/multilevel models | Measurement comparability, nesting, level of the construct and effect, group counts | Do not confuse within- and between-group relations; justify cross-group comparisons |
| Experiments | Assignment unit, ITT versus treatment received, attrition, compliance, exclusions, multiple outcomes | Say which population and estimand the reported effect addresses |
| Mediation/moderation | Temporal ordering, mediator confounding, scale, indirect effect/interaction uncertainty | Distinguish descriptive pathways, conditional associations, and causally identified mechanisms |
| Text/ML/DML/CATE | Construct validation, training/test separation, overlap, target estimand, model selection | Separate prediction and measurement from causal estimation; ask for diagnostics actually needed by the chosen method |
| Qualitative/mixed/review/meta-analysis | Case/search selection, coding or extraction, contradictory evidence, integration or synthesis rule | Bound process claims, distinguish synthesis from new identification, and report unresolved evidence |

For measurement comparability, inspect the equality constraints actually tested:
the [lavaan multiple-group guide](https://lavaan.ugent.be/tutorial/groups.html)
distinguishes configural, metric, and scalar invariance. Do not impose a universal
fit cutoff or equate reliability with invariance.
For nonlinear-model reporting, the
[statsmodels marginal-effects reference](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.LogitResults.get_margeff.html)
distinguishes average marginal effects from effects evaluated at specified values.
These implementation references were inspected on 2026-09-07; they do not replace
a design-specific methodological justification.

For shift-share designs, [Borusyak, Hull, and Jaravel's practical guide](https://www.aeaweb.org/articles?id=10.1257/jep.20231370)
distinguishes identification from shocks and identification from shares. State
which argument is being used rather than requiring both sources to be exogenous
or assigning every estimate a simple complier interpretation.

Structural estimation, macro/time-series models, specialized asset-pricing tests,
and fsQCA need their own supplied specification and authoritative method reference.
Route to a focused review of that material; do not claim specialist validation
merely because a broad field label or generic risk card is present.

Report unsuitable routes and unresolved threats, not only a preferred estimator.
Bind method recommendations to verified sources in the evidence ledger.

The executable companion is `assets/method-safety-cards.json` plus
`scripts/build_method_safety_report.py`. It joins each deterministic language
finding to assumptions, diagnostics, remaining threats, reporting requirements,
and rewrite guidance. Known overclaim patterns appear as issues; conditional
claims needing design context appear separately as advisories and do not block
otherwise valid writing. A negated statement may need no finding at all.
Inspect the actual paragraph before deciding that wording needs correction.
A passing regex screen is not proof that the design is identified; changed
numbers, citations, and other protected facts retain their strict patch checks.

Legacy sources merged: `empirical-method-router.md`, `method-decision-tree.md`,
`method-reproducibility.md`, plus `v3-method-safety.md`.
