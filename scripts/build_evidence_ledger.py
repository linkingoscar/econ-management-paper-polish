#!/usr/bin/env python3
"""Build a many-to-many, locator-aware writing evidence ledger.

Metadata candidates remain useful for search, but they cannot be emitted as
direct-citation evidence. This script validates provenance and records rejected
bindings instead of silently dropping them.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from writing_contract import write_json


CLAIM_RE = re.compile(r"^CLM-[0-9A-Za-z_-]+$")
SOURCE_RE = re.compile(r"^SRC-[0-9A-Za-z_-]+$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
LEVELS = {"full_text", "official_page", "metadata", "candidate"}
STATUSES = {"verified", "metadata-only", "candidate", "rejected", "stale"}
USES = {"direct_citation", "background_only", "method-diagnosis", "candidate_only", "do_not_cite"}


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def raw_entries(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("entries"), list):
        return value["entries"]
    raise ValueError("input must be an array or an object with an entries array")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(raw: Any) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    rejections: list[dict[str, Any]] = []
    source_index: dict[str, dict[str, Any]] = {}
    doi_index: dict[str, str] = {}
    seen_pairs: set[tuple[str, str]] = set()
    for index, item in enumerate(raw_entries(raw)):
        prefix = f"entries[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        entry = dict(item)
        claim_id = entry.get("claim_id")
        source = dict(entry.get("source") or {})
        source_id = entry.get("source_id") or source.get("source_id")
        verification = dict(entry.get("verification") or {})
        allowed_use = entry.get("allowed_use", ["direct_citation"])
        if isinstance(allowed_use, str):
            allowed_use = [allowed_use]
        status = verification.get("status", "verified" if verification.get("level") in {"full_text", "official_page"} else "metadata-only")
        level = verification.get("level", "metadata")
        if not isinstance(claim_id, str) or not CLAIM_RE.fullmatch(claim_id):
            errors.append(f"{prefix}.claim_id must match CLM-<id>")
        if not isinstance(source_id, str) or not SOURCE_RE.fullmatch(source_id):
            errors.append(f"{prefix}.source_id must match SRC-<id>")
        if not isinstance(entry.get("claim"), str) or not entry["claim"].strip():
            errors.append(f"{prefix}.claim must be a non-empty string")
        if not isinstance(source.get("title"), str) or not source["title"].strip():
            errors.append(f"{prefix}.source.title must be a non-empty string")
        if not isinstance(source.get("url"), str) or not re.match(r"^https?://", source["url"]):
            errors.append(f"{prefix}.source.url must start with http:// or https://")
        if source.get("doi") is not None and (not isinstance(source.get("doi"), str) or not DOI_RE.fullmatch(source["doi"].strip())):
            errors.append(f"{prefix}.source.doi is not a valid DOI-shaped string")
        if isinstance(source.get("doi"), str) and DOI_RE.fullmatch(source["doi"].strip()):
            doi = source["doi"].strip().lower()
            previous_source = doi_index.get(doi)
            if previous_source and previous_source != source_id:
                errors.append(f"{prefix}.source.doi duplicates source_id {previous_source}")
            else:
                doi_index[doi] = source_id
        if level not in LEVELS:
            errors.append(f"{prefix}.verification.level must be one of {sorted(LEVELS)}")
        if status not in STATUSES:
            errors.append(f"{prefix}.verification.status must be one of {sorted(STATUSES)}")
        if not isinstance(verification.get("checked_at"), str) or not verification["checked_at"].strip():
            errors.append(f"{prefix}.verification.checked_at must be non-empty")
        if not isinstance(allowed_use, list) or not allowed_use or any(use not in USES for use in allowed_use):
            errors.append(f"{prefix}.allowed_use must be a non-empty array from {sorted(USES)}")
        locator = verification.get("locator")
        if not isinstance(locator, dict) or not any(str(value).strip() for value in locator.values() if value is not None):
            if "direct_citation" in allowed_use:
                errors.append(f"{prefix}.verification.locator is required for direct_citation")
        support_scope = verification.get("support_scope")
        if not isinstance(support_scope, str) or not support_scope.strip():
            errors.append(f"{prefix}.verification.support_scope must be non-empty")
        limitations = verification.get("limitations", [])
        if not isinstance(limitations, list) or any(not isinstance(value, str) or not value.strip() for value in limitations):
            errors.append(f"{prefix}.verification.limitations must be an array of strings")
        if isinstance(claim_id, str) and isinstance(source_id, str):
            pair = (claim_id, source_id)
            if pair in seen_pairs:
                errors.append(f"{prefix} duplicates claim/source binding {claim_id}/{source_id}")
            seen_pairs.add(pair)
        entry["source_id"] = source_id
        source["source_id"] = source_id
        verification["status"] = status
        verification["level"] = level
        entry["source"] = source
        entry["verification"] = verification
        entry["allowed_use"] = allowed_use
        if status in {"rejected", "candidate", "stale", "metadata-only"} and "direct_citation" in allowed_use:
            rejections.append({"claim_id": claim_id, "source_id": source_id, "reason": f"{status} evidence cannot be direct citation", "action": "downgrade or verify before citing"})
            errors.append(f"{prefix} direct_citation is incompatible with verification.status={status}")
        if isinstance(source_id, str):
            source_index.setdefault(source_id, source)
        entries.append(entry)
    pack = {"schema_version": "1.0", "generated_at": raw.get("generated_at", now()) if isinstance(raw, dict) else now(), "entries": entries, "rejections": rejections, "source_index": source_index}
    return pack, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        pack, errors = normalize(load(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        pack, errors = None, [f"cannot build evidence ledger: {exc}"]
    output = None
    if pack is not None and not errors and args.output:
        try:
            write_json(args.output, pack)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write evidence ledger: {exc}")
    result = {"status": "pass" if pack is not None and not errors else "fail", "errors": errors, "output": output, "ledger": pack}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if pack:
            print(f"entries: {len(pack['entries'])}; rejections: {len(pack['rejections'])}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
