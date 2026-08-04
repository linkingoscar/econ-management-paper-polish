#!/usr/bin/env python3
"""Adjudicate isolated AI reviews without trusting model self-approval."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from ai_review_contract import RISK_POLICY, validate_ai_review, validate_ai_review_packet
from writing_contract import load_json, utc_now, write_json


def adjudicate(packet: dict, reviews: list[dict]) -> dict:
    if not isinstance(packet, dict):
        raise ValueError("AI review packet must be an object")
    errors = validate_ai_review_packet(packet)
    if packet.get("artifact", {}).get("truncated") is True:
        errors.append("truncated artifact cannot receive an AI approval decision")
    accepted: list[str] = []
    rejected: list[dict] = []
    reviewers: set[str] = set()
    for review in reviews:
        review_errors = validate_ai_review(review, packet)
        if not isinstance(review, dict):
            rejected.append({"review_id": "unknown", "errors": review_errors})
            continue
        reviewer_id = review.get("reviewer", {}).get("reviewer_id") if isinstance(review.get("reviewer"), dict) else None
        if reviewer_id in reviewers:
            review_errors.append("reviewer_id is not unique; reviews must be isolated")
        if review.get("verdict") != "approve":
            review_errors.append("review verdict is not approve")
        if any(item.get("status") != "pass" for item in review.get("checks", []) if isinstance(item, dict)):
            review_errors.append("all required checks must pass")
        if review_errors:
            rejected.append({"review_id": review.get("review_id", "unknown"), "errors": review_errors})
        else:
            reviewers.add(reviewer_id)
            accepted.append(review["review_id"])
    risk = packet.get("risk_level", "high")
    required = RISK_POLICY.get(risk, RISK_POLICY["high"])["required_reviews"]
    enough = len(accepted) >= required
    if risk == "high":
        status, decision = "blocked", "author-required"
        errors.append("high-risk scholarly meaning requires author confirmation even after AI review")
    elif errors or rejected or not enough:
        status, decision = "blocked", "blocked"
        if not enough:
            errors.append(f"requires {required} valid isolated reviews; received {len(accepted)}")
    else:
        status, decision = "pass", "ai-approved"
    return {
        "schema_version": "1.0", "decision_id": f"AIG-{uuid.uuid4().hex[:12]}", "packet_id": packet.get("packet_id", "unknown"),
        "artifact_kind": packet.get("artifact_kind", "unknown"), "artifact_sha256": packet.get("artifact", {}).get("sha256", ""),
        "risk_level": risk, "status": status, "decision": decision, "required_reviews": required,
        "accepted_reviews": accepted, "rejected_reviews": rejected, "generated_at": utc_now(), "errors": errors,
        "limitations": ["Approval is bound to the exact artifact hash.", "AI consensus is a process gate, not proof of factual truth.", "Protected facts and high-risk scholarly meaning remain author-controlled."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("reviews", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        packet = load_json(args.packet)
        decision = adjudicate(packet, [load_json(path) for path in args.reviews])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        decision = {"status": "fail", "decision": "blocked", "errors": [f"cannot adjudicate reviews: {exc}"]}
    output = None
    if args.output and decision.get("schema_version"):
        write_json(args.output, decision)
        output = str(args.output)
    result = {"status": decision["status"], "output": output, "decision": decision, "errors": decision.get("errors", [])}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"status: {result['status']} ({decision['decision']})")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
