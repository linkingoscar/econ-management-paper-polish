#!/usr/bin/env python3
"""Enforce review-issue lifecycle transitions and append an auditable event."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_contract import load_json, utc_now, validate_review_ledger, write_json


ALLOWED = {
    "raised": {"triaged", "invalid", "blocked"},
    "triaged": {"proposed", "invalid", "blocked"},
    "proposed": {"applied", "blocked", "invalid"},
    "applied": {"verified", "blocked"},
    "verified": {"closed", "blocked"},
    "blocked": {"triaged", "proposed"},
    "invalid": set(),
    "closed": set(),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("issue_id")
    parser.add_argument("to_status", choices=sorted(ALLOWED))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--rationale", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    updated = None
    try:
        updated = load_json(args.ledger)
        errors.extend(validate_review_ledger(updated))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read ledger: {exc}")
    if updated is not None and not errors:
        matches = [issue for issue in updated["issues"] if issue.get("issue_id") == args.issue_id]
        if not matches:
            errors.append(f"unknown issue_id: {args.issue_id}")
        else:
            issue = matches[0]
            current = issue.get("status")
            if args.to_status not in ALLOWED.get(current, set()):
                errors.append(f"invalid transition: {current} -> {args.to_status}")
            if not args.actor.strip() or not args.rationale.strip():
                errors.append("actor and rationale are required for every transition")
            if issue.get("decision") == "author-required" and args.to_status in {"applied", "verified", "closed"} and not args.evidence:
                errors.append("author-required issue needs at least one evidence reference before closure stages")
            if not errors:
                at = utc_now()
                issue["status"] = args.to_status
                issue.setdefault("history", []).append({"at": at, "event": "status-transition", "from": current, "to": args.to_status, "actor": args.actor, "rationale": args.rationale, "evidence": args.evidence})
                updated.setdefault("transition_log", []).append({"issue_id": args.issue_id, "at": at, "from": current, "to": args.to_status, "actor": args.actor, "rationale": args.rationale, "evidence": args.evidence})
                updated["generated_at"] = at
                updated["counts"] = {}
                for item in updated["issues"]:
                    key = f"{item.get('status')}:{item.get('decision')}"
                    updated["counts"][key] = updated["counts"].get(key, 0) + 1
                errors.extend(validate_review_ledger(updated))
                if not errors:
                    try:
                        write_json(args.output, updated)
                    except OSError as exc:
                        errors.append(f"cannot write transitioned ledger: {exc}")
    result = {"status": "pass" if updated is not None and not errors else "fail", "output": str(args.output), "errors": errors, "ledger": updated}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
