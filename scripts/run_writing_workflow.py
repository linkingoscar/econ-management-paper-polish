#!/usr/bin/env python3
"""Run the dependency-free v3.1 writing gates for one workspace.

This orchestrator is intentionally serial and read-only with respect to the
manuscript. It records every stage, skipped capability, and failure so a later
run can resume from the checkpoint without treating a partial run as complete.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from writing_contract import (
    load_json,
    utc_now,
    validate_capability_report,
    validate_checkpoint,
    validate_route_card,
    validate_workspace_manifest,
    write_json,
)


def run_script(root: Path, script: str, args: list[str]) -> tuple[int, dict[str, Any], str]:
    process = subprocess.run(
        [sys.executable, str(root / "scripts" / script), *args, "--json"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {"status": "fail", "errors": [process.stdout.strip() or process.stderr.strip() or "script returned no JSON"]}
    return process.returncode, payload, process.stderr.strip()


def append_event(path: Path, run_id: str, stage: str, status: str, action: str, *, output: Any = None, errors: list[str] | None = None) -> None:
    event = {
        "schema_version": "1.0",
        "run_id": run_id,
        "event_id": f"{run_id}-{stage}",
        "at": utc_now(),
        "stage": stage,
        "status": status,
        "action": action,
        "output": output if output is not None else {},
        "errors": errors or [],
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def workflow(workspace: Path, variables: list[str], allow_unresolved_route: bool) -> dict[str, Any]:
    workspace = workspace.resolve()
    manifest_path = workspace / "workspace-manifest.json"
    if not manifest_path.exists():
        return {"status": "fail", "errors": [f"workspace manifest not found: {manifest_path}"]}
    manifest = load_json(manifest_path)
    manifest_errors = validate_workspace_manifest(manifest)
    if manifest_errors:
        return {"status": "fail", "errors": manifest_errors}
    run_id = f"RUN-{manifest['workspace_id']}-{utc_now().replace(':', '').replace('-', '')[:15]}"
    journal_path = workspace / manifest["paths"].get("revision_journal", "revision-journal.jsonl")
    checkpoint_path = workspace / manifest["paths"].get("checkpoint", "checkpoint.json")
    capability_path = workspace / manifest["paths"].get("capability_report", "capability-report.json")
    root = Path(__file__).resolve().parents[1]
    checks: list[dict[str, Any]] = []
    limitations: list[str] = []
    errors: list[str] = []

    route_path = workspace / manifest["paths"].get("route_card", "route-card.json")
    if route_path.exists():
        route = load_json(route_path)
        route_errors = validate_route_card(route)
        route_status = "pass" if not route_errors else "fail"
        checks.append({"stage": "route", "status": route_status, "mode": "Verified", "artifact": str(route_path), "errors": route_errors})
        append_event(journal_path, run_id, "route", route_status, "validate route card", output={"route_id": route.get("route_id")}, errors=route_errors)
        if route_errors:
            errors.extend(route_errors)
        if route.get("unresolved") and not allow_unresolved_route:
            message = "route card has unresolved fields; pass --allow-unresolved-route for audit-only execution"
            errors.append(message)
            limitations.append(message)
    else:
        errors.append(f"route card not found: {route_path}")
        checks.append({"stage": "route", "status": "fail", "mode": "Conceptual", "artifact": str(route_path), "errors": ["missing route card"]})

    original = workspace / manifest["paths"].get("original_manuscript", "manuscript/original.md")
    current = workspace / manifest["paths"].get("current_manuscript", "manuscript/current.md")
    intake_path = workspace / manifest["paths"].get("intake", "intake.json")
    if intake_path.exists() and route_path.exists():
        try:
            intake = load_json(intake_path)
            intake.update({"status": "validated" if not route_errors else "invalid", "route_id": route.get("route_id"), "validated_at": utc_now(), "route_errors": route_errors})
            write_json(intake_path, intake)
            append_event(journal_path, run_id, "intake", "pass" if not route_errors else "fail", "persist route validation in intake", output={"path": str(intake_path)}, errors=route_errors)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot update intake artifact: {exc}")
    paper_spine_path = workspace / manifest["paths"].get("paper_spine", "paper-spine.json")
    if current.exists() and not paper_spine_path.exists():
        code, payload, stderr = run_script(root, "build_paper_spine.py", ["--manuscript", str(current), "--paper-id", manifest.get("paper_id", "paper-unknown"), "--output", str(paper_spine_path)])
        candidate_status = payload.get("status", "fail")
        checks.append({"stage": "paper-spine-candidate", "status": candidate_status, "mode": "Verified", "artifact": str(paper_spine_path), "errors": payload.get("errors", [])})
        append_event(journal_path, run_id, "paper-spine-candidate", candidate_status, "extract unconfirmed candidate claim map", output={"path": str(paper_spine_path), "confirmation_required": True}, errors=payload.get("errors", []))
        if candidate_status != "pass":
            errors.append("paper spine candidate extraction failed")
    snapshot_path = workspace / manifest["paths"].get("protected_snapshot", "protected-snapshot.json")
    if original.exists():
        code, payload, stderr = run_script(root, "build_protected_snapshot.py", [str(original), *sum((["--variable", variable] for variable in variables), [])])
        if code == 0 and payload.get("snapshot"):
            write_json(snapshot_path, payload["snapshot"])
        checks.append({"stage": "protected-snapshot", "status": payload.get("status", "fail"), "mode": "Verified", "artifact": str(snapshot_path), "errors": payload.get("errors", [])})
        append_event(journal_path, run_id, "protected-snapshot", payload.get("status", "fail"), "snapshot original manuscript", output={"path": str(snapshot_path)}, errors=payload.get("errors", []))
    else:
        message = "original manuscript is absent; no text-level writing audit was run"
        limitations.append(message)
        checks.append({"stage": "protected-snapshot", "status": "skipped", "mode": "Documented", "artifact": str(original), "errors": [message]})
        append_event(journal_path, run_id, "protected-snapshot", "skipped", "skip absent original manuscript", errors=[message])

    if original.exists() and current.exists():
        common = [str(original), str(current)]
        verify_args = [*common, *sum((["--variable", variable] for variable in variables), [])]
        if snapshot_path.exists():
            verify_args.extend(["--snapshot", str(snapshot_path)])
        code, payload, stderr = run_script(root, "verify_bounded_patch.py", verify_args)
        checks.append({"stage": "bounded-verification", "status": payload.get("status", "fail"), "mode": "Verified", "artifact": "stdout", "errors": payload.get("errors", [])})
        append_event(journal_path, run_id, "bounded-verification", payload.get("status", "fail"), "verify protected and meaning gates", output=payload, errors=payload.get("errors", []))
        if payload.get("status") != "pass":
            errors.append("bounded verification failed")
        for script, stage in (("build_method_safety_report.py", "method-language"),):
            code, payload, stderr = run_script(root, script, [str(current)])
            checks.append({"stage": stage, "status": payload.get("status", "fail"), "mode": "Verified", "artifact": "stdout", "errors": payload.get("errors", [])})
            append_event(journal_path, run_id, stage, payload.get("status", "fail"), f"run {stage} gate", output=payload, errors=payload.get("errors", []))
            if payload.get("status") != "pass":
                errors.append(f"{stage} gate failed")
        if current.suffix.lower() in {".tex", ".latex"}:
            code, payload, stderr = run_script(root, "compile_guard.py", [str(current), "--strict"])
            checks.append({"stage": "compile-guard", "status": payload.get("status", "fail"), "mode": "Verified" if payload.get("compile", {}).get("status") == "passed" else "Documented", "artifact": "stdout", "errors": payload.get("structural", {}).get("issues", [])})
            append_event(journal_path, run_id, "compile-guard", payload.get("status", "fail"), "run LaTeX guard", output=payload, errors=[])
            if payload.get("status") != "pass":
                errors.append("LaTeX structural/compile guard failed")
    else:
        message = "current manuscript is absent; candidate revision gates were not run"
        limitations.append(message)
        checks.append({"stage": "revision-gates", "status": "skipped", "mode": "Documented", "artifact": str(current), "errors": [message]})
        append_event(journal_path, run_id, "revision-gates", "skipped", "skip absent current manuscript", errors=[message])

    if not checks:
        limitations.append("No deterministic check ran.")
    has_verified = any(item.get("mode") == "Verified" and item.get("status") in {"pass", "skipped"} for item in checks)
    overall_mode = "Verified" if has_verified else "Documented"
    status = "failed" if errors else "complete" if original.exists() and current.exists() else "blocked"
    capability = {
        "schema_version": "1.0",
        "run_id": run_id,
        "generated_at": utc_now(),
        "overall_mode": overall_mode,
        "checks": checks,
        "permissions": ["filesystem:workspace-read", "filesystem:workspace-write:state-only"],
        "limitations": limitations,
        "output_ceiling": "Deterministic writing-state and manuscript-consistency audit; not theory adjudication, data replication, or proof of semantic equivalence.",
    }
    capability_errors = validate_capability_report(capability)
    if capability_errors:
        errors.extend(capability_errors)
    write_json(capability_path, capability)
    checkpoint = {
        "schema_version": "1.0",
        "run_id": run_id,
        "workspace_id": manifest["workspace_id"],
        "updated_at": utc_now(),
        "last_stage": checks[-1]["stage"] if checks else "initialized",
        "next_stage": "author-review" if not errors else "repair-failed-gates",
        "status": status,
        "artifacts": {"capability_report": str(capability_path), "revision_journal": str(journal_path)},
        "errors": errors,
    }
    checkpoint_errors = validate_checkpoint(checkpoint)
    if checkpoint_errors:
        errors.extend(checkpoint_errors)
    write_json(checkpoint_path, checkpoint)
    append_event(journal_path, run_id, "workflow", "pass" if not errors else "fail", "workflow complete", output={"checkpoint": str(checkpoint_path)}, errors=errors)
    return {"status": "pass" if not errors else "fail", "run_id": run_id, "workspace": str(workspace), "checks": checks, "errors": errors, "capability": capability, "checkpoint": checkpoint}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--variable", action="append", default=[])
    parser.add_argument("--allow-unresolved-route", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = workflow(args.workspace, args.variable, args.allow_unresolved_route)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "errors": [str(exc)]}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if result.get("run_id"):
            print(f"run_id: {result['run_id']}")
        for error in result.get("errors", []):
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
