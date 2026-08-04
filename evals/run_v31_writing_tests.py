#!/usr/bin/env python3
"""Run dependency-free v3.1 writing-foundation tests."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "evals" / "fixtures" / "writing"
METHOD_FIXTURES = ROOT / "evals" / "fixtures" / "method-safety"


def run(script: str, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    process = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args, "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{script} did not emit JSON: {process.stdout}\n{process.stderr}") from exc
    return process, payload


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        corpus = temp / "corpus"
        cards = temp / "cards"
        corpus.mkdir()
        cards.mkdir()
        for source in (FIXTURES / "target-a.md", FIXTURES / "target-b.md"):
            shutil.copy2(source, corpus / source.name)
        (corpus / "unreadable.bin").write_bytes(b"\x00\x01")
        manifest_path = temp / "corpus-manifest.json"

        process, payload = run(
            "prepare_corpus.py",
            str(corpus),
            "--corpus-id", "fixture-corpus",
            "--output", str(manifest_path),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "corpus manifest should build")
        expect(payload["items"] == 2 and payload["rejections"] == 1, "corpus readable/rejected counts should be deterministic")
        checks.append("corpus/manifest-and-rejection")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in manifest["items"]:
            source = corpus / item["path"]
            card_path = cards / f"STY-{item['source_id']}.json"
            process, payload = run(
                "extract_style_card.py",
                str(source),
                "--source-id", item["source_id"],
                "--output", str(card_path),
            )
            expect(process.returncode == 0 and payload["status"] == "pass", "style card should extract from text")
        checks.append("writing/style-card-extraction")

        profile_path = temp / "style-profile.json"
        process, payload = run(
            "build_style_profile.py",
            str(cards),
            "--manifest", str(manifest_path),
            "--target-outlet", "Example Journal",
            "--output", str(profile_path),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "style profile should aggregate cards")
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        expect(profile["copy_boundary"] == "structural-only" and profile["rules"], "style profile must be structural and non-empty")
        checks.append("writing/style-profile-and-boundary")

        process, payload = run("validate_style_profile_gate.py", str(profile_path))
        expect(process.returncode != 0 and payload["gate"] == "human-confirmation-required", "draft style profile must require human confirmation")
        confirmed = deepcopy(profile)
        confirmed["status"] = "confirmed"
        confirmed["human_confirmed"] = True
        confirmed["confirmation"] = {
            "confirmed_at": "2026-08-04T00:00:00Z",
            "confirmed_by": "fixture-author",
            "notes": "Reviewed structural rules, conflicts, source roles, and copy boundary.",
        }
        confirmed_path = temp / "style-profile-confirmed.json"
        confirmed_path.write_text(json.dumps(confirmed, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("validate_style_profile_gate.py", str(confirmed_path))
        expect(process.returncode == 0 and payload["status"] == "pass", "confirmed style profile should pass the human gate")
        checks.append("writing/dynamic-style-human-gate")

        spine_path = temp / "paper-spine.json"
        process, payload = run(
            "build_paper_spine.py",
            str(FIXTURES / "paper-spine-input.json"),
            "--output", str(spine_path),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "paper spine should normalize")
        spine = json.loads(spine_path.read_text(encoding="utf-8"))
        expect(spine["contribution_chain"][0]["claim_id"] == "ARG-001", "paper spine must assign stable argument IDs")
        checks.append("argument/paper-spine")

        process, payload = run(
            "check_claim_evidence.py",
            str(spine_path),
            "--evidence-pack", str(FIXTURES / "evidence-pack.json"),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "claim evidence should resolve against the evidence pack")
        checks.append("argument/claim-evidence-binding")

        ledger_path = temp / "review-ledger.json"
        process, payload = run(
            "build_issue_ledger.py",
            str(FIXTURES / "review-issues.json"),
            "--output", str(ledger_path),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "review ledger should build")
        routed_path = temp / "review-ledger-routed.json"
        process, payload = run(
            "route_review_issues.py",
            str(ledger_path),
            "--output", str(routed_path),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "review ledger should route")
        routed = json.loads(routed_path.read_text(encoding="utf-8"))
        decisions = [issue["decision"] for issue in routed["issues"]]
        expect(decisions == ["safe-fix", "author-required"], "review pre-router should protect high-risk method issues")
        checks.append("revision/ledger-and-risk-router")

        process, payload = run(
            "propose_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-good.md"),
            "--variable", "Treatment",
        )
        expect(process.returncode == 0 and payload["status"] == "pass" and payload["risk"] == "safe-fix", "unchanged protected patch should pass")
        process, payload = run(
            "propose_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-bad.md"),
            "--variable", "Treatment",
        )
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["risk"] == "author-required", "changed protected patch should block")
        checks.append("revision/bounded-protected-patch")

        process, payload = run(
            "verify_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-good.md"),
            "--variable", "Treatment",
        )
        expect(process.returncode == 0 and payload["verified"], "bounded patch verifier should pass the protected fixture")
        checks.append("revision/bounded-verification")

        process, payload = run(
            "meaning_audit.py",
            str(FIXTURES / "meaning-original.md"),
            str(FIXTURES / "meaning-risk.md"),
        )
        expect(process.returncode != 0 and payload["decision"] == "author-required", "meaning-risk marker changes must be blocked")
        process, payload = run(
            "meaning_audit.py",
            str(FIXTURES / "meaning-original.md"),
            str(FIXTURES / "meaning-confirmed.md"),
            "--author-confirmed",
            "--rationale",
            "Author reviewed the identification wording and supplied supporting evidence.",
        )
        expect(process.returncode == 0 and payload["decision"] == "author-confirmed", "author-confirmed meaning changes should pass with a rationale")
        checks.append("revision/meaning-gate")

        process, payload = run("verify_bounded_patch.py", str(FIXTURES / "meaning-original.md"), str(FIXTURES / "meaning-risk.md"))
        expect(process.returncode != 0 and payload["meaning_gate"]["status"] == "fail", "bounded verifier must include the meaning gate")
        process, payload = run(
            "verify_bounded_patch.py",
            str(FIXTURES / "meaning-original.md"),
            str(FIXTURES / "meaning-confirmed.md"),
            "--author-confirmed",
            "--rationale",
            "Author reviewed the identification wording and supplied supporting evidence.",
        )
        expect(process.returncode == 0 and payload["verified"], "bounded verifier should accept explicitly confirmed meaning changes")
        checks.append("revision/bounded-meaning-verification")

        process, payload = run("check_method_language.py", str(METHOD_FIXTURES / "overclaim-en.md"))
        expect(process.returncode != 0 and payload["issue_count"] >= 3, "English method overclaims should be detected")
        process, payload = run("check_method_language.py", str(METHOD_FIXTURES / "overclaim-zh.md"))
        expect(process.returncode != 0 and payload["issue_count"] >= 3, "Chinese method overclaims should be detected")
        process, payload = run("check_method_language.py", str(METHOD_FIXTURES / "safe.md"))
        expect(process.returncode == 0 and payload["issue_count"] == 0, "qualified method wording should not be over-flagged")
        checks.append("method-safety/language-gate")

        process, payload = run("compile_guard.py", str(FIXTURES / "compile-good.tex"))
        expect(process.returncode == 0 and payload["structural"]["status"] == "pass", "good LaTeX should pass the structural compile guard")
        process, payload = run("compile_guard.py", str(FIXTURES / "compile-bad.tex"))
        expect(process.returncode != 0 and payload["structural"]["status"] == "fail", "bad LaTeX should fail the structural compile guard")
        checks.append("engineering/latex-compile-guard")

        recall_good = temp / "review-ledger-recall-good.json"
        recall_good.write_text(json.dumps(routed, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("check_issue_recall.py", str(routed_path), str(recall_good))
        expect(process.returncode == 0 and payload["status"] == "pass", "unchanged issue ledger should pass recall")
        recall_missing = deepcopy(routed)
        recall_missing["issues"] = recall_missing["issues"][:-1]
        recall_missing_path = temp / "review-ledger-recall-missing.json"
        recall_missing_path.write_text(json.dumps(recall_missing, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("check_issue_recall.py", str(routed_path), str(recall_missing_path))
        expect(process.returncode != 0 and payload["missing_issue_ids"], "dropped review issue must fail recall")
        recall_closed = deepcopy(routed)
        recall_closed["issues"][0]["status"] = "closed"
        recall_closed_path = temp / "review-ledger-recall-closed.json"
        recall_closed_path.write_text(json.dumps(recall_closed, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("check_issue_recall.py", str(routed_path), str(recall_closed_path))
        expect(process.returncode != 0 and payload["silently_closed"], "silently closed issue must fail recall")
        checks.append("revision/review-issue-recall")

        provenance = temp / "provenance.json"
        provenance.write_text(
            json.dumps(
                {
                    "component": "fixture-adapter",
                    "source_url": "https://example.org/adapter",
                    "source_commit": "abc123",
                    "license": "MIT",
                    "capabilities": ["file:read"],
                    "status": "documented",
                    "last_tested": "2026-08-04",
                }
            ),
            encoding="utf-8",
        )
        process, payload = run("scan_skill_provenance.py", str(provenance))
        expect(process.returncode == 0 and payload["status"] == "pass", "provenance manifest should validate")
        checks.append("engineering/provenance")

    print(f"v3.1 writing tests passed ({len(checks)} checks)")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"v3.1 writing tests failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
