#!/usr/bin/env python3
"""Normalize reviewer comments into the v3.1 writing issue ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from writing_contract import ISSUE_DECISIONS, SEVERITIES, utc_now, validate_review_ledger, load_json, write_json


def raw_issues(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("issues"), list):
        return value["issues"]
    raise ValueError("input must be an array or an object with an issues array")


def normalize(value: Any) -> dict[str, Any]:
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_issues(value), start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"issues[{index - 1}] must be an object")
        item = dict(raw)
        item.setdefault("issue_id", f"ISS-{index:03d}")
        item.setdefault("statement", item.get("issue") or item.get("comment") or "")
        item.setdefault("category", "presentation")
        item.setdefault("severity", "moderate")
        item.setdefault("decision", "unresolved")
        item.setdefault("status", "raised")
        item.setdefault("evidence", [])
        item.setdefault("preserve", ["numbers", "variables", "citations"])
        item.setdefault("history", [{"at": utc_now(), "event": "raised"}])
        if item["issue_id"] in seen:
            raise ValueError(f"duplicate issue_id: {item['issue_id']}")
        seen.add(item["issue_id"])
        normalized.append(item)
    ledger = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "issues": normalized,
        "counts": {},
        "gates": {
            "unresolved_issues": True if normalized else False,
            "author_confirmation_required": any(item["decision"] == "author-required" for item in normalized),
        },
    }
    for item in normalized:
        key = f"{item['status']}:{item['decision']}"
        ledger["counts"][key] = ledger["counts"].get(key, 0) + 1
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    ledger = None
    try:
        ledger = normalize(load_json(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"cannot build issue ledger: {exc}")
    if ledger is not None:
        errors.extend(validate_review_ledger(ledger))
    output = None
    if ledger is not None and not errors and args.output:
        try:
            write_json(args.output, ledger)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write issue ledger: {exc}")
    result = {"status": "pass" if ledger is not None and not errors else "fail", "errors": errors, "output": output, "ledger": ledger}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if ledger:
            print(f"issues: {len(ledger['issues'])}")
            print(f"counts: {ledger['counts']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
