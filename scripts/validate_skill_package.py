#!/usr/bin/env python3
"""Run the repository-owned subset of the Codex Skill package contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---", 4)
    if end < 0:
        return {}, ["SKILL.md frontmatter is not closed"]
    values: dict[str, str] = {}
    current = None
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            current = match.group(1)
            raw_value = match.group(2).strip().strip('"\'')
            values[current] = "" if raw_value in {">", "|", ">-", "|-", ">+", "|+"} else raw_value
        elif current and line.startswith(("  ", "\t")):
            values[current] += " " + line.strip()
    if set(values) != {"name", "description"}:
        errors.append(f"frontmatter keys must be name and description (found {sorted(values)})")
    if not values.get("name") or not values.get("description"):
        errors.append("frontmatter name and description must be non-empty")
    if len(values.get("description", "")) > 1024:
        errors.append(f"description is {len(values['description'])} characters; maximum is 1024")
    return values, errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL.md is missing"]
    values, fm_errors = frontmatter(skill.read_text(encoding="utf-8"))
    errors.extend(fm_errors)
    body_lines = len(skill.read_text(encoding="utf-8").splitlines())
    if body_lines > 500:
        errors.append(f"SKILL.md has {body_lines} lines; maximum is 500")
    metadata = root / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append("agents/openai.yaml is missing")
    else:
        metadata_text = metadata.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in metadata_text:
                errors.append(f"agents/openai.yaml is missing {key}")
    for directory in ("assets", "references/v3", "scripts", "evals"):
        if not (root / directory).is_dir():
            errors.append(f"required package directory is missing: {directory}")
    if values.get("name") != "econ-management-paper-polish":
        errors.append("frontmatter name does not match the package name")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        errors = validate(root)
    except (OSError, UnicodeError) as exc:
        errors = [f"cannot validate skill package: {exc}"]
    result = {"status": "pass" if not errors else "fail", "root": str(root), "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
