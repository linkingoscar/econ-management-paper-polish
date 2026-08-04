#!/usr/bin/env python3
"""Verify a proposed writing patch without applying it to the manuscript."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from meaning_audit import compare_text
from propose_bounded_patch import compare, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--author-confirmed", action="store_true", help="Allow a meaning-risk patch only with explicit author confirmation.")
    parser.add_argument("--rationale", default="", help="Record the author's reason for confirming a meaning-risk patch.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        old = args.original.read_text(encoding="utf-8")
        new = args.revised.read_text(encoding="utf-8")
    except OSError as exc:
        result = {"status": "fail", "errors": [f"cannot read manuscript: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    protection = compare(counts(old, args.variable), counts(new, args.variable), args.allow_added)
    meaning = compare_text(old, new, author_confirmed=args.author_confirmed, rationale=args.rationale)
    overall_status = "pass" if protection["status"] == "pass" and meaning["status"] == "pass" else "fail"
    result = {
        "status": overall_status,
        "verified": overall_status == "pass",
        "applied": False,
        "protection": protection,
        "meaning_gate": meaning,
        "errors": [],
    }
    if protection["status"] != "pass":
        result["errors"].append("protected token counts changed")
    if meaning["status"] != "pass":
        result["errors"].append("meaning-risk markers changed and require author confirmation")
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"verified: {result['verified']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
