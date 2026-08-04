#!/usr/bin/env python3
"""Apply a conservative deterministic pre-router to review issues.

The router never overwrites an explicit decision. Semantic adjudication remains
an author/reviewer task; this script only marks obvious low-risk presentation
items as safe-fix and high-risk method/theory/evidence items as author-required.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_contract import load_json, validate_review_ledger, write_json


LOW_RISK_CATEGORIES = {"presentation", "formatting", "cross-reference", "cosmetic"}
HIGH_RISK_CATEGORIES = {"method-safety", "methodological", "theoretical", "evidence", "causal", "identification"}


def route(ledger: dict) -> dict:
    output = json.loads(json.dumps(ledger))
    for issue in output.get("issues", []):
        if issue.get("decision") not in {None, "", "unresolved"}:
            continue
        category = str(issue.get("category", "")).lower()
        severity = str(issue.get("severity", "moderate")).lower()
        if category in HIGH_RISK_CATEGORIES or severity in {"major", "blocking"}:
            issue["decision"] = "author-required"
        elif category in LOW_RISK_CATEGORIES and severity in {"cosmetic", "moderate"}:
            issue["decision"] = "safe-fix"
        else:
            issue["decision"] = "unresolved"
        issue.setdefault("history", []).append({"event": "deterministic-pre-route", "decision": issue["decision"]})
        if issue["status"] == "raised":
            issue["status"] = "triaged"
    output["gates"] = {
        **output.get("gates", {}),
        "unresolved_issues": any(item.get("decision") == "unresolved" for item in output.get("issues", [])),
        "author_confirmation_required": any(item.get("decision") == "author-required" for item in output.get("issues", [])),
    }
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        ledger = load_json(args.ledger)
        errors.extend(validate_review_ledger(ledger))
    except (OSError, json.JSONDecodeError) as exc:
        ledger = None
        errors.append(f"cannot read issue ledger: {exc}")
    routed = route(ledger) if ledger is not None and not errors else None
    if routed is not None:
        errors.extend(validate_review_ledger(routed))
    output = None
    if routed is not None and not errors and args.output:
        try:
            write_json(args.output, routed)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write routed ledger: {exc}")
    result = {"status": "pass" if routed is not None and not errors else "fail", "errors": errors, "output": output, "ledger": routed}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
