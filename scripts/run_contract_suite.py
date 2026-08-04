#!/usr/bin/env python3
"""Run all dependency-free repository and writing reliability gates serially."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from writing_contract import utc_now, write_json


def command_specs(root: Path, include_dogfood: bool = True) -> list[tuple[str, list[str]]]:
    python = sys.executable
    specs = [
        ("repository-contract", [python, str(root / "scripts" / "validate_v3.py"), ".", "--json"]),
        ("skill-package", [python, str(root / "scripts" / "validate_skill_package.py"), ".", "--json"]),
        ("skill-creator-quick-validation", [python, "-X", "utf8", str(root / "scripts" / "quick_validate.py"), ".", "--json"]),
        ("repro-lock", [python, str(root / "scripts" / "validate_repro_lock.py"), ".", "--json"]),
        ("legacy-smoke", [python, str(root / "evals" / "run_smoke_tests.py")]),
        ("extended-offline", [python, str(root / "evals" / "run_extended_tests.py")]),
        ("v31-writing", [python, str(root / "evals" / "run_v31_writing_tests.py")]),
        ("writing-benchmark", [python, str(root / "scripts" / "run_writing_benchmark.py"), "--json"]),
        ("platform-smoke", [python, str(root / "scripts" / "run_platform_smoke.py"), "--json"]),
    ]
    if include_dogfood:
        specs.append(("local-dogfood", [python, str(root / "scripts" / "run_dogfood_suite.py"), "--json"]))
    return specs


def run(root: Path, include_dogfood: bool) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for name, command in command_specs(root, include_dogfood):
        started = time.monotonic()
        process = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        elapsed = round(time.monotonic() - started, 3)
        results.append({
            "name": name,
            "status": "pass" if process.returncode == 0 else "fail",
            "returncode": process.returncode,
            "duration_seconds": elapsed,
            "stdout_tail": (process.stdout or "")[-4000:],
            "stderr_tail": (process.stderr or "")[-4000:],
        })
    counts = {"total": len(results), "passed": sum(item["status"] == "pass" for item in results), "failed": sum(item["status"] == "fail" for item in results)}
    return {
        "schema_version": "1.0",
        "status": "pass" if counts["failed"] == 0 else "fail",
        "generated_at": utc_now(),
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "cwd": str(root)},
        "commands": results,
        "counts": counts,
        "limitations": [
            "The suite is dependency-free and offline; external databases, model calls, and author rubric remain outside the gate.",
            "LaTeX is reported as Documented when no compiler is installed; structural validation still runs.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skip-dogfood", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = run(args.root.resolve(), not args.skip_dogfood)
    if args.output:
        try:
            write_json(args.output, report)
            report["output"] = str(args.output)
        except OSError as exc:
            report["status"] = "fail"
            report.setdefault("errors", []).append(f"cannot write report: {exc}")
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"commands: {report['counts']['passed']}/{report['counts']['total']}")
        for item in report["commands"]:
            print(f"- {item['name']}: {item['status']} ({item['duration_seconds']}s)")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
