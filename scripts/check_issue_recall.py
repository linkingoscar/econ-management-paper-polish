#!/usr/bin/env python3
"""Ensure a revision ledger does not silently drop or close review issues."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from writing_contract import load_json, validate_review_ledger


def has_verification_event(issue: dict[str, Any]) -> bool:
    history = issue.get("history", [])
    if not isinstance(history, list):
        return False
    for event in history:
        if not isinstance(event, dict):
            continue
        status = str(event.get("status", "")).lower()
        event_name = str(event.get("event", "")).lower()
        if status in {"verified", "closed"} or "verif" in event_name or event_name == "closed-after-verification":
            return True
    return False


def check(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_issues = {issue["issue_id"]: issue for issue in before["issues"]}
    after_issues = {issue["issue_id"]: issue for issue in after["issues"]}
    missing = sorted(set(before_issues) - set(after_issues))
    silently_closed: list[str] = []
    for issue_id, old_issue in before_issues.items():
        new_issue = after_issues.get(issue_id)
        if not new_issue:
            continue
        old_status = old_issue.get("status")
        new_status = new_issue.get("status")
        if old_status not in {"verified", "closed"} and new_status in {"verified", "closed"} and not has_verification_event(new_issue):
            silently_closed.append(issue_id)
    errors = [f"issue was dropped: {issue_id}" for issue_id in missing]
    errors.extend(f"issue was closed without a verification history event: {issue_id}" for issue_id in silently_closed)
    return {
        "schema_version": "1.0",
        "status": "fail" if errors else "pass",
        "decision": "author-required" if errors else "safe-fix",
        "before_issue_ids": sorted(before_issues),
        "after_issue_ids": sorted(after_issues),
        "missing_issue_ids": missing,
        "silently_closed": silently_closed,
        "errors": errors,
        "scope": "issue-id recall and explicit verification-history gate; it does not judge substantive resolution",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="Ledger before a revision cycle")
    parser.add_argument("after", type=Path, help="Ledger after a revision cycle")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        before = load_json(args.before)
        after = load_json(args.after)
        errors.extend(f"before: {error}" for error in validate_review_ledger(before))
        errors.extend(f"after: {error}" for error in validate_review_ledger(after))
    except (OSError, json.JSONDecodeError) as exc:
        before = after = None
        errors.append(f"cannot read ledger: {exc}")
    if errors:
        result = {"schema_version": "1.0", "status": "fail", "decision": "author-required", "errors": errors}
    else:
        result = check(before, after)
        result["before_file"] = str(args.before)
        result["after_file"] = str(args.after)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in result.get("errors", []):
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
