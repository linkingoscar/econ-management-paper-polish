#!/usr/bin/env python3
"""Validate adapter provenance manifests and the dependency-free reproducibility lock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_contract import validate_provenance_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    lock_path = root / "adapters" / "repro-lock.json"
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        lock = {}
        errors.append(f"cannot read adapters/repro-lock.json: {exc}")
    if lock.get("schema_version") != "1.0":
        errors.append("repro lock schema_version must be '1.0'")
    if not isinstance(lock.get("dependencies"), list):
        errors.append("repro lock dependencies must be an array")
    if not isinstance(lock.get("commands"), list) or not lock["commands"]:
        errors.append("repro lock commands must be non-empty")
    components = lock.get("components", [])
    if not isinstance(components, list) or not components:
        errors.append("repro lock components must be non-empty")
    else:
        for relative in components:
            path = root / "adapters" / relative
            if not path.is_file():
                errors.append(f"missing locked component manifest: adapters/{relative}")
                continue
            try:
                errors.extend(f"adapters/{relative}: {error}" for error in validate_provenance_manifest(json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"adapters/{relative}: invalid JSON ({exc})")
    result = {"status": "pass" if not errors else "fail", "lock": str(lock_path), "components": len(components) if isinstance(components, list) else 0, "errors": errors, "policy": "Verified only means local smoke-tested; external/network components remain Documented until tested in that environment."}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
