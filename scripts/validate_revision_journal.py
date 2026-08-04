#!/usr/bin/env python3
"""Validate the JSONL revision journal as an append-only workflow fact source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [f"cannot read journal: {exc}"]
    if not lines:
        return ["journal must contain at least one event"]
    for index, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {index}: invalid JSON ({exc})")
            continue
        if not isinstance(event, dict):
            errors.append(f"line {index}: event must be an object")
            continue
        for key in ("schema_version", "run_id", "stage", "status", "at"):
            if not isinstance(event.get(key), str) or not event[key].strip():
                errors.append(f"line {index}: {key} must be non-empty")
        if not ((isinstance(event.get("event"), str) and event["event"].strip()) or (isinstance(event.get("action"), str) and event["action"].strip())):
            errors.append(f"line {index}: event/action must be non-empty")
        event_id = event.get("event_id")
        if event_id:
            if event_id in seen:
                errors.append(f"line {index}: duplicate event_id {event_id}")
            seen.add(event_id)
        if not isinstance(event.get("errors", []), list):
            errors.append(f"line {index}: errors must be an array")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors = validate(args.journal)
    result = {"status": "pass" if not errors else "fail", "journal": str(args.journal), "events": len(args.journal.read_text(encoding="utf-8").splitlines()) if args.journal.is_file() else 0, "errors": errors, "append_only": True}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"events: {result['events']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
