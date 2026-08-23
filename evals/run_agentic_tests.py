#!/usr/bin/env python3
"""Run offline tests for blinded Agent judging and adversarial generation."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.agentic_benchmark_contract import build_judge_prompt, canonical_sha256, adjudicate_agentic_reviews, validate_agentic_packet
from scripts.audit_latex import audit as audit_latex
from scripts.build_agentic_review_packet import build
from scripts.generate_adversarial_mutations import generate
from scripts.writing_contract import load_json


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_review(packet: dict, index: int, winner: str, *, provider: str = "fixture", model: str = "same-model") -> dict:
    profile = packet["judge_profiles"][index]
    raw_response = json.dumps({"fixture": index}, sort_keys=True)
    scores = []
    for variant in packet["blind_variants"]:
        is_winner = variant["blind_id"] == winner
        scores.append(
            {
                "blind_id": variant["blind_id"],
                "criteria": [
                    {
                        "criterion_id": criterion["criterion_id"],
                        "score": 4 if is_winner else 2,
                        "reason": "Fixture preference used to test deterministic adjudication precedence.",
                        "evidence": ["fixture-locator"],
                    }
                    for criterion in packet["rubric"]
                ],
            }
        )
    return {
        "schema_version": "1.0",
        "review_id": f"review-{index}",
        "packet_id": packet["packet_id"],
        "packet_sha256": canonical_sha256(packet),
        "reviewer": {
            "kind": "ai",
            "reviewer_id": f"isolated-{index}",
            "provider": provider,
            "model": model,
            "isolated_pass": True,
        },
        "provenance": {
            "judge_profile_id": profile["judge_profile_id"],
            "request_id": f"fixture-request-{index}",
            "prompt_sha256": hashlib.sha256(build_judge_prompt(packet, profile).encode("utf-8")).hexdigest(),
            "raw_response_sha256": hashlib.sha256(raw_response.encode("utf-8")).hexdigest(),
            "attempt": 1,
            "finish_reason": "stop",
        },
        "raw_response": raw_response,
        "scores": scores,
        "pairwise": {"verdict": "winner", "winner": winner, "reason": "Fixture vote."},
        "confidence": 0.8,
        "limitations": ["Synthetic fixture review."],
        "created_at": "2026-08-24T00:00:00Z",
    }


def build_fixture(case_id: str) -> tuple[dict, dict]:
    manifest = load_json(ROOT / "evals" / "agentic" / "manifest.json")
    variants = {
        "candidate-a": ROOT / "evals" / "agentic" / "fixtures" / "candidate-safe.md",
        "candidate-b": ROOT / "evals" / "agentic" / "fixtures" / "candidate-number-swap.md",
    }
    return build(manifest, case_id, variants, seed="offline-agentic-test", max_chars=50000)


def main() -> int:
    checks: list[str] = []
    packet, mapping = build_fixture("results-low-risk")
    expect(not validate_agentic_packet(packet), "generated packet must satisfy its contract")
    expect("blind_mapping" not in packet and all("hard_audit" not in item for item in packet["blind_variants"]), "public packet leaked private adjudication data")
    checks.append("packet/blind-private-separation")

    tampered = copy.deepcopy(packet)
    tampered["blind_variants"][0]["content"] += "tampered"
    expect(any("content hash" in item for item in validate_agentic_packet(tampered)), "variant content tampering must be rejected")
    malformed = copy.deepcopy(packet)
    malformed["blind_variants"][0]["blind_id"] = {"not": "hashable"}
    malformed_errors = validate_agentic_packet(malformed)
    malformed_decision = adjudicate_agentic_reviews(malformed, [], mapping)
    expect(malformed_errors and malformed_decision["status"] == "fail", "malformed packet fields must fail closed without crashing")
    checks.append("packet/content-hash-binding")

    safe_blind = next(blind for blind, variant in mapping["blind_to_variant"].items() if variant == "candidate-a")
    unsafe_blind = next(blind for blind, variant in mapping["blind_to_variant"].items() if variant == "candidate-b")
    expect(mapping["hard_audits"][safe_blind]["status"] == "pass" and mapping["hard_audits"][unsafe_blind]["status"] == "fail", "hard audit fixture classification changed")
    checks.append("gates/local-number-binding")

    reviews = [make_review(packet, index, unsafe_blind) for index in range(3)]
    decision = adjudicate_agentic_reviews(packet, reviews, mapping)
    expect(decision["status"] == "pass" and decision["winner_blind"] == safe_blind and decision["decision_reason"] == "hard-gate-precedence", "hard gates must override unanimous Agent preference")
    expect(decision["confidence_mode"] == "single-model-low-confidence", "same-model panels must be labeled low confidence")
    checks.append("adjudication/hard-gate-precedence")
    checks.append("adjudication/single-model-label")

    cross_reviews = [
        make_review(packet, 0, unsafe_blind, provider="provider-a", model="model-a"),
        make_review(packet, 1, unsafe_blind, provider="provider-b", model="model-b"),
        make_review(packet, 2, unsafe_blind, provider="provider-a", model="model-a"),
    ]
    cross_decision = adjudicate_agentic_reviews(packet, cross_reviews, mapping)
    expect(cross_decision["confidence_mode"] == "cross-model-evaluated", "mixed provider/model panels must record cross-model evaluation")
    checks.append("adjudication/cross-model-label")

    invalid_reviews = copy.deepcopy(reviews)
    invalid_reviews[2]["packet_sha256"] = "0" * 64
    invalid_decision = adjudicate_agentic_reviews(packet, invalid_reviews, mapping)
    expect(invalid_decision["status"] == "fail" and invalid_decision["rejected_reviews"], "invalid review must fail closed")
    checks.append("adjudication/invalid-review-fail-closed")

    high_packet, high_mapping = build_fixture("results-high-risk")
    high_safe = next(blind for blind, variant in high_mapping["blind_to_variant"].items() if variant == "candidate-a")
    high_reviews = [make_review(high_packet, index, high_safe) for index in range(3)]
    high_decision = adjudicate_agentic_reviews(high_packet, high_reviews, high_mapping)
    expect(high_decision["status"] == "blocked" and high_decision["decision"] == "high-risk-no-ai-authorization", "high-risk Agent consensus must remain blocked")
    checks.append("adjudication/high-risk-no-ai-authorization")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        candidate_process = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_agentic_candidates.py"), str(ROOT / "evals" / "agentic" / "manifest.json"), "results-low-risk", "--output-dir", str(temp / "candidates"), "--dry-run", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        candidate_dry = json.loads(candidate_process.stdout)
        packet_path = temp / "packet.json"
        packet_path.write_text(json.dumps(packet, ensure_ascii=False), encoding="utf-8")
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_agentic_judges.py"), str(packet_path), "--output-dir", str(temp / "runs"), "--dry-run", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        dry = json.loads(process.stdout)
        expect(candidate_process.returncode == 0 and candidate_dry["status"] == "pass" and len(candidate_dry["candidate_prompts"]) == 2 and not candidate_dry["outputs"], "candidate dry run must validate isolated prompts without calling models")
        expect(process.returncode == 0 and dry["status"] == "pass" and dry["capability"] == "Documented" and not dry["outputs"], "judge dry run must validate prompts without calling models")
    checks.append("runners/offline-candidate-and-judge-dry-run")

    adversarial_manifest = load_json(ROOT / "evals" / "adversarial" / "manifest.json")
    with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
        first = generate(adversarial_manifest, Path(first_dir))
        second = generate(adversarial_manifest, Path(second_dir))
        expect(first == second and first["mutation_count"] == 8 and not first["skipped"], "adversarial suite must be deterministic and cover all configured operators")
        expect(all(item["oracle_issue_codes"] for item in first["cases"] if item["operator"] != "safe-control"), "every admitted mutation needs oracle evidence")
    checks.append("adversarial/deterministic-eight-operators")
    checks.append("adversarial/independent-oracle-evidence")

    with tempfile.TemporaryDirectory() as temp_dir:
        duplicate = Path(temp_dir) / "duplicate.tex"
        duplicate.write_text("\\documentclass{article}\n\\begin{document}\n\\label{x}\n\\label{x}\n\\end{document}\n", encoding="utf-8")
        latex = audit_latex(duplicate)
        expect(any(item["code"] == "duplicate-label" for item in latex["issues"]), "LaTeX audit must reject duplicate labels")
    checks.append("latex/duplicate-label")

    print(f"agentic benchmark tests passed ({len(checks)} checks)")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"agentic benchmark tests failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
