#!/usr/bin/env python3
"""Bundle an original/revised pair for provisional AI writing-effect review."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from ai_review_contract import sha256_path
from writing_contract import load_json, utc_now, validate_writing_review_bundle, write_json


def document(path: Path, max_chars: int) -> dict:
    content = path.read_text(encoding="utf-8")
    return {"path": str(path), "sha256": sha256_path(path), "content": content[:max_chars], "truncated": len(content) > max_chars}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--style-profile", type=Path)
    parser.add_argument("--paper-spine", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-chars", type=int, default=40000)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    value = None
    try:
        context = {}
        for key, path in (("style_profile", args.style_profile), ("paper_spine", args.paper_spine)):
            if path:
                context[key] = {"path": str(path), "sha256": sha256_path(path), "value": load_json(path)}
        value = {
            "schema_version": "1.0", "bundle_id": f"WRB-{uuid.uuid4().hex[:12]}",
            "original": document(args.original, max(1000, args.max_chars)), "revised": document(args.revised, max(1000, args.max_chars)),
            "context": context, "review_scope": ["claim-clarity", "argument-flow", "evidence-alignment", "method-language", "author-voice"],
            "created_at": utc_now(),
            "limitations": ["This bundle supports provisional AI comparison only.", "Factual truth, causal identification, and author intent remain outside automatic approval."],
        }
        errors.extend(validate_writing_review_bundle(value))
        if not errors:
            write_json(args.output, value)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"cannot build writing review bundle: {exc}")
    result = {"status": "pass" if value is not None and not errors else "fail", "output": str(args.output) if value else None, "bundle": value, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else f"status: {result['status']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
