"""Optional, dependency-free integration adapters for v3."""

from .protocols import AgentResult, AgentTask, RagHit, SearchRequest, SourceRecord

__all__ = ["AgentResult", "AgentTask", "RagHit", "SearchRequest", "SourceRecord"]
