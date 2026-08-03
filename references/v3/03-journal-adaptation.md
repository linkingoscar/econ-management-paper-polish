# Journal Adaptation Pack

## Evidence rule

Do not infer a current requirement from memory or an old template. Build a journal
card from the official author page or publisher instructions, record the URL and
checked date, identify article type and stage (`submission`, `revision`,
`accepted-manuscript`, or `production`), and mark claims as `verified`, `inferred`,
`stale`, or `unknown`. Validate it with `scripts/validate_journal_card.py`.

## Adaptation dimensions

- contribution type and expected theory/identification depth;
- abstract, word, table, figure, appendix, and reference constraints;
- Chinese CSSCI, English economics, English management, finance/accounting, or
  field-journal prose conventions;
- submission-stage formatting versus accepted-manuscript production requirements.

Treat outlet-family heuristics as hypotheses until the official source confirms them.
If access is unavailable, state that the adaptation is documented rather than
verified. Never convert a style preference into a mandatory rule.

## Output

Return the journal card, source status, applicability, checked date, and unresolved
unknowns alongside any prose changes. A stale card must trigger re-verification, not
silent reuse.

Legacy sources merged: `journal-families-econ.md`, `journal-families-management.md`,
`journal-style-adaptation.md`, `journal-style-card.md`.
