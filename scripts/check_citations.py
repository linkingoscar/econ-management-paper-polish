#!/usr/bin/env python3
"""Check citation keys, bibliography keys, DOI/URL shapes, and placeholders."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
PANDOC_RE = re.compile(r"\[@([^\]]+)\]")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>\]]+", re.IGNORECASE)


def citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(text):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    for match in PANDOC_RE.finditer(text):
        for key in re.split(r"\s*;\s*", match.group(1)):
            key = re.sub(r"^@", "", key.strip())
            if key:
                keys.add(key)
    return keys


def result_for(text: str, bib_text: str | None, strict: bool) -> dict:
    cited = citation_keys(text)
    bib = set(BIB_KEY_RE.findall(bib_text or ""))
    missing = sorted(cited - bib) if bib_text is not None else []
    unused = sorted(bib - cited) if bib_text is not None else []
    urls = URL_RE.findall(text)
    dois = DOI_RE.findall(text)
    placeholders = sorted(set(re.findall(r"\[(?:citation needed|需补充[^\]]*)\]", text, re.I)))
    malformed_doi = [token for token in re.findall(r"\b10\.\d{1,3}/\S+", text) if not DOI_RE.fullmatch(token.rstrip(".,;"))]
    failed = bool(missing or placeholders or (strict and malformed_doi))
    if bib_text is None and cited:
        note = "No bibliography file supplied; citation keys were collected but not matched."
    else:
        note = None
    output = {
        "status": "fail" if failed else "pass",
        "cited_keys": sorted(cited),
        "bibliography_keys": sorted(bib),
        "missing_bibliography_keys": missing,
        "unused_bibliography_keys": unused,
        "doi_count": len(dois),
        "url_count": len(urls),
        "malformed_doi_candidates": malformed_doi,
        "citation_placeholders": placeholders,
    }
    if note:
        output["note"] = note
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", type=Path)
    parser.add_argument("--bib", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        text = args.text.read_text(encoding="utf-8")
        bib_text = args.bib.read_text(encoding="utf-8") if args.bib else None
    except OSError as exc:
        print(f"error: cannot read input: {exc}", file=sys.stderr)
        return 2
    result = result_for(text, bib_text, args.strict)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"cited keys: {len(result['cited_keys'])}")
        print(f"missing bibliography keys: {result['missing_bibliography_keys'] or 'none'}")
        print(f"citation placeholders: {result['citation_placeholders'] or 'none'}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
