# Methods And Identification Pack

## Required chain

```text
data structure → source of variation → target estimand → assumptions
→ observable diagnostics → estimator/design → remaining threats → reporting
```

If variation or estimand is unclear, diagnose the design and use association
language. A method label is not an identification argument.

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

Report unsuitable routes and unresolved threats, not only a preferred estimator.
Bind method recommendations to verified sources in the evidence ledger.

The executable companion is `assets/method-safety-cards.json` plus
`scripts/build_method_safety_report.py`. It joins each deterministic language
finding to assumptions, diagnostics, remaining threats, reporting requirements,
and a conservative rewrite. A finding remains author-required; a passing regex
screen is not proof that the design is identified.

Legacy sources merged: `empirical-method-router.md`, `method-decision-tree.md`,
`method-reproducibility.md`, plus `v3-method-safety.md`.
