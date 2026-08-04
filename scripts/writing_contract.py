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
STYLE_PROFILE_STATUSES = {"draft", "confirmed", "blocked"}
ISSUE_STATUSES = {"raised", "triaged", "proposed", "applied", "verified", "closed", "blocked"}
ISSUE_DECISIONS = {"safe-fix", "author-required", "invalid", "unresolved"}
SEVERITIES = {"cosmetic", "moderate", "major", "blocking"}
TASK_MODES = {"polish", "diagnose", "adapt", "review", "revise", "audit"}
DISCIPLINES = {"economics", "management", "finance", "accounting", "marketing", "information-systems", "public-administration", "mixed"}
ROUTE_LANGUAGES = {"zh-CN", "en-US", "bilingual", "unspecified"}
EVIDENCE_MODES = {"offline", "metadata", "web-verified", "user-provided-fulltext"}


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
    if value.get("status") not in STYLE_PROFILE_STATUSES:
        errors.append(f"status must be one of {sorted(STYLE_PROFILE_STATUSES)}")
    if not isinstance(value.get("human_confirmed"), bool):
        errors.append("human_confirmed must be boolean")
    confirmation = value.get("confirmation")
    if not isinstance(confirmation, dict):
        errors.append("confirmation must be an object")
    else:
        if not (confirmation.get("confirmed_at") is None or nonempty(confirmation.get("confirmed_at"))):
            errors.append("confirmation.confirmed_at must be a string or null")
        if not (confirmation.get("confirmed_by") is None or nonempty(confirmation.get("confirmed_by"))):
            errors.append("confirmation.confirmed_by must be a string or null")
        if not isinstance(confirmation.get("notes"), str):
            errors.append("confirmation.notes must be a string")
    if value.get("status") == "confirmed" and value.get("human_confirmed") is not True:
        errors.append("confirmed style profile must set human_confirmed=true")
    if value.get("human_confirmed") is True and value.get("status") != "confirmed":
        errors.append("human_confirmed=true requires status=confirmed")
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


