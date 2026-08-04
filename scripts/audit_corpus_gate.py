#!/usr/bin/env python3
"""Audit corpus authorization, freshness, sample size, and extraction gates."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from writing_contract import load_json, validate_corpus_manifest, utc_now


KNOWN_LICENSE = {"verified", "known", "user-provided", "permission-granted", "public-domain", "mit", "cc-by", "cc-by-nc"}


def parse_time(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def audit(manifest: dict[str, Any], *, min_target: int, min_field: int, min_author: int, max_age_days: int, require_license: bool, require_fulltext: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    now = datetime.now(timezone.utc)
    items = manifest.get("items", [])
    roles = {"target-journal": 0, "field-or-topic": 0, "author-or-lab-exemplar": 0, "author-guideline": 0, "other": 0}
    extraction = {"fulltext": 0, "metadata-only": 0, "unsupported": 0}
    seen_hashes: dict[str, str] = {}
    for item in items:
        role = item.get("role", "other")
        roles[role] = roles.get(role, 0) + 1
        extraction[item.get("extraction", "unsupported")] = extraction.get(item.get("extraction", "unsupported"), 0) + 1
        digest = item.get("sha256")
        if digest in seen_hashes:
            warnings.append(f"duplicate content hash: {item.get('path')} and {seen_hashes[digest]}")
        elif digest:
            seen_hashes[digest] = item.get("path", "")
        if require_license and str(item.get("license_status", "")).strip().lower() not in KNOWN_LICENSE:
            errors.append(f"license status is not verified for {item.get('path')}: {item.get('license_status')}")
        if require_fulltext and item.get("use") == "structural-style-only" and item.get("extraction") != "fulltext":
            errors.append(f"style extraction is not fulltext: {item.get('path')}")
        accessed = parse_time(item.get("accessed_at") or manifest.get("created_at"))
        if accessed is None:
            errors.append(f"missing or invalid accessed_at: {item.get('path')}")
        elif (now - accessed).days > max_age_days:
            errors.append(f"stale corpus item: {item.get('path')}")
    if roles["target-journal"] < min_target:
        errors.append(f"target-journal sample is {roles['target-journal']}; minimum is {min_target}")
    if roles["field-or-topic"] < min_field:
        errors.append(f"field-or-topic sample is {roles['field-or-topic']}; minimum is {min_field}")
    if roles["author-or-lab-exemplar"] < min_author:
        errors.append(f"author-or-lab-exemplar sample is {roles['author-or-lab-exemplar']}; minimum is {min_author}")
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "generated_at": utc_now(),
        "counts": {"roles": roles, "extraction": extraction, "items": len(items)},
        "errors": errors,
        "warnings": warnings,
        "policy": {"min_target": min_target, "min_field": min_field, "min_author": min_author, "max_age_days": max_age_days, "require_license": require_license, "require_fulltext": require_fulltext},
        "scope": "corpus authorization/freshness/sample gate; it does not judge journal quality or substantive evidence",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--min-target", type=int, default=5)
    parser.add_argument("--min-field", type=int, default=2)
    parser.add_argument("--min-author", type=int, default=1)
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--require-license", action="store_true")
    parser.add_argument("--require-fulltext", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        manifest = load_json(args.manifest)
        errors = validate_corpus_manifest(manifest)
        result = audit(manifest, min_target=args.min_target, min_field=args.min_field, min_author=args.min_author, max_age_days=args.max_age_days, require_license=args.require_license, require_fulltext=args.require_fulltext) if not errors else {"schema_version": "1.0", "status": "fail", "errors": errors, "warnings": []}
    except (OSError, json.JSONDecodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "errors": [f"cannot read corpus manifest: {exc}"], "warnings": []}
    result["manifest"] = str(args.manifest)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in result.get("errors", []):
            print(f"- {error}")
        for warning in result.get("warnings", []):
            print(f"warning: {warning}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
