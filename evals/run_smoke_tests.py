#!/usr/bin/env python3
"""Run dependency-free smoke tests for the v3 reliability core."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "evals" / "fixtures"


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def json_output(result: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{result.args} did not emit JSON: {result.stdout}\n{result.stderr}") from exc


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks: list[str] = []
    original = FIXTURES / "original.md"
    good = FIXTURES / "revised-good.md"
    bad = FIXTURES / "revised-bad.md"
    bib = FIXTURES / "sample.bib"

    result = run_script("check_numeric_consistency.py", str(original), str(good), "--json")
    expect(result.returncode == 0 and json_output(result)["status"] == "pass", "good numeric comparison should pass")
    checks.append("numeric-preservation/pass")
    result = run_script("check_numeric_consistency.py", str(original), str(bad), "--json")
    expect(result.returncode != 0 and json_output(result)["status"] == "fail", "changed p-value should fail numeric comparison")
    checks.append("numeric-preservation/fail-detection")

    result = run_script("compare_manuscript_versions.py", str(original), str(good), "--variable", "Treatment", "--json")
    expect(result.returncode == 0 and json_output(result)["status"] == "pass", "good version comparison should pass")
    checks.append("version-comparison/pass")

    result = run_script("check_citations.py", str(original), "--bib", str(bib), "--strict", "--json")
    expect(result.returncode == 0 and json_output(result)["status"] == "pass", "matched citation should pass")
    checks.append("citation-ledger/pass")
    with tempfile.TemporaryDirectory() as temp_dir:
        bad_citation = Path(temp_dir) / "bad.md"
        bad_citation.write_text("A claim \\citep{unknown}. [citation needed]\n", encoding="utf-8")
        result = run_script("check_citations.py", str(bad_citation), "--bib", str(bib), "--strict", "--json")
        report = json_output(result)
        expect(result.returncode != 0 and report["status"] == "fail", "missing citation and placeholder should fail")
    checks.append("citation-ledger/fail-detection")

    good_tex = r"""\documentclass{article}
\usepackage{booktabs}
\usepackage{threeparttable}
\usepackage{natbib}
\usepackage{amsmath}
\begin{document}
\begin{equation}\label{eq:main} y = x \end{equation}
See \ref{eq:main} and \citep{smith2022}.
\begin{table}\begin{threeparttable}\toprule x \\ \bottomrule\end{threeparttable}\end{table}
\bibliography{sample}
\end{document}
"""
    bad_tex = r"""\documentclass{article}
\begin{document}
\begin{table}\begin{threeparttable}\toprule x \\ \bottomrule\end{threeparttable}\end{table}
See \ref{missing}.
\end{document}
"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        good_tex_path = temp / "good.tex"
        bad_tex_path = temp / "bad.tex"
        good_tex_path.write_text(good_tex, encoding="utf-8")
        bad_tex_path.write_text(bad_tex, encoding="utf-8")
        (temp / "sample.bib").write_text(bib.read_text(encoding="utf-8"), encoding="utf-8")
        result = run_script("audit_latex.py", str(good_tex_path), "--bib", str(temp / "sample.bib"), "--strict", "--json")
        expect(result.returncode == 0 and json_output(result)["status"] == "pass", "complete LaTeX fixture should pass")
        result = run_script("audit_latex.py", str(bad_tex_path), "--strict", "--json")
        report = json_output(result)
        expect(result.returncode != 0 and report["status"] == "fail", "missing LaTeX package/reference should fail")
    checks.append("latex-audit/pass-and-fail")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        evidence_input = temp / "evidence.json"
        evidence_input.write_text(
            json.dumps(
                {
                    "entries": [
                        {
                            "claim_id": "CLM-smoke-1",
                            "claim": "The design identifies a treatment effect under stated assumptions.",
                            "source": {"title": "A Design Discussion", "url": "https://doi.org/10.1234/example.2022"},
                            "verification": {"level": "full_text", "checked_at": "2026-08-03", "support": "Methods section"},
                            "allowed_use": "direct_citation",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        evidence_output = temp / "evidence-pack.json"
        result = run_script("build_evidence_pack.py", str(evidence_input), "--output", str(evidence_output), "--json")
        expect(result.returncode == 0 and json_output(result)["status"] == "pass" and evidence_output.exists(), "valid evidence pack should build")
        weak_evidence = temp / "weak-evidence.json"
        weak_evidence.write_text(
            json.dumps(
                {
                    "entries": [
                        {
                            "claim_id": "CLM-smoke-weak",
                            "claim": "Metadata alone establishes the full result.",
                            "source": {"title": "Metadata record", "url": "https://example.org/metadata"},
                            "verification": {"level": "metadata", "checked_at": "2026-08-03"},
                            "allowed_use": "direct_citation",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        result = run_script("build_evidence_pack.py", str(weak_evidence), "--json")
        expect(result.returncode != 0 and json_output(result)["status"] == "fail", "metadata-only direct citation should fail")
        journal = temp / "journal-card.json"
        journal.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "target_outlet": "Example Journal",
                    "verification_basis": "Official author guidelines",
                    "checked_at": "2026-08-03",
                    "claims": [
                        {
                            "claim": "Abstract word limit",
                            "value": "250 words",
                            "source_url": "https://example.org/guidelines",
                            "status": "verified",
                            "applies_to": "Research article",
                            "stage": "submission",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        result = run_script("validate_journal_card.py", str(journal), "--json")
        expect(result.returncode == 0 and json_output(result)["status"] == "pass", "valid journal card should pass")
    checks.append("evidence-and-journal-contracts/pass-and-guard")

    result = run_script("validate_v3.py", str(ROOT), "--json")
    expect(result.returncode == 0 and json_output(result)["status"] == "pass", "repository contract should pass")
    checks.append("repository-contract/pass")

    print(f"v3 smoke tests passed ({len(checks)} checks)")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"v3 smoke tests failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
