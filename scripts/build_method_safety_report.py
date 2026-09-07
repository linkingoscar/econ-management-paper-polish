#!/usr/bin/env python3
"""Join deterministic method-language findings to writing-safe risk-card guidance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_method_language import check


CARD_MAP = {
    "staggered-did": "MTH-STAGGERED-DID",
    "event-study": "MTH-STAGGERED-DID",
    "continuous-treatment": "MTH-CONTINUOUS-TREATMENT",
    "bartik-iv": "MTH-BARTIK-IV",
    "cate": "MTH-CATE",
    "mediation": "MTH-MEDIATION",
    "quantile-oaxaca": "MTH-QUANTILE-OAXACA",
    "survey": "MTH-SURVEY",
    "qualitative": "MTH-QUALITATIVE",
}


def enrich(issue: dict, cards: dict) -> dict:
    card = cards.get(CARD_MAP.get(issue.get("method")))
    advisory = issue.get("basis") == "context-needed"
    return {
        **issue,
        "risk_card_id": card.get("method_id") if card else None,
        "why": (
            "Check the supplied design and qualification before judging this sentence; the keyword match alone is not an error."
            if advisory else
            "A known overclaim pattern was found; inspect its context, assumptions, and diagnostics."
        ),
        # Preserve Chinese guidance for Chinese manuscripts. This is guidance for
        # a rewrite, not an instruction to paste an unrelated canned sentence.
        "conservative_rewrite": (
            issue["recommendation"] if issue.get("language") == "zh" or not card
            else card["conservative_rewrite"]
        ),
        "author_inputs_required": (
            card.get("reporting_requirements", []) if card
            else ["State the estimand, assumptions, diagnostics, and remaining threats."]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "method-safety-cards.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        text = args.manuscript.read_text(encoding="utf-8")
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        cards = {card.get("method_id"): card for card in catalog.get("cards", [])}
        findings = check(text, args.manuscript)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        findings = {"schema_version": "1.0", "status": "fail", "issue_count": 0, "issues": []}
        cards = {}
        errors.append(f"cannot build method safety report: {exc}")
    enriched = [enrich(issue, cards) for issue in findings.get("issues", [])]
    advisories = [enrich(issue, cards) for issue in findings.get("advisories", [])]
    report = {
        "schema_version": "1.0",
        "status": "fail" if enriched or errors else "pass",
        "file": str(args.manuscript),
        "issue_count": len(enriched),
        "issues": enriched,
        "advisory_count": len(advisories),
        "advisories": advisories,
        "decision": "author-required" if enriched or errors else findings["decision"],
        "scope": "writing-safe explanation and conservative rewrite guidance; not a causal-inference proof",
        "errors": errors,
    }
    output = None
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            output = str(args.output)
        except OSError as exc:
            report["status"] = "fail"
            report.setdefault("errors", []).append(f"cannot write report: {exc}")
    result = {**report, "output": output}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"issues: {result['issue_count']}")
        for issue in enriched:
            print(f"- line {issue['line']}: {issue['code']}: {issue['conservative_rewrite']}")
        for advisory in advisories:
            print(f"- review context at line {advisory['line']}: {advisory['recommendation']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
