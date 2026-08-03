#!/usr/bin/env python3
"""Run a dependency-free structural audit on a LaTeX manuscript."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^]]*\])?\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eq)?ref\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^]]*\])?\s*\{([^}]+)\}")
GRAPHIC_RE = re.compile(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}")
BIB_RE = re.compile(r"\\bibliography\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def add_issue(issues: list[dict], severity: str, code: str, message: str, line: int | None = None) -> None:
    item = {"severity": severity, "code": code, "message": message}
    if line is not None:
        item["line"] = line
    issues.append(item)


def read_bib_paths(tex_path: Path, explicit: Path | None, text: str) -> list[Path]:
    if explicit:
        return [explicit]
    paths: list[Path] = []
    for match in BIB_RE.finditer(text):
        for name in match.group(1).split(","):
            name = name.strip()
            if name:
                path = tex_path.parent / (name if name.endswith(".bib") else f"{name}.bib")
                paths.append(path)
    return paths


def image_exists(tex_path: Path, name: str) -> bool:
    candidate = tex_path.parent / name
    if candidate.exists():
        return True
    if candidate.suffix:
        return False
    return any((tex_path.parent / f"{name}{suffix}").exists() for suffix in (".pdf", ".png", ".jpg", ".jpeg", ".eps"))


def audit(tex_path: Path, bib_path: Path | None = None, strict: bool = False) -> dict:
    text = tex_path.read_text(encoding="utf-8")
    issues: list[dict] = []
    packages = {package.strip() for raw in PACKAGE_RE.findall(text) for package in raw.split(",")}
    labels = set(LABEL_RE.findall(text))
    refs = [(match.group(1), line_number(text, match.start())) for match in REF_RE.finditer(text)]
    cites = [key.strip() for match in CITE_RE.finditer(text) for key in match.group(1).split(",")]

    if not re.search(r"\\documentclass(?:\[[^]]*\])?\{[^}]+\}", text):
        add_issue(issues, "error", "missing-documentclass", "No \\documentclass declaration found.")
    if "\\begin{document}" not in text:
        add_issue(issues, "error", "missing-document-begin", "No \\begin{document} found.")
    if "\\end{document}" not in text:
        add_issue(issues, "error", "missing-document-end", "No \\end{document} found.")

    requirements = {
        "threeparttable": (r"\\begin\{threeparttable\}|\\begin\{tablenotes\}", "threeparttable"),
        "booktabs": (r"\\(?:toprule|midrule|bottomrule|addlinespace)", "booktabs"),
        "graphicx": (r"\\includegraphics", "graphicx"),
        "amsmath": (r"\\begin\{(?:align|equation)|\\eqref\{", "amsmath"),
        "natbib": (r"\\cite(?:t|p|author|year)", "natbib"),
        "subcaption": (r"\\begin\{subfigure\}", "subcaption"),
    }
    for package_name, (pattern, required_package) in requirements.items():
        match = re.search(pattern, text)
        if match and required_package not in packages:
            add_issue(
                issues,
                "error",
                "missing-package",
                f"Command requires \\usepackage{{{required_package}}}.",
                line_number(text, match.start()),
            )

    for ref, line in refs:
        if ref not in labels:
            add_issue(issues, "error", "undefined-reference", f"Reference '{ref}' has no matching label.", line)

    bib_paths = read_bib_paths(tex_path, bib_path, text)
    bib_keys: set[str] = set()
    for path in bib_paths:
        if not path.exists():
            add_issue(issues, "error", "missing-bib-file", f"Bibliography file not found: {path.name}")
            continue
        bib_keys.update(BIB_KEY_RE.findall(path.read_text(encoding="utf-8")))
    if cites and bib_paths:
        for key in sorted(set(cites) - bib_keys):
            add_issue(issues, "error", "undefined-citation", f"Citation '{key}' has no matching BibTeX entry.")

    for match in GRAPHIC_RE.finditer(text):
        if not image_exists(tex_path, match.group(1)):
            add_issue(
                issues,
                "error",
                "missing-figure",
                f"Figure file not found: {match.group(1)}",
                line_number(text, match.start()),
            )

    errors = sum(1 for issue in issues if issue["severity"] == "error")
    warnings = sum(1 for issue in issues if issue["severity"] == "warning")
    return {
        "status": "fail" if errors or (strict and warnings) else "pass",
        "file": str(tex_path),
        "packages": sorted(packages),
        "labels": sorted(labels),
        "references": sorted({ref for ref, _ in refs}),
        "citations": sorted(set(cites)),
        "issues": issues,
        "error_count": errors,
        "warning_count": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path)
    parser.add_argument("--bib", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = audit(args.tex, args.bib, args.strict)
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot audit input: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"errors: {result['error_count']}; warnings: {result['warning_count']}")
        for issue in result["issues"]:
            location = f" (line {issue['line']})" if "line" in issue else ""
            print(f"{issue['severity']}: {issue['code']}: {issue['message']}{location}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
