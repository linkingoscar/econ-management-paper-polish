#!/usr/bin/env python3
"""Require explicit human confirmation before using a dynamic style profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from audit_corpus_gate import audit as audit_corpus
from audit_style_overlap import audit as audit_overlap
from writing_contract import load_json, validate_style_profile


def evaluate(profile: dict, *, manifest: Path | None = None, corpus: Path | None = None, candidate: Path | None = None, min_target: int = 5, min_field: int = 2, min_author: int = 1, max_age_days: int = 365, require_license: bool = False, require_fulltext: bool = False) -> dict:
    errors = validate_style_profile(profile)
    if not errors and profile.get("status") != "confirmed":
        errors.append("style profile is still a draft; human confirmation is required")
    if not errors and profile.get("human_confirmed") is not True:
        errors.append("human_confirmed must be true before revision use")
    confirmation = profile.get("confirmation", {})
    if not errors and (not confirmation.get("confirmed_at") or not confirmation.get("confirmed_by")):
        errors.append("confirmation must record confirmed_at and confirmed_by")
    corpus_report = None
    overlap_report = None
    if manifest:
        corpus_report = audit_corpus(load_json(manifest), min_target=min_target, min_field=min_field, min_author=min_author, max_age_days=max_age_days, require_license=require_license, require_fulltext=require_fulltext)
        errors.extend(corpus_report.get("errors", []))
    if corpus and candidate:
        overlap_report = audit_overlap(corpus, candidate, 8, 24)
        if overlap_report.get("status") != "pass":
            errors.append("candidate contains verbatim overlap with style corpus")
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "profile_id": profile.get("style_profile_id"),
        "human_confirmed": profile.get("human_confirmed", False),
        "decision": "safe-fix" if not errors else "author-required",
        "gate": "human-confirmed" if not errors else "human-confirmation-required",
        "errors": errors,
        "corpus_gate": corpus_report,
        "overlap_gate": overlap_report,
        "scope": "structural style observations only; this gate does not authorize copying source language",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--corpus", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--min-target", type=int, default=5)
    parser.add_argument("--min-field", type=int, default=2)
    parser.add_argument("--min-author", type=int, default=1)
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--require-license", action="store_true")
    parser.add_argument("--require-fulltext", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        profile = load_json(args.profile)
        result = evaluate(profile, manifest=args.manifest, corpus=args.corpus, candidate=args.candidate, min_target=args.min_target, min_field=args.min_field, min_author=args.min_author, max_age_days=args.max_age_days, require_license=args.require_license, require_fulltext=args.require_fulltext)
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
