#!/usr/bin/env python3
"""Ingest local notes and run reproducible lexical retrieval."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.rag import MarkdownIndex


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--ingest", type=Path, nargs="*", default=[])
    parser.add_argument("--query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        index = MarkdownIndex([]) if args.reset or not args.index.exists() else MarkdownIndex.load(args.index)
        ingested = index.ingest(args.ingest) if args.ingest else 0
        if args.ingest:
            index.save(args.index)
        hits = index.search(args.query, args.top_k) if args.query else []
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"status": "fail", "capability": "Verified", "errors": [str(exc)]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"error: {exc}", file=sys.stderr)
        return 2
    result = {"status": "pass", "capability": "Verified", "index": str(args.index), "ingested_chunks": ingested, "indexed_chunks": len(index.chunks), "hits": [hit.to_dict() for hit in hits], "note": "Lexical retrieval is a candidate finder; verify claim support before citation."}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: pass ({len(index.chunks)} chunks; {len(hits)} hits)")
        for hit in hits:
            print(f"- {hit.score:.3f} {hit.path}: {hit.text[:180]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
