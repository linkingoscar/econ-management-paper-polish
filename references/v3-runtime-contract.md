# v3 Runtime Contract

Use this file for v3.0 tasks. v2 reference modules remain available for backward compatibility, but v3 work should follow the contracts below.

## Execution Order

1. Create a routing card from the user's request and manuscript context.
2. Declare the capability mode and source-access level.
3. Select only the relevant discipline, method, evidence, and section references.
4. Run deterministic scripts before making claims about numbers, citations, or LaTeX.
5. Produce a structured report with findings, evidence, limitations, and unresolved risks.

Do not claim that a check was run when no script, source, or supplied artifact was available.

## Routing Card

```yaml
discipline: economics|management|finance|accounting|marketing|is|other
subfield: [specific subfield or unspecified]
language: zh-CN|en|bilingual|other
method: theory|archival-empirical|survey|experiment|qualitative|review|mixed|unspecified
target_outlet: [journal, family, or unspecified]
section: [section or full-manuscript]
task_mode: polish|rewrite|review|method-diagnosis|evidence-augmentation|revision|pipeline
evidence_mode: supplied-files|web-verified|metadata-only|user-guided|no-external-sources
causal_claim: true|false|unclear
confidence: high|medium|low
assumptions: []
```

The agent must state why each non-obvious route was selected. Users may override the route; record the override and its risk.

## Capability Modes

- **Verified**: the relevant script or source check ran successfully.
- **Documented**: the workflow is supported by references, but no deterministic check ran.
- **Conceptual**: the task needs unavailable infrastructure, data, or a connector.

The final report must distinguish these modes. A manuscript-text audit is not a data or code replication.

## Structured State

When work spans multiple turns, store or return these artifacts when possible:

- `paper-state.json` validated against `assets/paper-state.schema.json`.
- `evidence-pack.json` validated against `assets/evidence-pack.schema.json`.
- `journal-card.json` validated against `assets/journal-card.schema.json`.
- `assets/revision-matrix.md` for reviewer/risk actions and
  `assets/audit-report.md` for capability, checks, and unresolved limitations.

Every revision item should record its reason, evidence, location, status, and unresolved limitation.
