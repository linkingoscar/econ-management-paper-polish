# v3 Deterministic Audit Contract

Use scripts for checks where exactness matters. The model may interpret findings, but must not silently change the artifact.

## Script-backed Checks

| Check | Script | Minimum output |
|---|---|---|
| Numeric preservation | `check_numeric_consistency.py` | added, missing, and repeated numeric tokens |
| Citation/BibTeX consistency | `check_citations.py` | missing keys, unused keys, malformed DOI/URL |
| LaTeX structure | `audit_latex.py` | missing packages, labels, refs, figures, citations |
| Meaning-risk markers | `meaning_audit.py` | changed causal, identification, strength, uncertainty, and scope markers |
| Method-language safety | `check_method_language.py` | line-level known overclaim patterns and recommendations |
| LaTeX compile guard | `compile_guard.py` | structural status plus isolated compiler status/capability |
| Review issue recall | `check_issue_recall.py` | dropped IDs and silent closures |
| Dynamic style confirmation gate | `validate_style_profile_gate.py` | human record or hash-bound two-pass AI decision |
| AI review adjudication | `build_ai_review_packet.py`, `adjudicate_ai_reviews.py` | fixed risk, exact hash, isolated reviews, complete checks |
| Evidence ledger | `build_evidence_pack.py` | schema and duplicate claim validation |
| Journal card | `validate_journal_card.py` | source URL, status, and required-field validation |
| Skill repository | `validate_v3.py` | required files, frontmatter, links, and schemas |

## Interpretation Rules

- A clean script result means only that the checked invariant passed.
- It does not establish causal identification, citation correctness beyond the checked source, or actual data replication.
- Report skipped checks and unavailable inputs explicitly.
