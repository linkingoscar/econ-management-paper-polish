# Method Decision Tree

Use this before recommending, rewriting, or "upgrading" empirical methods. Pair with `empirical-method-router.md`.

## Step 1: Identify The Empirical Object

Ask or infer:

- What is the outcome?
- What is the focal treatment/explanatory variable?
- What is the unit of observation?
- What is the time dimension?
- Is the claim causal, associative, predictive, descriptive, or theoretical?
- What is the source of variation?

If the source of variation is unknown, do not write causal identification language.

## Step 2: Classify Data Structure

- Cross-sectional observational data.
- Panel data.
- Repeated cross-sections.
- Policy/event shock data.
- Survey or questionnaire.
- Experiment or field experiment.
- Qualitative/case data.
- Text/image/platform trace data.
- Network/geospatial data.
- Mixed methods.

Data structure constrains method choice. Do not recommend DID without before/after treated/control variation; do not recommend RD without a threshold assignment rule; do not recommend IV without a plausible instrument.

## Step 3: Locate Identification Variation

Choose the best fitting route:

### A. Random Assignment Exists

Route: RCT/field experiment/lab experiment.

Must check: randomization, balance, manipulation, attrition, compliance, external validity.

### B. Policy Or Event Shock Exists

Route: DID, event study, synthetic control, interrupted time series, or policy evaluation.

Must check: treated/control comparability, parallel trends, anticipation, spillovers, staggered timing, treatment intensity, dynamic effects.

### C. Assignment Threshold Exists

Route: RD or fuzzy RD.

Must check: running variable, cutoff, manipulation, bandwidth, local validity, covariate balance.

### D. Plausible Exogenous Instrument Exists

Route: IV/2SLS or related design.

Must check: relevance, exclusion, monotonicity when needed, first-stage strength, weak-IV risk, LATE interpretation.

### E. Aggregate Treated Unit With Donor Pool Exists

Route: synthetic control, generalized synthetic control, matrix completion.

Must check: pre-treatment fit, donor validity, placebo tests, post-treatment shocks.

### F. No Clear Exogenous Variation

Route: panel FE, controls, matching/weighting, sensitivity analysis, prediction/measurement design, or descriptive association.

Must check: do not use causal language; emphasize robustness and limitations.

## Step 4: Diagnose Main Threat

Map threat to response:

- Omitted variables -> fixed effects, controls, design-based variation, sensitivity analysis, Oster-type bounds if appropriate and verified.
- Reverse causality -> timing, lag structure, IV, policy shock, event design.
- Selection -> matching/weighting, Heckman-type models, design restrictions, sensitivity checks.
- Measurement error -> alternative proxies, validation, IV if suitable, manual validation, database documentation.
- Bad controls -> remove post-treatment controls; explain control logic.
- Spillovers -> redefine treatment/control, spatial/network checks, exposure models.
- Staggered treatment bias -> modern DID estimators, cohort/event-time analysis, robust aggregation.
- Multiple testing -> pre-specified hypotheses, correction, theory-driven grouping.
- Common-method bias -> design remedies, temporal separation, multiple sources, reliability/validity tests.

Do not say a method "solves" a threat unless assumptions are credible and stated.

## Step 5: Field And Journal Fit

Check whether the recommended method is acceptable and expected in the target field:

- Economics/finance/accounting: identification credibility and robustness usually dominate.
- Management/strategy/OB: theory alignment, construct validity, and identification all matter.
- Marketing/IS: method expectations depend on behavioral, quantitative, platform, or design-science route.
- Chinese CSSCI: method explanation must be clear, but top journals increasingly expect credible identification and robustness.

For target-journal claims, use `journal-style-card.md`.

## Step 6: Method Support References

Before citing method references:

- Verify canonical method source or recent field application.
- Use `evidence-grading.md` to grade confidence.
- Use APA by default.

If only implementation is discussed, software/package documentation is acceptable but not enough for methodological justification.

## Decision Output Template

```text
Method diagnosis
- Data structure:
- Claim type:
- Source of variation:
- Main threat:
- Suitable route:
- Unsuitable routes:
- Required checks:
- Suggested wording:
- Method references:
- Reviewer risks:
```

## Red-Line Conditions

Do not recommend:

- DID without treated/control and pre/post structure.
- RD without a real cutoff.
- IV without exclusion logic.
- PSM as a cure for endogeneity.
- Mediation as proof of mechanism when mediator timing and confounding are unresolved.
- DML/causal forest merely because the paper uses many controls.
- Text/ML constructs without validation.

