#!/usr/bin/env python3
"""List claims affected when an evidence source is withdrawn from the ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_contract import load_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("source_id")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        ledger = load_json(args.ledger)
        entries = ledger.get("entries", [])
        affected = [
            {"claim_id": entry.get("claim_id"), "claim": entry.get("claim"), "allowed_use": entry.get("allowed_use", []), "locator": (entry.get("verification") or {}).get("locator")}
            for entry in entries if isinstance(entry, dict) and entry.get("source_id") == args.source_id
        ]
        source = ledger.get("source_index", {}).get(args.source_id)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        affected = []
        source = None
        errors.append(f"cannot read evidence ledger: {exc}")
    result = {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "source_id": args.source_id,
        "source_present": source is not None,
        "affected_claims": affected,
        "impact_count": len(affected),
        "action": "review-or-rebind-claims-before-source-removal" if affected else "no-claim-binding-found",
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"impact_count: {result['impact_count']}")
        for item in affected:
            print(f"- {item['claim_id']}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
