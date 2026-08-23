#!/usr/bin/env python3
"""Generate deterministic scholarly-writing mutations and verify independent oracles.

The generator never asks the detector under test to create its own examples. Each
operator must make exactly one bounded mutation and the configured safety oracle
must reject it before the case is admitted to the generated suite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

from audit_latex import audit as audit_latex
from check_local_bindings import audit_local_bindings
from meaning_audit import compare_text
from writing_contract import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
CITATION_RE = re.compile(r"\[@([A-Za-z0-9_:./-]+)\]")
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?)(?:%)?(?![A-Za-z])")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def swap_first_two(pattern: re.Pattern[str], text: str) -> str | None:
    matches = list(pattern.finditer(text))
    for first_index, first in enumerate(matches):
        for second in matches[first_index + 1 :]:
            if first.group(0) == second.group(0):
                continue
            return (
                text[: first.start()]
                + second.group(0)
                + text[first.end() : second.start()]
                + first.group(0)
                + text[second.end() :]
            )
    return None


def replace_once(text: str, old: str, new: str) -> str | None:
    if old not in text:
        return None
    return text.replace(old, new, 1)


def mutate_number_swap(text: str) -> str | None:
    return swap_first_two(NUMBER_RE, text)


def mutate_citation_swap(text: str) -> str | None:
    return swap_first_two(CITATION_RE, text)


def mutate_direction_flip(text: str) -> str | None:
    for old, new in (("positive", "negative"), ("正向", "负向"), ("increased", "decreased")):
        result = replace_once(text, old, new)
        if result is not None:
            return result
    return None


def mutate_significance_flip(text: str) -> str | None:
    for old, new in (("statistically significant", "not statistically significant"), ("显著", "不显著")):
        result = replace_once(text, old, new)
        if result is not None:
            return result
    return None


def mutate_causal_upgrade(text: str) -> str | None:
    for old, new in (("is associated with", "causes"), ("was associated with", "caused"), ("与", "导致")):
        result = replace_once(text, old, new)
        if result is not None:
            return result
    return None


def mutate_latex_ref_break(text: str) -> str | None:
    match = re.search(r"\\(?:eq)?ref\{([^}]+)\}", text)
    if not match:
        return None
    return text[: match.start(1)] + match.group(1) + "-missing" + text[match.end(1) :]


def mutate_latex_package_remove(text: str) -> str | None:
    match = re.search(r"^\\usepackage(?:\[[^]]*\])?\{(?:amsmath|booktabs|graphicx|threeparttable)\}\s*\r?\n?", text, re.MULTILINE)
    if not match:
        return None
    return text[: match.start()] + text[match.end() :]


def mutate_latex_environment_break(text: str) -> str | None:
    match = re.search(r"\\end\{(equation|align|table|figure)\}", text)
    if not match:
        return None
    return text[: match.start(1)] + "document" + text[match.end(1) :]


OPERATORS: dict[str, tuple[Callable[[str], str | None], str]] = {
    "number-binding-swap": (mutate_number_swap, "local-binding"),
    "citation-claim-swap": (mutate_citation_swap, "local-binding"),
    "direction-flip": (mutate_direction_flip, "meaning"),
    "significance-flip": (mutate_significance_flip, "meaning"),
    "association-to-causal": (mutate_causal_upgrade, "meaning"),
    "latex-reference-break": (mutate_latex_ref_break, "latex"),
    "latex-required-package-remove": (mutate_latex_package_remove, "latex"),
    "latex-environment-break": (mutate_latex_environment_break, "latex"),
}


def resolve_source(raw: str) -> Path:
    path = (ROOT / raw).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"seed path escapes repository root: {raw}") from exc
    return path


def oracle_result(kind: str, original: str, mutated: str, output_path: Path) -> dict[str, Any]:
    if kind == "local-binding":
        result = audit_local_bindings(original, mutated)
        codes = sorted({item["kind"] for item in result["issues"]})
    elif kind == "meaning":
        result = compare_text(original, mutated)
        codes = sorted(result["changed_categories"])
    elif kind == "latex":
        result = audit_latex(output_path)
        codes = sorted({item["code"] for item in result["issues"]})
    else:
        raise ValueError(f"unknown oracle: {kind}")
    return {"status": result["status"], "issue_codes": codes}


def validate_manifest(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema_version") != "1.0":
        return ["manifest must be an object with schema_version 1.0"]
    if not isinstance(value.get("suite_id"), str) or not value["suite_id"].strip():
        errors.append("suite_id must be non-empty")
    seeds = value.get("seeds")
    if not isinstance(seeds, list) or not seeds:
        errors.append("seeds must be a non-empty array")
        return errors
    ids: list[str] = []
    for index, seed in enumerate(seeds):
        if not isinstance(seed, dict):
            errors.append(f"seeds[{index}] must be an object")
            continue
        for key in ("seed_id", "path"):
            if not isinstance(seed.get(key), str) or not seed[key].strip():
                errors.append(f"seeds[{index}].{key} must be non-empty")
        ids.append(seed.get("seed_id", ""))
        operators = seed.get("operators")
        if not isinstance(operators, list) or not operators:
            errors.append(f"seeds[{index}].operators must be non-empty")
        elif len(set(operators)) != len(operators) or any(item not in OPERATORS for item in operators):
            errors.append(f"seeds[{index}].operators contains duplicates or unknown operators")
    if len(set(ids)) != len(ids):
        errors.append("seed_id values must be unique")
    return errors


def generate(manifest: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    cases: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for seed in manifest["seeds"]:
        source_path = resolve_source(seed["path"])
        source = source_path.read_text(encoding="utf-8")
        extension = source_path.suffix or ".txt"
        control_name = f"{seed['seed_id']}--control{extension}"
        control_path = output_dir / control_name
        shutil.copyfile(source_path, control_path)
        cases.append(
            {
                "case_id": f"{seed['seed_id']}--control",
                "seed_id": seed["seed_id"],
                "operator": "safe-control",
                "expected": "pass",
                "path": control_name,
                "source_sha256": sha256_text(source),
                "mutated_sha256": sha256_text(source),
            }
        )
        for operator_name in seed["operators"]:
            operator, oracle = OPERATORS[operator_name]
            mutated = operator(source)
            if mutated is None:
                skipped.append({"seed_id": seed["seed_id"], "operator": operator_name, "reason": "precondition-not-found"})
                continue
            if mutated == source:
                raise ValueError(f"operator {operator_name} reported success without changing {seed['seed_id']}")
            name = f"{seed['seed_id']}--{operator_name}{extension}"
            output_path = output_dir / name
            output_path.write_text(mutated, encoding="utf-8")
            oracle_check = oracle_result(oracle, source, mutated, output_path)
            if oracle_check["status"] != "fail":
                output_path.unlink(missing_ok=True)
                raise ValueError(f"oracle {oracle} did not reject {seed['seed_id']} / {operator_name}")
            cases.append(
                {
                    "case_id": f"{seed['seed_id']}--{operator_name}",
                    "seed_id": seed["seed_id"],
                    "operator": operator_name,
                    "oracle": oracle,
                    "oracle_issue_codes": oracle_check["issue_codes"],
                    "expected": "fail",
                    "path": name,
                    "source_sha256": sha256_text(source),
                    "mutated_sha256": sha256_text(mutated),
                }
            )
    return {
        "schema_version": "1.0",
        "suite_id": manifest["suite_id"],
        "generator": "scripts/generate_adversarial_mutations.py",
        "deterministic": True,
        "case_count": len(cases),
        "mutation_count": sum(item["operator"] != "safe-control" for item in cases),
        "cases": cases,
        "skipped": skipped,
        "limitations": [
            "Synthetic mutations test detector sensitivity, not manuscript truth or journal acceptance.",
            "Each mutation is admitted only when an independent deterministic oracle rejects it.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        if args.output_dir.resolve() == args.manifest_output.resolve():
            raise ValueError("output directory and manifest output must differ")
        result = generate(load_json(args.manifest), args.output_dir)
        write_json(args.manifest_output, result)
        summary = {"status": "pass", "case_count": result["case_count"], "mutation_count": result["mutation_count"], "skipped": result["skipped"]}
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        summary = {"status": "fail", "errors": [str(exc)]}
    print(json.dumps(summary, ensure_ascii=False, indent=2) if args.as_json else f"status: {summary['status']}")
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
