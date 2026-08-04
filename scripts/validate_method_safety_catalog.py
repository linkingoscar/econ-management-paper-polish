#!/usr/bin/env python3
"""Validate the writing-first method safety catalog and its authority metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


METHOD_ID = re.compile(r"^MTH-[A-Z0-9_-]+$")


def validate(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["catalog must be an object"]
    if value.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    cards = value.get("cards")
    if not isinstance(cards, list) or not cards:
        return errors + ["cards must be a non-empty array"]
    seen: set[str] = set()
    required = ("method_id", "method", "data_structure", "identifying_variation", "estimand", "assumptions", "diagnostics", "remaining_threats", "cannot_solve", "reporting_requirements", "authority_sources")
    for index, card in enumerate(cards):
        prefix = f"cards[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in required:
            if key not in card or (isinstance(card[key], str) and not card[key].strip()):
                errors.append(f"{prefix}.{key} is required")
        method_id = card.get("method_id")
        if not isinstance(method_id, str) or not METHOD_ID.fullmatch(method_id):
            errors.append(f"{prefix}.method_id must match MTH-<id>")
        elif method_id in seen:
            errors.append(f"{prefix}.method_id duplicates {method_id}")
        else:
            seen.add(method_id)
        for key in ("assumptions", "diagnostics", "remaining_threats", "cannot_solve", "reporting_requirements"):
            if not isinstance(card.get(key), list) or not card[key] or any(not isinstance(item, str) or not item.strip() for item in card[key]):
                errors.append(f"{prefix}.{key} must be a non-empty array of strings")
        sources = card.get("authority_sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}.authority_sources must be non-empty")
        else:
            for source_index, source in enumerate(sources):
                source_prefix = f"{prefix}.authority_sources[{source_index}]"
                if not isinstance(source, dict):
                    errors.append(f"{source_prefix} must be an object")
                    continue
                for key in ("title", "url", "checked_at", "status"):
                    if not isinstance(source.get(key), str) or not source[key].strip():
                        errors.append(f"{source_prefix}.{key} is required")
                if isinstance(source.get("url"), str) and not source["url"].startswith(("http://", "https://")):
                    errors.append(f"{source_prefix}.url must be http(s)")
                if source.get("status") not in {"verified", "documented", "needs-author-review"}:
                    errors.append(f"{source_prefix}.status is invalid")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        value = json.loads(args.catalog.read_text(encoding="utf-8"))
        errors = validate(value)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors = [f"cannot read catalog: {exc}"]
    result = {"status": "pass" if not errors else "fail", "catalog": str(args.catalog), "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
