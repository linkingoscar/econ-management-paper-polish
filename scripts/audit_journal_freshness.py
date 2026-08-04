#!/usr/bin/env python3
"""Audit journal-card freshness and status before style adaptation."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_journal_card import parse_timestamp, validate
from writing_contract import utc_now, write_json


def audit(card: Any, max_age_days: int) -> dict[str, Any]:
    errors = validate(card, max_age_days=max_age_days)
    warnings: list[str] = []
    findings: list[dict[str, Any]] = []
    claims = card.get("claims", []) if isinstance(card, dict) else []
    stale_statuses = 0
    unknown_statuses = 0
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            continue
        status = claim.get("status")
        finding = {"index": index, "claim": claim.get("claim"), "status": status, "source_url": claim.get("source_url")}
        if status == "stale":
            stale_statuses += 1
            errors.append(f"claims[{index}].status=stale cannot drive dynamic journal adaptation")
            finding["decision"] = "blocked"
        elif status == "unknown":
            unknown_statuses += 1
            errors.append(f"claims[{index}].status=unknown cannot drive dynamic journal adaptation")
            finding["decision"] = "blocked"
        else:
            finding["decision"] = "usable-with-source-check"
        findings.append(finding)
    checked = parse_timestamp(card.get("checked_at")) if isinstance(card, dict) else None
    age_days = None if checked is None else round((datetime.now(timezone.utc) - checked).total_seconds() / 86400, 3)
    if age_days is not None and age_days < -0.01:
        errors.append("checked_at is in the future")
    if not claims:
        warnings.append("journal card contains no claims")
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "generated_at": utc_now(),
        "max_age_days": max_age_days,
        "counts": {"claims": len(claims), "stale_statuses": stale_statuses, "unknown_statuses": unknown_statuses, "age_days": age_days},
        "findings": findings,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path)
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    if args.max_age_days < 0:
        errors.append("--max-age-days must be non-negative")
    try:
        card = json.loads(args.card.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        card = {}
        errors.append(f"cannot read journal card: {exc}")
    report = audit(card, args.max_age_days) if not errors else {"schema_version": "1.0", "status": "fail", "generated_at": utc_now(), "max_age_days": args.max_age_days, "counts": {"claims": 0, "stale_statuses": 0, "unknown_statuses": 0, "age_days": None}, "findings": [], "errors": errors, "warnings": []}
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
        print(f"claims: {report['counts']['claims']}; age_days: {report['counts']['age_days']}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
