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


def confusion(expected: list[str], observed: list[str]) -> dict[str, int | float]:
    pairs = list(zip(expected, observed))
    valid = [(exp, got) for exp, got in pairs if exp in {"pass", "fail"} and got in {"pass", "fail"}]
    tp = sum(exp == "fail" and got == "fail" for exp, got in valid)
    fp = sum(exp == "pass" and got == "fail" for exp, got in valid)
    fn = sum(exp == "fail" and got == "pass" for exp, got in valid)
    tn = sum(exp == "pass" and got == "pass" for exp, got in valid)
    total = max(len(expected), len(observed))
    invalid = total - len(valid)
    return {
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "invalid": invalid,
        "evaluated": len(valid),
        "total": total,
        "accuracy": round((tp + tn) / total, 3) if total else 0.0,
    }


def run_gold(root: Path, manifest_path: Path) -> tuple[dict, list[dict]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected: list[str] = []
    observed: list[str] = []
    details: list[dict] = []
    for case in manifest.get("cases", []):
        path = root / case["path"]
        process = subprocess.run([sys.executable, str(root / "scripts" / "check_method_language.py"), str(path), "--json"], cwd=root, text=True, capture_output=True, check=False)
        try:
            payload = json.loads(process.stdout)
            issue_count = payload.get("issue_count") if isinstance(payload, dict) else None
            if not isinstance(issue_count, int) or isinstance(issue_count, bool) or issue_count < 0:
                raise ValueError("detector output lacks a valid issue_count")
            actual = "fail" if issue_count else "pass"
            if payload.get("status") != actual or (actual == "pass") != (process.returncode == 0):
                raise ValueError("detector status, issue_count, and exit code disagree")
        except (json.JSONDecodeError, ValueError) as exc:
            payload = {"error": str(exc), "stderr": process.stderr.strip()}
            actual = "error"
        expected.append(case["expected"])
        observed.append(actual)
        details.append({"id": case["id"], "expected": case["expected"], "observed": actual, "discipline": case.get("discipline"), "language": case.get("language"), "section": case.get("section"), "issue_count": payload.get("issue_count"), "error": payload.get("error")})
    return confusion(expected, observed), details


def run_mutations(root: Path, manifest_path: Path) -> tuple[dict, list[dict]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected: list[str] = []
    observed: list[str] = []
    details: list[dict] = []
    for case in manifest.get("cases", []):
        command = [sys.executable, str(root / "scripts" / "propose_bounded_patch.py"), str(root / case["original"]), str(root / case["revised"]), "--variable", case["variable"], "--json"]
        process = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        try:
            payload = json.loads(process.stdout)
            actual = payload.get("status") if isinstance(payload, dict) else None
            if actual not in {"pass", "fail"} or not isinstance(payload.get("protection"), dict) or not isinstance(payload.get("local_bindings"), dict):
                raise ValueError("detector output lacks a valid bounded-patch result")
            if (actual == "pass") != (process.returncode == 0):
                raise ValueError("detector status and exit code disagree")
        except (json.JSONDecodeError, ValueError) as exc:
            payload = {"error": str(exc), "stderr": process.stderr.strip()}
            actual = "error"
        expected.append(case["expected"])
        observed.append(actual)
        details.append({"id": case["id"], "expected": case["expected"], "observed": actual, "risk": payload.get("risk"), "error": payload.get("error")})
    return confusion(expected, observed), details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--gold", type=Path, default=Path("evals/gold/writing-cases.json"))
    parser.add_argument("--mutations", type=Path, default=Path("evals/mutations/writing-mutations.json"))
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
    benchmark_errors: list[dict] = []
    try:
        gold_metrics, gold_details = run_gold(root, root / args.gold)
        mutation_metrics, mutation_details = run_mutations(root, root / args.mutations)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as exc:
        gold_metrics, mutation_metrics = {}, {}
        gold_details, mutation_details = [], [{"error": str(exc)}]
        benchmark_errors.append({"error": f"cannot run detector cases: {exc}"})
    for detector, metrics in (("method_language", gold_metrics), ("protected_patch", mutation_metrics)):
        if not metrics or metrics.get("invalid", 0):
            benchmark_errors.append({"detector": detector, "error": f"invalid detector results: {metrics.get('invalid', 'unknown')}"})
    failures = ([] if process.returncode == 0 else [{"stdout": process.stdout, "stderr": process.stderr}]) + benchmark_errors
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
            "detectors": {
                "method_language": gold_metrics,
                "protected_patch": mutation_metrics,
            },
            "coverage": {
                "gold_cases": len(gold_details),
                "mutation_cases": len(mutation_details),
                "quadrants": [{"discipline": discipline, "language": language} for discipline, language in sorted({(item.get("discipline"), item.get("language")) for item in gold_details if item.get("discipline")})],
                "sections": sorted({item.get("section") for item in gold_details if item.get("section")}),
            },
        },
        "failures": failures,
        "limitations": [
            "Synthetic fixtures only; this is not dogfooding on a user manuscript.",
            "No live journal, database, or model call is included.",
            "Gold and mutation metrics cover deterministic gates, not author voice, substantive contribution, or journal acceptance.",
        ],
        "case_details": {"gold": gold_details, "mutations": mutation_details},
    }
    output = None
    return_code = 0 if process.returncode == 0 and not report["failures"] else 1
    report["status"] = "pass" if return_code == 0 else "fail"
    if args.output:
        try:
            write_json(args.output, report)
            output = str(args.output)
        except OSError as exc:
            report["failures"].append({"error": f"cannot write benchmark report: {exc}"})
            report["status"] = "fail"
            return_code = 1
    if args.as_json:
        print(json.dumps({**report, "output": output}, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"checks: {len(checks)}")
        if output:
            print(f"output: {output}")
        if process.returncode != 0:
            print(process.stderr, file=sys.stderr)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
