#!/usr/bin/env python3
"""Check whether numeric tokens changed between two manuscript versions.

This is intentionally strict. It is designed for line polishing, where numbers,
years, percentages, p-values, and equation constants should remain unchanged.
Use --allow-added for substantive revisions that intentionally add results.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from protected_fields import economic_numeric_inventory, numeric_tokens


def extract_numeric_tokens(text: str) -> Counter[str]:
    return Counter(numeric_tokens(text))


def report(original: Counter[str], revised: Counter[str], allow_added: bool) -> dict:
    missing = original - revised
    added = revised - original
    result = {
        "original_total": sum(original.values()),
        "revised_total": sum(revised.values()),
        "missing": dict(sorted(missing.items())),
        "added": dict(sorted(added.items())),
        "status": "pass" if not missing and (allow_added or not added) else "fail",
    }
    if allow_added and added:
        result["note"] = "Added numeric tokens were allowed by --allow-added."
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--economic-units", action="store_true",
                        help="Opt-in translation check for CNY, percent and percentage-point equivalence; requires known CNY context for 元/yuan.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        original_text = args.original.read_text(encoding="utf-8")
        revised_text = args.revised.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read input: {exc}", file=sys.stderr)
        return 2

    result = report(
        extract_numeric_tokens(original_text),
        extract_numeric_tokens(revised_text),
        args.allow_added,
    )
    if args.economic_units:
        original, old_records = economic_numeric_inventory(original_text)
        revised, new_records = economic_numeric_inventory(revised_text)
        strict_result = result
        result = report(original, revised, args.allow_added)
        result["strict_numeric_check"] = strict_result
        result["normalized_quantities"] = {"original": old_records, "revised": new_records}
        result["scope"] = (
            "Limited CNY/percent/percentage-point inventory equivalence. Requires established CNY context for 元/yuan. "
            "Does not check local claim binding, unrecognized units, citations, or translation meaning; does not authorize apply."
        )
    else:
        result["scope"] = "Strict numeric-token counts only; not a claim of semantic equivalence."
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"original tokens: {result['original_total']}")
        print(f"revised tokens: {result['revised_total']}")
        print(f"missing: {result['missing'] or 'none'}")
        print(f"added: {result['added'] or 'none'}")
        if args.economic_units:
            print(f"scope: {result['scope']}")
            for label, records in result["normalized_quantities"].items():
                for record in records:
                    print(f"- {label}: {record['text']} -> {record['equivalent']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
