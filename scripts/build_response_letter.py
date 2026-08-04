#!/usr/bin/env python3
"""Derive a response-letter scaffold from the review ledger without inventing replies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_contract import load_json, write_json


def render(ledger: dict) -> str:
    lines = ["# Response to reviewers", "", "<!-- Generated from the issue ledger. Replace bracketed fields with author-confirmed text. -->", ""]
    for issue in ledger.get("issues", []):
        source = issue.get("source", {})
        label = source.get("id") or issue.get("issue_id")
        lines.extend([
            f"## {issue.get('issue_id')}: {label}",
            "",
            f"**Reviewer comment:** {issue.get('statement', '')}",
            "",
            f"**Decision/status:** {issue.get('decision', 'unresolved')} / {issue.get('status', 'raised')}",
            "",
            "**Author response:** [author-confirmed response; do not leave this placeholder in a submission copy]",
            "",
            "**Change made:** [section, page/line, and exact bounded change]",
            "",
            f"**Evidence / verification:** {', '.join(issue.get('evidence', [])) or '[add evidence or verification record]'}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        ledger = load_json(args.ledger)
        text = render(ledger)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        ledger = None
        text = ""
        errors.append(f"cannot build response letter: {exc}")
    result = {"status": "pass" if not errors else "fail", "output": str(args.output), "issues": len(ledger.get("issues", [])) if ledger else 0, "placeholder_policy": "author-confirmation-required", "errors": errors}
    if args.report:
        try:
            write_json(args.report, result)
            result["report"] = str(args.report)
        except OSError as exc:
            errors.append(f"cannot write response-letter report: {exc}")
            result["status"] = "fail"
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"issues: {result['issues']}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
