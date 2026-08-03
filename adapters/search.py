"""Provider fan-out and metadata deduplication."""

from __future__ import annotations

import re
from typing import Iterable

from .protocols import SearchProvider, SearchRequest, SourceRecord


def _key(record: SourceRecord) -> str:
    if record.doi:
        return "doi:" + record.doi.lower().strip()
    return "title:" + re.sub(r"\W+", " ", record.title.lower()).strip()


class MultiProviderSearch:
    def __init__(self, providers: Iterable[SearchProvider]) -> None:
        self.providers = list(providers)

    def search(self, request: SearchRequest) -> tuple[list[SourceRecord], list[str]]:
        records: list[SourceRecord] = []
        errors: list[str] = []
        for provider in self.providers:
            try:
                records.extend(provider.search(request))
            except Exception as exc:  # provider failure is reported, not hidden
                errors.append(f"{getattr(provider, 'name', provider.__class__.__name__)}: {exc}")
        unique: dict[str, SourceRecord] = {}
        for record in records:
            key = _key(record)
            if key not in unique or (not unique[key].abstract and record.abstract):
                unique[key] = record
        return list(unique.values())[: request.max_results], errors
