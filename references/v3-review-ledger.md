# v3.1 Review Ledger And Bounded Revision

Use one issue per reviewer request or manuscript risk. Preserve source locator,
statement, category, severity, decision, evidence, protected fields, status, and
history.

Lifecycle:

raised → triaged → safe-fix | author-required | invalid → proposed → applied
→ verified → closed.

The deterministic pre-router may classify obvious presentation items as safe-fix
and methodological, theoretical, evidence, or major items as author-required.
It must not overwrite an explicit decision.

Patch proposals never overwrite the manuscript by default. Before applying a
candidate revision, compare numbers, variables, citation keys, equations, table/
figure labels, and anchors. Meaning-changing, identification, theory, result, and
contribution edits require author confirmation. Failed gates produce a rollback
and retain the issue history.

## Recall gate

At the start and end of every revision cycle, serialize the ledger and run
`scripts/check_issue_recall.py`. The after-ledger must retain every before-ledger
`issue_id`; new issues are allowed, but dropped IDs fail the gate. An issue that
moves from an unresolved status to `verified` or `closed` must contain a history
event recording verification. Changing the status alone is a silent closure and
is blocked. The recall gate checks lifecycle integrity, not whether the author's
substantive response is correct.
