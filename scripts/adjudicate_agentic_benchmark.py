#!/usr/bin/env python3
"""Deterministically adjudicate blinded agent reviews with hard-gate precedence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_benchmark_contract import adjudicate_agentic_reviews
from writing_contract import load_json, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("mapping", type=Path, help="Private blind mapping and hard audits.")
    parser.add_argument("reviews", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        packet = load_json(args.packet)
        mapping = load_json(args.mapping)
        decision = adjudicate_agentic_reviews(packet, [load_json(path) for path in args.reviews], mapping)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        decision = {
            "schema_version": "1.0",
            "status": "fail",
            "decision": "blocked",
            "errors": [f"cannot adjudicate agentic benchmark: {exc}"],
        }
    output = None
    if args.output and decision.get("packet_id"):
        try:
            write_json(args.output, decision)
            output = str(args.output)
        except OSError as exc:
            decision.setdefault("errors", []).append(f"cannot write decision: {exc}")
            decision["status"] = "fail"
            decision["decision"] = "blocked"
    result = {"status": decision["status"], "output": output, "decision": decision, "errors": decision.get("errors", [])}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"status: {result['status']} ({decision['decision']})")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
