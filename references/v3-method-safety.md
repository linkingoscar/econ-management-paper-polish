# v3 Method Safety Layer

Use this file before recommending an estimator, robustness check, or causal wording.

## Required Chain

```text
data structure
→ source of identifying variation
→ estimand
→ assumptions
→ observable diagnostics
→ estimator or design
→ remaining threats
→ reporting requirements
```

A method name alone is not a justification. If the source of variation or estimand is unclear, use association language and ask for the missing design information.

## Red Lines

- Do not call an event-study plot a proof of parallel trends.
- Do not present matching, controls, or fixed effects as automatic cures for endogeneity.
- Do not recommend a staggered-treatment estimator without checking treatment timing, never-treated/not-yet-treated controls, treatment-effect heterogeneity, and the target estimand.
- Do not describe a mechanism as proven when the mediator is post-treatment, endogenous, or only a proxy.
- Do not require one universal balance threshold, bandwidth, pre-trend window, or robustness test without explaining its context.
- Separate descriptive mediation from causal mediation and state the identification assumptions for the latter.
- Keep survey, experiment, qualitative, review, and archival empirical standards distinct.

## Writing gate

Run `scripts/check_method_language.py` on the manuscript before accepting a prose
revision. It is intentionally conservative: it catches known overclaim patterns in
Chinese and English, reports line-level evidence and a recommendation, and never
rewrites the sentence. A flagged sentence is `author-required`; a qualified
sentence should state the diagnostic evidence, estimand, assumptions, and remaining
threats rather than merely swapping in softer adjectives.

## Output

```text
Method diagnosis
- Data structure:
- Claim type:
- Identifying variation:
- Target estimand:
- Key assumptions:
- Diagnostics available:
- Suitable route:
- Unsuitable or insufficient routes:
- Remaining threats:
- Reporting checklist:
- Verified method sources:
```
