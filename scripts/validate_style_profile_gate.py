#!/usr/bin/env python3
"""Require explicit human confirmation before using a dynamic style profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_contract import load_json, validate_style_profile


def evaluate(profile: dict) -> dict:
    errors = validate_style_profile(profile)
    if not errors and profile.get("status") != "confirmed":
        errors.append("style profile is still a draft; human confirmation is required")
    if not errors and profile.get("human_confirmed") is not True:
        errors.append("human_confirmed must be true before revision use")
    confirmation = profile.get("confirmation", {})
    if not errors and (not confirmation.get("confirmed_at") or not confirmation.get("confirmed_by")):
        errors.append("confirmation must record confirmed_at and confirmed_by")
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "profile_id": profile.get("style_profile_id"),
        "human_confirmed": profile.get("human_confirmed", False),
        "decision": "safe-fix" if not errors else "author-required",
        "gate": "human-confirmed" if not errors else "human-confirmation-required",
        "errors": errors,
        "scope": "structural style observations only; this gate does not authorize copying source language",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        profile = load_json(args.profile)
        result = evaluate(profile)
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "schema_version": "1.0",
            "status": "fail",
            "profile_id": None,
            "human_confirmed": False,
            "decision": "author-required",
            "gate": "human-confirmation-required",
            "errors": [f"cannot read style profile: {exc}"],
        }
    result["profile_file"] = str(args.profile)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"gate: {result['gate']}")
        for error in result.get("errors", []):
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
