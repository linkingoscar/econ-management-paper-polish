#!/usr/bin/env python3
"""Create a deterministic protected-field snapshot for a manuscript."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from writing_contract import utc_now, validate_protected_snapshot, write_json


NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)(?:%|[eE][-+]?\d+)?(?![A-Za-z])")
CITATION_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
PAREN_CITATION_RE = re.compile(r"\[@([^\]]+)\]")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eq)?ref\{([^}]+)\}")
EQUATION_RE = re.compile(r"\\begin\{(?:equation|align|equation\*)\}.*?\\end\{(?:equation|align|equation\*)\}", re.DOTALL)
HEADING_RE = re.compile(r"^(?:#{1,6}\s+|\\(?:section|subsection|subsubsection)\{)(.+?)(?:\})?$", re.MULTILINE)


def normalize_number(value: str) -> str:
    return value.replace(",", "")


def snapshot(path: Path, variables: list[str], locked_fragments: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    numbers = Counter(normalize_number(match.group(0)) for match in NUMBER_RE.finditer(text))
    citations: list[str] = []
    for match in CITATION_RE.finditer(text):
        citations.extend(item.strip() for item in match.group(1).split(",") if item.strip())
    citations.extend(item.strip() for match in PAREN_CITATION_RE.finditer(text) for item in match.group(1).split(";") if item.strip())
    variable_counts = Counter({variable: len(re.findall(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text)) for variable in variables})
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    anchors = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            anchors.append({
                "line": line_number,
                "sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                "text_prefix": line.strip()[:120],
                "length": len(line),
            })
    headings = [match.group(1).strip() for match in HEADING_RE.finditer(text) if match.group(1).strip()]
    return {
        "schema_version": "1.0",
        "snapshot_id": f"SNAP-{digest[:16]}",
        "source_path": str(path),
        "sha256": digest,
        "created_at": utc_now(),
        "protected": {
            "numbers": dict(sorted(numbers.items())),
            "citations": dict(sorted(Counter(citations).items())),
            "variables": dict(sorted(variable_counts.items())),
            "latex_labels": sorted(set(LABEL_RE.findall(text))),
            "latex_refs": sorted(set(REF_RE.findall(text))),
            "locked_fragments": locked_fragments,
            "equations": [hashlib.sha256(value.encode("utf-8")).hexdigest() for value in EQUATION_RE.findall(text)],
            "anchors": anchors,
            "section_headings": headings,
        },
        "counts": {
            "number_tokens": sum(numbers.values()),
            "citation_tokens": len(citations),
            "variable_tokens": sum(variable_counts.values()),
            "latex_labels": len(set(LABEL_RE.findall(text))),
            "latex_refs": len(set(REF_RE.findall(text))),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--locked-fragment", action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    value = None
    try:
        value = snapshot(args.manuscript, args.variable, args.locked_fragment)
        errors.extend(validate_protected_snapshot(value))
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot snapshot manuscript: {exc}")
    output = None
    if value is not None and not errors and args.output:
        try:
            write_json(args.output, value)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write snapshot: {exc}")
    result = {"status": "pass" if value is not None and not errors else "fail", "errors": errors, "output": output, "snapshot": value}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if value:
            print(f"snapshot_id: {value['snapshot_id']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
