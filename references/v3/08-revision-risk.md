# Revision And Risk Pack

## Revision lifecycle

Track one row per reviewer request or manuscript risk: ID, location, issue, action,
evidence/Claim ID, status, and unresolved limitation. Use `open`, `in_progress`,
`blocked`, `verified`, and `closed`. Do not mark a response verified until its text,
source, or deterministic check has been inspected.

The executable issue ledger uses the stricter transitions
`raised → triaged → proposed → applied → verified → closed` (with explicit
`blocked`/`invalid` exits). Use `scripts/transition_issue.py`; do not edit a status
or delete an issue directly. `scripts/apply_bounded_patch.py` and
`scripts/rollback_bounded_patch.py` require separate output paths, source hashes,
and an auditable author confirmation for protected changes. Derive a response-letter
scaffold with `scripts/build_response_letter.py`; bracketed text remains an author
responsibility.

## Risk categories

- methodological: estimand, assumptions, treatment timing, inference, robustness;
- theoretical: construct ambiguity, mechanism leap, missing boundary condition;
- evidence: unsupported claim, stale rule, candidate source presented as fact;
- presentation: number/table/citation mismatch, unclear scope, overcausal wording;
- publication: outlet fit, article type, stage-specific formatting, transparency.

For reviewer responses, quote the request briefly, acknowledge the valid concern,
state the exact change and location, cite new evidence by Claim ID, and state what
remains unresolved. Offer conservative and substantive revision paths separately;
do not imply that a cosmetic change solved an identification threat.

Legacy sources merged: `revision-matrix.md`, `risk-register.md`,
`topic-revision-advisor.md`.
