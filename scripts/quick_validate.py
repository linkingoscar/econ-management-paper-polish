#!/usr/bin/env python3
"""Dependency-free mirror of the Codex Skill Creator quick package checks.

The upstream quick_validate.py is also run locally with ``py -X utf8`` when the
Codex system skill is installed. This copy keeps the same frontmatter/name/
description gates available in repository CI without depending on PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_skill_package import frontmatter


def validate(root: Path) -> list[str]:
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL.md not found"]
    text = skill.read_text(encoding="utf-8")
    values, errors = frontmatter(text)
    name = values.get("name", "").strip()
    if name and not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append("name must be hyphen-case")
    if name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append("name cannot start/end with hyphen or contain consecutive hyphens")
    if len(name) > 64:
        errors.append("name is longer than 64 characters")
    description = values.get("description", "").strip()
    if "<" in description or ">" in description:
        errors.append("description cannot contain angle brackets")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        errors = validate(args.root.resolve())
    except (OSError, UnicodeError) as exc:
        errors = [f"cannot read skill: {exc}"]
    result = {"status": "pass" if not errors else "fail", "root": str(args.root.resolve()), "errors": errors, "upstream_reference": "Codex skill-creator quick_validate.py"}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Skill is valid!" if result["status"] == "pass" else "Skill is invalid!")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
