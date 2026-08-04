#!/usr/bin/env python3
"""Shared validators and helpers for the v3.1 writing contracts.

The module is deliberately dependency-free. It validates the small, persistent
artifacts that connect writing diagnosis, journal adaptation, evidence, and
reviewer response. It does not decide whether a claim is substantively true.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
CORPUS_ROLES = {"target-journal", "field-or-topic", "author-or-lab-exemplar", "author-guideline", "other"}
CORPUS_USES = {"structural-style-only", "journal-rule", "user-provided-evidence", "metadata-only"}
EXTRACTIONS = {"fulltext", "metadata-only", "unsupported"}
CONFIDENCES = {"high", "medium", "low", "unknown"}
STYLE_STATUSES = {"observed", "inferred", "conflict", "unknown"}
ISSUE_STATUSES = {"raised", "triaged", "proposed", "applied", "verified", "closed", "blocked"}
ISSUE_DECISIONS = {"safe-fix", "author-required", "invalid", "unresolved"}
SEVERITIES = {"cosmetic", "moderate", "major", "blocking"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def list_of_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def validate_corpus_manifest(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["corpus manifest must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("corpus_id", "created_at", "purpose"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    items = value.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
        return errors
    seen: set[str] = set()
    for index, item in enumerate(items):
        prefix = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("source_id", "path", "sha256", "license_status", "use"):
            if not nonempty(item.get(key)):
                errors.append(f"{prefix}.{key} must be a non-empty string")
        source_id = item.get("source_id")
        if isinstance(source_id, str):
            if source_id in seen:
                errors.append(f"{prefix}.source_id duplicates {source_id}")
            seen.add(source_id)
        if item.get("role") not in CORPUS_ROLES:
            errors.append(f"{prefix}.role must be one of {sorted(CORPUS_ROLES)}")
        if item.get("extraction") not in EXTRACTIONS:
            errors.append(f"{prefix}.extraction must be one of {sorted(EXTRACTIONS)}")
        if item.get("use") not in CORPUS_USES:
            errors.append(f"{prefix}.use must be one of {sorted(CORPUS_USES)}")
        if isinstance(item.get("sha256"), str) and not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            errors.append(f"{prefix}.sha256 must be a lowercase SHA-256 hex string")
        if not isinstance(item.get("readable"), bool):
            errors.append(f"{prefix}.readable must be boolean")
    rejections = value.get("rejections", [])
    if not isinstance(rejections, list):
        errors.append("rejections must be an array")
    return errors


def validate_style_card(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["style card must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("style_card_id", "source_id", "section"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(value.get("observations"), dict):
        errors.append("observations must be an object")
    if value.get("confidence") not in CONFIDENCES:
        errors.append(f"confidence must be one of {sorted(CONFIDENCES)}")
    if value.get("copy_boundary") != "structural-only":
        errors.append("copy_boundary must be structural-only")
    locators = value.get("locators", [])
    if not isinstance(locators, list):
        errors.append("locators must be an array")
    return errors


def validate_style_profile(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["style profile must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("style_profile_id", "reviewed_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not list_of_strings(value.get("inputs")):
        errors.append("inputs must be an array of non-empty strings")
    priority = value.get("priority_order")
    if priority != ["P1-preserve", "P2-target", "P3-secondary", "P4-static", "P5-cleanup"]:
        errors.append("priority_order must preserve P1 through P5 ordering")
    if value.get("copy_boundary") != "structural-only":
        errors.append("copy_boundary must be structural-only")
    if not isinstance(value.get("rules"), list):
        errors.append("rules must be an array")
    if not isinstance(value.get("conflicts"), list):
        errors.append("conflicts must be an array")
    return errors


def validate_paper_spine(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["paper spine must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if not nonempty(value.get("paper_id")):
        errors.append("paper_id must be a non-empty string")
    for key in ("research_question", "main_claim"):
        if key in value and value[key] is not None and not isinstance(value[key], str):
            errors.append(f"{key} must be a string or null")
    chain = value.get("contribution_chain")
    if not isinstance(chain, list):
        errors.append("contribution_chain must be an array")
        return errors
    seen: set[str] = set()
    for index, claim in enumerate(chain):
        prefix = f"contribution_chain[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("claim_id", "claim", "section"):
            if not nonempty(claim.get(key)):
                errors.append(f"{prefix}.{key} must be a non-empty string")
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str):
            if claim_id in seen:
                errors.append(f"{prefix}.claim_id duplicates {claim_id}")
            seen.add(claim_id)
        if not list_of_strings(claim.get("evidence", [])):
            errors.append(f"{prefix}.evidence must be an array of strings")
        if not list_of_strings(claim.get("method_dependency", [])):
            errors.append(f"{prefix}.method_dependency must be an array of strings")
        if claim.get("risk", "unknown") not in {"low", "medium", "high", "unknown"}:
            errors.append(f"{prefix}.risk is invalid")
    if not list_of_strings(value.get("open_questions", [])):
        errors.append("open_questions must be an array of strings")
    return errors


def validate_review_ledger(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["review ledger must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if not nonempty(value.get("generated_at")):
        errors.append("generated_at must be a non-empty string")
    issues = value.get("issues")
    if not isinstance(issues, list):
        errors.append("issues must be an array")
        return errors
    seen: set[str] = set()
    for index, issue in enumerate(issues):
        prefix = f"issues[{index}]"
        if not isinstance(issue, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("issue_id", "statement", "category", "severity", "decision", "status"):
            if not nonempty(issue.get(key)):
                errors.append(f"{prefix}.{key} must be a non-empty string")
        issue_id = issue.get("issue_id")
        if isinstance(issue_id, str):
            if issue_id in seen:
                errors.append(f"{prefix}.issue_id duplicates {issue_id}")
            seen.add(issue_id)
        if issue.get("severity") not in SEVERITIES:
            errors.append(f"{prefix}.severity must be one of {sorted(SEVERITIES)}")
        if issue.get("decision") not in ISSUE_DECISIONS:
            errors.append(f"{prefix}.decision must be one of {sorted(ISSUE_DECISIONS)}")
        if issue.get("status") not in ISSUE_STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(ISSUE_STATUSES)}")
        if not list_of_strings(issue.get("preserve", [])):
            errors.append(f"{prefix}.preserve must be an array of strings")
        if not isinstance(issue.get("history", []), list):
            errors.append(f"{prefix}.history must be an array")
    return errors


def validate_provenance_manifest(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["provenance manifest must be an object"]
    for key in ("component", "source_url", "source_commit", "license", "status", "last_tested"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if nonempty(value.get("source_url")) and not re.match(r"^https?://", value["source_url"]):
        errors.append("source_url must start with http:// or https://")
    capabilities = value.get("capabilities")
    if not list_of_strings(capabilities):
        errors.append("capabilities must be an array of strings")
    if value.get("status") not in {"verified", "documented", "conceptual"}:
        errors.append("status must be verified, documented, or conceptual")
    return errors
