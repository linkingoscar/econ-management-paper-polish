#!/usr/bin/env python3
"""Validate one v3.1 writing artifact using the dependency-free contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_contract import (
    load_json,
    validate_capability_report,
    validate_corpus_gate_report,
    validate_contract_suite_report,
    validate_dogfood_manifest,
    validate_environment_report,
    validate_evidence_freshness_report,
    validate_evidence_ledger,
    validate_checkpoint,
    validate_corpus_manifest,
    validate_paper_spine,
    validate_protected_snapshot,
    validate_provenance_manifest,
    validate_review_ledger,
    validate_route_card,
    validate_style_card,
    validate_style_profile,
    validate_style_overlap_report,
    validate_journal_freshness_report,
    validate_response_validation_report,
    validate_revision_matrix,
    validate_workspace_manifest,
)


VALIDATORS = {
    "corpus-manifest": validate_corpus_manifest,
    "paper-spine": validate_paper_spine,
    "provenance": validate_provenance_manifest,
    "review-ledger": validate_review_ledger,
    "style-card": validate_style_card,
    "style-profile": validate_style_profile,
    "route-card": validate_route_card,
    "capability-report": validate_capability_report,
    "protected-snapshot": validate_protected_snapshot,
    "checkpoint": validate_checkpoint,
    "workspace-manifest": validate_workspace_manifest,
    "evidence-ledger": validate_evidence_ledger,
    "corpus-gate-report": validate_corpus_gate_report,
    "style-overlap-report": validate_style_overlap_report,
    "evidence-freshness-report": validate_evidence_freshness_report,
    "journal-freshness-report": validate_journal_freshness_report,
    "environment-report": validate_environment_report,
    "dogfood-manifest": validate_dogfood_manifest,
    "response-validation-report": validate_response_validation_report,
    "revision-matrix": validate_revision_matrix,
    "contract-suite-report": validate_contract_suite_report,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(VALIDATORS))
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        value = load_json(args.input)
        errors = VALIDATORS[args.kind](value)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"cannot read JSON input: {exc}"]
    result = {"status": "pass" if not errors else "fail", "kind": args.kind, "input": str(args.input), "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
