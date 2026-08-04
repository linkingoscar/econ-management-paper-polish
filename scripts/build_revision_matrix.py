#!/usr/bin/env python3
"""Derive a stable CSV/JSON revision matrix from the review ledger."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from writing_contract import load_json, utc_now, validate_review_ledger, write_json


FIELDS = ["issue_id", "source_id", "category", "severity", "decision", "status", "statement", "proposed_action", "evidence_count", "last_transition"]


def rows(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for issue in ledger.get("issues", []):
        source = issue.get("source") if isinstance(issue.get("source"), dict) else {}
        history = issue.get("history") if isinstance(issue.get("history"), list) else []
        last = history[-1] if history and isinstance(history[-1], dict) else {}
        evidence = issue.get("evidence") if isinstance(issue.get("evidence"), list) else []
        output.append({
            "issue_id": issue.get("issue_id", ""),
            "source_id": source.get("id", ""),
            "category": issue.get("category", ""),
            "severity": issue.get("severity", ""),
            "decision": issue.get("decision", ""),
            "status": issue.get("status", ""),
            "statement": issue.get("statement", ""),
            "proposed_action": issue.get("proposed_action", ""),
            "evidence_count": len(evidence),
            "last_transition": last.get("to", issue.get("status", "")),
        })
    return output


def build(ledger: dict[str, Any], source: Path) -> dict[str, Any]:
    errors = validate_review_ledger(ledger)
    matrix = rows(ledger) if not errors else []
    counts: dict[str, int] = {}
    for row in matrix:
        key = f"{row['status']}:{row['decision']}"
        counts[key] = counts.get(key, 0) + 1
    return {"schema_version": "1.0", "status": "pass" if not errors else "fail", "generated_at": utc_now(), "source_ledger": str(source), "rows": matrix, "counts": counts, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        ledger = load_json(args.ledger)
        report = build(ledger, args.ledger)
        if report["status"] == "pass":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            if args.output.suffix.lower() == ".csv":
                with args.output.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=FIELDS)
                    writer.writeheader()
                    writer.writerows(report["rows"])
            else:
                write_json(args.output, report)
            report["output"] = str(args.output)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        report = {"schema_version": "1.0", "status": "fail", "generated_at": utc_now(), "source_ledger": str(args.ledger), "rows": [], "counts": {}, "errors": [f"cannot build revision matrix: {exc}"]}
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"rows: {len(report.get('rows', []))}")
        for error in report.get("errors", []):
            print(f"- {error}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
