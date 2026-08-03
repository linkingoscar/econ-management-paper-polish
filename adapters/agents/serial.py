"""Deterministic multi-role orchestration that also works without sub-agents."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable

from ..protocols import AgentResult, AgentTask


def validate_tasks(tasks: Iterable[AgentTask]) -> tuple[list[AgentTask], list[str]]:
    values = list(tasks)
    errors: list[str] = []
    by_id: dict[str, AgentTask] = {}
    for task in values:
        if not task.task_id or task.task_id in by_id:
            errors.append(f"duplicate or empty task id: {task.task_id!r}")
        by_id[task.task_id] = task
    for task in values:
        for dependency in task.depends_on:
            if dependency not in by_id:
                errors.append(f"{task.task_id} depends on unknown task {dependency}")
    indegree = {task.task_id: 0 for task in values}
    edges: dict[str, list[str]] = {task.task_id: [] for task in values}
    for task in values:
        for dependency in task.depends_on:
            if dependency in by_id:
                indegree[task.task_id] += 1
                edges[dependency].append(task.task_id)
    queue = deque(task.task_id for task in values if indegree[task.task_id] == 0)
    ordered_ids: list[str] = []
    while queue:
        task_id = queue.popleft()
        ordered_ids.append(task_id)
        for child in edges[task_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(ordered_ids) != len(values):
        errors.append("task dependency graph contains a cycle")
    return [by_id[task_id] for task_id in ordered_ids], errors


Handler = Callable[[AgentTask], AgentResult]


class SerialAgentRunner:
    """Run role tasks in dependency order; handlers are explicit and replaceable."""

    def __init__(self, handlers: dict[str, Handler] | None = None) -> None:
        self.handlers = handlers or {}

    def run(self, tasks: Iterable[AgentTask]) -> tuple[list[AgentResult], list[str]]:
        ordered, errors = validate_tasks(tasks)
        if errors:
            return [], errors
        results: dict[str, AgentResult] = {}
        output: list[AgentResult] = []
        for task in ordered:
            failed = [results[dependency] for dependency in task.depends_on if results[dependency].status not in {"pass", "dry-run"}]
            if failed:
                result = AgentResult(task.task_id, task.role, "blocked", error="dependency failed", capability="Documented")
            elif task.role not in self.handlers:
                result = AgentResult(task.task_id, task.role, "conceptual", error="no handler registered for this role", capability="Conceptual")
            else:
                try:
                    result = self.handlers[task.role](task)
                except Exception as exc:  # handlers are isolated per task
                    result = AgentResult(task.task_id, task.role, "fail", error=str(exc), capability="Verified")
            results[task.task_id] = result
            output.append(result)
        return output, []
