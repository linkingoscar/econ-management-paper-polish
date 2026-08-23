#!/usr/bin/env python3
"""Run isolated blind judge profiles for an agentic benchmark packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.agents import OpenAICompatibleAgent
from adapters.protocols import AgentTask
from scripts.agentic_benchmark_contract import build_judge_prompt, canonical_sha256, validate_agentic_packet, validate_agentic_review
from scripts.writing_contract import load_json, utc_now, write_json


def parse_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        stripped = fenced.group(1)
    value = json.loads(stripped)
    if not isinstance(value, dict):
        raise ValueError("judge output must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--judges", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    outputs: list[dict[str, str]] = []
    try:
        packet = load_json(args.packet)
        errors.extend(validate_agentic_packet(packet))
        required = packet.get("judge_policy", {}).get("minimum_judges", 3) if isinstance(packet, dict) else 3
        count = args.judges or required
        profiles = packet.get("judge_profiles", []) if isinstance(packet, dict) else []
        if count < required:
            errors.append(f"judges cannot be below policy minimum {required}")
        if count > len(profiles):
            errors.append("judges exceed declared judge profiles")
        selected = profiles[:count]
        prompts = [(profile, build_judge_prompt(packet, profile)) for profile in selected] if not errors else []
        if args.dry_run and not errors:
            result = {
                "status": "pass",
                "capability": "Documented",
                "packet_id": packet["packet_id"],
                "judges_requested": count,
                "judge_profiles": [
                    {"judge_profile_id": profile["judge_profile_id"], "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(), "prompt_chars": len(prompt)}
                    for profile, prompt in prompts
                ],
                "run_manifest": None,
                "outputs": [],
                "errors": [],
                "limitations": ["Dry run verifies packet and prompts; no model was called."],
            }
        elif not errors:
            run_dir = args.output_dir / packet["packet_id"]
            if run_dir.exists() and any(run_dir.iterdir()):
                raise ValueError("content-addressed judge run directory is not empty; stale outputs are never reused")
            run_dir.mkdir(parents=True, exist_ok=True)
            agent = OpenAICompatibleAgent()
            for index, (profile, prompt) in enumerate(prompts, start=1):
                agent_result = agent.run(AgentTask(f"{packet['packet_id']}-judge-{index}", profile["role"], prompt))
                if agent_result.status != "pass" or not agent_result.output:
                    errors.append(agent_result.error or f"judge {index} failed")
                    continue
                finish_reason = str(agent_result.provenance.get("finish_reason", "unreported"))
                if finish_reason not in {"stop", "unreported"}:
                    errors.append(f"judge {index} response did not finish cleanly: {finish_reason}")
                    continue
                try:
                    body = parse_json(agent_result.output)
                    reviewer_id = f"{profile['judge_profile_id']}-attempt-1"
                    review = {
                        "schema_version": "1.0",
                        "review_id": f"{packet['packet_id']}-{reviewer_id}",
                        "packet_id": packet["packet_id"],
                        "packet_sha256": canonical_sha256(packet),
                        "reviewer": {
                            "kind": "ai",
                            "reviewer_id": reviewer_id,
                            "provider": agent_result.provenance.get("provider", "openai-compatible"),
                            "model": agent_result.provenance.get("model", "unknown"),
                            "isolated_pass": True,
                        },
                        "provenance": {
                            "judge_profile_id": profile["judge_profile_id"],
                            "request_id": str(agent_result.provenance.get("request_id", agent_result.task_id)),
                            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                            "raw_response_sha256": hashlib.sha256(agent_result.output.encode("utf-8")).hexdigest(),
                            "attempt": 1,
                            "finish_reason": finish_reason,
                        },
                        "raw_response": agent_result.output,
                        "scores": body.get("scores"),
                        "pairwise": body.get("pairwise"),
                        "confidence": body.get("confidence"),
                        "limitations": body.get("limitations"),
                        "created_at": utc_now(),
                    }
                    review_errors = validate_agentic_review(review, packet)
                    if review_errors:
                        errors.extend([f"judge {index}: {item}" for item in review_errors])
                        continue
                    output = run_dir / f"{profile['judge_profile_id']}.json"
                    write_json(output, review)
                    outputs.append({"path": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()})
                except (json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"judge {index} returned invalid JSON: {exc}")
            run_manifest = {
                "schema_version": "1.0",
                "packet_id": packet["packet_id"],
                "packet_sha256": canonical_sha256(packet),
                "status": "pass" if len(outputs) == count and not errors else "blocked",
                "capability": "Verified",
                "expected_outputs": count,
                "outputs": outputs,
                "generated_at": utc_now(),
                "errors": errors,
                "limitations": ["Provider transport and schema are verified; scholarly truth is not."],
            }
            manifest_path = run_dir / "run-manifest.json"
            write_json(manifest_path, run_manifest)
            result = {
                "status": run_manifest["status"],
                "capability": "Verified",
                "packet_id": packet["packet_id"],
                "judges_requested": count,
                "run_manifest": str(manifest_path),
                "outputs": [item["path"] for item in outputs],
                "errors": errors,
                "limitations": run_manifest["limitations"],
            }
        else:
            result = {"status": "fail", "capability": "Conceptual", "outputs": [], "errors": errors, "limitations": []}
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "fail", "capability": "Conceptual", "outputs": [], "errors": [str(exc)], "limitations": []}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"status: {result['status']} ({result['capability']})")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
