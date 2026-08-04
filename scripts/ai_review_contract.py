#!/usr/bin/env python3
"""Shared, deterministic checks for bounded AI writing-review gates."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from writing_contract import nonempty


RISK_POLICY = {
    "low": {"required_reviews": 1, "decision": "ai-approved"},
    "medium": {"required_reviews": 2, "decision": "ai-approved"},
    "high": {"required_reviews": 2, "decision": "author-required"},
}
KIND_RISK = {
    "route-card": "low",
    "paper-spine": "medium",
    "style-profile": "medium",
    "journal-card": "medium",
    "response-letter": "medium",
    "writing-rubric": "medium",
    "meaning-change": "high",
}
ARTIFACT_KINDS = set(KIND_RISK)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_ai_review_packet(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["AI review packet must be an object"]
    if value.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    for key in ("packet_id", "artifact_kind", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("artifact_kind") not in ARTIFACT_KINDS:
        errors.append("artifact_kind is invalid")
    artifact = value.get("artifact")
    if not isinstance(artifact, dict):
        errors.append("artifact must be an object")
    else:
        if not nonempty(artifact.get("path")) or not isinstance(artifact.get("content"), str):
            errors.append("artifact must contain path and content")
        digest = artifact.get("sha256", "")
        if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            errors.append("artifact.sha256 must be a SHA-256 digest")
    risk = value.get("risk_level")
    if risk not in RISK_POLICY:
        errors.append("risk_level must be low, medium, or high")
    elif value.get("artifact_kind") in KIND_RISK and risk != KIND_RISK[value["artifact_kind"]]:
        errors.append("risk_level does not match the fixed artifact policy")
    checks = value.get("required_checks")
    if not isinstance(checks, list) or not checks:
        errors.append("required_checks must be a non-empty array")
    elif any(not isinstance(item, dict) or not nonempty(item.get("check_id")) for item in checks):
        errors.append("every required check must have check_id")
    policy = value.get("review_policy")
    if not isinstance(policy, dict):
        errors.append("review_policy must be an object")
    elif risk in RISK_POLICY:
        expected = RISK_POLICY[risk]
        if policy.get("minimum_reviews") != expected["required_reviews"]:
            errors.append("review_policy.minimum_reviews does not match fixed risk policy")
        if policy.get("terminal_decision") != expected["decision"]:
            errors.append("review_policy.terminal_decision does not match fixed risk policy")
        for key in ("isolated_passes", "unanimous_approval", "hash_binding"):
            if policy.get(key) is not True:
                errors.append(f"review_policy.{key} must be true")
    return errors


def validate_ai_review(value: Any, packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["AI review must be an object"]
    if value.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    for key in ("review_id", "packet_id", "artifact_kind", "artifact_sha256", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    expected = {
        "packet_id": packet.get("packet_id"),
        "artifact_kind": packet.get("artifact_kind"),
        "artifact_sha256": packet.get("artifact", {}).get("sha256"),
        "risk_level": packet.get("risk_level"),
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{key} does not match packet")
    reviewer = value.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("reviewer must be an object")
    else:
        if reviewer.get("kind") != "ai" or reviewer.get("isolated_pass") is not True:
            errors.append("reviewer must be an isolated AI pass")
        for key in ("reviewer_id", "provider", "model"):
            if not nonempty(reviewer.get(key)):
                errors.append(f"reviewer.{key} must be a non-empty string")
    if value.get("verdict") not in {"approve", "block", "escalate"}:
        errors.append("verdict is invalid")
    checks = value.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be an array")
    else:
        by_id = {item.get("check_id"): item for item in checks if isinstance(item, dict)}
        for required in packet.get("required_checks", []):
            check_id = required.get("check_id")
            item = by_id.get(check_id)
            if not isinstance(item, dict):
                errors.append(f"missing required check: {check_id}")
                continue
            if item.get("status") not in {"pass", "fail", "unknown"}:
                errors.append(f"check {check_id} has invalid status")
            if not nonempty(item.get("reason")):
                errors.append(f"check {check_id} must include a reason")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence or not all(nonempty(x) for x in evidence):
                errors.append(f"check {check_id} must include evidence")
    limitations = value.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(nonempty(x) for x in limitations):
        errors.append("limitations must be a non-empty array of strings")
    return errors


def validate_ai_gate_decision(value: Any, *, artifact_kind: str, artifact_sha256: str, minimum_reviews: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["AI gate decision must be an object"]
    if value.get("schema_version") != "1.0":
        errors.append("AI gate schema_version must be '1.0'")
    if value.get("artifact_kind") != artifact_kind:
        errors.append(f"AI gate artifact_kind must be {artifact_kind}")
    expected_risk = KIND_RISK.get(artifact_kind)
    if value.get("risk_level") != expected_risk:
        errors.append(f"AI gate risk_level must be {expected_risk}")
    if value.get("artifact_sha256") != artifact_sha256:
        errors.append("AI gate artifact hash does not match current file")
    if value.get("status") != "pass" or value.get("decision") != "ai-approved":
        errors.append("AI gate decision must be pass/ai-approved")
    if value.get("risk_level") == "high":
        errors.append("high-risk artifacts cannot be AI-approved")
    accepted = value.get("accepted_reviews")
    if not isinstance(accepted, list) or len(set(accepted)) < minimum_reviews:
        errors.append(f"AI gate requires at least {minimum_reviews} accepted isolated reviews")
    if value.get("required_reviews", 0) < minimum_reviews:
        errors.append("AI gate required_reviews is below policy")
    if value.get("rejected_reviews"):
        errors.append("AI gate contains rejected reviews")
    if value.get("errors"):
        errors.append("AI gate contains adjudication errors")
    return errors
