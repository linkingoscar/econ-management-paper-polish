#!/usr/bin/env python3
"""Regression tests for protected fields, benchmark failures, and route contracts."""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_writing_benchmark as benchmark
from build_agentic_review_packet import hard_audit
from build_protected_snapshot import snapshot
from check_numeric_consistency import extract_numeric_tokens
from check_method_language import check as check_method_language
from protected_fields import economic_numeric_inventory
from writing_contract import validate_route_card


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="econ-reliability-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def text(self, name, value):
        path = self.directory / name
        path.write_text(value, encoding="utf-8")
        return path

    def run_script(self, name, *args):
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *map(str, args), "--json"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"}, check=False,
        )
        return process.returncode, json.loads(process.stdout)

    def test_harmful_edits_fail_proposal_verifier_and_apply(self):
        cases = [
            ("unicode-sign", "The coefficient is −0.15.", "The coefficient is 0.15."),
            ("unit-scale", "Revenue is 5 million dollars.", "Revenue is 5 billion dollars."),
            ("chinese-scale", "收入为5亿元。", "收入为5万元。"),
            ("author", "Smith (2020) reports this estimate.", "Jones (2020) reports this estimate."),
            ("parenthetical-author", "Prior evidence (Smith, 2020) supports this.", "Prior evidence (Jones, 2020) supports this."),
            ("negation", "We do not establish a causal effect.", "We do establish a causal effect."),
            ("equation", r"The model is $Y = \alpha + \beta X$.", r"The model is $Y = \alpha - \beta X$."),
            ("pvalue", "The estimate has p<0.05.", "The estimate has p>0.05."),
        ]
        for name, old, new in cases:
            with self.subTest(name=name):
                original = self.text("original.md", old)
                revised = self.text("revised.md", new)
                for script in ("propose_bounded_patch.py", "verify_bounded_patch.py"):
                    code, result = self.run_script(script, original, revised)
                    self.assertNotEqual(code, 0, script)
                    self.assertEqual(result["status"], "fail", script)
                output = self.directory / (name + "-applied.md")
                code, result = self.run_script("apply_bounded_patch.py", original, revised, "--output", output)
                self.assertNotEqual(code, 0)
                self.assertFalse(result["applied"])
                self.assertFalse(output.exists())
                self.assertEqual(original.read_text(encoding="utf-8"), old)
                self.assertEqual(hard_audit(old, new, [])["status"], "fail")

    def test_safe_copyediting_and_sign_normalization_pass(self):
        pairs = [
            ("The coefficient is −0.15.", "The coefficient equals -0.15."),
            ("Revenue is 5 million dollars.", "Revenue equals 5 million dollars."),
            ("Smith (2020) reports this estimate.", "Smith (2020) presents this estimate."),
            (r"The model is $Y = \alpha + \beta X$.", r"We use the model $Y = \alpha + \beta X$."),
        ]
        for old, new in pairs:
            with self.subTest(old=old):
                original = self.text("original.md", old)
                revised = self.text("revised.md", new)
                code, result = self.run_script("verify_bounded_patch.py", original, revised)
                self.assertEqual(code, 0, result)
                self.assertEqual(result["status"], "pass")
                self.assertIn("semantic", result["verification_scope"])

    def test_snapshots_and_numeric_audits_share_sign_and_field_extraction(self):
        text = r"The estimate is −0.15. Revenue is 5 million dollars. Smith (2020) uses $Y = X + Z$."
        state = snapshot(self.text("source.md", text), ["X"], [])
        self.assertEqual(state["protected"]["numbers"], dict(extract_numeric_tokens(text)))
        self.assertIn("-0.15", state["protected"]["numbers"])
        self.assertIn("5 million dollars", state["protected"]["quantities"])
        self.assertIn("author-year:Smith (2020)", state["protected"]["citations"])
        self.assertEqual(len(state["protected"]["equations"]), 1)

    def test_allow_added_does_not_authorize_replacing_units(self):
        original = self.text("original.md", "Revenue is 5 million dollars.")
        revised = self.text("revised.md", "Revenue is 5 billion dollars.")
        code, result = self.run_script("verify_bounded_patch.py", original, revised, "--allow-added")
        self.assertNotEqual(code, 0)
        self.assertEqual(result["protection"]["status"], "fail")

    def test_workflow_rejects_unit_change(self):
        workspace = self.directory / "workspace"
        self.assertEqual(self.run_script("init_writing_workspace.py", workspace)[0], 0)
        self.assertEqual(self.run_script(
            "build_route_card.py", "--task-mode", "polish", "--discipline", "economics",
            "--language", "en-US", "--output", workspace / "route-card.json",
        )[0], 0)
        (workspace / "manuscript/original.md").write_text("Revenue is 5 million dollars.", encoding="utf-8")
        (workspace / "manuscript/current.md").write_text("Revenue is 5 billion dollars.", encoding="utf-8")
        code, result = self.run_script("run_writing_workflow.py", workspace)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["checkpoint"]["status"], "failed")

    def test_benchmark_mismatches_fail_and_matching_results_pass(self):
        original = self.text("original.md", "The coefficient is 0.15.")
        changed = self.text("changed.md", "The coefficient is 0.25.")
        safe = self.text("safe.md", "The estimated coefficient is 0.15.")
        gold = self.text("gold.md", "We report the sample size.")
        gold_manifest = self.text("gold.json", json.dumps({"cases": [{"id": "safe", "path": str(gold), "expected": "pass"}]}))
        real_run = subprocess.run

        def run_without_foundation(command, **kwargs):
            # The foundation suite runs separately in CI. Keep real detector and
            # report/exit-code behavior here, without running that suite per case.
            if any(str(arg).endswith("run_v31_writing_tests.py") for arg in command):
                return subprocess.CompletedProcess(command, 0, "- foundation-already-tested\n", "")
            return real_run(command, **kwargs)

        for kind, revised, expected, expected_exit in (
            ("false-negative", safe, "fail", 1),
            ("false-positive", changed, "pass", 1),
            ("matching", changed, "fail", 0),
            ("empty", changed, "fail", 1),
        ):
            with self.subTest(kind=kind):
                cases = [] if kind == "empty" else [{"id": kind, "original": str(original), "revised": str(revised), "variable": "X", "expected": expected}]
                mutations = self.text("mutations.json", json.dumps({"cases": cases}))
                output = self.directory / "benchmark.json"
                argv = ["benchmark", "--gold", str(gold_manifest), "--mutations", str(mutations), "--output", str(output)]
                with patch.object(sys, "argv", argv), patch.object(benchmark.subprocess, "run", side_effect=run_without_foundation), contextlib.redirect_stdout(io.StringIO()):
                    code = benchmark.main()
                report = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(code, expected_exit, report)
                self.assertEqual(report["status"], "pass" if code == 0 else "fail")
                if kind in {"false-negative", "false-positive"}:
                    metric = kind.replace("-", "_")
                    self.assertEqual(report["metrics"]["detectors"]["protected_patch"][metric], 1)
                    self.assertTrue(report["failures"])

    def test_documented_route_is_accepted_by_validator_and_cli(self):
        document = (ROOT / "references/v3/01-intake-routing.md").read_text(encoding="utf-8")
        example = json.loads(re.search(r"```json\s*\n(.*?)\n```", document, re.DOTALL).group(1))
        self.assertEqual(validate_route_card(example), [])
        args = []
        for field in ("task_mode", "discipline", "language", "evidence_mode", "execution", "preservation", "confidence"):
            args.extend(["--" + field.replace("_", "-"), example[field]])
        code, result = self.run_script("build_route_card.py", *args)
        self.assertEqual(code, 0, result)
        self.assertEqual(validate_route_card(result["route_card"]), [])

    def test_method_negation_and_measurement_are_not_overclaims(self):
        safe = [
            "The survey demonstrates high internal consistency.",
            "问卷调查证实了量表具有较高的内部一致性。",
            "案例研究的发现不具有普适性。",
            "The case study is not generalizable to the population.",
            "The Bartik instrument is not exogenous by construction.",
            "Bartik工具变量并非天然外生。",
            "The event-study plot does not prove parallel trends.",
            "Parallel trends are not proven by the event-study plot.",
            "平行趋势不能由事件研究证明。",
            "中介分析不能证明因果机制。",
        ]
        for text in safe:
            with self.subTest(text=text):
                result = check_method_language(text, Path("scenario.md"))
                self.assertEqual(result["status"], "pass", result)
                self.assertEqual(result["issue_count"], 0)
                self.assertEqual(result["advisory_count"], 0)
                self.assertEqual(result["decision"], "no-known-overclaim")

    def test_method_assertions_and_clause_boundaries_remain_protected(self):
        overclaims = [
            "Parallel trends are proven by the event-study plot.",
            "平行趋势由事件研究证明。",
            "The event-study plot not only proves parallel trends but also confirms the assumption.",
            "事件研究不仅证明平行趋势，而且支持因果解释。",
            "事件研究不但证明平行趋势，而且支持因果解释。",
            "The survey proves a causal effect.",
            "The case study proves a causal effect.",
            "案例研究证明因果效应。",
            "The Bartik instrument is exogenous by construction.",
            "Bartik工具变量保证排除限制。",
            "The case study is not generalizable, but this case study proves a population-wide causal effect.",
            "案例研究不具有普适性，但案例研究证明总体规律。",
            "The event-study plot does not prove parallel trends and the event-study plot proves parallel trends.",
        ]
        for text in overclaims:
            with self.subTest(text=text):
                code, result = self.run_script("check_method_language.py", self.text("method.md", text))
                self.assertNotEqual(code, 0, result)
                self.assertGreater(result["issue_count"], 0)
                self.assertEqual(result["decision"], "author-required")
        located = check_method_language(
            "The survey does not establish causality.\nParallel trends are proven by the event-study plot.",
            Path("scenario.md"),
        )
        self.assertEqual([issue["line"] for issue in located["issues"]], [2])

    def test_context_advisories_survive_reporting_without_blocking_workflow(self):
        text = "Bartik工具变量的外生性需要额外论证。"
        source = self.text("method.md", text)
        for script in ("check_method_language.py", "build_method_safety_report.py"):
            code, result = self.run_script(script, source)
            self.assertEqual(code, 0, result)
            self.assertEqual(result["issue_count"], 0)
            self.assertEqual(result["advisory_count"], 1)
            self.assertEqual(result["decision"], "review-needed")
            self.assertEqual(result["advisories"][0]["basis"], "context-needed")
        self.assertEqual(hard_audit(text, text, [])["status"], "pass")
        conditional = check_method_language(
            "The Bartik instrument is valid only under the stated exclusion restriction.",
            Path("scenario.md"),
        )
        self.assertEqual(conditional["status"], "pass")
        self.assertEqual(conditional["advisory_count"], 1)
        workspace = self.directory / "workspace"
        self.assertEqual(self.run_script("init_writing_workspace.py", workspace)[0], 0)
        self.assertEqual(self.run_script(
            "build_route_card.py", "--task-mode", "polish", "--discipline", "economics",
            "--language", "zh-CN", "--output", workspace / "route-card.json",
        )[0], 0)
        for name in ("original", "current"):
            (workspace / f"manuscript/{name}.md").write_text(text, encoding="utf-8")
        code, result = self.run_script("run_writing_workflow.py", workspace)
        self.assertEqual(code, 0, result)
        self.assertIn("contextual advisories", json.dumps(result))
        journal = (workspace / "revision-journal.jsonl").read_text(encoding="utf-8")
        self.assertIn("context-needed", journal)

    def test_economic_translation_check_is_explicit_and_does_not_relax_apply(self):
        pairs = [
            ("总资产为1.5亿元。", "Total assets were RMB 150 million."),
            ("收入为5万元。", "Revenue was CNY 50,000."),
            ("占比提高2个百分点。", "The share increased by 2 percentage points."),
            ("占比提高2个百分点。", "The share increased by 200 basis points."),
            ("销售额增长5%。", "Sales increased by 5 percent."),
            ("净收入为−0.15亿元。", "Net income was RMB -15 million."),
        ]
        for old, new in pairs:
            with self.subTest(old=old, new=new):
                original = self.text("source.md", old)
                revised = self.text("translation.md", new)
                code, report = self.run_script("check_numeric_consistency.py", original, revised, "--economic-units")
                self.assertEqual(code, 0, report)
                self.assertTrue(report["normalized_quantities"]["original"])
                self.assertTrue(report["normalized_quantities"]["revised"])
                self.assertIn("does not authorize apply", report["scope"])
        original = self.text("source.md", pairs[0][0])
        revised = self.text("translation.md", pairs[0][1])
        self.assertNotEqual(self.run_script("check_numeric_consistency.py", original, revised)[0], 0)
        self.assertNotEqual(self.run_script("verify_bounded_patch.py", original, revised)[0], 0)
        output = self.directory / "applied.md"
        code, report = self.run_script("apply_bounded_patch.py", original, revised, "--output", output)
        self.assertNotEqual(code, 0)
        self.assertFalse(report["applied"])
        self.assertFalse(output.exists())

    def test_economic_translation_check_rejects_changed_quantities(self):
        cases = [
            ("总资产为1.5亿元。", "Total assets were RMB 150 billion."),
            ("总资产为1.5亿元。", "Total assets were USD 150 million."),
            ("占比提高2个百分点。", "The share increased by 2 percent."),
            ("净收入为−0.15亿元。", "Net income was RMB 15 million."),
            ("We received 5 million dollars.", "We received 5 billion dollars."),
            ("Revenue was RMB 150 million euros.", "Revenue was RMB 150."),
            ("Sales were 2.5 widgets.", "Sales were 2.6 widgets."),
        ]
        for old, new in cases:
            with self.subTest(old=old, new=new):
                code, result = self.run_script(
                    "check_numeric_consistency.py", self.text("old.md", old),
                    self.text("new.md", new), "--economic-units",
                )
                self.assertNotEqual(code, 0, result)
        # Even in opt-in mode, do not normalize a literal formula into prose.
        _, converted = economic_numeric_inventory(r"The notation is $5 yuan + X$.")
        self.assertEqual(converted, [])


if __name__ == "__main__":
    unittest.main()