def validate_route_card(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["route card must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("route_id", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("task_mode") not in TASK_MODES:
        errors.append(f"task_mode must be one of {sorted(TASK_MODES)}")
    if value.get("discipline") not in DISCIPLINES:
        errors.append(f"discipline must be one of {sorted(DISCIPLINES)}")
    if value.get("language") not in ROUTE_LANGUAGES:
        errors.append(f"language must be one of {sorted(ROUTE_LANGUAGES)}")
    if value.get("evidence_mode") not in EVIDENCE_MODES:
        errors.append(f"evidence_mode must be one of {sorted(EVIDENCE_MODES)}")
    if value.get("execution") not in {"serial", "bounded_parallel"}:
        errors.append("execution must be serial or bounded_parallel")
    if value.get("preservation") not in {"strict", "standard", "user-defined"}:
        errors.append("preservation must be strict, standard, or user-defined")
    if value.get("confidence") not in CONFIDENCES:
        errors.append(f"confidence must be one of {sorted(CONFIDENCES)}")
    for key in ("rationale", "unresolved"):
        if not list_of_strings(value.get(key, [])):
            errors.append(f"{key} must be an array of strings")
    if not isinstance(value.get("user_overrides", []), list):
        errors.append("user_overrides must be an array")
    return errors


def validate_capability_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["capability report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("run_id", "generated_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("overall_mode") not in {"Verified", "Documented", "Conceptual"}:
        errors.append("overall_mode must be Verified, Documented, or Conceptual")
    if not isinstance(value.get("checks"), list):
        errors.append("checks must be an array")
    if not list_of_strings(value.get("permissions")):
        errors.append("permissions must be an array of strings")
    if not list_of_strings(value.get("limitations")):
        errors.append("limitations must be an array of strings")
    if not nonempty(value.get("output_ceiling")):
        errors.append("output_ceiling must be a non-empty string")
    return errors


def validate_protected_snapshot(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["protected snapshot must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("snapshot_id", "source_path", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(value.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", value.get("sha256", "")):
        errors.append("sha256 must be a lowercase SHA-256 hex string")
    protected = value.get("protected")
    if not isinstance(protected, dict):
        errors.append("protected must be an object")
    else:
        for key in ("numbers", "citations", "variables"):
            if not isinstance(protected.get(key), dict):
                errors.append(f"protected.{key} must be an object")
        for key in ("latex_labels", "latex_refs", "locked_fragments"):
            if not list_of_strings(protected.get(key, [])):
                errors.append(f"protected.{key} must be an array of strings")
    if not isinstance(value.get("counts"), dict):
        errors.append("counts must be an object")
    return errors


def validate_checkpoint(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["checkpoint must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("run_id", "workspace_id", "updated_at", "last_stage"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("status") not in {"running", "pass", "blocked", "failed", "complete"}:
        errors.append("status is invalid")
    if not isinstance(value.get("artifacts"), dict):
        errors.append("artifacts must be an object")
    if not isinstance(value.get("errors", []), list):
        errors.append("errors must be an array")
    return errors


def validate_workspace_manifest(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["workspace manifest must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("workspace_id", "paper_id", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(value.get("paths"), dict):
        errors.append("paths must be an object")
    if not isinstance(value.get("policy"), dict):
        errors.append("policy must be an object")
    return errors


def validate_evidence_ledger(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["evidence ledger must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    entries = value.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be an array")
        return errors
    pairs: set[tuple[str, str]] = set()
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_id, source_id = entry.get("claim_id"), entry.get("source_id")
        if not isinstance(claim_id, str) or not claim_id.startswith("CLM-"):
            errors.append(f"{prefix}.claim_id must start with CLM-")
        if not isinstance(source_id, str) or not source_id.startswith("SRC-"):
            errors.append(f"{prefix}.source_id must start with SRC-")
        if isinstance(claim_id, str) and isinstance(source_id, str):
            pair = (claim_id, source_id)
            if pair in pairs:
                errors.append(f"{prefix} duplicates claim/source pair")
            pairs.add(pair)
        if not nonempty(entry.get("claim")):
            errors.append(f"{prefix}.claim must be non-empty")
        source = entry.get("source")
        if not isinstance(source, dict) or not nonempty(source.get("title")) or not nonempty(source.get("url")):
            errors.append(f"{prefix}.source must contain title and url")
        verification = entry.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{prefix}.verification must be an object")
        else:
            for key in ("level", "status", "checked_at", "support_scope"):
                if not nonempty(verification.get(key)):
                    errors.append(f"{prefix}.verification.{key} must be non-empty")
            if not isinstance(verification.get("limitations"), list):
                errors.append(f"{prefix}.verification.limitations must be an array")
        allowed_use = entry.get("allowed_use")
        if not list_of_strings(allowed_use):
            errors.append(f"{prefix}.allowed_use must be a non-empty array of strings")
        elif "direct_citation" in allowed_use:
            if not isinstance(verification, dict) or not isinstance(verification.get("locator"), dict):
                errors.append(f"{prefix}.direct_citation requires verification.locator")
    if not isinstance(value.get("rejections", []), list):
        errors.append("rejections must be an array")
    if not isinstance(value.get("source_index", {}), dict):
        errors.append("source_index must be an object")
    return errors


def validate_corpus_gate_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["corpus gate report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    for key in ("errors", "warnings"):
        if not isinstance(value.get(key, []), list):
            errors.append(f"{key} must be an array")
    return errors


def validate_style_overlap_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["style overlap report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    if not isinstance(value.get("overlaps", []), list):
        errors.append("overlaps must be an array")
    return errors


def validate_evidence_freshness_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["evidence freshness report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    if not nonempty(value.get("generated_at")):
        errors.append("generated_at must be a non-empty string")
    if not isinstance(value.get("max_age_days"), int) or value.get("max_age_days") < 0:
        errors.append("max_age_days must be a non-negative integer")
    if not isinstance(value.get("counts"), dict):
        errors.append("counts must be an object")
    if not isinstance(value.get("findings", []), list):
        errors.append("findings must be an array")
    for key in ("errors", "warnings"):
        if not isinstance(value.get(key, []), list):
            errors.append(f"{key} must be an array")
    return errors


def validate_journal_freshness_report(value: Any) -> list[str]:
    return validate_evidence_freshness_report(value)


def validate_environment_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["environment report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    if not nonempty(value.get("generated_at")):
        errors.append("generated_at must be a non-empty string")
    for key in ("runtime", "capabilities"):
        if not isinstance(value.get(key), dict):
            errors.append(f"{key} must be an object")
    if not isinstance(value.get("checks", []), list):
        errors.append("checks must be an array")
    for key in ("errors", "limitations"):
        if not isinstance(value.get(key, []), list):
            errors.append(f"{key} must be an array")
    return errors


def validate_dogfood_manifest(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["dogfood manifest must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("policy") != "synthetic-fixtures-only":
        errors.append("policy must be synthetic-fixtures-only")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty array")
    return errors


def validate_response_validation_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["response validation report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    for key in ("ledger", "letter"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(value.get("counts"), dict):
        errors.append("counts must be an object")
    for key in ("errors", "warnings"):
        if not isinstance(value.get(key, []), list):
            errors.append(f"{key} must be an array")
    return errors


def validate_revision_matrix(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["revision matrix must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    for key in ("generated_at", "source_ledger"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(value.get("rows"), list):
        errors.append("rows must be an array")
    if not isinstance(value.get("counts"), dict):
        errors.append("counts must be an object")
    if not isinstance(value.get("errors", []), list):
        errors.append("errors must be an array")
    return errors


def validate_contract_suite_report(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["contract suite report must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("status") not in {"pass", "fail"}:
        errors.append("status must be pass or fail")
    if not nonempty(value.get("generated_at")):
        errors.append("generated_at must be a non-empty string")
    if not isinstance(value.get("environment"), dict):
        errors.append("environment must be an object")
    if not isinstance(value.get("commands"), list):
        errors.append("commands must be an array")
    if not isinstance(value.get("counts"), dict):
        errors.append("counts must be an object")
    if not isinstance(value.get("limitations", []), list):
        errors.append("limitations must be an array")
    return errors


def validate_ai_review_packet_contract(value: Any) -> list[str]:
    from ai_review_contract import validate_ai_review_packet
    return validate_ai_review_packet(value)


def validate_ai_review_contract(value: Any) -> list[str]:
    """Validate standalone review shape; packet binding is checked at adjudication."""
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["AI review must be an object"]
    for key in ("review_id", "packet_id", "artifact_kind", "artifact_sha256", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    if value.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("risk_level is invalid")
    if value.get("verdict") not in {"approve", "block", "escalate"}:
        errors.append("verdict is invalid")
    reviewer = value.get("reviewer")
    if not isinstance(reviewer, dict) or reviewer.get("kind") != "ai" or reviewer.get("isolated_pass") is not True:
        errors.append("reviewer must describe an isolated AI pass")
    if not isinstance(value.get("checks"), list) or not value.get("checks"):
        errors.append("checks must be a non-empty array")
    if not list_of_strings(value.get("limitations")):
        errors.append("limitations must be a non-empty array of strings")
    return errors


def validate_ai_gate_decision_contract(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["AI gate decision must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("decision_id", "packet_id", "artifact_kind", "artifact_sha256", "generated_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("status") not in {"pass", "fail", "blocked"}:
        errors.append("status is invalid")
    if value.get("decision") not in {"ai-approved", "blocked", "author-required"}:
        errors.append("decision is invalid")
    if not isinstance(value.get("required_reviews"), int) or value.get("required_reviews", 0) < 1:
        errors.append("required_reviews must be a positive integer")
    for key in ("accepted_reviews", "rejected_reviews", "errors", "limitations"):
        if not isinstance(value.get(key), list):
            errors.append(f"{key} must be an array")
    if value.get("risk_level") == "high" and value.get("decision") == "ai-approved":
        errors.append("high-risk decision cannot be ai-approved")
    return errors


def validate_writing_review_bundle(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["writing review bundle must be an object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be '1.0'")
    for key in ("bundle_id", "created_at"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    for key in ("original", "revised"):
        document = value.get(key)
        if not isinstance(document, dict):
            errors.append(f"{key} must be an object")
            continue
        if not nonempty(document.get("path")) or not isinstance(document.get("content"), str):
            errors.append(f"{key} must contain path and content")
        if not isinstance(document.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", document.get("sha256", "")):
            errors.append(f"{key}.sha256 must be a lowercase SHA-256 digest")
    if not isinstance(value.get("context"), dict):
        errors.append("context must be an object")
    if not list_of_strings(value.get("review_scope")):
        errors.append("review_scope must be a non-empty array of strings")
    return errors
