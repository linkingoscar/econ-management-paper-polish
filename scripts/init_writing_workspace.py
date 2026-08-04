#!/usr/bin/env python3
"""Initialize a non-destructive v3.1 writing workspace.

The initializer creates state directories and contracts but never copies or
rewrites a manuscript. Existing workspaces must be passed with --reuse.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from writing_contract import utc_now, validate_capability_report, validate_checkpoint, validate_route_card, validate_workspace_manifest, write_json


def slug(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z_-]+", "-", value.strip()).strip("-").lower() or "paper"


def initialize(root: Path, paper_id: str, reuse: bool) -> dict:
    root = root.resolve()
    manifest_path = root / "workspace-manifest.json"
    if manifest_path.exists() and not reuse:
        raise FileExistsError(f"workspace already exists; pass --reuse to continue: {manifest_path}")
    directories = ["manuscript", "corpus", "style-cards", "evidence", "review", "patches", "audits", "runs"]
    for directory in directories:
        (root / directory).mkdir(parents=True, exist_ok=True)
    now = utc_now()
    workspace_id = f"WS-{slug(paper_id)}-{now.replace(':', '').replace('-', '')[:15]}"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        workspace_id = manifest.get("workspace_id", workspace_id)
    else:
        manifest = {
            "schema_version": "1.0",
            "workspace_id": workspace_id,
            "paper_id": paper_id,
            "created_at": now,
            "paths": {
                "intake": "intake.json",
                "paper_spine": "paper-spine.json",
                "route_card": "route-card.json",
                "capability_report": "capability-report.json",
                "checkpoint": "checkpoint.json",
                "protected_snapshot": "protected-snapshot.json",
                "revision_journal": "revision-journal.jsonl",
                "original_manuscript": "manuscript/original.md",
                "current_manuscript": "manuscript/current.md",
                "evidence": "evidence/evidence-pack.json",
                "style_profile": "style-profile.json",
                "review_ledger": "review/review-ledger.json",
            },
            "policy": {
                "execution": "serial",
                "network": "off-by-default",
                "auto_apply": False,
                "copy_boundary": "structural-only",
                "author_confirmation_for": ["meaning", "method", "theory", "result", "contribution"],
            },
        }
        write_json(manifest_path, manifest)
    errors = validate_workspace_manifest(manifest)
    if errors:
        raise ValueError("invalid workspace manifest: " + "; ".join(errors))

    route_path = root / "route-card.json"
    if not route_path.exists():
        route = {
            "schema_version": "1.0",
            "route_id": f"ROUTE-{workspace_id}",
            "paper_id": paper_id,
            "task_mode": "audit",
            "discipline": "mixed",
            "subfield": None,
            "language": "unspecified",
            "section": None,
            "method": None,
            "target_outlet": None,
            "evidence_mode": "offline",
            "execution": "serial",
            "preservation": "strict",
            "confidence": "unknown",
            "rationale": ["Workspace initialized without inferring paper discipline or method."],
            "unresolved": ["Populate the route card before a substantive revision."],
            "user_overrides": [],
            "created_at": now,
        }
        write_json(route_path, route)
    else:
        route = json.loads(route_path.read_text(encoding="utf-8"))
    route_errors = validate_route_card(route)

    intake_path = root / manifest["paths"].get("intake", "intake.json")
    if not intake_path.exists():
        write_json(intake_path, {
            "schema_version": "1.0",
            "intake_id": f"INTAKE-{workspace_id}",
            "workspace_id": workspace_id,
            "status": "unreviewed",
            "route_card": "route-card.json",
            "rationale": route.get("rationale", []),
            "unresolved": route.get("unresolved", []),
            "user_overrides": route.get("user_overrides", []),
            "created_at": now,
            "policy": "The route is a persistent input contract; downstream scripts do not infer it again.",
        })

    capability_path = root / "capability-report.json"
    if not capability_path.exists():
        capability = {
            "schema_version": "1.0",
            "run_id": f"INIT-{workspace_id}",
            "generated_at": now,
            "overall_mode": "Documented",
            "checks": [],
            "permissions": ["filesystem:workspace-write"],
            "limitations": ["No manuscript, source database, or external model was supplied during initialization."],
            "output_ceiling": "Workspace scaffolding only; no claim, method, citation, or replication conclusion.",
        }
        write_json(capability_path, capability)
    else:
        capability = json.loads(capability_path.read_text(encoding="utf-8"))
    capability_errors = validate_capability_report(capability)

    checkpoint_path = root / "checkpoint.json"
    if not checkpoint_path.exists():
        checkpoint = {
            "schema_version": "1.0",
            "run_id": f"INIT-{workspace_id}",
            "workspace_id": workspace_id,
            "updated_at": now,
            "last_stage": "initialized",
            "next_stage": "route",
            "status": "pass",
            "artifacts": {"workspace_manifest": "workspace-manifest.json", "route_card": "route-card.json"},
            "errors": [],
        }
        write_json(checkpoint_path, checkpoint)
    else:
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    checkpoint_errors = validate_checkpoint(checkpoint)

    journal_path = root / "revision-journal.jsonl"
    if not journal_path.exists():
        journal_path.write_text(json.dumps({"schema_version": "1.0", "run_id": f"INIT-{workspace_id}", "stage": "initialized", "status": "pass", "at": now, "event": "workspace-created"}, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "status": "pass" if not route_errors and not capability_errors and not checkpoint_errors else "fail",
        "workspace": manifest,
        "route_errors": route_errors,
        "capability_errors": capability_errors,
        "checkpoint_errors": checkpoint_errors,
        "output": str(root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--paper-id", default="paper-unknown")
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = initialize(args.workspace, args.paper_id, args.reuse)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "errors": [str(exc)]}
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"status: fail\n- {exc}")
        return 1
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"workspace: {result['output']}")
        for key in ("route_errors", "capability_errors", "checkpoint_errors"):
            for error in result[key]:
                print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
