#!/usr/bin/env python3
"""Validate or scaffold a writing-focused paper spine and claim map."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from writing_contract import load_json, utc_now, validate_paper_spine, write_json


def scaffold(paper_id: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "paper_id": paper_id,
        "research_question": None,
        "main_claim": None,
        "contribution_chain": [],
        "open_questions": [],
        "created_at": utc_now(),
        "source_policy": "author-supplied-or-extracted; no claims invented",
    }


def normalize(value: Any, paper_id: str | None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("paper spine input must be an object")
    output = dict(value)
    output["schema_version"] = "1.0"
    if paper_id:
        output["paper_id"] = paper_id
    output.setdefault("paper_id", "paper-unknown")
    output.setdefault("research_question", None)
    output.setdefault("main_claim", None)
    output.setdefault("open_questions", [])
    chain = output.setdefault("contribution_chain", [])
    if not isinstance(chain, list):
        raise ValueError("contribution_chain must be an array")
    normalized_chain = []
    for index, claim in enumerate(chain, start=1):
        if not isinstance(claim, dict):
            raise ValueError(f"contribution_chain[{index - 1}] must be an object")
        item = dict(claim)
        item.setdefault("claim_id", f"ARG-{index:03d}")
        item.setdefault("evidence", [])
        item.setdefault("method_dependency", [])
        item.setdefault("risk", "unknown")
        normalized_chain.append(item)
    output["contribution_chain"] = normalized_chain
    return output


def extract_candidate(manuscript: Path, paper_id: str) -> dict[str, Any]:
    """Extract a reviewable candidate map; it never promotes text to author claims."""
    text = manuscript.read_text(encoding="utf-8")
    lines = text.splitlines()
    section = "unsectioned"
    chain: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line) or re.match(r"^\\(?:section|subsection|subsubsection)\{(.+?)\}", line)
        if heading:
            section = heading.group(1).strip()
            continue
        if not line.strip() or line.lstrip().startswith(("#", "%")):
            continue
        content = re.sub(r"\s+", " ", line.strip())
        if len(content) < 24:
            continue
        sentence = re.split(r"(?<=[.!?。！？])\s+", content)[0].strip()
        if len(sentence) < 20:
            sentence = content[:240]
        lowered = content.lower()
        if not any(token in lowered for token in ("we ", "we find", "we show", "we argue", "estimate", "result", "effect", "本文", "研究", "发现", "表明", "结果")):
            continue
        chain.append({
            "claim_id": f"ARG-CAND-{len(chain) + 1:03d}",
            "claim": sentence[:500],
            "section": section,
            "evidence": [],
            "method_dependency": [],
            "risk": "unknown",
            "status": "candidate",
            "confirmation_required": True,
            "source_locator": {"line_start": line_number, "line_end": line_number},
        })
    return {
        "schema_version": "1.0",
        "paper_id": paper_id,
        "research_question": None,
        "main_claim": None,
        "contribution_chain": chain,
        "open_questions": ["Confirm every extracted candidate claim against the author's intended contribution and evidence.", "Bind confirmed claims to evidence and method dependencies before revision."],
        "created_at": utc_now(),
        "candidate_status": "needs-human-confirmation",
        "source_path": str(manuscript),
        "source_policy": "candidate extraction only; no claims invented or confirmed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?", help="Existing paper-spine JSON; omit to create a scaffold")
    parser.add_argument("--manuscript", type=Path, help="Extract a candidate claim map from author text; output remains unconfirmed")
    parser.add_argument("--paper-id", default=None)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        if args.input and args.manuscript:
            raise ValueError("provide either an existing paper-spine JSON or --manuscript, not both")
        if args.manuscript:
            value = extract_candidate(args.manuscript, args.paper_id or args.manuscript.stem)
        elif args.input:
            value = normalize(load_json(args.input), args.paper_id)
        else:
            value = scaffold(args.paper_id or "paper-unknown")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        value = None
        errors.append(f"cannot build paper spine: {exc}")
    if value is not None:
        errors.extend(validate_paper_spine(value))
    output = None
    if value is not None and not errors and args.output:
        try:
            write_json(args.output, value)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write paper spine: {exc}")
    result = {"status": "pass" if value is not None and not errors else "fail", "errors": errors, "output": output, "paper_spine": value}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        if value:
            print(f"paper_id: {value['paper_id']}")
            print(f"claims: {len(value['contribution_chain'])}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
