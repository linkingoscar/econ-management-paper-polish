# v3 Evidence Ledger

Use this file whenever a response adds, replaces, verifies, or relies on an external source.

## Evidence Rules

- A source is not citable merely because its title or abstract looks relevant.
- Each claim receives a stable `CLM-*` identifier.
- Record the source URL, checked date, verification level, exact support location when available, and scope limitations.
- `full_text` and `official_page` can normally support direct citation; `metadata` is cautious background support; `candidate` is not inserted into the manuscript; `rejected` is never cited.
- Journal rules must state whether they apply to initial submission, revision, or accepted-manuscript production.
- If a source is stale or access is limited, downgrade the claim instead of filling the gap from memory.

## Entry Example

```json
{
  "claim_id": "CLM-journal-001",
  "claim": "The current submission instructions require ...",
  "source": {
    "title": "Official author instructions",
    "authors": "Publisher or journal",
    "year": 2026,
    "venue": "Journal",
    "url": "https://example.org/authors"
  },
  "verification": {
    "level": "official_page",
    "checked_at": "2026-08-03",
    "location": "Manuscript preparation > Abstract",
    "support": "Exact rule paraphrase",
    "limitations": "Applies to initial submission only"
  },
  "allowed_use": "direct_citation",
  "tags": ["journal-rule"]
}
```

Use `scripts/build_evidence_pack.py` to validate a ledger before treating it as complete.
