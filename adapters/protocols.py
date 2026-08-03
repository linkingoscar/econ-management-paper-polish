"""Stable data contracts shared by source, RAG, and agent adapters."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Protocol


@dataclass
class SearchRequest:
    query: str
    max_results: int = 10
    year_from: int | None = None
    year_to: int | None = None
    mailto: str | None = None


@dataclass
class SourceRecord:
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    doi: str | None = None
    url: str | None = None
    abstract: str | None = None
    provider: str = "unknown"
    provider_id: str | None = None
    retrieved_at: str | None = None
    access_tier: str = "metadata"
    open_access_url: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("raw", None)
        return value


class SearchProvider(Protocol):
    name: str

    def search(self, request: SearchRequest) -> list[SourceRecord]:
        """Return normalized metadata candidates; never mark them citable."""


@dataclass
class RagHit:
    chunk_id: str
    path: str
    text: str
    score: float
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTask:
    task_id: str
    role: str
    prompt: str
    depends_on: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    task_id: str
    role: str
    status: str
    output: str | None = None
    error: str | None = None
    capability: str = "Conceptual"
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
