# v3 Runtime Contract

Use this file for audits and tracked v3 workflows. Ordinary polish, translation,
drafting, and one-off reviewer replies follow the lightweight route in SKILL.md
and the writing/style packs. The structured reporting below is not a prerequisite
for returning a revised paragraph.

## Execution Order

1. Infer the route from the user's request and manuscript context; persist a card when the task needs a workspace or tracking.
2. Declare the capability mode and source-access level.
3. Select only the relevant discipline, method, evidence, and section references.
4. Run deterministic scripts before making claims about numbers, citations, or LaTeX.
5. Produce a structured report with findings, evidence, limitations, and unresolved risks.

Do not claim that a check was run when no script, source, or supplied artifact was available.

## Routing Card

Use the validated example and task mapping in
[Intake And Routing](v3/01-intake-routing.md). The enum source is
[route-card.schema.json](../assets/route-card.schema.json), shared by the CLI and
validator. Do not use display labels such as `rewrite`, `is`, or `en` as persisted
enum values; use `revise`, `information-systems`, and `en-US` respectively.

The agent must state why each non-obvious route was selected. Users may override the route; record the override and its risk.

## Capability Modes

- **Verified**: the relevant script or source check ran successfully.
- **Documented**: the workflow is supported by references, but no deterministic check ran.
- **Conceptual**: the task needs unavailable infrastructure, data, or a connector.

The final report must distinguish these modes. A manuscript-text audit is not a data or code replication.
`Verified` means the named check ran, not that every scholarly claim is correct.
For protected-field checks, `pass`/`checks-passed` means no covered violation was
detected; keep semantic and source-support review separate.

## Structured State

When work spans multiple turns, store or return these artifacts when possible:

- `paper-state.json` validated against `assets/paper-state.schema.json`.
- `evidence-pack.json` validated against `assets/evidence-pack.schema.json`.
- `journal-card.json` validated against `assets/journal-card.schema.json`.
- `assets/revision-matrix.md` for reviewer/risk actions and
  `assets/audit-report.md` for capability, checks, and unresolved limitations.

Every revision item should record its reason, evidence, location, status, and unresolved limitation.
