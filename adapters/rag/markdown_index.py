"""Small dependency-free lexical RAG index for local manuscript/literature notes."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

from ..protocols import RagHit


TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


class MarkdownIndex:
    schema_version = "1.0"

    def __init__(self, chunks: list[dict[str, Any]] | None = None) -> None:
        self.chunks = chunks or []

    @classmethod
    def load(cls, path: Path) -> "MarkdownIndex":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if payload.get("schema_version") != cls.schema_version or not isinstance(payload.get("chunks"), list):
            raise ValueError("unsupported RAG index schema")
        return cls(payload["chunks"])

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"schema_version": self.schema_version, "chunks": self.chunks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def ingest(self, paths: Iterable[Path], max_chars: int = 2_000_000, words_per_chunk: int = 180) -> int:
        added = 0
        for root in paths:
            candidates = [root] if root.is_file() else sorted(root.rglob("*")) if root.is_dir() else []
            for path in candidates:
                if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json"}:
                    continue
                if path.stat().st_size > max_chars:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
                if not paragraphs:
                    continue
                for index, paragraph in enumerate(paragraphs):
                    words = paragraph.split()
                    pieces = [" ".join(words[start : start + words_per_chunk]) for start in range(0, len(words), words_per_chunk)] or [paragraph]
                    for piece_index, piece in enumerate(pieces):
                        chunk_id = hashlib.sha256(f"{path.resolve()}:{index}:{piece_index}".encode("utf-8")).hexdigest()[:16]
                        self.chunks = [chunk for chunk in self.chunks if chunk.get("chunk_id") != chunk_id]
                        self.chunks.append({"chunk_id": chunk_id, "path": str(path), "title": path.stem, "text": piece, "metadata": {"suffix": path.suffix.lower()}})
                        added += 1
        return added

    def search(self, query: str, top_k: int = 5) -> list[RagHit]:
        query_terms = _tokens(query)
        if not query_terms:
            return []
        document_frequency: dict[str, int] = {}
        for chunk in self.chunks:
            for term in set(_tokens(str(chunk.get("text", "")))):
                document_frequency[term] = document_frequency.get(term, 0) + 1
        total = max(len(self.chunks), 1)
        hits: list[RagHit] = []
        for chunk in self.chunks:
            terms = _tokens(str(chunk.get("text", "")))
            if not terms:
                continue
            score = 0.0
            matched: list[str] = []
            for term in query_terms:
                count = terms.count(term)
                if count:
                    matched.append(term)
                    score += (1.0 + math.log(count)) * math.log((total + 1) / (document_frequency.get(term, 0) + 1))
            if score:
                metadata = dict(chunk.get("metadata") or {})
                metadata["matched_terms"] = sorted(set(matched))
                hits.append(RagHit(str(chunk["chunk_id"]), str(chunk["path"]), str(chunk["text"]), score, chunk.get("title"), metadata))
        hits.sort(key=lambda hit: (-hit.score, hit.path, hit.chunk_id))
        return hits[: max(1, top_k)]
