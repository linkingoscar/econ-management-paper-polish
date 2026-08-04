#!/usr/bin/env python3
"""Run structural LaTeX checks and, when requested, an isolated compile.

The default mode is honest about capability: a passing structural audit is not
reported as a successful TeX compilation when no compiler is installed.
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

from audit_latex import audit


COMPILERS = ("tectonic", "pdflatex", "xelatex", "lualatex")


def compiler_info() -> dict[str, str] | None:
    for name in COMPILERS:
        path = shutil.which(name)
        if path:
            return {"name": name, "path": path}
    return None


def run_compile(tex_path: Path, compiler: dict[str, str], output_dir: Path) -> dict[str, Any]:
    name = compiler["name"]
    if name == "tectonic":
        command = [compiler["path"], "--outdir", str(output_dir), str(tex_path)]
    else:
        command = [
            compiler["path"],
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={output_dir}",
            tex_path.name,
        ]
    try:
        process = subprocess.run(
            command,
            cwd=tex_path.parent,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "failed", "command": command, "error": str(exc)}
    combined = (process.stdout or "") + (process.stderr or "")
    return {
        "status": "passed" if process.returncode == 0 else "failed",
        "command": command,
        "returncode": process.returncode,
        "log_tail": combined[-4000:],
    }


def guard(tex_path: Path, bib_path: Path | None, strict: bool, request_compile: bool, require_compile: bool) -> dict[str, Any]:
    structural = audit(tex_path, bib_path, strict)
    compiler = compiler_info()
    compile_result: dict[str, Any]
    if not request_compile:
        compile_result = {
            "status": "not-requested",
            "available": compiler is not None,
            "compiler": compiler,
        }
    elif compiler is None:
        compile_result = {
            "status": "unavailable",
            "available": False,
            "compiler": None,
            "message": "No tectonic/pdflatex/xelatex/lualatex executable was found.",
        }
    else:
        with tempfile.TemporaryDirectory(prefix="econ-paper-compile-") as output:
            compile_result = {
                "available": True,
                "compiler": compiler,
                **run_compile(tex_path, compiler, Path(output)),
            }
    compile_failed = compile_result["status"] in {"failed", "unavailable"} and (request_compile or require_compile)
    structural_failed = structural["status"] != "pass"
    status = "fail" if structural_failed or (require_compile and compile_failed) else "pass"
    if compiler and (compile_result["status"] == "passed" or not request_compile):
        capability = "verified" if compile_result["status"] == "passed" else "documented"
    else:
        capability = "documented"
    return {
        "schema_version": "1.0",
        "status": status,
        "file": str(tex_path),
        "structural": structural,
        "compile": compile_result,
        "compile_required": require_compile,
        "capability": capability,
        "gate": "pass" if status == "pass" else "blocked",
        "scope": "structural-audit-plus-optional-isolated-compiler; structural pass is not compile proof",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path)
    parser.add_argument("--bib", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--compile", action="store_true", dest="request_compile", help="Attempt an isolated compile if a compiler is available.")
    parser.add_argument("--require-compile", action="store_true", help="Fail when a requested compile is unavailable or fails.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.require_compile:
        args.request_compile = True
    try:
        result = guard(args.tex, args.bib, args.strict, args.request_compile, args.require_compile)
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "file": str(args.tex), "errors": [str(exc)]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"structural: {result['structural']['status']}")
        print(f"compile: {result['compile']['status']}")
        print(f"capability: {result['capability']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
