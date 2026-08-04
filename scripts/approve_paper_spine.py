#!/usr/bin/env python3
"""Promote a candidate paper spine for structural use after AI consensus."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from ai_review_contract import sha256_path, validate_ai_gate_decision
from writing_contract import load_json, utc_now, validate_paper_spine, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spine", type=Path)
    parser.add_argument("ai_decision", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    value = None
    try:
        spine, decision = load_json(args.spine), load_json(args.ai_decision)
        errors.extend(validate_paper_spine(spine))
        errors.extend(validate_ai_gate_decision(decision, artifact_kind="paper-spine", artifact_sha256=sha256_path(args.spine), minimum_reviews=2))
        if not errors:
            value = deepcopy(spine)
            value["candidate_status"] = "ai-reviewed"
            value["review"] = {"mode": "ai-consensus", "decision_id": decision["decision_id"], "review_ids": decision["accepted_reviews"], "reviewed_at": utc_now()}
            value["author_adoption_required"] = True
            for claim in value.get("contribution_chain", []):
                claim["status"] = "ai-reviewed-candidate"
                claim["confirmation_required"] = False
                claim["author_adoption_required"] = True
            write_json(args.output, value)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot approve paper spine: {exc}")
    result = {"status": "pass" if value is not None and not errors else "blocked", "output": str(args.output) if value else None, "paper_spine": value, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"status: {result['status']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
