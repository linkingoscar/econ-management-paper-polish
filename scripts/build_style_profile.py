#!/usr/bin/env python3
"""Aggregate deterministic style cards into a writing-only style profile.

The profile reports observed structural tendencies and conflicts. It does not
produce target-journal prose or store reusable source sentences.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from writing_contract import load_json, utc_now, validate_style_card, validate_style_profile, write_json


PRIORITY_ORDER = ["P1-preserve", "P2-target", "P3-secondary", "P4-static", "P5-cleanup"]
ROLE_WEIGHTS = {
    "target-journal": 3.0,
    "author-guideline": 3.0,
    "field-or-topic": 2.0,
    "author-or-lab-exemplar": 1.0,
    "other": 1.0,
}


def load_cards(directory: Path) -> tuple[list[dict[str, Any]], list[str]]:
    cards: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(directory.glob("STY-*.json")):
        try:
            card = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: cannot read JSON ({exc})")
            continue
        card_errors = validate_style_card(card)
        if card_errors:
            errors.extend(f"{path.name}: {error}" for error in card_errors)
        else:
            cards.append(card)
    if not cards:
        errors.append("cards directory contains no valid style cards")
    return cards, errors


def weighted_mean(values: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in values)
    return sum(value * weight for value, weight in values) / total_weight if total_weight else 0.0


def support_locators(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"style_card_id": card["style_card_id"], "source_id": card.get("source_id"), "locators": card.get("locators", [])[:20]}
        for card in cards
    ]


def build_profile(cards: list[dict[str, Any]], outlet: str | None, source_roles: dict[str, str] | None = None) -> dict[str, Any]:
    source_roles = source_roles or {}
    move_counts: dict[str, list[tuple[float, float]]] = {}
    paragraph_stats: list[tuple[dict[str, Any], float]] = []
    citation_stats: list[tuple[float, float]] = []
    for card in cards:
        weight = ROLE_WEIGHTS.get(source_roles.get(card.get("source_id"), "other"), 1.0)
        observations = card.get("observations", {})
        for move, value in observations.get("rhetorical_moves", {}).items():
            if isinstance(value, dict) and isinstance(value.get("share"), (int, float)):
                move_counts.setdefault(move, []).append((float(value["share"]), weight))
        paragraph = observations.get("paragraph_length", {})
        if isinstance(paragraph, dict) and isinstance(paragraph.get("median_sentences"), (int, float)):
            paragraph_stats.append((paragraph, weight))
        citation = observations.get("citation_behavior", {})
        if isinstance(citation, dict) and isinstance(citation.get("citation_density"), (int, float)):
            citation_stats.append((float(citation["citation_density"]), weight))

    rules: list[dict[str, Any]] = []
    if move_counts:
        rules.append({
            "id": "rhetorical-moves",
            "priority": "P2-target",
            "status": "observed",
            "recommendation": "Use observed rhetorical moves as a diagnostic checklist; do not copy source wording.",
            "observed": {
                move: {
                    "mean_share": round(weighted_mean(values), 3),
                    "card_count": len(values),
                }
                for move, values in sorted(move_counts.items())
            },
            "support": [card["style_card_id"] for card in cards],
            "support_locators": support_locators(cards),
        })
    if paragraph_stats:
        medians = [float(item["median_sentences"]) for item, _ in paragraph_stats]
        rule = {
            "id": "paragraph-length",
            "priority": "P2-target",
            "status": "observed",
            "recommendation": "Use paragraph length as a range for diagnosis, never as a hard rewrite constraint.",
            "observed": {
                "mean_card_median": round(weighted_mean([(value, weight) for (item, weight), value in zip(paragraph_stats, medians)]), 2),
                "min_card_median": min(medians),
                "max_card_median": max(medians),
            },
            "support": [card["style_card_id"] for card in cards],
            "support_locators": support_locators(cards),
        }
        rules.append(rule)
    if citation_stats:
        rules.append({
            "id": "citation-density",
            "priority": "P2-target",
            "status": "observed",
            "recommendation": "Check whether citations appear where claims require them; do not add citations to match a numeric target.",
            "observed": {
                "mean_density": round(weighted_mean(citation_stats), 3),
                "card_count": len(citation_stats),
            },
            "support": [card["style_card_id"] for card in cards],
            "support_locators": support_locators(cards),
        })

    conflicts: list[dict[str, Any]] = []
    if paragraph_stats and max(float(item["median_sentences"]) for item, _ in paragraph_stats) - min(float(item["median_sentences"]) for item, _ in paragraph_stats) >= 3:
        conflicts.append({
            "field": "paragraph_length",
            "candidates": sorted({float(item["median_sentences"]) for item, _ in paragraph_stats}),
            "decision": "report-range-do-not-hard-code",
            "rationale": "The supplied corpus has materially different paragraph lengths.",
        })
    if len({card.get("confidence") for card in cards}) > 1:
        conflicts.append({
            "field": "confidence",
            "candidates": sorted({card.get("confidence") for card in cards}),
            "decision": "retain-card-level-confidence",
            "rationale": "Heuristic extraction confidence differs across source files.",
        })

    reviewed = utc_now()
    reviewed_dt = datetime.fromisoformat(reviewed.replace("Z", "+00:00"))
    recheck_after = (reviewed_dt + timedelta(days=180)).date().isoformat()
    slug = re.sub(r"[^0-9A-Za-z_-]+", "-", (outlet or "writing").strip()).strip("-").lower() or "writing"
    section_profiles: dict[str, dict[str, Any]] = {}
    for card in cards:
        section = card.get("section", "whole-document")
        observations = card.get("observations", {})
        section_profiles.setdefault(section, {"inputs": [], "rhetorical_moves": {}, "locators": []})
        section_profiles[section]["inputs"].append(card["style_card_id"])
        section_profiles[section]["locators"].extend(card.get("locators", [])[:20])
        for move, value in observations.get("rhetorical_moves", {}).items():
            if isinstance(value, dict) and isinstance(value.get("share"), (int, float)):
                section_profiles[section]["rhetorical_moves"].setdefault(move, []).append(value["share"])
    for section, value in section_profiles.items():
        value["rhetorical_moves"] = {move: round(sum(shares) / len(shares), 3) for move, shares in value["rhetorical_moves"].items()}
        value["locators"] = value["locators"][:50]
    profile = {
        "schema_version": "1.0",
        "style_profile_id": f"PRO-{slug}-{reviewed[:10]}",
        "target_outlet": outlet or "unspecified",
        "inputs": [card["style_card_id"] for card in cards],
        "priority_order": PRIORITY_ORDER,
        "rules": rules,
        "conflicts": conflicts,
        "copy_boundary": "structural-only",
        "status": "draft",
        "human_confirmed": False,
        "confirmation": {
            "confirmed_at": None,
            "confirmed_by": None,
            "notes": "Profile is a structural draft. A human must review conflicts, source roles, and copyright boundary before revision use.",
        },
        "reviewed_at": reviewed,
        "recheck_after": recheck_after,
        "source_policy": "observed-structure-only",
        "source_roles": source_roles,
        "role_weights": ROLE_WEIGHTS,
        "section_profiles": section_profiles,
    }
    return profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cards", type=Path, help="Directory of STY-*.json style cards")
    parser.add_argument("--manifest", type=Path, help="Optional corpus manifest to cross-check source IDs")
    parser.add_argument("--target-outlet", default=None)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    if not args.cards.is_dir():
        errors.append(f"cards directory is not a directory: {args.cards}")
        cards = []
    else:
        cards, card_errors = load_cards(args.cards)
        errors.extend(card_errors)
    source_roles: dict[str, str] = {}
    if args.manifest and args.manifest.exists() and cards:
        try:
            manifest = load_json(args.manifest)
            source_ids = {item.get("source_id") for item in manifest.get("items", []) if isinstance(item, dict)}
            source_roles = {item.get("source_id"): item.get("role", "other") for item in manifest.get("items", []) if isinstance(item, dict)}
            for card in cards:
                if card.get("source_id") not in source_ids:
                    errors.append(f"{card['style_card_id']}: source_id is absent from corpus manifest")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read manifest: {exc}")
    profile = build_profile(cards, args.target_outlet, source_roles) if cards else None
    if profile is not None:
        errors.extend(validate_style_profile(profile))
    output = None
    if profile is not None and not errors and args.output:
        try:
            write_json(args.output, profile)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write style profile: {exc}")
    result = {"status": "pass" if profile is not None and not errors else "fail", "errors": errors, "output": output, "style_profile": profile}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if profile:
            print(f"style_profile_id: {profile['style_profile_id']}")
            print(f"rules: {len(profile['rules'])}")
            print(f"conflicts: {len(profile['conflicts'])}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
