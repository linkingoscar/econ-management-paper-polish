"""Crossref REST metadata adapter.

Crossref metadata is a candidate source record. It is not full-text evidence and
must pass the v3 evidence-ledger verification step before citation.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from ..protocols import SearchRequest, SourceRecord


class ProviderError(RuntimeError):
    """An external provider could not be queried or normalized."""


def _year(message: dict) -> int | None:
    for field in ("published", "published-print", "published-online", "issued", "created"):
        parts = message.get(field, {}).get("date-parts", [])
        if parts and parts[0] and isinstance(parts[0][0], int):
            return parts[0][0]
    return None


def _authors(message: dict) -> list[str]:
    values = []
    for author in message.get("author", []) or []:
        if not isinstance(author, dict):
            continue
        name = " ".join(part for part in (author.get("given"), author.get("family")) if part)
        if not name:
            name = author.get("name") or author.get("literal") or ""
        if name:
            values.append(name)
    return values


def _clean_abstract(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


class CrossrefProvider:
    name = "crossref"
    base_url = "https://api.crossref.org/works"

    def __init__(self, timeout: float = 20.0, user_agent: str = "econ-management-paper-polish/3.0") -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    def _get(self, url: str, mailto: str | None = None) -> dict:
        agent = self.user_agent + (f" (mailto:{mailto})" if mailto else "")
        request = Request(url, headers={"Accept": "application/json", "User-Agent": agent})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ProviderError(f"Crossref request failed: {exc}") from exc

    def _normalize(self, message: dict) -> SourceRecord:
        doi = message.get("DOI")
        doi = doi.strip() if isinstance(doi, str) else None
        url = message.get("URL") or (f"https://doi.org/{doi}" if doi else None)
        title = (message.get("title") or ["Untitled"])[0]
        return SourceRecord(
            title=str(title).strip(),
            authors=_authors(message),
            year=_year(message),
            venue=(message.get("container-title") or [None])[0],
            doi=doi,
            url=url,
            abstract=_clean_abstract(message.get("abstract")),
            provider=self.name,
            provider_id=str(message.get("DOI") or message.get("URL") or ""),
            retrieved_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            access_tier="metadata",
            raw=message,
        )

    def search(self, request: SearchRequest) -> list[SourceRecord]:
        params = {"query.bibliographic": request.query, "rows": str(max(1, min(request.max_results, 100)))}
        if request.year_from is not None or request.year_to is not None:
            start = request.year_from or 1
            end = request.year_to or 9999
            params["filter"] = f"from-pub-date:{start}-01-01,until-pub-date:{end}-12-31"
        url = f"{self.base_url}?{urlencode(params)}"
        payload = self._get(url, request.mailto)
        items = payload.get("message", {}).get("items", [])
        return [self._normalize(item) for item in items if isinstance(item, dict)]

    def get_by_doi(self, doi: str, mailto: str | None = None) -> SourceRecord:
        normalized = doi.removeprefix("https://doi.org/").strip()
        payload = self._get(f"{self.base_url}/{quote(normalized, safe='')}", mailto)
        message = payload.get("message")
        if not isinstance(message, dict):
            raise ProviderError("Crossref DOI response did not contain a message object")
        return self._normalize(message)
