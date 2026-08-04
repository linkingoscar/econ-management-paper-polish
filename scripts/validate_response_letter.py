#!/usr/bin/env python3
"""Validate a submission-ready response letter against the review ledger.

The generated response-letter scaffold intentionally contains placeholders. This
validator is the explicit final gate: it requires every ledger issue, closed
status, evidence, and no unresolved bracketed author fields.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from writing_contract import load_json, validate_review_ledger, write_json


PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{2,}\]")


def validate(ledger: Any, text: str, ledger_path: Path, letter_path: Path) -> dict[str, Any]:
    errors = validate_review_ledger(ledger)
    warnings: list[str] = []
    missing: list[str] = []
    unclosed: list[str] = []
    for issue in ledger.get("issues", []) if isinstance(ledger, dict) else []:
        issue_id = issue.get("issue_id")
        if not isinstance(issue_id, str) or not issue_id:
            continue
        if issue_id not in text:
            missing.append(issue_id)
        if issue.get("status") != "closed":
            unclosed.append(issue_id)
        history = issue.get("history") if isinstance(issue.get("history"), list) else []
        historical_evidence = [item for event in history if isinstance(event, dict) for item in (event.get("evidence") or []) if isinstance(item, str) and item.strip()]
        evidence = issue.get("evidence") if isinstance(issue.get("evidence"), list) else []
        if issue.get("status") == "closed" and not evidence and not historical_evidence:
            errors.append(f"{issue_id} is closed without evidence")
    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if missing:
        errors.append("response letter is missing issue IDs: " + ", ".join(missing))
    if unclosed:
        errors.append("ledger issues are not closed: " + ", ".join(unclosed))
    if placeholders:
        errors.append("response letter contains unresolved placeholders: " + ", ".join(placeholders[:10]))
    if "Generated from the issue ledger" in text:
        warnings.append("response letter still contains generated-scaffold marker")
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "ledger": str(ledger_path),
        "letter": str(letter_path),
        "counts": {"issues": len(ledger.get("issues", [])) if isinstance(ledger, dict) else 0, "missing_issue_ids": len(missing), "unclosed_issues": len(unclosed), "placeholders": len(placeholders)},
        "missing_issue_ids": missing,
        "unclosed_issues": unclosed,
        "placeholders": placeholders,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("letter", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        ledger = load_json(args.ledger)
        text = args.letter.read_text(encoding="utf-8")
        report = validate(ledger, text, args.ledger, args.letter)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        report = {"schema_version": "1.0", "status": "fail", "ledger": str(args.ledger), "letter": str(args.letter), "counts": {"issues": 0, "missing_issue_ids": 0, "unclosed_issues": 0, "placeholders": 0}, "errors": [f"cannot validate response letter: {exc}"], "warnings": []}
    if args.output:
        try:
            write_json(args.output, report)
            report["output"] = str(args.output)
        except OSError as exc:
            report["errors"].append(f"cannot write report: {exc}")
            report["status"] = "fail"
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
