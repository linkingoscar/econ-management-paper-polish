#!/usr/bin/env python3
"""Check whether paper-spine claims have explicit writing evidence references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from writing_contract import load_json, validate_paper_spine


CLAIM_ID_RE = re.compile(r"^CLM-[0-9A-Za-z_-]+$")
AUTHOR_ANCHOR_RE = re.compile(r"^(table|figure|result|appendix|data|user)-[0-9A-Za-z_-]+$", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_spine", type=Path)
    parser.add_argument("--evidence-pack", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        spine = load_json(args.paper_spine)
        errors.extend(validate_paper_spine(spine))
    except (OSError, json.JSONDecodeError) as exc:
        spine = None
        errors.append(f"cannot read paper spine: {exc}")
    evidence_ids: set[str] = set()
    if args.evidence_pack:
        try:
            evidence = load_json(args.evidence_pack)
            entries = evidence.get("entries", []) if isinstance(evidence, dict) else evidence
            if not isinstance(entries, list):
                errors.append("evidence pack entries must be an array")
            else:
                evidence_ids = {entry.get("claim_id") for entry in entries if isinstance(entry, dict)}
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read evidence pack: {exc}")

    claims: list[dict] = []
    missing: list[dict] = []
    if spine is not None and not errors:
        for claim in spine.get("contribution_chain", []):
            references = claim.get("evidence", [])
            unresolved = []
            for reference in references:
                if CLAIM_ID_RE.fullmatch(reference) and reference not in evidence_ids:
                    unresolved.append(reference)
                elif not CLAIM_ID_RE.fullmatch(reference) and not AUTHOR_ANCHOR_RE.fullmatch(reference):
                    unresolved.append(reference)
            record = {
                "claim_id": claim["claim_id"],
                "evidence_count": len(references),
                "unresolved": unresolved,
                "status": "pass" if references and not unresolved else "fail",
            }
            claims.append(record)
            if record["status"] == "fail":
                missing.append(record)
    if spine is not None and not spine.get("contribution_chain"):
        errors.append("contribution_chain must contain at least one claim for an evidence check")
    result = {
        "status": "pass" if not errors and not missing else "fail",
        "errors": errors,
        "claims": claims,
        "missing": missing,
        "evidence_ids": sorted(evidence_ids),
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for item in claims:
            print(f"- {item['claim_id']}: {item['status']} ({item['evidence_count']} evidence)")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
