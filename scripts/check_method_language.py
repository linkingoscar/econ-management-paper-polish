#!/usr/bin/env python3
"""Detect a small, conservative set of method-language overclaims.

This is a writing gate, not a causal-inference engine.  It flags phrases that
are incompatible with the v3 method-safety red lines and leaves the actual
revision decision to the author.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PATTERNS: tuple[dict[str, Any], ...] = (
    {
        "code": "event-study-proves-parallel-trends",
        "method": "event-study",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:event[- ]study|event[- ]time plot|pre[- ]trend plot)\b[^.\n]{0,120}"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,60}\bparallel trends?\b",
            re.IGNORECASE,
        ),
        "recommendation": "Describe pre-trend evidence as a diagnostic or consistency check; do not call it proof of parallel trends.",
    },
    {
        "code": "event-study-proves-parallel-trends-zh",
        "method": "event-study",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"事件研究[^。\n]{0,100}(?:证明|证实|验证)[^。\n]{0,40}平行趋势", re.IGNORECASE),
        "recommendation": "将事件研究表述为对趋势一致性的诊断证据，并说明剩余假设，不要写成证明平行趋势。",
    },
    {
        "code": "matching-solves-endogeneity",
        "method": "matching",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:psm|propensity[- ]score matching|matching|matched sample)\b[^.\n]{0,100}"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}\bendogeneity\b",
            re.IGNORECASE,
        ),
        "recommendation": "State which observables are balanced and which unobserved-confounding threats remain; matching alone does not solve endogeneity.",
    },
    {
        "code": "controls-or-heckman-solves-endogeneity",
        "method": "controls-or-heckman",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:control variables?|fixed effects?|heckman(?: correction)?)\b[^.\n]{0,100}"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}\bendogeneity\b",
            re.IGNORECASE,
        ),
        "recommendation": "Explain the identifying variation and residual confounding; controls or a Heckman correction are not automatic cures for endogeneity.",
    },
    {
        "code": "matching-solves-endogeneity-zh",
        "method": "matching-or-controls",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(
            r"(?:倾向得分匹配|PSM|匹配方法|匹配样本|控制变量|固定效应|Heckman)[^。\n]{0,80}"
            r"(?:解决|消除|克服|完全处理|排除)[^。\n]{0,25}内生性",
            re.IGNORECASE,
        ),
        "recommendation": "说明匹配或控制变量实际平衡了什么，以及未观测混淆仍可能存在；不要写成解决内生性。",
    },
    {
        "code": "mediation-proves-causal-mechanism",
        "method": "mediation",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(
            r"\b(?:mediation|mediator|mediation analysis)\b[^.\n]{0,100}"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,55}\b(?:causal mechanism|causality)\b",
            re.IGNORECASE,
        ),
        "recommendation": "Separate descriptive mediation from causal mediation and state the mediator and identification assumptions.",
    },
    {
        "code": "mediation-proves-causal-mechanism-zh",
        "method": "mediation",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:中介分析|中介效应|中介变量)[^。\n]{0,80}(?:证明|证实|验证)[^。\n]{0,35}(?:因果机制|因果关系)", re.IGNORECASE),
        "recommendation": "区分描述性中介与因果中介，并明确中介变量的时序、外生性和识别假设。",
    },
    {
        "code": "association-overclaim-causality",
        "method": "observational-causality",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(
            r"\b(?:observational|descriptive|correlational|association)\b[^.\n]{0,80}"
            r"\b(?:causal effect|causes?|causally|causal impact)\b",
            re.IGNORECASE,
        ),
        "recommendation": "Use association language unless the manuscript states an identification design and its assumptions.",
    },
    {
        "code": "association-overclaim-causality-zh",
        "method": "observational-causality",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:相关性|描述性分析|观察性研究)[^。\n]{0,60}(?:因果效应|导致|因果影响)", re.IGNORECASE),
        "recommendation": "如果没有清楚的识别设计和假设，请使用相关性或关联性表述，而不是因果表述。",
    },
)


NEGATED_EN = re.compile(
    r"\b(?:not|never|cannot|can't|doesn't|don't|does not|do not|without)\b[^.\n]{0,30}"
    r"\b(?:prove|demonstrate|establish|confirm|solve|eliminate|remove|cure|address|identify|causal)\w*\b",
    re.IGNORECASE,
)
NEGATED_ZH = re.compile(r"(?:不|并非|不能|无法|未能|没有)[^。\n]{0,30}(?:证明|证实|验证|解决|消除|克服|识别|因果)", re.IGNORECASE)


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def check(text: str, path: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    for item in PATTERNS:
        for match in item["pattern"].finditer(text):
            matched_text = match.group(0).strip()
            if (item["language"] == "en" and NEGATED_EN.search(matched_text)) or (
                item["language"] == "zh" and NEGATED_ZH.search(matched_text)
            ):
                continue
            issues.append(
                {
                    "code": item["code"],
                    "method": item["method"],
                    "language": item["language"],
                    "severity": item["severity"],
                    "line": line_number(text, match.start()),
                    "match": matched_text,
                    "recommendation": item["recommendation"],
                }
            )
    issues.sort(key=lambda issue: (issue["line"], issue["code"], issue["match"]))
    blocking = sum(issue["severity"] == "blocking" for issue in issues)
    major = sum(issue["severity"] == "major" for issue in issues)
    return {
        "schema_version": "1.0",
        "status": "fail" if issues else "pass",
        "file": str(path),
        "issue_count": len(issues),
        "blocking_count": blocking,
        "major_count": major,
        "issues": issues,
        "decision": "author-required" if issues else "safe-fix",
        "scope": "deterministic-method-language-screen; not a causal-inference proof",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        text = args.manuscript.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "file": str(args.manuscript), "errors": [str(exc)]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    result = check(text, args.manuscript)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"issues: {result['issue_count']}")
        for issue in result["issues"]:
            print(f"- line {issue['line']}: {issue['code']}: {issue['match']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
