#!/usr/bin/env python3
"""Audit evidence-ledger verification dates without changing the ledger.

Freshness is a writing safety gate, not a claim that a source has become false.
Old records are reported as stale so a direct citation cannot silently reuse an
unrechecked source; the ledger remains the fact source and is never mutated.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from writing_contract import utc_now, validate_evidence_ledger, write_json


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def audit(ledger: Any, max_age_days: int) -> dict[str, Any]:
    errors: list[str] = validate_evidence_ledger(ledger)
    warnings: list[str] = []
    findings: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)
    entries = ledger.get("entries") if isinstance(ledger, dict) else None
    if not isinstance(entries, list):
        errors.append("ledger.entries must be an array")
        entries = []
    counts = {"total": len(entries), "fresh": 0, "stale": 0, "future": 0, "invalid_date": 0, "direct_citation_blocked": 0}
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        verification = entry.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{prefix}.verification must be an object")
            continue
        checked_at = verification.get("checked_at")
        parsed = parse_timestamp(checked_at)
        source_id = entry.get("source_id") or entry.get("source", {}).get("source_id")
        claim_id = entry.get("claim_id")
        allowed_use = entry.get("allowed_use", [])
        direct = isinstance(allowed_use, list) and "direct_citation" in allowed_use
        status = verification.get("status")
        finding: dict[str, Any] = {"claim_id": claim_id, "source_id": source_id, "checked_at": checked_at, "verification_status": status, "direct_citation": direct}
        status_blocked = direct and status in {"metadata-only", "candidate", "rejected", "stale"}
        if status_blocked:
            counts["direct_citation_blocked"] += 1
            errors.append(f"{prefix} direct_citation is incompatible with verification.status={status}")
            finding["status"] = "blocked"
            finding["reason"] = f"{status} evidence cannot be directly cited"
        if parsed is None:
            counts["invalid_date"] += 1
            errors.append(f"{prefix}.verification.checked_at is not a valid ISO-8601 timestamp")
            finding.update({"status": "invalid", "reason": "invalid checked_at"})
            findings.append(finding)
            continue
        age_days = (now - parsed).total_seconds() / 86400
        finding["age_days"] = round(age_days, 3)
        if age_days < -0.01:
            counts["future"] += 1
            errors.append(f"{prefix}.verification.checked_at is in the future")
            finding.update({"status": "future", "reason": "future checked_at"})
        elif age_days > max_age_days:
            counts["stale"] += 1
            finding.update({"status": "stale", "reason": f"older than {max_age_days} days"})
            if direct and not status_blocked:
                counts["direct_citation_blocked"] += 1
                errors.append(f"{prefix} direct_citation is stale ({age_days:.1f} days old; limit {max_age_days})")
            else:
                warnings.append(f"{prefix} is stale but not marked for direct citation")
        else:
            counts["fresh"] += 1
            finding.update({"status": "fresh", "reason": "within freshness window"})
        findings.append(finding)
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "generated_at": utc_now(),
        "max_age_days": max_age_days,
        "counts": counts,
        "findings": findings,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    if args.max_age_days < 0:
        errors.append("--max-age-days must be non-negative")
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        ledger = {}
        errors.append(f"cannot read evidence ledger: {exc}")
    report = audit(ledger, args.max_age_days) if not errors else {
        "schema_version": "1.0", "status": "fail", "generated_at": utc_now(), "max_age_days": args.max_age_days,
        "counts": {"total": 0, "fresh": 0, "stale": 0, "future": 0, "invalid_date": 0, "direct_citation_blocked": 0},
        "findings": [], "errors": errors, "warnings": [],
    }
    if errors and report["errors"] != errors:
        report["errors"].extend(errors)
        report["status"] = "fail"
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
        print(f"fresh: {report['counts']['fresh']}; stale: {report['counts']['stale']}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
