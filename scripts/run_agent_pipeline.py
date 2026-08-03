#!/usr/bin/env python3
"""Validate and run a bounded dependency-aware multi-role agent pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.agents import OpenAICompatibleAgent, SerialAgentRunner, validate_tasks
from adapters.protocols import AgentTask


def load_tasks(path: Path) -> list[AgentTask]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    raw_tasks = payload.get("tasks") if isinstance(payload, dict) else payload
    if not isinstance(raw_tasks, list):
        raise ValueError("input must be a task array or an object with tasks")
    tasks = []
    for index, value in enumerate(raw_tasks):
        if not isinstance(value, dict):
            raise ValueError(f"tasks[{index}] must be an object")
        tasks.append(AgentTask(str(value.get("task_id", "")), str(value.get("role", "")), str(value.get("prompt", "")), list(value.get("depends_on", [])), dict(value.get("context", {}))))
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--provider", choices=("serial", "openai-compatible"), default="serial")
    parser.add_argument("--dry-run", action="store_true", help="Validate dependency graph without calling a provider")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        tasks = load_tasks(args.input)
        ordered, errors = validate_tasks(tasks)
        if errors:
            result = {"status": "fail", "capability": "Verified", "errors": errors, "results": []}
        elif args.dry_run:
            result = {"status": "pass", "capability": "Verified", "errors": [], "order": [task.task_id for task in ordered], "results": []}
        else:
            agent = OpenAICompatibleAgent() if args.provider == "openai-compatible" else None
            handlers = {task.role: agent.run for task in tasks} if agent else {}
            results, run_errors = SerialAgentRunner(handlers).run(tasks)
            result = {"status": "pass" if not run_errors and all(item.status in {"pass", "conceptual"} for item in results) else "fail", "capability": "Verified" if agent else "Conceptual", "errors": run_errors, "results": [item.to_dict() for item in results]}
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "capability": "Verified", "errors": [str(exc)], "results": []}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']} ({result['capability']})")
        for item in result.get("results", []):
            print(f"- {item.get('task_id')}: {item.get('status')}")
        for error in result.get("errors", []):
            print(f"error: {error}", file=sys.stderr)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
