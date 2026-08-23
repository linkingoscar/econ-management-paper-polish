#!/usr/bin/env python3
"""Run a conservative lexical meaning gate for a candidate writing patch.

The gate compares method, causal, result, contribution, and uncertainty
markers.  Equal marker counts are not semantic equivalence; a changed marker
requires author confirmation rather than an automatic rewrite.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


MARKERS: dict[str, tuple[str, ...]] = {
    "causal": (
        r"\bcausal(?:ly)?\b",
        r"\bcauses?\b",
        r"\bleads? to\b",
        r"\bimpact(?:s|ed|ing)?\b",
        r"\b(?:effect|effects|effected)\b",
        r"因果",
        r"导致",
        r"影响",
    ),
    "identification": (
        r"\bidentif(?:y|ies|ied|ication)\b",
        r"\bexogenous\b",
        r"\bendogeneity\b",
        r"\bparallel trends?\b",
        r"识别",
        r"外生",
        r"内生性",
        r"平行趋势",
    ),
    "strength": (
        r"\bprove[sd]?\b",
        r"\bdemonstrate[sd]?\b",
        r"\bestablish(?:es|ed)?\b",
        r"\bconfirm(?:s|ed)?\b",
        r"\bshow(?:s|ed|ing)?\b",
        r"证明",
        r"证实",
        r"验证",
        r"表明",
    ),
    "uncertainty": (
        r"\bmay\b",
        r"\bmight\b",
        r"\bcould\b",
        r"\bsuggest(?:s|ed|ing)?\b",
        r"\bconsistent with\b",
        r"可能",
        r"或许",
        r"表明……但不证明",
        r"与……一致",
    ),
    "scope": (
        r"\blocal effect\b",
        r"\blocal average treatment effect\b",
        r"\bgeneraliz(?:e|able|ation)\b",
        r"\bexternal validity\b",
        r"局部效应",
        r"外部有效性",
        r"可推广",
    ),
    "positive_direction": (
        r"\bpositive(?:ly)?\b",
        r"\bincreas(?:e|es|ed|ing)\b",
        r"\bhigher\b",
        r"正向",
        r"提高",
        r"增加",
    ),
    "negative_direction": (
        r"\bnegative(?:ly)?\b",
        r"\bdecreas(?:e|es|ed|ing)\b",
        r"\blower\b",
        r"负向",
        r"降低",
        r"减少",
    ),
    "significant": (
        r"(?<!not )\bstatistically significant\b",
        r"(?<!not )\bsignificant\b",
        r"(?<!不)显著",
    ),
    "nonsignificant": (
        r"\bnot statistically significant\b",
        r"\bnot significant\b",
        r"\binsignificant\b",
        r"不显著",
    ),
}


def counts(text: str) -> dict[str, int]:
    result: Counter[str] = Counter()
    for category, patterns in MARKERS.items():
        for pattern in patterns:
            result[category] += len(re.findall(pattern, text, flags=re.IGNORECASE))
    return dict(sorted(result.items()))


def compare_text(original: str, revised: str, *, author_confirmed: bool = False, rationale: str = "") -> dict[str, Any]:
    old_counts = counts(original)
    new_counts = counts(revised)
    changed = {
        category: {"original": old_counts.get(category, 0), "revised": new_counts.get(category, 0)}
        for category in sorted(set(old_counts) | set(new_counts))
        if old_counts.get(category, 0) != new_counts.get(category, 0)
    }
    if changed and not author_confirmed:
        status = "fail"
        decision = "author-required"
        reason = "semantic-risk-marker-change"
    elif changed and author_confirmed:
        status = "pass"
        decision = "author-confirmed"
        reason = "semantic-risk-marker-change-confirmed-by-author"
    else:
        status = "pass"
        decision = "safe-fix"
        reason = "no-count-change-in-protected-meaning-markers"
    return {
        "schema_version": "1.0",
        "status": status,
        "decision": decision,
        "reason": reason,
        "marker_counts": {"original": old_counts, "revised": new_counts},
        "changed_categories": changed,
        "rationale": rationale if author_confirmed else "",
        "scope": "lexical-safety-gate; equal marker counts do not establish semantic equivalence",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--author-confirmed", action="store_true")
    parser.add_argument("--rationale", default="")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        original = args.original.read_text(encoding="utf-8")
        revised = args.revised.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "decision": "author-required", "errors": [str(exc)]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    result = compare_text(original, revised, author_confirmed=args.author_confirmed, rationale=args.rationale)
    result["original_file"] = str(args.original)
    result["revised_file"] = str(args.revised)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"decision: {result['decision']}")
        print(f"reason: {result['reason']}")
        for category, values in result["changed_categories"].items():
            print(f"- {category}: {values['original']} -> {values['revised']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
