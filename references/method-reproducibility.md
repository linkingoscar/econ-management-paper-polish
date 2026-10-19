# Method reporting and interpretation checks

Use with [reproducibility-audit](reproducibility-audit.md).
A reporting check identifies what is documented; it does not prove an analysis ran.

## Applicable information

For the actual analysis, inspect the estimand/question, procedure, model if used,
sample, variables/transformations, weights, inference method and implementation
details needed to understand or repeat it.
Report controls, fixed effects or clustering when used or relevant; they are not
universal requirements. Record "not reported", "not applicable" and "unverified"
separately from a confirmed methodological error.

## Conditional checks

- **Regression/panel:** equation and text agree; controls/FE and their roles are
  clear; outcome scale, dependence and inference are described. Do not prescribe
  a fixed SE type, cluster level or bootstrap count without the design.
- **DID/event study:** target effects, timing, comparison groups, estimator,
  aggregation, assumptions, anticipation and uncertainty are specified.
  A two-group/two-period Post × Treat equation is one special case, not the required
  form for staggered or multi-period studies. Non-significant pre-trends do not
  prove parallel trends. Absence of an event plot may be a reporting/design
  limitation, not proof that no valid analysis is possible.
  The authors' [did introduction](https://bcallaway11.github.io/did/articles/did-basics.html)
  illustrates group-time effects and aggregation.
- **IV:** record first stage, relevant weak-identification diagnostics, exclusion
  and independence arguments, estimation/inference and the target effect.
  Overidentification tests apply only where identified by the design and cannot
  prove all instruments valid. Do not assume every IV estimand has the same LATE
  interpretation or impose a universal F threshold.
- **RD:** state the rule/cutoff, sharp/fuzzy design, local target, bandwidth,
  functional form and inference. Check sorting/continuity evidence appropriate
  to the running variable; no named density test is mandatory for every design.
- **Matching/weighting:** state target population, covariates and timing, procedure,
  overlap, balance, weighting and inference. A conventional balance threshold
  is not proof of exchangeability or absence of unmeasured confounding.
- **Heterogeneity:** define groups/interaction contrasts and their uncertainty;
  one significant subgroup and one non-significant subgroup do not demonstrate
  a statistically significant difference.

## Mediation and mechanisms

Distinguish a causal indirect/direct effect from a descriptive mediator association.
Inspect construct definitions, treatment–mediator–outcome ordering, the chosen
estimand and its identification assumptions. For common causal mediation
approaches, treatment and mediator ignorability and mediator-outcome confounding
are central; exposure-induced confounders may require different designs/methods.

Randomizing treatment does not automatically randomize the mediator.
A significant indirect-effect estimate, bootstrap interval or coefficient
attenuation does not alone identify a mechanism. Baron–Kenny steps, a Sobel test
and "no direct path from an instrument to the outcome" are not universal mediation
requirements. Instrumental-variable mediation has additional, design-specific
restrictions; do not conflate an exposure with an instrument.

Discuss sensitivity to assumptions and rival explanations where material.
[Imai, Keele and Yamamoto (2010)](https://imai.fas.harvard.edu/research/files/mediation.pdf)
derive mediation identification under a version of sequential ignorability and
examine sensitivity to violations; this is a conditional framework, not a checklist
proving causality in every study.

## Other research approaches

For qualitative work inspect sampling, evidence collection, analysis and interpretive
trace; do not invent coding, saturation or member checking.
For prediction inspect actual evaluation, leakage and deployment population.
For theory/structural work distinguish assumptions, derivation/proof, calibration,
estimation, fit and counterfactuals.

## Output

Locate omissions and conflicts and explain their effect on interpretation or
reproduction. A statement such as "the draft does not specify the cluster level"
is different from "the analysis used the wrong cluster level".
Do not assign reproducibility stars or report successful execution without code
and output evidence.
