#!/usr/bin/env python3
"""Detect long verbatim overlaps between a style corpus and a candidate draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".tex", ".latex", ".html", ".xml"}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def word_ngrams(text: str, size: int) -> set[str]:
    tokens = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", normalize(text))
    return {" ".join(tokens[index:index + size]) for index in range(max(0, len(tokens) - size + 1))}


def char_ngrams(text: str, size: int) -> set[str]:
    clean = re.sub(r"\s+", "", normalize(text))
    return {clean[index:index + size] for index in range(max(0, len(clean) - size + 1))}


def sources(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and ".git" not in path.parts:
            yield path


def audit(corpus: Path, candidate: Path, min_words: int, min_chars: int) -> dict:
    candidate_text = candidate.read_text(encoding="utf-8")
    candidate_words = word_ngrams(candidate_text, min_words)
    candidate_chars = char_ngrams(candidate_text, min_chars)
    overlaps: list[dict] = []
    for source in sources(corpus):
        try:
            source_text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        word_hits = sorted(candidate_words & word_ngrams(source_text, min_words))
        char_hits = sorted(candidate_chars & char_ngrams(source_text, min_chars))
        if word_hits or char_hits:
            overlaps.append({"source": str(source), "word_overlap_count": len(word_hits), "char_overlap_count": len(char_hits), "word_examples": word_hits[:5], "char_examples": char_hits[:3]})
    return {
        "schema_version": "1.0",
        "status": "fail" if overlaps else "pass",
        "candidate": str(candidate),
        "corpus": str(corpus),
        "overlaps": overlaps,
        "policy": {"min_words": min_words, "min_chars": min_chars, "action": "author-required" if overlaps else "safe-fix"},
        "scope": "verbatim-overlap screen; it is not a plagiarism or authorship determination",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--min-words", type=int, default=8)
    parser.add_argument("--min-chars", type=int, default=24)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = audit(args.corpus, args.candidate, args.min_words, args.min_chars)
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "errors": [str(exc)]}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for item in result.get("overlaps", []):
            print(f"- overlap: {item['source']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
