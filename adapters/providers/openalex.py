"""OpenAlex works-search metadata adapter."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..protocols import SearchRequest, SourceRecord


class ProviderError(RuntimeError):
    """An external provider could not be queried or normalized."""


def _abstract(inverted: object) -> str | None:
    if not isinstance(inverted, dict):
        return None
    positions: dict[int, str] = {}
    for word, indexes in inverted.items():
        if not isinstance(word, str) or not isinstance(indexes, list):
            continue
        for index in indexes:
            if isinstance(index, int):
                positions[index] = word
    if not positions:
        return None
    return " ".join(positions[index] for index in sorted(positions))


def _authors(work: dict) -> list[str]:
    values = []
    for authorship in work.get("authorships", []) or []:
        author = authorship.get("author", {}) if isinstance(authorship, dict) else {}
        name = author.get("display_name") if isinstance(author, dict) else None
        if name:
            values.append(name)
    return values


class OpenAlexProvider:
    name = "openalex"
    base_url = "https://api.openalex.org/works"

    def __init__(self, timeout: float = 20.0, user_agent: str = "econ-management-paper-polish/3.0") -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    def _get(self, url: str) -> dict:
        request = Request(url, headers={"Accept": "application/json", "User-Agent": self.user_agent})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ProviderError(f"OpenAlex request failed: {exc}") from exc

    def _normalize(self, work: dict) -> SourceRecord:
        doi = work.get("doi")
        doi = doi.removeprefix("https://doi.org/").strip() if isinstance(doi, str) else None
        primary = work.get("primary_location") if isinstance(work.get("primary_location"), dict) else {}
        source = primary.get("source") if isinstance(primary.get("source"), dict) else {}
        open_access = work.get("open_access") if isinstance(work.get("open_access"), dict) else {}
        oa_url = (work.get("best_oa_location") or {}).get("landing_page_url") if isinstance(work.get("best_oa_location"), dict) else None
        return SourceRecord(
            title=str(work.get("title") or "Untitled").strip(),
            authors=_authors(work),
            year=work.get("publication_year") if isinstance(work.get("publication_year"), int) else None,
            venue=source.get("display_name") if isinstance(source, dict) else None,
            doi=doi,
            url=work.get("id") or (f"https://doi.org/{doi}" if doi else None),
            abstract=_abstract(work.get("abstract_inverted_index")),
            provider=self.name,
            provider_id=work.get("id"),
            retrieved_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            access_tier="metadata",
            open_access_url=oa_url if open_access.get("is_oa") else None,
            raw=work,
        )

    def search(self, request: SearchRequest) -> list[SourceRecord]:
        params = {"search": request.query, "per-page": str(max(1, min(request.max_results, 100)))}
        filters = []
        if request.year_from is not None:
            filters.append(f"from_publication_date:{request.year_from}-01-01")
        if request.year_to is not None:
            filters.append(f"to_publication_date:{request.year_to}-12-31")
        if filters:
            params["filter"] = ",".join(filters)
        if request.mailto:
            params["mailto"] = request.mailto
        payload = self._get(f"{self.base_url}?{urlencode(params)}")
        results = payload.get("results", [])
        return [self._normalize(work) for work in results if isinstance(work, dict)]
