#!/usr/bin/env python3
"""Validate a journal-card JSON file and optionally flag stale verification."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUSES = {"verified", "inferred", "stale", "unknown"}


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


def validate(card: Any, max_age_days: int | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(card, dict):
        return ["journal card must be a JSON object"]
    if card.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if not isinstance(card.get("target_outlet"), str) or not card["target_outlet"].strip():
        errors.append("target_outlet must be a non-empty string")
    if not isinstance(card.get("verification_basis"), str) or not card["verification_basis"].strip():
        errors.append("verification_basis must be a non-empty string")
    checked_at = parse_timestamp(card.get("checked_at"))
    if checked_at is None:
        errors.append("checked_at must be an ISO-8601 date or timestamp")
    elif max_age_days is not None:
        age_days = (datetime.now(timezone.utc) - checked_at).total_seconds() / 86400
        if age_days > max_age_days:
            errors.append(f"journal card is stale ({age_days:.1f} days old; limit {max_age_days})")
    claims = card.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        return errors
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("claim", "value"):
            if not isinstance(claim.get(key), str) or not claim[key].strip():
                errors.append(f"{prefix}.{key} must be a non-empty string")
        if not isinstance(claim.get("source_url"), str) or not re.match(r"^https?://", claim["source_url"]):
            errors.append(f"{prefix}.source_url must start with http:// or https://")
        if claim.get("status") not in STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(STATUSES)}")
        if not isinstance(claim.get("applies_to"), str) or not claim["applies_to"].strip():
            errors.append(f"{prefix}.applies_to must identify the manuscript/article type")
        if claim.get("stage") not in {"submission", "revision", "accepted-manuscript", "production", "all", "unknown"}:
            errors.append(f"{prefix}.stage must identify the applicable submission stage")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path)
    parser.add_argument("--max-age-days", type=int, default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        with args.card.open("r", encoding="utf-8") as handle:
            card = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "errors": [f"cannot read JSON input: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    errors = validate(card, args.max_age_days)
    result = {"status": "pass" if not errors else "fail", "errors": errors, "claims": len(card.get("claims", [])) if isinstance(card, dict) and isinstance(card.get("claims"), list) else 0}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
