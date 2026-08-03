# Intake And Routing Pack

## Route first

Create a machine-readable card before editing:

```yaml
discipline: economics|management|finance|accounting|marketing|is|other
subfield: specific or unspecified
language: zh-CN|en|bilingual|other
method: theory|archival-empirical|panel|did|iv|rd|survey|experiment|qualitative|review|mixed|unspecified
target_outlet: named outlet, family, or unspecified
section: named section or full-manuscript
task_mode: polish|rewrite|review|method-diagnosis|evidence|revision|pipeline
evidence_mode: supplied-files|web-verified|metadata-only|user-guided|none
causal_claim: true|false|unclear
confidence: high|medium|low
assumptions: []
```

Explain non-obvious choices, record user overrides, and do not let later packs
silently reclassify the paper. Mixed papers may carry multiple discipline or method
labels. Confidence is about routing, not truth of the manuscript.

## Routing hints

- Economics: lead with identification, estimand, economic magnitude, and policy or
  welfare meaning.
- Management/organization: lead with constructs, theory mechanism, boundary
  conditions, hypothesis logic, and managerial/theoretical contribution.
- Finance, accounting, marketing, IS, operations, public management, tourism, and
  innovation: start from the nearest economics or management route, then add the
  field-specific conventions in `02-writing-style.md`.

## Task mode

- `polish`: meaning fixed; run protected-token checks.
- `rewrite`: argument order may change; retain claims unless the user authorizes
  substantive changes.
- `review`/`method-diagnosis`: report risks before suggested prose.
- `evidence`/`revision`: require the evidence ledger and revision matrix.

Legacy sources merged: `intake-and-modes.md`, `discipline-router.md`,
`subfields-economics.md`, `subfields-management.md`.
