#!/usr/bin/env python3
"""Create a deterministic protected-field snapshot for a manuscript."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from writing_contract import utc_now, validate_protected_snapshot, write_json
from protected_fields import LABEL_RE, REF_RE, equation_tokens, protected_counts


HEADING_RE = re.compile(r"^(?:#{1,6}\s+|\\(?:section|subsection|subsubsection)\{)(.+?)(?:\})?$", re.MULTILINE)


def snapshot(path: Path, variables: list[str], locked_fragments: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = protected_counts(text, variables)
    numbers, citations, variable_counts = (fields[key] for key in ("numbers", "citations", "variables"))
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
            "citations": dict(sorted(citations.items())),
            "variables": dict(sorted(variable_counts.items())),
            "quantities": dict(sorted(fields["quantities"].items())),
            "pvalue_relations": dict(sorted(fields["pvalue_relations"].items())),
            "latex_labels": sorted(set(LABEL_RE.findall(text))),
            "latex_refs": sorted(set(REF_RE.findall(text))),
            "locked_fragments": locked_fragments,
            "equations": [hashlib.sha256(value.encode("utf-8")).hexdigest() for value in equation_tokens(text)],
            "anchors": anchors,
            "section_headings": headings,
        },
        "counts": {
            "number_tokens": sum(numbers.values()),
            "citation_tokens": sum(citations.values()),
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
