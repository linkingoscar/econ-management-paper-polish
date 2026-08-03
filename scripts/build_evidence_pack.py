#!/usr/bin/env python3
"""Validate and normalize an evidence ledger into the v3 evidence-pack shape.

The script does not decide whether a source supports a claim. It checks that a
human or retrieval step supplied enough provenance to make that decision
auditable, and rejects citation uses that are marked as candidates or rejected.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CLAIM_ID_RE = re.compile(r"^CLM-[0-9A-Za-z_-]+$")
LEVELS = {"full_text", "official_page", "metadata", "candidate", "rejected"}
ALLOWED_USES = {"direct_citation", "background_only", "candidate_only", "do_not_cite"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_entries(raw: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if isinstance(raw, list):
        entries = raw
    elif isinstance(raw, dict) and isinstance(raw.get("entries"), list):
        entries = raw["entries"]
    else:
        return [], ["input must be a JSON array or an object with an entries array"]

    errors: list[str] = []
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_id = entry.get("claim_id")
        claim = entry.get("claim")
        source = entry.get("source")
        verification = entry.get("verification")
        allowed_use = entry.get("allowed_use")
        if not isinstance(claim_id, str) or not CLAIM_ID_RE.fullmatch(claim_id):
            errors.append(f"{prefix}.claim_id must match CLM-<id>")
        elif claim_id in seen:
            errors.append(f"{prefix}.claim_id duplicates {claim_id}")
        else:
            seen.add(claim_id)
        if not isinstance(claim, str) or not claim.strip():
            errors.append(f"{prefix}.claim must be a non-empty string")
        if not isinstance(source, dict):
            errors.append(f"{prefix}.source must be an object")
        else:
            if not isinstance(source.get("title"), str) or not source["title"].strip():
                errors.append(f"{prefix}.source.title must be a non-empty string")
            url = source.get("url")
            if not isinstance(url, str) or not re.match(r"^https?://", url):
                errors.append(f"{prefix}.source.url must start with http:// or https://")
        if not isinstance(verification, dict):
            errors.append(f"{prefix}.verification must be an object")
        else:
            if verification.get("level") not in LEVELS:
                errors.append(f"{prefix}.verification.level must be one of {sorted(LEVELS)}")
            if not isinstance(verification.get("checked_at"), str) or not verification["checked_at"].strip():
                errors.append(f"{prefix}.verification.checked_at must be a non-empty string")
        if allowed_use not in ALLOWED_USES:
            errors.append(f"{prefix}.allowed_use must be one of {sorted(ALLOWED_USES)}")
        elif allowed_use == "direct_citation" and isinstance(verification, dict):
            level = verification.get("level")
            if level not in {"full_text", "official_page"}:
                errors.append(f"{prefix} direct_citation requires full_text or official_page verification")
        normalized.append(entry)
    return normalized, errors


def build_pack(raw: Any) -> tuple[dict[str, Any], list[str]]:
    entries, errors = validate_entries(raw)
    generated_at = None
    if isinstance(raw, dict):
        generated_at = raw.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at.strip():
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    pack = {"schema_version": "1.0", "generated_at": generated_at, "entries": entries}
    return pack, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, help="Write the normalized pack to this JSON file")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit a machine-readable validation report")
    args = parser.parse_args()

    try:
        raw = load_json(args.input)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "errors": [f"cannot read JSON input: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2

    pack, errors = build_pack(raw)
    status = "pass" if not errors else "fail"
    output_path = None
    if status == "pass" and args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            output_path = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write output: {exc}")
            status = "fail"

    result = {"status": status, "errors": errors, "output": output_path, "pack": pack}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif status == "pass":
        print(f"status: pass ({len(pack['entries'])} evidence entries)")
        if output_path:
            print(f"output: {output_path}")
        else:
            print(json.dumps(pack, ensure_ascii=False, indent=2))
    else:
        print("status: fail")
        for error in errors:
            print(f"- {error}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
