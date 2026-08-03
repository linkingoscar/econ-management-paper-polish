# v3 Deterministic Audit Contract

Use scripts for checks where exactness matters. The model may interpret findings, but must not silently change the artifact.

## Script-backed Checks

| Check | Script | Minimum output |
|---|---|---|
| Numeric preservation | `check_numeric_consistency.py` | added, missing, and repeated numeric tokens |
| Citation/BibTeX consistency | `check_citations.py` | missing keys, unused keys, malformed DOI/URL |
| LaTeX structure | `audit_latex.py` | missing packages, labels, refs, figures, citations |
| Evidence ledger | `build_evidence_pack.py` | schema and duplicate claim validation |
| Journal card | `validate_journal_card.py` | source URL, status, and required-field validation |
| Skill repository | `validate_v3.py` | required files, frontmatter, links, and schemas |

## Interpretation Rules

- A clean script result means only that the checked invariant passed.
- It does not establish causal identification, citation correctness beyond the checked source, or actual data replication.
- Report skipped checks and unavailable inputs explicitly.
