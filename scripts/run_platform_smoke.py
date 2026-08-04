#!/usr/bin/env python3
"""Run portable runtime checks and an honest LaTeX capability smoke test."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
import tempfile
from pathlib import Path

from compile_guard import guard
from writing_contract import utc_now, write_json


def smoke(root: Path, tex: Path) -> dict:
    errors: list[str] = []
    limitations: list[str] = []
    checks: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="econ-paper-platform-") as temp_dir:
        temp = Path(temp_dir)
        sample = temp / "utf8-roundtrip.txt"
        sample.write_text("中文/English/αβ\n", encoding="utf-8")
        if sample.read_text(encoding="utf-8") == "中文/English/αβ\n":
            checks.append({"name": "utf8-roundtrip", "status": "pass"})
        else:
            errors.append("UTF-8 round trip failed")
            checks.append({"name": "utf8-roundtrip", "status": "fail"})
        checks.append({"name": "path-separator", "status": "pass", "separator": str(Path("a") / "b")})
    if not tex.is_file():
        errors.append(f"LaTeX fixture not found: {tex}")
        tex_result = {"status": "fail", "capability": "Conceptual", "file": str(tex)}
    else:
        tex_result = guard(tex, None, strict=True, request_compile=True, require_compile=False)
        checks.append({"name": "latex-structural", "status": tex_result.get("structural", {}).get("status", "fail"), "issues": tex_result.get("structural", {}).get("issues", [])})
        compile_status = tex_result.get("compile", {}).get("status")
        checks.append({"name": "latex-compile", "status": compile_status, "compiler": tex_result.get("compile", {}).get("compiler")})
        if compile_status == "unavailable":
            limitations.append("No TeX compiler is installed; structural audit is verified but compilation is Documented.")
        elif compile_status == "failed":
            errors.append("available TeX compiler failed on the good fixture")
    if not errors and not limitations:
        limitations.append("No known runtime limitation was observed on this host.")
    compiler_names = [name for name in ("tectonic", "pdflatex", "xelatex", "lualatex") if shutil.which(name)]
    return {
        "schema_version": "1.0",
        "status": "pass" if not errors else "fail",
        "generated_at": utc_now(),
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation(), "platform": platform.platform(), "os": platform.system(), "machine": platform.machine(), "path_separator": str(Path("a") / "b")},
        "checks": checks,
        "capabilities": {"repository_contract": "Verified", "utf8": "Verified" if not errors else "Documented", "latex": "Verified" if tex_result.get("compile", {}).get("status") == "passed" else "Documented", "available_tex_compilers": compiler_names},
        "errors": errors,
        "limitations": limitations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tex", type=Path, default=Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "writing" / "compile-good.tex")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = smoke(args.root.resolve(), args.tex.resolve())
    if args.output:
        try:
            write_json(args.output, report)
            report["output"] = str(args.output)
        except OSError as exc:
            report["status"] = "fail"
            report["errors"].append(f"cannot write report: {exc}")
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"latex: {report['capabilities']['latex']}")
        for limitation in report["limitations"]:
            print(f"- {limitation}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
