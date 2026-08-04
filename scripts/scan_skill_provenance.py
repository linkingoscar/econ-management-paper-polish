#!/usr/bin/env python3
"""Validate provenance manifests for optional writing adapters and components."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_contract import load_json, validate_provenance_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors: list[str] = []
    components: list[str] = []
    for path in args.manifests:
        try:
            value = load_json(path)
            manifest_errors = validate_provenance_manifest(value)
            errors.extend(f"{path}: {error}" for error in manifest_errors)
            if isinstance(value, dict) and isinstance(value.get("component"), str):
                components.append(value["component"])
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: cannot read JSON ({exc})")
    result = {
        "status": "pass" if not errors else "fail",
        "manifests": len(args.manifests),
        "components": components,
        "errors": errors,
        "verified": not errors,
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"components: {', '.join(components) if components else 'none'}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
