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


def write_fixture_review(packet: dict, path: Path, reviewer_id: str) -> None:
    value = {
        "schema_version": "1.0",
        "review_id": f"REV-{reviewer_id}",
        "packet_id": packet["packet_id"],
        "artifact_kind": packet["artifact_kind"],
        "artifact_sha256": packet["artifact"]["sha256"],
        "risk_level": packet["risk_level"],
        "reviewer": {"kind": "ai", "reviewer_id": reviewer_id, "provider": "fixture", "model": f"fixture-{reviewer_id}", "isolated_pass": True},
        "verdict": "approve",
        "checks": [{"check_id": item["check_id"], "status": "pass", "reason": f"Fixture verifies {item['check_id']}.", "evidence": [f"artifact:{item['check_id']}"]} for item in packet["required_checks"]],
        "limitations": ["Synthetic fixture review; no external facts verified."],
        "created_at": "2026-08-04T00:00:00Z",
    }
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


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
        expect(profile["role_weights"]["target-journal"] > profile["role_weights"]["other"], "target-journal evidence should receive the highest profile weight")
        checks.append("writing/style-profile-and-boundary")

        process, payload = run(
            "audit_corpus_gate.py",
            str(manifest_path),
            "--min-target", "2",
            "--require-license",
        )
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["errors"], "unlicensed corpus should fail the corpus gate")
        licensed_manifest = deepcopy(manifest)
        licensed_manifest["source_policy"]["license_status"] = "user-provided"
        for item in licensed_manifest["items"]:
            item["license_status"] = "user-provided"
        licensed_manifest_path = temp / "corpus-manifest-licensed.json"
        licensed_manifest_path.write_text(json.dumps(licensed_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run(
            "audit_corpus_gate.py",
            str(licensed_manifest_path),
            "--min-target", "2",
            "--min-field", "0",
            "--min-author", "0",
            "--require-license",
            "--require-fulltext",
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "licensed full-text corpus should pass the corpus gate")
        candidate_copy = temp / "candidate-copy.md"
        candidate_copy.write_text((corpus / "target-a.md").read_text(encoding="utf-8"), encoding="utf-8")
        process, payload = run("audit_style_overlap.py", str(corpus), str(candidate_copy))
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["overlaps"], "copied corpus prose should trigger the overlap gate")
        candidate_safe = temp / "candidate-safe.md"
        candidate_safe.write_text("This fixture reports a separately reasoned result with distinct wording.\n", encoding="utf-8")
        process, payload = run("audit_style_overlap.py", str(corpus), str(candidate_safe))
        expect(process.returncode == 0 and payload["status"] == "pass", "distinct candidate prose should pass the overlap gate")
        checks.append("writing/corpus-license-and-overlap-gates")

        process, payload = run("validate_style_profile_gate.py", str(profile_path))
        expect(process.returncode != 0 and payload["gate"] == "confirmation-required", "draft style profile must require a valid confirmation gate")
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
        style_plan_path = temp / "style-revision-plan.json"
        process, payload = run("plan_style_revision.py", str(FIXTURES / "target-a.md"), str(confirmed_path), "--section", "whole-document", "--output", str(style_plan_path))
        expect(process.returncode == 0 and payload["status"] == "pass" and not payload["plan"]["confirmation_required"] and payload["plan"]["confirmation_mode"] == "human", "confirmed profile should produce a structural revision plan without applying prose")
        process, payload = run("plan_style_revision.py", str(FIXTURES / "target-a.md"), str(profile_path), "--section", "whole-document")
        expect(process.returncode != 0 and payload["status"] == "blocked", "draft profile must not drive a revision plan")
        checks.append("writing/section-style-revision-plan")

        style_packet_path = temp / "style-review-packet.json"
        process, payload = run("build_ai_review_packet.py", str(profile_path), "--kind", "style-profile", "--output", str(style_packet_path))
        expect(process.returncode == 0 and payload["packet"]["risk_level"] == "medium", "style profile should create a medium-risk AI packet")
        style_packet = json.loads(style_packet_path.read_text(encoding="utf-8"))
        process, payload = run("run_ai_reviews.py", str(style_packet_path), "--output-dir", str(temp / "live-ai-reviews"), "--dry-run")
        expect(process.returncode == 0 and payload["capability"] == "Documented" and payload["reviews_requested"] == 2, "AI review adapter dry run should expose the required review count without claiming a live test")
        checks.append("writing/ai-review-adapter-dry-run")
        style_review_a, style_review_b = temp / "style-review-a.json", temp / "style-review-b.json"
        write_fixture_review(style_packet, style_review_a, "style-a")
        write_fixture_review(style_packet, style_review_b, "style-b")
        one_review_decision = temp / "style-one-review-decision.json"
        process, payload = run("adjudicate_ai_reviews.py", str(style_packet_path), str(style_review_a), "--output", str(one_review_decision))
        expect(process.returncode != 0 and payload["decision"]["status"] == "blocked", "medium-risk AI gate must reject a single review")
        style_decision_path = temp / "style-decision.json"
        process, payload = run("adjudicate_ai_reviews.py", str(style_packet_path), str(style_review_a), str(style_review_b), "--output", str(style_decision_path))
        expect(process.returncode == 0 and payload["decision"]["decision"] == "ai-approved", "two isolated reviews should approve a medium-risk style profile")
        process, payload = run("adjudicate_ai_reviews.py", str(style_packet_path), str(style_review_a), str(style_review_a))
        expect(process.returncode != 0 and payload["decision"]["status"] == "blocked", "duplicated reviewer identity must not satisfy isolation")
        process, payload = run("validate_style_profile_gate.py", str(profile_path), "--ai-decision", str(style_decision_path))
        expect(process.returncode == 0 and payload["gate"] == "ai-consensus", "AI consensus should satisfy the style profile gate")
        tampered_profile_path = temp / "style-profile-tampered.json"
        tampered_profile = deepcopy(profile)
        tampered_profile["target_outlet"] = "Changed after review"
        tampered_profile_path.write_text(json.dumps(tampered_profile, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("validate_style_profile_gate.py", str(tampered_profile_path), "--ai-decision", str(style_decision_path))
        expect(process.returncode != 0 and any("hash" in error for error in payload["errors"]), "AI decision must not authorize a changed artifact")
        ai_style_plan = temp / "ai-style-plan.json"
        process, payload = run("plan_style_revision.py", str(FIXTURES / "target-a.md"), str(profile_path), "--ai-decision", str(style_decision_path), "--output", str(ai_style_plan))
        expect(process.returncode == 0 and payload["plan"]["confirmation_mode"] == "ai-consensus", "AI-confirmed profile should drive only a structural plan")
        checks.append("writing/hash-bound-ai-style-consensus")
        rubric_bundle_path = temp / "writing-review-bundle.json"
        process, payload = run("build_writing_review_bundle.py", str(FIXTURES / "target-a.md"), str(FIXTURES / "target-b.md"), "--style-profile", str(profile_path), "--output", str(rubric_bundle_path))
        expect(process.returncode == 0 and payload["bundle"]["review_scope"] == ["claim-clarity", "argument-flow", "evidence-alignment", "method-language", "author-voice"], "writing-effect bundle should preserve the original/revised pair and rubric scope")
        rubric_packet_path = temp / "writing-rubric-packet.json"
        process, payload = run("build_ai_review_packet.py", str(rubric_bundle_path), "--kind", "writing-rubric", "--output", str(rubric_packet_path))
        expect(process.returncode == 0 and payload["packet"]["risk_level"] == "medium", "provisional writing rubric should require two AI reviews")
        checks.append("writing/provisional-ai-effect-rubric")
        for kind, artifact in (("ai-review-packet", style_packet_path), ("ai-review", style_review_a), ("ai-gate-decision", style_decision_path), ("writing-review-bundle", rubric_bundle_path)):
            process, payload = run("validate_writing_contract.py", kind, str(artifact))
            expect(process.returncode == 0 and payload["status"] == "pass", f"{kind} should pass the shared contract")
        checks.append("writing/ai-artifact-contracts")

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
        manuscript_candidate = temp / "candidate-manuscript.md"
        manuscript_candidate.write_text("# Introduction\n\nWe find that the policy changes investment under the stated design.\n\n# Results\n\nThe results show a positive association in the observed sample.\n", encoding="utf-8")
        candidate_spine_path = temp / "candidate-paper-spine.json"
        process, payload = run("build_paper_spine.py", "--manuscript", str(manuscript_candidate), "--paper-id", "candidate-paper", "--output", str(candidate_spine_path))
        expect(process.returncode == 0 and payload["status"] == "pass" and payload["paper_spine"]["candidate_status"] == "needs-review" and len(payload["paper_spine"]["contribution_chain"]) == 2, "paper spine should extract reviewable candidate claims from text")
        checks.append("argument/reverse-outline-candidate")
        spine_packet_path = temp / "spine-review-packet.json"
        process, payload = run("build_ai_review_packet.py", str(candidate_spine_path), "--kind", "paper-spine", "--output", str(spine_packet_path))
        spine_packet = json.loads(spine_packet_path.read_text(encoding="utf-8"))
        spine_review_a, spine_review_b = temp / "spine-review-a.json", temp / "spine-review-b.json"
        write_fixture_review(spine_packet, spine_review_a, "spine-a")
        write_fixture_review(spine_packet, spine_review_b, "spine-b")
        spine_decision_path = temp / "spine-decision.json"
        process, payload = run("adjudicate_ai_reviews.py", str(spine_packet_path), str(spine_review_a), str(spine_review_b), "--output", str(spine_decision_path))
        expect(process.returncode == 0, "two isolated reviews should approve candidate spine for structural use")
        reviewed_spine_path = temp / "paper-spine-ai-reviewed.json"
        process, payload = run("approve_paper_spine.py", str(candidate_spine_path), str(spine_decision_path), "--output", str(reviewed_spine_path))
        expect(process.returncode == 0 and payload["paper_spine"]["candidate_status"] == "ai-reviewed" and payload["paper_spine"]["author_adoption_required"], "AI consensus should remove workflow confirmation while preserving author adoption boundary")
        checks.append("argument/hash-bound-ai-spine-consensus")

        meaning_packet_path = temp / "meaning-review-packet.json"
        process, payload = run("build_ai_review_packet.py", str(manuscript_candidate), "--kind", "meaning-change", "--output", str(meaning_packet_path))
        meaning_packet = json.loads(meaning_packet_path.read_text(encoding="utf-8"))
        meaning_review_a, meaning_review_b = temp / "meaning-review-a.json", temp / "meaning-review-b.json"
        write_fixture_review(meaning_packet, meaning_review_a, "meaning-a")
        write_fixture_review(meaning_packet, meaning_review_b, "meaning-b")
        process, payload = run("adjudicate_ai_reviews.py", str(meaning_packet_path), str(meaning_review_a), str(meaning_review_b))
        expect(process.returncode != 0 and payload["decision"]["decision"] == "author-required", "AI consensus must not self-approve high-risk scholarly meaning")
        checks.append("meaning/high-risk-author-boundary")

        process, payload = run(
            "check_claim_evidence.py",
            str(spine_path),
            "--evidence-pack", str(FIXTURES / "evidence-pack.json"),
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "claim evidence should resolve against the evidence pack")
        checks.append("argument/claim-evidence-binding")

        evidence_input = temp / "evidence-ledger-input.json"
        evidence_input.write_text(
            json.dumps(
                {
                    "entries": [
                        {
                            "claim_id": "CLM-001",
                            "claim": "The policy increased investment.",
                            "source": {"source_id": "SRC-001", "title": "Fixture source", "authors": ["Fixture Author"], "year": 2024, "url": "https://example.org/fixture-source", "doi": "10.1234/fixture.001"},
                            "verification": {"level": "full_text", "status": "verified", "checked_at": "2026-08-04", "locator": {"page": 12, "table": "Table 3"}, "support_scope": "Supports the direction and sample context only.", "limitations": ["Does not establish a universal effect."]},
                            "allowed_use": ["direct_citation", "background_only"],
                        },
                        {
                            "claim_id": "CLM-002",
                            "claim": "The mechanism is consistent with the theory.",
                            "source": {"source_id": "SRC-001", "title": "Fixture source", "authors": ["Fixture Author"], "year": 2024, "url": "https://example.org/fixture-source", "doi": "10.1234/fixture.001"},
                            "verification": {"level": "full_text", "status": "verified", "checked_at": "2026-08-04", "locator": {"page": 15}, "support_scope": "Provides a theoretical interpretation.", "limitations": []},
                            "allowed_use": ["background_only"],
                        },
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        evidence_ledger = temp / "evidence-ledger.json"
        process, payload = run(
            "build_evidence_ledger.py",
            str(evidence_input),
            "--output", str(evidence_ledger),
        )
        expect(
            process.returncode == 0 and payload["status"] == "pass" and len(payload["ledger"]["entries"]) == 2,
            f"evidence ledger should preserve many-to-many claim/source bindings: {payload}",
        )
        ledger = json.loads(evidence_ledger.read_text(encoding="utf-8"))
        expect(len(ledger["source_index"]) == 1 and ledger["rejections"] == [], "evidence ledger should deduplicate source metadata")
        process, payload = run("validate_writing_contract.py", "evidence-ledger", str(evidence_ledger))
        expect(process.returncode == 0 and payload["status"] == "pass", "evidence ledger should pass the shared writing contract")
        process, payload = run("check_evidence_impact.py", str(evidence_ledger), "SRC-001")
        expect(process.returncode == 0 and payload["impact_count"] == 2 and {item["claim_id"] for item in payload["affected_claims"]} == {"CLM-001", "CLM-002"}, "source withdrawal should list all impacted claims")
        invalid_evidence = temp / "evidence-ledger-invalid.json"
        invalid_evidence.write_text(
            json.dumps(
                {
                    "entries": [
                        {
                            "claim_id": "CLM-003",
                            "claim": "Candidate evidence.",
                            "source": {"source_id": "SRC-002", "title": "Metadata-only source", "url": "https://example.org/metadata"},
                            "verification": {"level": "metadata", "status": "metadata-only", "checked_at": "2026-08-04", "support_scope": "Metadata only.", "limitations": ["No full text checked."]},
                            "allowed_use": ["direct_citation"],
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        process, payload = run("build_evidence_ledger.py", str(invalid_evidence), "--output", str(temp / "invalid-ledger.json"))
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["ledger"]["rejections"], "unsafe direct citation should be rejected")
        checks.append("evidence/many-to-many-ledger-and-rejections")

        process, payload = run("audit_evidence_freshness.py", str(evidence_ledger), "--max-age-days", "365")
        expect(process.returncode == 0 and payload["status"] == "pass" and payload["counts"]["fresh"] == 2, "fresh evidence bindings should pass the freshness gate")
        stale_ledger = deepcopy(ledger)
        stale_ledger["entries"][0]["verification"]["checked_at"] = "2020-01-01"
        stale_ledger_path = temp / "evidence-ledger-stale.json"
        stale_ledger_path.write_text(json.dumps(stale_ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("audit_evidence_freshness.py", str(stale_ledger_path), "--max-age-days", "365")
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["counts"]["direct_citation_blocked"] == 1, "stale direct-citation evidence must be blocked")
        checks.append("evidence/freshness-and-stale-direct-citation-gate")

        journal_card = {
            "schema_version": "1.0",
            "target_outlet": "Fixture Journal",
            "verification_basis": "official author guideline fixture",
            "checked_at": "2026-08-04",
            "claims": [{"claim": "submission language", "value": "English", "source_url": "https://example.org/fixture-journal", "status": "verified", "applies_to": "research article", "stage": "submission"}],
        }
        journal_card_path = temp / "journal-card.json"
        journal_card_path.write_text(json.dumps(journal_card, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("audit_journal_freshness.py", str(journal_card_path), "--max-age-days", "365")
        expect(process.returncode == 0 and payload["status"] == "pass" and payload["counts"]["claims"] == 1, "fresh journal card should pass the freshness gate")
        stale_card = deepcopy(journal_card)
        stale_card["checked_at"] = "2020-01-01"
        stale_card_path = temp / "journal-card-stale.json"
        stale_card_path.write_text(json.dumps(stale_card, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("audit_journal_freshness.py", str(stale_card_path), "--max-age-days", "365")
        expect(process.returncode != 0 and payload["status"] == "fail", "stale journal card must block dynamic adaptation")
        checks.append("journal/freshness-and-stale-adaptation-gate")

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

        issue_proposed = temp / "review-ledger-proposed.json"
        process, payload = run(
            "transition_issue.py", str(routed_path), "ISS-001", "proposed",
            "--output", str(issue_proposed), "--actor", "fixture-author", "--rationale", "Scope and acceptance criteria are recorded.",
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "triaged issue should transition to proposed")
        issue_applied = temp / "review-ledger-applied.json"
        process, payload = run(
            "transition_issue.py", str(issue_proposed), "ISS-001", "applied",
            "--output", str(issue_applied), "--actor", "fixture-author", "--rationale", "Verified safe-fix output is available.",
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "proposed issue should transition to applied")
        issue_verified = temp / "review-ledger-verified.json"
        process, payload = run(
            "transition_issue.py", str(issue_applied), "ISS-001", "verified",
            "--output", str(issue_verified), "--actor", "fixture-author", "--rationale", "Post-apply gates pass.",
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "applied issue should transition to verified")
        issue_closed = temp / "review-ledger-closed.json"
        process, payload = run(
            "transition_issue.py", str(issue_verified), "ISS-001", "closed",
            "--output", str(issue_closed), "--actor", "fixture-author", "--rationale", "Reviewer issue is closed with a traceable verification.", "--evidence", "apply-report.json",
        )
        expect(process.returncode == 0 and payload["status"] == "pass", "verified issue should transition to closed")
        process, payload = run("build_response_letter.py", str(issue_closed), "--output", str(temp / "response-letter.md"))
        expect(process.returncode == 0 and payload["status"] == "pass" and "ISS-001" in (temp / "response-letter.md").read_text(encoding="utf-8"), "response letter should derive from the ledger")
        process, payload = run(
            "transition_issue.py", str(routed_path), "ISS-001", "closed",
            "--output", str(temp / "invalid-transition.json"), "--actor", "fixture-author", "--rationale", "Should fail.",
        )
        expect(process.returncode != 0 and payload["status"] == "fail", "illegal direct issue closure must fail")
        matrix_json = temp / "revision-matrix.json"
        matrix_csv = temp / "revision-matrix.csv"
        process, payload = run("build_revision_matrix.py", str(issue_closed), "--output", str(matrix_json))
        expect(process.returncode == 0 and payload["status"] == "pass" and matrix_json.is_file(), "revision matrix JSON should derive from the ledger")
        process, payload = run("build_revision_matrix.py", str(issue_closed), "--output", str(matrix_csv))
        expect(process.returncode == 0 and payload["status"] == "pass" and matrix_csv.read_text(encoding="utf-8").startswith("issue_id,"), "revision matrix CSV should be exportable")
        scaffold = temp / "response-scaffold.md"
        process, payload = run("build_response_letter.py", str(issue_closed), "--output", str(scaffold))
        process, payload = run("validate_response_letter.py", str(issue_closed), str(scaffold))
        expect(process.returncode != 0 and payload["status"] == "fail" and payload["counts"]["placeholders"] > 0, "response scaffold must not pass submission validation")
        single_closed = json.loads(issue_closed.read_text(encoding="utf-8"))
        single_closed["issues"] = [single_closed["issues"][0]]
        single_closed_path = temp / "review-ledger-single-closed.json"
        single_closed_path.write_text(json.dumps(single_closed, ensure_ascii=False, indent=2), encoding="utf-8")
        complete_letter = temp / "response-complete.md"
        complete_letter.write_text("## ISS-001\n\nReviewer comment addressed.\n\nAuthor response: We clarified the scope and retained all protected values.\n\nChange made: The wording was updated in the method section.\n\nEvidence: apply-report.json\n", encoding="utf-8")
        process, payload = run("validate_response_letter.py", str(single_closed_path), str(complete_letter))
        expect(process.returncode == 0 and payload["status"] == "pass", "complete response letter should pass submission validation")
        checks.append("revision/issue-transitions-and-response-letter")

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

        _, proposed_good = run(
            "propose_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-good.md"),
            "--variable", "Treatment",
        )
        applied_path = temp / "applied.md"
        process, payload = run(
            "apply_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-good.md"),
            "--output", str(applied_path),
            "--variable", "Treatment",
            "--expected-original-sha256", proposed_good["original_sha256"],
            "--report", str(temp / "apply-report.json"),
        )
        expect(process.returncode == 0 and payload["applied"] and applied_path.read_text(encoding="utf-8") == (FIXTURES / "original.md").read_text(encoding="utf-8"), "verified safe-fix should apply to a separate output")
        rollback_path = temp / "rollback.md"
        process, payload = run(
            "rollback_bounded_patch.py",
            str(FIXTURES / "original.md"),
            "--output", str(rollback_path),
            "--expected-original-sha256", proposed_good["original_sha256"],
        )
        expect(process.returncode == 0 and payload["restored"] and rollback_path.read_text(encoding="utf-8") == applied_path.read_text(encoding="utf-8"), "rollback should restore the known-good snapshot")
        process, payload = run(
            "apply_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-bad.md"),
            "--output", str(temp / "bad-applied.md"),
            "--variable", "Treatment",
        )
        expect(process.returncode != 0 and not payload["applied"], "unsafe patch must not apply without explicit confirmation")
        process, payload = run(
            "apply_bounded_patch.py",
            str(FIXTURES / "original.md"),
            str(FIXTURES / "revised-bad.md"),
            "--output", str(temp / "author-confirmed.md"),
            "--variable", "Treatment",
            "--allow-author-required",
            "--author-confirmed",
            "--confirmed-by", "fixture-author",
            "--rationale", "The author supplied a corrected coefficient and citation after checking the underlying table.",
        )
        expect(process.returncode == 0 and payload["applied"] and payload["confirmation"]["confirmed_by"] == "fixture-author", "author-required patch should need an auditable confirmation record")
        checks.append("revision/apply-rollback-hash-gate")

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
        process, payload = run("check_method_language.py", str(METHOD_FIXTURES / "extended-overclaim-en.md"))
        expect(process.returncode != 0 and payload["issue_count"] >= 6, "extended English method overclaims should be detected")
        process, payload = run("check_method_language.py", str(METHOD_FIXTURES / "extended-overclaim-zh.md"))
        expect(process.returncode != 0 and payload["issue_count"] >= 5, "extended Chinese method overclaims should be detected")
        process, payload = run("build_method_safety_report.py", str(METHOD_FIXTURES / "extended-overclaim-en.md"))
        expect(process.returncode != 0 and payload["issue_count"] >= 6 and all(issue["conservative_rewrite"] for issue in payload["issues"]), "method findings should include conservative rewrite guidance")
        process, payload = run("validate_method_safety_catalog.py", str(ROOT / "assets" / "method-safety-cards.json"))
        expect(process.returncode == 0 and payload["status"] == "pass", "method safety catalog should validate")
        checks.append("method-safety/risk-card-catalog")

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
        process, payload = run("validate_skill_package.py", str(ROOT))
        expect(process.returncode == 0 and payload["status"] == "pass", "skill package contract should pass")
        process, payload = run("quick_validate.py", str(ROOT))
        expect(process.returncode == 0 and payload["status"] == "pass", "Skill Creator-compatible quick validation should pass")
        process, payload = run("validate_repro_lock.py", str(ROOT))
        expect(process.returncode == 0 and payload["status"] == "pass", "reproducibility lock should pass")
        checks.append("engineering/package-and-repro-lock")

        workspace = temp / "paper-workspace"
        process, payload = run("init_writing_workspace.py", str(workspace), "--paper-id", "fixture-paper")
        expect(process.returncode == 0 and payload["status"] == "pass", "writing workspace should initialize")
        original = workspace / "manuscript" / "original.md"
        current = workspace / "manuscript" / "current.md"
        manuscript = "The estimate is 0.25 (p<0.05) for Treatment.\n"
        original.write_text(manuscript, encoding="utf-8")
        current.write_text(manuscript, encoding="utf-8")
        route_path = workspace / "route-card.json"
        route = json.loads(route_path.read_text(encoding="utf-8"))
        route.update({
            "task_mode": "audit",
            "discipline": "economics",
            "language": "en-US",
            "confidence": "high",
            "unresolved": [],
            "rationale": ["Fixture route is explicit and reviewed."],
        })
        route_path.write_text(json.dumps(route, ensure_ascii=False, indent=2), encoding="utf-8")
        process, payload = run("run_writing_workflow.py", str(workspace), "--variable", "Treatment")
        expect(process.returncode == 0 and payload["status"] == "pass", "writing workflow should run all applicable gates")
        checkpoint = json.loads((workspace / "checkpoint.json").read_text(encoding="utf-8"))
        capability = json.loads((workspace / "capability-report.json").read_text(encoding="utf-8"))
        snapshot = json.loads((workspace / "protected-snapshot.json").read_text(encoding="utf-8"))
        expect(checkpoint["status"] == "complete" and capability["overall_mode"] == "Verified", "workflow must persist a completed checkpoint and capability report")
        expect(snapshot["sha256"] and snapshot["protected"]["anchors"], "workflow must persist protected line anchors")
        journal_lines = (workspace / "revision-journal.jsonl").read_text(encoding="utf-8").splitlines()
        expect(len(journal_lines) >= 4, "workflow must persist stage events")
        process, payload = run("validate_revision_journal.py", str(workspace / "revision-journal.jsonl"))
        expect(process.returncode == 0 and payload["status"] == "pass", "revision journal should validate as append-only JSONL")
        process, payload = run("run_platform_smoke.py", "--root", str(ROOT))
        expect(process.returncode == 0 and payload["status"] == "pass" and payload["capabilities"]["utf8"] == "Verified", "portable platform smoke should pass with honest TeX capability reporting")
        checks.append("engineering/workspace-route-checkpoint-workflow")

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
