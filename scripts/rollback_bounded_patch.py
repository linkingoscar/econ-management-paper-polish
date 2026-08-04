#!/usr/bin/env python3
"""Restore a manuscript output from a known original snapshot without deleting files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from writing_contract import utc_now, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="Known-good manuscript snapshot")
    parser.add_argument("--output", type=Path, required=True, help="Separate restored manuscript path")
    parser.add_argument("--expected-original-sha256")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    result = {"schema_version": "1.0", "status": "fail", "restored": False, "created_at": utc_now(), "errors": errors}
    try:
        text = args.original.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        text = ""
        errors.append(f"cannot read original snapshot: {exc}")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    result.update({"original": str(args.original), "output": str(args.output), "original_sha256": digest})
    if args.expected_original_sha256 and args.expected_original_sha256 != digest:
        errors.append("original snapshot hash does not match the expected value")
    if args.output.resolve() == args.original.resolve():
        errors.append("rollback output must be a separate path")
    if not errors:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            result["status"] = "pass"
            result["restored"] = True
        except OSError as exc:
            errors.append(f"cannot write rollback output: {exc}")
    if args.report:
        try:
            write_json(args.report, result)
            result["report"] = str(args.report)
        except OSError as exc:
            errors.append(f"cannot write rollback report: {exc}")
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"restored: {result['restored']}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
