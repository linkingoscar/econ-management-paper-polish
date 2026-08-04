#!/usr/bin/env python3
"""Run the complete local writing workflow on an explicit fixture manifest.

This is an automated dogfood harness for the workflow plumbing. It copies only
public repository fixtures into temporary workspaces, never writes manuscripts
back to the repository, and labels every result synthetic-only. It is useful
for catching broken routing/checkpoint/journal wiring, but it is not evidence
of author voice, causal validity, or real-paper quality.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from writing_contract import utc_now, write_json


def run_json(root: Path, script: str, arguments: list[str]) -> tuple[int, dict[str, Any]]:
    process = subprocess.run([sys.executable, str(root / "scripts" / script), *arguments, "--json"], cwd=root, text=True, capture_output=True, check=False)
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {"status": "fail", "errors": [process.stdout.strip() or process.stderr.strip() or "script returned no JSON"]}
    return process.returncode, payload


def within_root(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"fixture path escapes repository: {relative}") from exc
    return candidate


def validate_manifest(manifest: Any, root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["dogfood manifest must be an object"]
    if manifest.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if manifest.get("policy") != "synthetic-fixtures-only":
        errors.append("policy must be synthetic-fixtures-only")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty array")
        return errors
    seen: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("id", "source", "discipline", "language", "method", "expected_workflow"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"{prefix}.{key} must be a non-empty string")
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in seen:
                errors.append(f"{prefix}.id duplicates {case_id}")
            seen.add(case_id)
        if case.get("expected_workflow") not in {"pass", "fail"}:
            errors.append(f"{prefix}.expected_workflow must be pass or fail")
        source = case.get("source")
        if isinstance(source, str):
            try:
                if not within_root(root, source).is_file():
                    errors.append(f"{prefix}.source does not exist: {source}")
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")
    return errors


def run_case(root: Path, case: dict[str, Any], workspace: Path) -> dict[str, Any]:
    case_id = case["id"]
    source = within_root(root, case["source"])
    init_code, init = run_json(root, "init_writing_workspace.py", [str(workspace), "--paper-id", case_id])
    errors = list(init.get("errors", []))
    if init_code != 0 or init.get("status") != "pass":
        return {"id": case_id, "status": "fail", "observed_workflow": "fail", "expected_workflow": case["expected_workflow"], "errors": errors or ["workspace initialization failed"], "artifacts": []}
    manuscript_dir = workspace / "manuscript"
    original = manuscript_dir / "original.md"
    current = manuscript_dir / "current.md"
    shutil.copy2(source, original)
    shutil.copy2(source, current)
    route_args = [
        "--paper-id", case_id,
        "--task-mode", "audit",
        "--discipline", case["discipline"],
        "--language", case["language"],
        "--method", case["method"],
        "--evidence-mode", "offline",
        "--confidence", "high",
        "--output", str(workspace / "route-card.json"),
    ]
    if case.get("section"):
        route_args.extend(["--section", case["section"]])
    route_code, route = run_json(root, "build_route_card.py", route_args)
    errors.extend(route.get("errors", []))
    if route_code != 0 or route.get("status") != "pass":
        return {"id": case_id, "status": "fail", "observed_workflow": "fail", "expected_workflow": case["expected_workflow"], "errors": errors or ["route card build failed"], "artifacts": []}
    workflow_code, workflow = run_json(root, "run_writing_workflow.py", [str(workspace), "--variable", "Treatment"])
    observed = "pass" if workflow.get("status") == "pass" and workflow_code == 0 else "fail"
    expected = case["expected_workflow"]
    expected_match = observed == expected
    required = ["workspace-manifest.json", "intake.json", "route-card.json", "capability-report.json", "checkpoint.json", "protected-snapshot.json", "revision-journal.jsonl", "paper-spine.json"]
    artifacts = [name for name in required if (workspace / name).is_file()]
    missing = [name for name in required if name not in artifacts]
    if missing:
        errors.append("missing workflow artifacts: " + ", ".join(missing))
    if not expected_match:
        errors.append(f"expected workflow={expected}, observed={observed}")
    return {
        "id": case_id,
        "status": "pass" if expected_match and not missing else "fail",
        "expected_workflow": expected,
        "observed_workflow": observed,
        "workflow_run_id": workflow.get("run_id"),
        "expected_reason": case.get("expected_reason"),
        "errors": errors,
        "artifacts": artifacts,
        "method_issue_count": next((item.get("output", {}).get("issue_count") for item in workflow.get("checks", []) if item.get("stage") == "method-language"), None),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "evals" / "dogfood" / "manifest.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        manifest = {}
        errors.append(f"cannot read dogfood manifest: {exc}")
    errors.extend(validate_manifest(manifest, root))
    cases: list[dict[str, Any]] = []
    if not errors:
        with tempfile.TemporaryDirectory(prefix="econ-paper-dogfood-") as temp_dir:
            temp_root = Path(temp_dir)
            for case in manifest["cases"]:
                cases.append(run_case(root, case, temp_root / case["id"]))
    counts = {"total": len(cases), "passed": sum(item["status"] == "pass" for item in cases), "failed": sum(item["status"] == "fail" for item in cases), "expected_workflow_pass": sum(item.get("expected_workflow") == "pass" for item in cases), "expected_workflow_fail": sum(item.get("expected_workflow") == "fail" for item in cases)}
    report = {
        "schema_version": "1.0",
        "status": "pass" if not errors and counts["failed"] == 0 and counts["total"] > 0 else "fail",
        "suite": manifest.get("suite", "unknown"),
        "policy": "synthetic-fixtures-only",
        "generated_at": utc_now(),
        "counts": counts,
        "cases": cases,
        "errors": errors,
        "limitations": [
            "All inputs are repository-owned synthetic fixtures; no real or anonymous manuscript was supplied.",
            "The harness checks workflow wiring, state artifacts, and known deterministic gates only.",
            "No human rubric, author-voice judgment, causal adjudication, or journal acceptance claim is produced.",
        ],
    }
    if args.output:
        try:
            write_json(args.output, report)
            report["output"] = str(args.output)
        except OSError as exc:
            report["errors"].append(f"cannot write dogfood report: {exc}")
            report["status"] = "fail"
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"cases: {counts['passed']}/{counts['total']}")
        for item in cases:
            print(f"- {item['id']}: {item['status']} (workflow {item.get('observed_workflow')})")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
