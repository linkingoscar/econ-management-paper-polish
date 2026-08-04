#!/usr/bin/env python3
"""Run the offline v3.1 writing foundation suite and emit a benchmark report."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

from writing_contract import utc_now, write_json


CHECK_RE = re.compile(r"^- (.+)$", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    process = subprocess.run(
        [sys.executable, str(root / "evals" / "run_v31_writing_tests.py")],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    checks = CHECK_RE.findall(process.stdout)
    report = {
        "schema_version": "1.0",
        "suite": "v3.1-writing-foundation",
        "generated_at": utc_now(),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "network_tests": False,
        },
        "metrics": {
            "checks_total": len(checks),
            "checks_passed": len(checks) if process.returncode == 0 else 0,
            "pass_rate": 1.0 if process.returncode == 0 and checks else 0.0,
            "protected_patch_preservation_target": 1.0,
            "citation_fabrication_target": 0.0,
        },
        "failures": [] if process.returncode == 0 else [{"stdout": process.stdout, "stderr": process.stderr}],
        "limitations": [
            "Synthetic fixtures only; this is not dogfooding on a user manuscript.",
            "No live journal, database, or model call is included.",
        ],
    }
    output = None
    if args.output:
        try:
            write_json(args.output, report)
            output = str(args.output)
        except OSError as exc:
            report["failures"].append({"error": f"cannot write benchmark report: {exc}"})
            process.returncode = 1
    if args.as_json:
        print(json.dumps({**report, "output": output}, ensure_ascii=False, indent=2))
    else:
        print(f"status: {'pass' if process.returncode == 0 else 'fail'}")
        print(f"checks: {len(checks)}")
        if output:
            print(f"output: {output}")
        if process.returncode != 0:
            print(process.stderr, file=sys.stderr)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
