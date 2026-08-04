#!/usr/bin/env python3
"""Create a reviewable bounded-writing patch report without editing the manuscript."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from writing_contract import write_json


NUMBER_RE = re.compile(
    r"(?<![A-Za-z])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)(?:%|[eE][-+]?\d+)?(?![A-Za-z])"
)
CITATION_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
PAREN_CITATION_RE = re.compile(r"\[@([^\]]+)\]")


def normalize_number(value: str) -> str:
    return value.replace("−", "-").replace("–", "-").replace("—", "-").replace(",", "")


def counts(text: str, variables: list[str]) -> dict[str, Counter[str]]:
    citations: list[str] = []
    for match in CITATION_RE.finditer(text):
        citations.extend(item.strip() for item in match.group(1).split(",") if item.strip())
    citations.extend(item.strip() for match in PAREN_CITATION_RE.finditer(text) for item in match.group(1).split(";") if item.strip())
    variable_counts = Counter()
    for variable in variables:
        variable_counts[variable] = len(re.findall(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text))
    return {
        "numbers": Counter(normalize_number(match.group(0)) for match in NUMBER_RE.finditer(text)),
        "citations": Counter(citations),
        "variables": variable_counts,
    }


def compare(old: dict[str, Counter[str]], new: dict[str, Counter[str]], allow_added: bool) -> dict:
    changes: dict[str, dict[str, dict[str, int]]] = {}
    for category in ("numbers", "citations", "variables"):
        category_changes = {}
        for token in sorted(set(old[category]) | set(new[category])):
            if old[category][token] != new[category][token]:
                category_changes[token] = {"original": old[category][token], "revised": new[category][token]}
        if category_changes:
            changes[category] = category_changes
    missing_numbers = old["numbers"] - new["numbers"]
    added_numbers = new["numbers"] - old["numbers"]
    blocking = bool(missing_numbers or changes.get("variables") or changes.get("citations") or (added_numbers and not allow_added))
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
        "status": protection["status"],
        "risk": "safe-fix" if protection["status"] == "pass" else "author-required",
        "applied": False,
        "protection": protection,
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
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
