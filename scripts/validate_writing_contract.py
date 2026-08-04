#!/usr/bin/env python3
"""Validate one v3.1 writing artifact using the dependency-free contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_contract import (
    load_json,
    validate_corpus_manifest,
    validate_paper_spine,
    validate_provenance_manifest,
    validate_review_ledger,
    validate_style_card,
    validate_style_profile,
)


VALIDATORS = {
    "corpus-manifest": validate_corpus_manifest,
    "paper-spine": validate_paper_spine,
    "provenance": validate_provenance_manifest,
    "review-ledger": validate_review_ledger,
    "style-card": validate_style_card,
    "style-profile": validate_style_profile,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(VALIDATORS))
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        value = load_json(args.input)
        errors = VALIDATORS[args.kind](value)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"cannot read JSON input: {exc}"]
    result = {"status": "pass" if not errors else "fail", "kind": args.kind, "input": str(args.input), "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
