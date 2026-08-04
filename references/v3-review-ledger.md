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
