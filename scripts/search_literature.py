#!/usr/bin/env python3
"""Search Crossref/OpenAlex and emit normalized metadata candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.protocols import SearchRequest
from adapters.providers import CrossrefProvider, OpenAlexProvider
from adapters.search import MultiProviderSearch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--provider", choices=("crossref", "openalex", "both"), default="both")
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--year-from", type=int)
    parser.add_argument("--year-to", type=int)
    parser.add_argument("--mailto", help="Polite-pool contact passed to providers")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    providers = []
    if args.provider in {"crossref", "both"}:
        providers.append(CrossrefProvider(timeout=args.timeout))
    if args.provider in {"openalex", "both"}:
        providers.append(OpenAlexProvider(timeout=args.timeout))
    searcher = MultiProviderSearch(providers)
    request = SearchRequest(args.query, max(1, min(args.max_results, 100)), args.year_from, args.year_to, args.mailto)
    records, errors = searcher.search(request)
    result = {
        "status": "pass" if records or not errors else "fail",
        "capability": "Verified" if records else "Documented" if errors else "Verified",
        "query": args.query,
        "providers": [provider.name for provider in providers],
        "records": [record.to_dict() for record in records],
        "errors": errors,
        "note": "Metadata candidates require evidence-ledger verification before citation.",
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']} ({len(records)} records)")
        for record in records:
            doi = f" doi:{record.doi}" if record.doi else ""
            print(f"- {record.title} ({record.year or 'n.d.'}) [{record.provider}]{doi}")
        for error in errors:
            print(f"warning: {error}", file=sys.stderr)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
