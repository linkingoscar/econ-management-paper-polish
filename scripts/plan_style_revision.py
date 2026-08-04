#!/usr/bin/env python3
"""Create a bounded structural plan from a human- or AI-confirmed style profile."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import median

from ai_review_contract import sha256_path
from validate_style_profile_gate import evaluate as evaluate_style_gate
from writing_contract import load_json, write_json


def sentence_count(text: str) -> int:
    return max(1, len([part for part in re.split(r"(?<=[.!?。！？])\s+", text.strip()) if part.strip()]))


def plan(manuscript: Path, profile: dict, section: str, confirmation_mode: str) -> dict:
    text = manuscript.read_text(encoding="utf-8")
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    target = profile.get("section_profiles", {}).get(section, {})
    paragraph_rule = next((rule for rule in profile.get("rules", []) if rule.get("id") == "paragraph-length"), {})
    observed = paragraph_rule.get("observed", {})
    actions = []
    if paragraphs and observed:
        current_median = median(sentence_count(value) for value in paragraphs)
        low = float(observed.get("min_card_median", 0))
        high = float(observed.get("max_card_median", 0))
        if low and current_median < low:
            actions.append({"type": "structural-diagnostic", "code": "paragraphs-shorter-than-corpus-range", "observed": current_median, "target_range": [low, high], "recommendation": "Check whether short paragraphs need an explicit claim, warrant, or transition; do not pad mechanically.", "locators": target.get("locators", [])[:10]})
        elif high and current_median > high:
            actions.append({"type": "structural-diagnostic", "code": "paragraphs-longer-than-corpus-range", "observed": current_median, "target_range": [low, high], "recommendation": "Check whether the paragraph contains multiple rhetorical moves that should be separated; do not split without preserving logic.", "locators": target.get("locators", [])[:10]})
    if not actions:
        actions.append({"type": "structural-diagnostic", "code": "no-range-alert", "recommendation": "Review rhetorical moves and citation placement against the confirmed profile; no automatic prose change is proposed.", "locators": target.get("locators", [])[:10]})
    return {
        "schema_version": "1.0",
        "status": "pass",
        "manuscript": str(manuscript),
        "style_profile_id": profile["style_profile_id"],
        "section": section,
        "actions": actions,
        "copy_boundary": "structural-only",
        "confirmation_required": False,
        "confirmation_mode": confirmation_mode,
        "errors": [],
        "policy": "Diagnostic plan only; it cannot copy source prose or apply edits.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--section", default="whole-document")
    parser.add_argument("--ai-decision", type=Path, help="Hash-bound decision from adjudicate_ai_reviews.py")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    value = None
    try:
        profile = load_json(args.profile)
        ai_decision = load_json(args.ai_decision) if args.ai_decision else None
        gate = evaluate_style_gate(profile, ai_decision=ai_decision, profile_sha256=sha256_path(args.profile))
        if gate["status"] != "pass":
            errors.extend(gate["errors"])
        elif not args.manuscript.is_file():
            errors.append(f"manuscript not found: {args.manuscript}")
        else:
            value = plan(args.manuscript, profile, args.section, gate["confirmation_mode"])
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"cannot build style revision plan: {exc}")
    if value is None:
        value = {"schema_version": "1.0", "status": "blocked", "manuscript": str(args.manuscript), "style_profile_id": "unknown", "section": args.section, "actions": [], "copy_boundary": "structural-only", "confirmation_required": True, "confirmation_mode": "none", "errors": errors}
    elif errors:
        value["status"] = "blocked"
        value["errors"] = errors
    output = None
    if args.output:
        try:
            write_json(args.output, value)
            output = str(args.output)
        except OSError as exc:
            value["status"] = "blocked"
            value.setdefault("errors", []).append(f"cannot write style revision plan: {exc}")
    result = {"status": value["status"], "output": output, "plan": value, "errors": value.get("errors", [])}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"actions: {len(value['actions'])}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
