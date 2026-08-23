"""Optional OpenAI-compatible HTTP agent adapter.

The adapter is opt-in. It reads the API key from the environment and never prints
the key. Without credentials it returns a transparent Conceptual result.
"""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..protocols import AgentResult, AgentTask


class OpenAICompatibleAgent:
    def __init__(self, base_url: str | None = None, api_key: str | None = None, model: str | None = None, timeout: float = 60.0) -> None:
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL")
        self.timeout = timeout

    def run(self, task: AgentTask) -> AgentResult:
        if not self.api_key or not self.model:
            return AgentResult(task.task_id, task.role, "conceptual", error="OPENAI_API_KEY and OPENAI_MODEL are required", capability="Conceptual")
        payload = {"model": self.model, "temperature": 0, "messages": [{"role": "system", "content": f"You are the {task.role} role. Return a bounded report; do not invent evidence."}, {"role": "user", "content": task.prompt}]}
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            choice = body.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content")
            if not isinstance(content, str) or not content.strip():
                return AgentResult(task.task_id, task.role, "fail", error="provider returned no message content", capability="Verified")
            return AgentResult(
                task.task_id,
                task.role,
                "pass",
                output=content,
                capability="Verified",
                provenance={
                    "provider": "openai-compatible",
                    "model": self.model,
                    "request_id": body.get("id", "unreported"),
                    "finish_reason": choice.get("finish_reason", "unreported"),
                },
            )
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            return AgentResult(task.task_id, task.role, "fail", error=f"agent request failed: {exc}", capability="Verified")
