#!/usr/bin/env python3
"""Build a deterministic manifest for journal-adaptation writing corpora.

The scanner records file identity and extraction capability only. It does not
read a PDF as if it were verified full text, and it never generates prose or
copies source sentences.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from writing_contract import utc_now, validate_corpus_manifest, write_json


TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".tex", ".latex", ".bib", ".json", ".yaml",
    ".yml", ".csv", ".tsv", ".html", ".xml",
}
METADATA_SUFFIXES = {".pdf", ".docx", ".pptx", ".xlsx"}
IGNORED_PARTS = {".git", ".rag", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_readable(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return True


def build_manifest(root: Path, corpus_id: str | None, role: str, purpose: str, license_status: str, use: str, exclude: Path | None = None) -> dict:
    files = [
        path for path in root.rglob("*")
        if path.is_file() and not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
        and (exclude is None or path.resolve() != exclude.resolve())
    ]
    files.sort(key=lambda item: item.relative_to(root).as_posix().lower())
    items: list[dict] = []
    rejections: list[dict] = []
    created_at = utc_now()
    for index, path in enumerate(files, start=1):
        relative = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        digest = sha256(path)
        if suffix in TEXT_SUFFIXES:
            readable = text_readable(path)
            extraction = "fulltext" if readable else "unsupported"
        elif suffix in METADATA_SUFFIXES:
            readable = True
            extraction = "metadata-only"
        else:
            readable = False
            extraction = "unsupported"
        item = {
            "source_id": f"SRC-{index:04d}",
            "path": relative,
            "role": role,
            "sha256": digest,
            "accessed_at": created_at,
            "readable": readable,
            "extraction": extraction,
            "pages": None,
            "license_status": license_status,
            "use": use,
        }
        if extraction == "unsupported" or not readable:
            rejections.append({
                "source_id": item["source_id"],
                "path": relative,
                "reason": "unsupported-or-unreadable",
                "action": "excluded-from-style-profile",
            })
        else:
            items.append(item)
    manifest = {
        "schema_version": "1.0",
        "corpus_id": corpus_id or f"corpus-{root.name or 'root'}",
        "created_at": created_at,
        "purpose": purpose,
        "source_policy": {
            "role": role,
            "license_status": license_status,
            "use": use,
            "copy_boundary": "structural-only",
        },
        "items": items,
        "rejections": rejections,
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Directory containing journal/style materials")
    parser.add_argument("--corpus-id", default=None)
    parser.add_argument("--role", default="target-journal", choices=["target-journal", "field-or-topic", "author-or-lab-exemplar", "author-guideline", "other"])
    parser.add_argument("--purpose", default="journal-adaptation", choices=["journal-adaptation", "writing-style", "evidence"])
    parser.add_argument("--license-status", default="unknown")
    parser.add_argument("--use", default="structural-style-only", choices=["structural-style-only", "journal-rule", "user-provided-evidence", "metadata-only"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        result = {"status": "fail", "errors": [f"corpus root is not a directory: {root}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    manifest = build_manifest(root, args.corpus_id, args.role, args.purpose, args.license_status, args.use, args.output)
    errors = validate_corpus_manifest(manifest)
    output = None
    if not errors and args.output:
        try:
            write_json(args.output, manifest)
            output = str(args.output)
        except OSError as exc:
            errors.append(f"cannot write manifest: {exc}")
    result = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "items": len(manifest["items"]),
        "rejections": len(manifest["rejections"]),
        "output": output,
        "manifest": manifest,
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"items: {result['items']}")
        print(f"rejections: {result['rejections']}")
        if output:
            print(f"output: {output}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
