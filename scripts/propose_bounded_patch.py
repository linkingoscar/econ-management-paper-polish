#!/usr/bin/env python3
"""Create a reviewable bounded-writing patch report without editing the manuscript."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from check_local_bindings import audit_local_bindings
from meaning_audit import compare_text
from protected_fields import protected_counts as counts
from writing_contract import write_json


def compare(old: dict[str, Counter[str]], new: dict[str, Counter[str]], allow_added: bool) -> dict:
    changes: dict[str, dict[str, dict[str, int]]] = {}
    for category in sorted(old.keys() | new.keys()):
        category_changes = {}
        for token in sorted(set(old.get(category, {})) | set(new.get(category, {}))):
            before = old.get(category, Counter())[token]
            after = new.get(category, Counter())[token]
            if before != after:
                category_changes[token] = {"original": before, "revised": after}
        if category_changes:
            changes[category] = category_changes
    missing_numbers = old["numbers"] - new["numbers"]
    added_numbers = new["numbers"] - old["numbers"]
    # --allow-added permits new numeric/quantity observations, not replacing an
    # existing quantity, citation, variable, equation, label, or p-value relation.
    blocking = any(
        old.get(category, Counter()) - new.get(category, Counter())
        or not (allow_added and category in {"numbers", "quantities"})
        for category in changes
    )
    return {
        "status": "pass" if not blocking else "fail",
        "changes": changes,
        "missing_numbers": dict(sorted(missing_numbers.items())),
        "added_numbers": dict(sorted(added_numbers.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        old_text = args.original.read_text(encoding="utf-8")
        new_text = args.revised.read_text(encoding="utf-8")
    except OSError as exc:
        result = {"status": "fail", "errors": [f"cannot read manuscript: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    protection = compare(counts(old_text, args.variable), counts(new_text, args.variable), args.allow_added)
    local_bindings = audit_local_bindings(old_text, new_text, allow_added=args.allow_added)
    meaning = compare_text(old_text, new_text)
    passed = all(gate["status"] == "pass" for gate in (protection, local_bindings, meaning))
    diff = "\n".join(difflib.unified_diff(old_text.splitlines(), new_text.splitlines(), fromfile=str(args.original), tofile=str(args.revised), lineterm=""))
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    changed_anchors = []
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag != "equal":
            changed_anchors.append({
                "operation": tag,
                "original_lines": [old_start + 1, old_end],
                "revised_lines": [new_start + 1, new_end],
                "original_hash": hashlib.sha256("\n".join(old_lines[old_start:old_end]).encode("utf-8")).hexdigest(),
                "revised_hash": hashlib.sha256("\n".join(new_lines[new_start:new_end]).encode("utf-8")).hexdigest(),
            })
    result = {
        "status": "pass" if passed else "fail",
        "risk": "checks-passed" if passed else "author-required",
        "scope": "Known protected-field and lexical checks only; pass is not semantic approval or authorization.",
        "applied": False,
        "protection": protection,
        "local_bindings": local_bindings,
        "meaning_gate": meaning,
        "changed_lines": sum(1 for line in diff.splitlines() if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))),
        "original_sha256": hashlib.sha256(old_text.encode("utf-8")).hexdigest(),
        "revised_sha256": hashlib.sha256(new_text.encode("utf-8")).hexdigest(),
        "anchors": changed_anchors,
        "diff": diff,
        "errors": [],
    }
    if args.output:
        try:
            write_json(args.output, result)
            result["output"] = str(args.output)
        except OSError as exc:
            result["errors"].append(f"cannot write patch report: {exc}")
            result["status"] = "fail"
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"risk: {result['risk']}")
        print(f"changed lines: {result['changed_lines']}")
        print(f"protection: {result['protection']['status']}")
        print(f"local bindings: {result['local_bindings']['status']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
