# Empirical Method Router

Use this file when polishing or drafting empirical strategy, robustness, endogeneity, mechanisms, heterogeneity, methods justification, or when suggesting advanced/current empirical methods. For method selection, run `method-decision-tree.md` first.

## First Principle

Match method to research question, data structure, identification threat, and target field. Do not recommend a method because it sounds advanced.

Before recommending or rewriting a method section, identify:

- Outcome, treatment/exposure, mediator/moderator, and unit of observation.
- Data structure: cross-section, panel, repeated cross-section, matched data, survey, experiment, event data, network/platform logs, text, geospatial data.
- Source of variation: policy shock, staggered adoption, threshold, instrument, randomized treatment, discontinuity, exposure intensity, timing, network spillover, or observational association.
- Main threat: omitted variables, reverse causality, selection, measurement error, simultaneity, anticipation, spillovers, attrition, weak instruments, bad controls, multiple testing.
- Target outlet and field norms.

## Method Families

### Baseline Panel Or Archival Regression

Use when the design is observational and no credible quasi-experimental variation is claimed.

Writing style:

- Explain fixed effects, controls, clustering, and economic magnitude.
- Use association language unless identification is strong.
- Recommend robustness around alternative measures, samples, fixed effects, clustering, and omitted-variable sensitivity.

### Difference-In-Differences And Event Studies

Use when treatment timing or policy shocks create before/after treated/control variation.

Checks:

- Parallel trends or pre-trends.
- Treatment timing, anticipation, and dynamic effects.
- Staggered adoption issues and appropriate estimators when treatment timing varies.
- Spillovers and treatment contamination.

If suggesting a modern DID estimator, first search current method literature and recent field applications. Do not cite method names without verification.

### Instrumental Variables

Use when an instrument plausibly shifts treatment but not the outcome except through treatment.

Checks:

- Relevance, exclusion restriction, monotonicity if relevant.
- First-stage strength and weak-IV diagnostics.
- Plausible violation channels.
- Whether the estimate is LATE and for whom.

### Regression Discontinuity

Use when treatment assignment changes at a threshold.

Checks:

- Running variable and cutoff.
- Manipulation/sorting.
- Bandwidth choice and sensitivity.
- Covariate balance and local interpretation.

### Synthetic Control And Matrix Completion

Use for aggregate interventions with limited treated units or policy shocks.

Checks:

- Pre-treatment fit.
- Donor pool validity.
- Placebo and permutation tests.
- Whether post-treatment shocks contaminate interpretation.

### Matching, Weighting, And Selection Models

Use for covariate imbalance or sample selection, but do not describe them as solving endogeneity by themselves.

Checks:

- Common support.
- Balance diagnostics.
- Sensitivity to unobservables.
- Selection equation assumptions for Heckman-type models.

### Mediation, Mechanism, And Moderation

Use when theory requires a channel or boundary condition.

Checks:

- Whether the mediator is measured after treatment.
- Whether the mediator is itself endogenous.
- Whether interaction terms are interpreted correctly.
- Whether mechanism evidence is direct or only suggestive.

### Text, ML, And High-Dimensional Methods

Use when variables are constructed from text, images, digital traces, or high-dimensional predictors.

Checks:

- Construct validity and labeling.
- Model training/evaluation leakage.
- Interpretability.
- Out-of-sample validation.
- Whether ML is prediction, measurement, heterogeneity discovery, or causal estimation.

For causal ML or double/debiased machine learning, search and verify method references before citing.

## Source Support For Methods

For method claims, retrieve and cite at least one of:

- A canonical methodology article/book.
- A recent field-journal paper using the method in a similar setting.
- Official software/package documentation for implementation only.

When the task is journal-specific, inspect recent papers in that journal family and summarize the observed method conventions.

## Writing Patterns

Use precise language:

- "We estimate..." for model description.
- "The identifying variation comes from..." when there is a design.
- "This specification absorbs..." for fixed effects.
- "The results are consistent with..." for suggestive evidence.
- "This design mitigates [specific threat]" instead of "solves endogeneity."

Avoid:

- "To overcome all endogeneity problems..."
- "The robustness tests prove..."
- "The mechanism is verified..." without direct channel evidence.
- "Advanced method" as a justification.

## Output For Method Support Tasks

Default output:

1. Method diagnosis: data, variation, threats.
2. Recommended method route.
3. Draft/revised method paragraph.
4. Required checks and robustness tests.
5. Method references in APA, with traceable DOI/URL.
6. Caveats and reviewer-risk notes.
