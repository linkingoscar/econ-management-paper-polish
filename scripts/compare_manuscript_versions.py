#!/usr/bin/env python3
"""Compare manuscript versions and surface protected-token changes."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

from check_numeric_consistency import extract_numeric_tokens, report


def token_counts(text: str, variables: list[str]) -> dict[str, int]:
    counts = dict(extract_numeric_tokens(text))
    for variable in variables:
        counts[f"variable:{variable}"] = len(re.findall(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text))
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        old = args.original.read_text(encoding="utf-8")
        new = args.revised.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read input: {exc}", file=sys.stderr)
        return 2
    numeric = report(extract_numeric_tokens(old), extract_numeric_tokens(new), args.allow_added)
    protected = {}
    old_tokens = token_counts(old, args.variable)
    new_tokens = token_counts(new, args.variable)
    for key in sorted(set(old_tokens) | set(new_tokens)):
        if old_tokens.get(key, 0) != new_tokens.get(key, 0):
            protected[key] = {"original": old_tokens.get(key, 0), "revised": new_tokens.get(key, 0)}
    diff_lines = list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm=""))
    result = {
        "status": "pass" if numeric["status"] == "pass" and not any(key.startswith("variable:") for key in protected) else "fail",
        "numeric": numeric,
        "protected_token_changes": protected,
        "changed_lines": sum(1 for line in diff_lines if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))),
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"changed lines: {result['changed_lines']}")
        print(f"numeric status: {numeric['status']}")
        print(f"protected token changes: {protected or 'none'}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
