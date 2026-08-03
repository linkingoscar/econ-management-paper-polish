#!/usr/bin/env python3
"""Check whether numeric tokens changed between two manuscript versions.

This is intentionally strict. It is designed for line polishing, where numbers,
years, percentages, p-values, and equation constants should remain unchanged.
Use --allow-added for substantive revisions that intentionally add results.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


NUMBER_RE = re.compile(
    r"(?<![A-Za-z])[-+]?"
    r"(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)"
    r"(?:%|[eE][-+]?\d+)?(?![A-Za-z])"
)


def normalize_token(token: str) -> str:
    token = token.replace("−", "-").replace("–", "-").replace("—", "-")
    token = token.replace(",", "")
    return token


def extract_numeric_tokens(text: str) -> Counter[str]:
    return Counter(normalize_token(match.group(0)) for match in NUMBER_RE.finditer(text))


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
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"original tokens: {result['original_total']}")
        print(f"revised tokens: {result['revised_total']}")
        print(f"missing: {result['missing'] or 'none'}")
        print(f"added: {result['added'] or 'none'}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
