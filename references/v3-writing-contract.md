# v3.1 Writing Contract

Use this contract for any polish, rewrite, journal adaptation, reviewer response,
or full-manuscript writing audit.

## Intake and preservation

Infer discipline, subfield, language, section, method, outlet, task mode, evidence
mode, and confidence. For workspace tasks, persist these using the validated
example in [Intake And Routing](v3/01-intake-routing.md). Record user overrides.

Default protected fields are numbers, units, p-values, sample sizes, variable names,
estimands, equations, citation keys, DOI strings, table/figure labels, claims,
contribution positioning, and limitations. A line polish must preserve them exactly.

## Writing modes

For a short meaning-preserving polish, load intake and style guidance, keep the
route in context, and return revised text first. Run the bounded verifier on the
original and candidate text (temporary text files are sufficient). A workspace,
paper spine, evidence ledger, or multi-Agent panel is not a prerequisite for this
mode. Add source/method checks when the content actually needs them.

Use the full workspace workflow for manuscript-wide audits, tracked reviewer
revisions, or sustained multi-turn work. Add only artifacts relevant to that task;
existing user authorization still governs substantive changes.

* polish: clarity and style only; run protected-token checks.
* diagnose: return paragraph/section risks before proposing prose.
* adapt: analyze supplied target-journal or field corpus, then revise only after
  the style profile passes its copy boundary.
* review: answer a one-off comment directly; use ledger issues for tracked revision.
* revise: propose bounded diffs linked to an issue, claim, or evidence entry.
* audit: run deterministic checks and report the output ceiling.

For section drafting, build prose from supplied notes/results without inventing
missing findings. For translation, use the target language and the translation
checks in [the style pack](v3/02-writing-style.md). No new route enum is needed:
persist as `revise` with the actual operation in the rationale when tracking is
requested. Ordinary drafting, translation, and one-off responses remain lightweight.

## Revision gate order

Run the gates in this order before a candidate patch is accepted:

1. **Protected fields** — compare numbers, units, p-values, sample sizes,
   variables, estimands, equations, citation keys, DOI strings, and table/figure
   labels. A changed token is author-required.
2. **Meaning gate** — compare causal, identification, strength, uncertainty, and
   scope markers with `scripts/meaning_audit.py`. This is a lexical safety screen,
   not a proof of semantic equivalence. A changed marker needs an author rationale.
3. **Method-language gate** — run `scripts/check_method_language.py`. Known
   overclaim patterns fail the screen and need inspection/correction or explicit
   adjudication. Contextual advisories are reported separately and do not block;
   a conditional claim may be warranted by the supplied design.
4. **LaTeX guard** — run `scripts/compile_guard.py`. Structural failures block the
   patch; an unavailable compiler is reported as `Documented`, not as a compile pass.
5. **Issue recall** — compare before/after ledgers with
   `scripts/check_issue_recall.py`; no issue ID may disappear, and a closure needs a
   verification history event.
6. **Author confirmation** — method, theory, identification, result, contribution,
   and meaning changes remain author-required even when all deterministic checks
   pass.

This strict acceptance sequence applies to bounded same-language patches and
tracked revision. A faithful translation changes lexical forms and can defeat
string-based sentence alignment without changing a claim. Inspect those flags
against the source and use the optional `check_numeric_consistency.py --economic-units`
report for covered equivalent quantities. A numeric pass does not clear other
findings or authorize bounded apply. Do not bypass apply protections or label a
failed strict report successful merely to deliver translated prose.

Respect substantive authorization already provided by the user; do not repeatedly
ask to reconfirm it. When the only change is a faithful translation, changed marker
spellings alone do not create a new scholarly authorization requirement.

The bounded verifier never applies a patch. Its report covers protected fields,
local bindings, source-snapshot drift, and lexical meaning. The workspace workflow
adds method-language and applicable LaTeX checks; run issue recall when a reviewer
ledger is involved. Do not report a check as passed merely because a different
script returned `pass`.

The shared protected-field screen recognizes Unicode numeric signs, common
economic quantity scales/units, LaTeX/Pandoc citation keys, common author-year
citations, delimited LaTeX equations, labels/references, and p-value relations.
It does not parse every unit, citation style, macro expansion, or unmarked formula.
The meaning screen counts negation and other risk markers; it cannot establish
semantic equivalence or catch every reassignment of unchanged words.
`pass`, `checks-passed`, and the verifier's compatibility field `verified: true`
refer only to these checks. They are not a scholarly approval. A changed covered
field blocks ordinary apply; explicit substantive authorization remains separate.

## Output contract

Every substantive output should identify:

1. what changed or was diagnosed;
2. which claim, section, issue, or source supports the action;
3. which protected fields were checked;
4. what remains author-required or unknown.

Never turn a text audit into a data/code replication claim.
