# Intake And Routing Pack

## Route first

Infer the route from the supplied request. For a short light polish, keep it in
context and explain only choices that affect the result. Persist a machine-readable
card for a workspace or a task that needs revision tracking.

The source of accepted values is [route-card.schema.json](../../assets/route-card.schema.json);
both the CLI and the Python validator use its enums. This is a valid example:

```json
{
  "schema_version": "1.0",
  "route_id": "ROUTE-example",
  "paper_id": "paper-example",
  "task_mode": "polish",
  "discipline": "information-systems",
  "subfield": "digital platforms",
  "language": "en-US",
  "method": "archival-empirical",
  "target_outlet": null,
  "section": "results",
  "evidence_mode": "metadata",
  "execution": "serial",
  "preservation": "strict",
  "confidence": "medium",
  "rationale": ["The supplied paragraph reports platform-level empirical results."],
  "unresolved": [],
  "user_overrides": [],
  "created_at": "2026-09-07T00:00:00Z"
}
```

Explain non-obvious choices, record user overrides, and do not let later packs
silently reclassify the paper. Use `mixed` for a mixed discipline and record its
components in `subfield` or `rationale`; the discipline field is a single enum value.
Confidence is about routing, not truth of the manuscript.

## Routing hints

- Economics: lead with identification, estimand, economic magnitude, and policy or
  welfare meaning.
- Management/organization: lead with constructs, theory mechanism, boundary
  conditions, hypothesis logic, and managerial/theoretical contribution.
- Finance, accounting, marketing, IS, operations, public management, tourism, and
  innovation: use the closest research paradigm, then follow the explicit detail
  links in [writing style](02-writing-style.md). Load the selected guide rather
  than using a discipline label as a substitute for writing guidance.

## Task mode

- `polish`: meaning fixed; run protected-token checks.
- `revise`: argument order may change; retain claims unless the user authorizes
  substantive changes.
- `diagnose`: method or argument diagnosis; report risks before suggested prose.
- `review`: organize reviewer concerns and responses.
- `adapt`: source-backed journal/style adaptation.
- `audit`: inspect consistency and report the checks' limits.

For evidence augmentation, select the writing task (`revise` or `audit`) and set
`evidence_mode` to the access actually used. Add an evidence ledger when sources
change, and a revision matrix when reviewer actions need tracking.

For section drafting or translation, infer the intended operation without adding
a new user-facing setup step. When a persisted route is actually needed, use
`revise`, the target language, and a rationale describing drafting or translation.
The output-language enum does not imply that a same-language lexical gate can
validate a translation; use the style pack's translation checks.

Legacy sources merged: `intake-and-modes.md`, `discipline-router.md`,
`subfields-economics.md`, `subfields-management.md`.
