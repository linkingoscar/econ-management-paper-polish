#!/usr/bin/env python3
"""Validate the repository contract for the v3 reliability core."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "README.en.md",
    "agents/openai.yaml",
    "assets/evidence-pack.schema.json",
    "assets/journal-card.schema.json",
    "assets/paper-state.schema.json",
    "assets/corpus-manifest.schema.json",
    "assets/style-card.schema.json",
    "assets/style-profile.schema.json",
    "assets/paper-spine.schema.json",
    "assets/review-issue.schema.json",
    "assets/review-ledger.schema.json",
    "assets/provenance-manifest.schema.json",
    "assets/writing-benchmark.schema.json",
    "references/v3-runtime-contract.md",
    "references/v3-evidence-ledger.md",
    "references/v3-method-safety.md",
    "references/v3-audit-contract.md",
    "references/v3-writing-contract.md",
    "references/v3-corpus-and-style.md",
    "references/v3-argument-evidence.md",
    "references/v3-review-ledger.md",
    "references/v3-capability-and-provenance.md",
    "references/v3/README.md",
    "references/v3/legacy-index.md",
    "adapters/README.md",
    "adapters/protocols.py",
    "adapters/search.py",
    "adapters/providers/crossref.py",
    "adapters/providers/openalex.py",
    "adapters/rag/markdown_index.py",
    "adapters/agents/serial.py",
    "adapters/agents/openai_compatible.py",
    "scripts/check_numeric_consistency.py",
    "scripts/check_citations.py",
    "scripts/audit_latex.py",
    "scripts/compare_manuscript_versions.py",
    "scripts/build_evidence_pack.py",
    "scripts/validate_journal_card.py",
    "scripts/validate_v3.py",
    "scripts/search_literature.py",
    "scripts/rag_search.py",
    "scripts/run_agent_pipeline.py",
    "scripts/writing_contract.py",
    "scripts/prepare_corpus.py",
    "scripts/extract_style_card.py",
    "scripts/build_style_profile.py",
    "scripts/build_paper_spine.py",
    "scripts/build_issue_ledger.py",
    "scripts/route_review_issues.py",
    "scripts/propose_bounded_patch.py",
    "scripts/verify_bounded_patch.py",
    "scripts/check_claim_evidence.py",
    "scripts/validate_writing_contract.py",
    "scripts/run_writing_benchmark.py",
    "scripts/scan_skill_provenance.py",
    "evals/run_smoke_tests.py",
    "evals/run_extended_tests.py",
    "evals/run_v31_writing_tests.py",
    "evals/README.md",
    "evals/evaluation-manifest.json",
    ".github/workflows/ci.yml",
)

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LINK_FILES = ("SKILL.md", "README.md", "README.en.md", "CONTRIBUTING.md", "adapters/README.md", "references/v3/README.md")


def validate_frontmatter(skill_path: Path) -> list[str]:
    errors: list[str] = []
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---", 4)
    if end == -1:
        return ["SKILL.md frontmatter is not closed"]
    keys = []
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:", line)
        if match:
            keys.append(match.group(1))
    if set(keys) != {"name", "description"}:
        errors.append(f"SKILL.md frontmatter keys must be name and description (found {keys})")
    if "name:" not in text[4:end] or "description:" not in text[4:end]:
        errors.append("SKILL.md frontmatter requires name and description")
    return errors


def validate_json(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path.as_posix()}: invalid JSON ({exc})"]
    if not isinstance(value, dict) or value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        return [f"{path.as_posix()}: expected a Draft 2020-12 JSON Schema"]
    return []


def validate_internal_links(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    for relative in LINK_FILES:
        source = root / relative
        if not source.is_file():
            continue
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^(?:https?|mailto):", target, re.IGNORECASE):
                continue
            candidate = (source.parent / unquote(target)).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {raw_target}")
                continue
            if not candidate.exists():
                errors.append(f"{relative}: broken local link: {raw_target}")
    return errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        errors.extend(validate_frontmatter(skill_path))
    for relative in (
        "assets/evidence-pack.schema.json",
        "assets/journal-card.schema.json",
        "assets/paper-state.schema.json",
        "assets/corpus-manifest.schema.json",
        "assets/style-card.schema.json",
        "assets/style-profile.schema.json",
        "assets/paper-spine.schema.json",
        "assets/review-issue.schema.json",
        "assets/review-ledger.schema.json",
        "assets/provenance-manifest.schema.json",
        "assets/writing-benchmark.schema.json",
    ):
        path = root / relative
        if path.is_file():
            errors.extend(validate_json(path))
    packs = sorted((root / "references" / "v3").glob("[0-9][0-9]-*.md"))
    if len(packs) != 14:
        errors.append(f"references/v3 must contain exactly 14 responsibility packs (found {len(packs)})")
    legacy_index = root / "references" / "v3" / "legacy-index.md"
    if legacy_index.is_file():
        legacy_rows = [line for line in legacy_index.read_text(encoding="utf-8").splitlines() if line.startswith("| `")]
        if len(legacy_rows) != 41:
            errors.append(f"legacy migration index must contain 41 rows (found {len(legacy_rows)})")
        for line in legacy_rows:
            fields = re.findall(r"`([^`]+)`", line)
            source = fields[0] if fields else ""
            destinations = fields[1:]
            if source and not (root / "references" / source).is_file():
                errors.append(f"legacy migration source missing: references/{source}")
            if not destinations:
                errors.append(f"legacy migration row has no v3 destination: {line}")
            for destination in destinations:
                if not (root / "references" / "v3" / destination).is_file():
                    errors.append(f"legacy migration destination missing: references/v3/{destination}")
    manifest = root / "evals" / "evaluation-manifest.json"
    if manifest.is_file():
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            if payload.get("schema_version") != "1.0" or payload.get("suite") != "v3-extended-local":
                errors.append("evals/evaluation-manifest.json has an unexpected contract")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"evals/evaluation-manifest.json: invalid JSON ({exc})")
    errors.extend(validate_internal_links(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate_root(root)
    result = {"status": "pass" if not errors else "fail", "root": str(root), "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"root: {root}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
