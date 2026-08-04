# v3.1 Writing Contract

Use this contract for any polish, rewrite, journal adaptation, reviewer response,
or full-manuscript writing audit.

## Intake and preservation

Create a routing card with discipline, subfield, language, section, method,
outlet, task mode, evidence mode, and confidence. Record user overrides.

Default protected fields are numbers, units, p-values, sample sizes, variable names,
estimands, equations, citation keys, DOI strings, table/figure labels, claims,
contribution positioning, and limitations. A line polish must preserve them exactly.

## Writing modes

* polish: clarity and style only; run protected-token checks.
* diagnose: return paragraph/section risks before proposing prose.
* adapt: analyze supplied target-journal or field corpus, then revise only after
  the style profile passes its copy boundary.
* review: decompose reviewer requests into ledger issues.
* revise: propose bounded diffs linked to an issue, claim, or evidence entry.
* audit: run deterministic checks and report the output ceiling.

## Revision gate order

Run the gates in this order before a candidate patch is accepted:

1. **Protected fields** — compare numbers, units, p-values, sample sizes,
   variables, estimands, equations, citation keys, DOI strings, and table/figure
   labels. A changed token is author-required.
2. **Meaning gate** — compare causal, identification, strength, uncertainty, and
   scope markers with `scripts/meaning_audit.py`. This is a lexical safety screen,
   not a proof of semantic equivalence. A changed marker needs an author rationale.
3. **Method-language gate** — run `scripts/check_method_language.py` and block
   event-study/parallel-trends, matching/endogeneity, mediation, and observational
   causal overclaims until rewritten or explicitly adjudicated.
4. **LaTeX guard** — run `scripts/compile_guard.py`. Structural failures block the
   patch; an unavailable compiler is reported as `Documented`, not as a compile pass.
5. **Issue recall** — compare before/after ledgers with
   `scripts/check_issue_recall.py`; no issue ID may disappear, and a closure needs a
   verification history event.
6. **Author confirmation** — method, theory, identification, result, contribution,
   and meaning changes remain author-required even when all deterministic checks
   pass.

The bounded verifier never applies a patch. It returns a machine-readable report,
including each gate, the output ceiling, and the unresolved author decision.

## Output contract

Every substantive output should identify:

1. what changed or was diagnosed;
2. which claim, section, issue, or source supports the action;
3. which protected fields were checked;
4. what remains author-required or unknown.

Never turn a text audit into a data/code replication claim.
