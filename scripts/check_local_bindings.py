#!/usr/bin/env python3
"""Conservatively check whether numbers and citations retain local context.

This deterministic screen complements global token counts. It does not prove
semantic equivalence; it flags reordered or relocated protected tokens for
author review.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any

from protected_fields import NUMBER_RE, citation_keys, mask_citations, numeric_tokens, quantity_tokens


SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[。！？])\s*|(?<=[.!?])\s+(?=[A-Z\u3400-\u4dbf\u4e00-\u9fff\\#])")


def protected_values(text: str) -> dict[str, list[str]]:
    number_text = mask_citations(text)
    return {
        "numbers": numeric_tokens(number_text),
        "citations": citation_keys(text),
        "quantities": quantity_tokens(number_text),
    }


def masked_context(text: str) -> str:
    masked = mask_citations(text, " <citation> ")
    masked = NUMBER_RE.sub(" <number> ", masked)
    return re.sub(r"\s+", " ", masked).strip().lower()


def segments(text: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for value in SENTENCE_BOUNDARY_RE.split(line.strip()):
            value = value.strip()
            if not value:
                continue
            protected = protected_values(value)
            result.append(
                {
                    "index": len(result),
                    "line": line_number,
                    "text": value,
                    "context": masked_context(value),
                    **protected,
                }
            )
    return result


def _is_subsequence(original: list[str], revised: list[str]) -> bool:
    iterator = iter(revised)
    return all(any(candidate == item for candidate in iterator) for item in original)


def audit_local_bindings(original: str, revised: str, *, allow_added: bool = False) -> dict[str, Any]:
    old_segments = [item for item in segments(original) if item["numbers"] or item["citations"]]
    new_segments = segments(revised)
    aligned: dict[int, tuple[int, float]] = {}
    next_new_index = 0
    for old_index, old in enumerate(old_segments):
        candidates = [
            (
                difflib.SequenceMatcher(None, old["context"], new["context"], autojunk=False).ratio(),
                new_index,
            )
            for new_index, new in enumerate(new_segments[next_new_index:], start=next_new_index)
        ]
        if not candidates:
            continue
        similarity, new_index = max(candidates, key=lambda item: (item[0], -item[1]))
        if similarity >= 0.35:
            aligned[old_index] = (new_index, similarity)
            next_new_index = new_index + 1

    issues: list[dict[str, Any]] = []
    for old_index, old in enumerate(old_segments):
        if old_index not in aligned:
            issues.append(
                {
                    "kind": "protected-segment-unmatched",
                    "original_line": old["line"],
                    "original": {"numbers": old["numbers"], "citations": old["citations"]},
                }
            )
            continue
        new_index, similarity = aligned[old_index]
        new = new_segments[new_index]
        numbers_match = _is_subsequence(old["numbers"], new["numbers"]) if allow_added else old["numbers"] == new["numbers"]
        if not numbers_match:
            issues.append(
                {
                    "kind": "number-binding-changed",
                    "original_line": old["line"],
                    "revised_line": new["line"],
                    "original": old["numbers"],
                    "revised": new["numbers"],
                    "context_similarity": round(similarity, 3),
                }
            )
        if old["citations"] != new["citations"]:
            issues.append(
                {
                    "kind": "citation-binding-changed",
                    "original_line": old["line"],
                    "revised_line": new["line"],
                    "original": old["citations"],
                    "revised": new["citations"],
                    "context_similarity": round(similarity, 3),
                }
            )
        quantities_match = _is_subsequence(old["quantities"], new["quantities"]) if allow_added else old["quantities"] == new["quantities"]
        if not quantities_match:
            issues.append({
                "kind": "quantity-binding-changed", "original_line": old["line"],
                "revised_line": new["line"], "original": old["quantities"], "revised": new["quantities"],
            })
    return {
        "schema_version": "1.0",
        "status": "fail" if issues else "pass",
        "issue_count": len(issues),
        "issues": issues,
        "aligned_protected_segments": len(aligned),
        "original_protected_segments": len(old_segments),
        "scope": "deterministic local number/citation binding screen; passing does not establish semantic equivalence",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--allow-added", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        original = args.original.read_text(encoding="utf-8")
        revised = args.revised.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "errors": [f"cannot read manuscript: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    result = audit_local_bindings(original, revised, allow_added=args.allow_added)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"issues: {result['issue_count']}")
        for issue in result["issues"]:
            print(f"- {issue['kind']} at original line {issue['original_line']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
