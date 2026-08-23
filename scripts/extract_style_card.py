#!/usr/bin/env python3
"""Extract a conservative, deterministic writing style card from text.

This is a structural heuristic, not a journal-quality judgment. PDF and other
binary sources are reported as metadata-only so the caller cannot mistake a
filename for full-text evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from statistics import mean, median

from writing_contract import validate_style_card, write_json


TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".tex", ".latex", ".html", ".xml"}
SENTENCE_RE = re.compile(r"(?<=[。！？])\s*|(?<=[.!?])\s+")
CITATION_RE = re.compile(r"(?:\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{[^}]+\}|\[[^\]]{2,80}\])")
HEADING_RE = re.compile(r"^\s*(?:#{1,6}\s+|\\(?:sub)*section\{)(.+?)(?:\})?\s*$", re.IGNORECASE)

MOVE_PATTERNS = {
    "establish-problem": re.compile(r"\b(problem|challenge|important|motivat|why it matters)\b|问题|挑战|重要|背景", re.IGNORECASE),
    "identify-gap": re.compile(r"\b(gap|little is known|however|remains unclear|understudied)\b|缺乏|不足|然而|尚不清楚|空白", re.IGNORECASE),
    "state-contribution": re.compile(r"\b(contribut|we show|this paper)\b|本文|贡献|发现", re.IGNORECASE),
    "describe-method": re.compile(r"\b(data|sample|identif|estimate|regression|experiment|survey)\b|数据|样本|识别|估计|回归|实验|调查", re.IGNORECASE),
    "interpret-result": re.compile(r"\b(result|finding|effect|magnitude|suggest)\b|结果|影响|效应|幅度|表明", re.IGNORECASE),
    "limit-scope": re.compile(r"\b(limit|caveat|external validity|future research)\b|局限|外部有效性|未来研究", re.IGNORECASE),
}


def sentence_count(paragraph: str) -> int:
    cleaned = re.sub(r"\s+", " ", paragraph.strip())
    if not cleaned:
        return 0
    parts = [part for part in SENTENCE_RE.split(cleaned) if part.strip()]
    return max(1, len(parts))


def split_paragraphs(lines: list[str]) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    start = None
    buffer: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if line.strip():
            if start is None:
                start = line_number
            buffer.append(line.strip())
        elif buffer:
            paragraphs.append((start or line_number, " ".join(buffer)))
            start = None
            buffer = []
    if buffer:
        paragraphs.append((start or len(lines), " ".join(buffer)))
    return paragraphs


def extract(source: Path, source_id: str, section: str) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    if source.suffix.lower() not in TEXT_SUFFIXES:
        return None, ["source is not a supported text format; use metadata-only manifest status"]
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, [f"cannot read source: {exc}"]
    lines = text.splitlines()
    paragraphs = split_paragraphs(lines)
    sentence_counts = [sentence_count(value) for _, value in paragraphs]
    citation_counts = [len(CITATION_RE.findall(value)) for _, value in paragraphs]
    headings = []
    for number, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append({"line": number, "text": match.group(1).strip()})
    moves: dict[str, dict] = {}
    move_locators: list[dict] = []
    for move, pattern in MOVE_PATTERNS.items():
        hits = []
        for line_number, paragraph in paragraphs:
            if pattern.search(paragraph):
                hits.append({"line": line_number, "excerpt": paragraph[:140]})
        if hits:
            moves[move] = {"paragraphs": len(hits), "share": round(len(hits) / max(1, len(paragraphs)), 3)}
            move_locators.extend({"line": item["line"], "move": move} for item in hits[:3])
    confidence = "high" if len(paragraphs) >= 20 else "medium" if len(paragraphs) >= 5 else "low"
    card = {
        "schema_version": "1.0",
        "style_card_id": f"STY-{source_id.removeprefix('SRC-')}-{section.lower().replace(' ', '-')}",
        "source_id": source_id,
        "section": section,
        "observations": {
            "extractor_type": "deterministic-structural-heuristic",
            "headings": headings[:100],
            "rhetorical_moves": moves,
            "paragraph_length": {
                "count": len(sentence_counts),
                "mean_sentences": round(mean(sentence_counts), 2) if sentence_counts else 0,
                "median_sentences": median(sentence_counts) if sentence_counts else 0,
                "min_sentences": min(sentence_counts) if sentence_counts else 0,
                "max_sentences": max(sentence_counts) if sentence_counts else 0,
            },
            "citation_behavior": {
                "paragraphs_with_citations": sum(1 for count in citation_counts if count),
                "citation_density": round(sum(citation_counts) / max(1, len(paragraphs)), 3),
            },
        },
        "locators": move_locators[:100],
        "confidence": confidence,
        "copy_boundary": "structural-only",
        "extractor": "scripts/extract_style_card.py",
    }
    return card, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--source-id", required=True, help="SRC-* identifier from corpus manifest")
    parser.add_argument("--section", default="whole-document")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    card, errors = extract(args.source, args.source_id, args.section)
    if card is not None:
        errors.extend(validate_style_card(card))
    output = None
    if card is not None and not errors and args.output:
        try:
            write_json(args.output, card)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write style card: {exc}")
    result = {"status": "pass" if card is not None and not errors else "fail", "errors": errors, "output": output, "style_card": card}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
        if card is not None:
            print(f"style_card_id: {card['style_card_id']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
