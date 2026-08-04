#!/usr/bin/env python3
"""Build and validate a persistent v3.1 Router 2.0 card.

The router is deliberately explicit: this script records supplied choices and
does not pretend to infer a method, journal, or discipline from prose.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from writing_contract import utc_now, validate_route_card, write_json


def parse_override(values: list[str]) -> list[dict[str, str]]:
    overrides: list[dict[str, str]] = []
    for value in values:
        if "=" not in value:
            raise ValueError(f"override must be key=value: {value}")
        key, replacement = value.split("=", 1)
        if not key.strip() or not replacement.strip():
            raise ValueError(f"override must have non-empty key and value: {value}")
        overrides.append({"field": key.strip(), "value": replacement.strip(), "recorded_at": utc_now()})
    return overrides


def build(args: argparse.Namespace) -> dict:
    now = utc_now()
    slug = re.sub(r"[^0-9A-Za-z_-]+", "-", args.paper_id or "paper").strip("-").lower() or "paper"
    rationale = args.rationale or ["Route fields were explicitly supplied for this run."]
    return {
        "schema_version": "1.0",
        "route_id": f"ROUTE-{slug}-{now.replace(':', '').replace('-', '')[:15]}",
        "paper_id": args.paper_id,
        "task_mode": args.task_mode,
        "discipline": args.discipline,
        "subfield": args.subfield,
        "language": args.language,
        "section": args.section,
        "method": args.method,
        "target_outlet": args.target_outlet,
        "evidence_mode": args.evidence_mode,
        "execution": args.execution,
        "preservation": args.preservation,
        "confidence": args.confidence,
        "rationale": rationale,
        "unresolved": args.unresolved,
        "user_overrides": parse_override(args.override),
        "created_at": now,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", default="paper-unknown")
    parser.add_argument("--task-mode", required=True, choices=["polish", "diagnose", "adapt", "review", "revise", "audit"])
    parser.add_argument("--discipline", required=True, choices=["economics", "management", "finance", "accounting", "marketing", "information-systems", "public-administration", "mixed"])
    parser.add_argument("--subfield")
    parser.add_argument("--language", default="unspecified", choices=["zh-CN", "en-US", "bilingual", "unspecified"])
    parser.add_argument("--section")
    parser.add_argument("--method")
    parser.add_argument("--target-outlet")
    parser.add_argument("--evidence-mode", default="offline", choices=["offline", "metadata", "web-verified", "user-provided-fulltext"])
    parser.add_argument("--execution", default="serial", choices=["serial", "bounded_parallel"])
    parser.add_argument("--preservation", default="strict", choices=["strict", "standard", "user-defined"])
    parser.add_argument("--confidence", default="medium", choices=["high", "medium", "low", "unknown"])
    parser.add_argument("--rationale", action="append", default=[])
    parser.add_argument("--unresolved", action="append", default=[])
    parser.add_argument("--override", action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    card = None
    try:
        card = build(args)
        errors.extend(validate_route_card(card))
    except ValueError as exc:
        errors.append(str(exc))
    output = None
    if card is not None and not errors and args.output:
        try:
            write_json(args.output, card)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write route card: {exc}")
    result = {"status": "pass" if card is not None and not errors else "fail", "errors": errors, "output": output, "route_card": card}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if card:
            print(f"route_id: {card['route_id']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
