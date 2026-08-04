# v3.1 Corpus And Style Contract

The corpus exists to describe writing structure, not to create a phrase bank.

## Two phases

1. Scan files into a corpus manifest with path, hash, role, readability, extraction
   level, license status, and use.
2. Generate style cards and aggregate them into a profile. A human confirms the
   profile before it is used for revision.

Every generated profile is `status=draft` and `human_confirmed=false`. Run
`scripts/validate_style_profile_gate.py` after the author has reviewed source
roles, conflicts, stale/unreadable inputs, and the structural-only copy boundary.
Only a profile with `status=confirmed`, `human_confirmed=true`, `confirmed_at`,
and `confirmed_by` can enter a revision route. No script may auto-confirm it.

The target corpus should normally contain 5–8 target-outlet papers, 2–5 field/topic
papers, and 1–3 author or lab exemplars. Treat these as defaults, not hard journal
requirements. A smaller or conflicting corpus remains labelled low-confidence.

## Style boundary

Allowed: section order, rhetorical moves, paragraph-length ranges, citation placement,
method/result narration order, figure-introduction structure, and terminology
observations.

Forbidden: copying sentences, distinctive metaphors, findings, conclusions,
citation paragraphs, or a target author's voice. Every profile carries the field
copy_boundary set to structural-only.

## Priority

P1 preserve > P2 target outlet > P3 field/topic > P4 static project rules > P5 cleanup.

If a style suggestion conflicts with a protected fact, discard the style suggestion.
If a source is unreadable, unauthorized, stale, or metadata-only, downgrade the
profile rather than guessing.

The dynamic profile is a diagnostic range, not a target phrase bank. It can guide
section order, rhetorical moves, paragraph ranges, citation placement, and
method/result narration; it cannot authorize copying a source sentence, finding,
conclusion, or distinctive voice.
