#!/usr/bin/env python3
"""Run dependency-free v3.1 writing-foundation tests."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "evals" / "fixtures" / "writing"


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
