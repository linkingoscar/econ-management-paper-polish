#!/usr/bin/env python3
"""Apply only a verified bounded-writing patch to a separate output file."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from meaning_audit import compare_text
from propose_bounded_patch import compare, counts
from writing_contract import utc_now, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="New manuscript path; the original is never overwritten by default.")
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--expected-original-sha256")
    parser.add_argument("--allow-author-required", action="store_true")
    parser.add_argument("--author-confirmed", action="store_true")
    parser.add_argument("--confirmed-by", default="")
    parser.add_argument("--rationale", default="")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    result: dict = {"schema_version": "1.0", "status": "fail", "applied": False, "errors": errors, "created_at": utc_now()}
    try:
        old = args.original.read_text(encoding="utf-8")
        new = args.revised.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read manuscript: {exc}")
        old = new = ""
    original_sha = hashlib.sha256(old.encode("utf-8")).hexdigest()
    revised_sha = hashlib.sha256(new.encode("utf-8")).hexdigest()
    result.update({"original": str(args.original), "revised": str(args.revised), "output": str(args.output), "original_sha256": original_sha, "revised_sha256": revised_sha})
    if args.expected_original_sha256 and args.expected_original_sha256 != original_sha:
        errors.append("original manuscript hash does not match the expected snapshot")
    if args.output.resolve() == args.original.resolve():
        errors.append("output must be a separate path; in-place overwrite is disabled")
    protection = compare(counts(old, args.variable), counts(new, args.variable), args.allow_added)
    meaning = compare_text(old, new, author_confirmed=args.author_confirmed, rationale=args.rationale)
    result["protection"] = protection
    result["meaning_gate"] = meaning
    if protection["status"] != "pass":
        if not args.allow_author_required:
            errors.append("protected fields changed; use an explicit author-required confirmation before applying")
        if not args.author_confirmed or not args.confirmed_by.strip() or not args.rationale.strip():
            errors.append("author-required apply needs --author-confirmed, --confirmed-by, and --rationale")
    if meaning["status"] != "pass":
        errors.append("meaning gate failed")
    if not errors:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(new, encoding="utf-8")
            result["status"] = "pass"
            result["applied"] = True
            result["confirmation"] = {"confirmed_at": utc_now(), "confirmed_by": args.confirmed_by or None, "rationale": args.rationale or None}
        except OSError as exc:
            errors.append(f"cannot write output manuscript: {exc}")
    if args.report:
        try:
            write_json(args.report, result)
            result["report"] = str(args.report)
        except OSError as exc:
            errors.append(f"cannot write apply report: {exc}")
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"applied: {result['applied']}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
