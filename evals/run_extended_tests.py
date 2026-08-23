#!/usr/bin/env python3
"""Run the offline, expanded v3 migration and adapter evaluation suite."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from adapters.agents.serial import SerialAgentRunner, validate_tasks
from adapters.protocols import AgentResult, AgentTask, SearchRequest, SourceRecord
from adapters.providers.crossref import CrossrefProvider
from adapters.providers.openalex import OpenAlexProvider
from adapters.rag import MarkdownIndex
from adapters.search import MultiProviderSearch
from scripts.run_writing_benchmark import confusion, run_gold


FIXTURES = ROOT / "evals" / "fixtures" / "expanded"
PYTHON_UTF8 = [sys.executable, "-X", "utf8"]


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks: list[str] = []
    v3_packs = sorted((ROOT / "references" / "v3").glob("[0-9][0-9]-*.md"))
    expect(len(v3_packs) == 14, "expected 14 migrated responsibility packs")
    checks.append("migration/14-packs")
    legacy_rows = (ROOT / "references" / "v3" / "legacy-index.md").read_text(encoding="utf-8").splitlines()
    expect(sum(1 for line in legacy_rows if line.startswith("| `")) == 41, "legacy migration index must cover 41 files")
    checks.append("migration/41-legacy-files")

    crossref = CrossrefProvider()
    crossref_record = crossref._normalize(
        {
            "DOI": "10.1000/example",
            "title": ["Example title"],
            "author": [{"given": "Ada", "family": "Smith"}],
            "container-title": ["Example Journal"],
            "published": {"date-parts": [[2024, 1, 1]]},
            "abstract": "<jats:p>Abstract text.</jats:p>",
        }
    )
    expect(crossref_record.doi == "10.1000/example" and crossref_record.year == 2024 and crossref_record.abstract == "Abstract text.", "Crossref normalization failed")
    checks.append("providers/crossref-normalization")
    openalex = OpenAlexProvider()
    openalex_record = openalex._normalize(
        {
            "id": "https://openalex.org/W1",
            "doi": "https://doi.org/10.1000/example",
            "title": "OpenAlex title",
            "publication_year": 2023,
            "authorships": [{"author": {"display_name": "Ada Smith"}}],
            "primary_location": {"source": {"display_name": "Example Journal"}},
            "abstract_inverted_index": {"Abstract": [0], "text": [1]},
            "open_access": {"is_oa": True},
            "best_oa_location": {"landing_page_url": "https://example.org/oa"},
        }
    )
    expect(openalex_record.doi == "10.1000/example" and openalex_record.abstract == "Abstract text" and openalex_record.open_access_url, "OpenAlex normalization failed")
    checks.append("providers/openalex-normalization")

    class FakeProvider:
        name = "fake"

        def search(self, request: SearchRequest) -> list[SourceRecord]:
            return [SourceRecord(title="Example title", doi="10.1000/example", provider="fake")]

    records, errors = MultiProviderSearch([FakeProvider(), FakeProvider()]).search(SearchRequest("example", 10))
    expect(len(records) == 1 and not errors, "provider deduplication failed")
    checks.append("providers/deduplication")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        index = MarkdownIndex()
        added = index.ingest([FIXTURES])
        expect(added >= 6, "expanded fixtures were not ingested")
        index_path = temp / "index.json"
        index.save(index_path)
        loaded = MarkdownIndex.load(index_path)
        hits = loaded.search("parallel trends", 3)
        expect(hits and "did_zh.md" in hits[0].path, "RAG lexical retrieval failed")
        cli_index = temp / "cli-index.json"
        process = subprocess.run([*PYTHON_UTF8, str(ROOT / "scripts" / "rag_search.py"), "--index", str(cli_index), "--ingest", str(FIXTURES), "--query", "parallel trends", "--json"], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        expect(process.returncode == 0, f"RAG CLI failed: {process.stderr.strip()}")
        cli_report = json.loads(process.stdout)
        expect(cli_report["status"] == "pass" and cli_report["hits"], "RAG CLI failed")
        chinese_source = temp / "innovation-zh.md"
        chinese_source.write_text("数字化转型显著提高企业创新绩效。", encoding="utf-8")
        chinese_index = MarkdownIndex()
        expect(chinese_index.ingest([chinese_source]) == 1, "single Chinese document should ingest")
        chinese_hits = chinese_index.search("数字化转型 创新绩效", 3)
        expect(chinese_hits and chinese_hits[0].score > 0, "Chinese lexical retrieval should work in a one-document corpus")
        long_chinese_source = temp / "long-zh.md"
        long_chinese_source.write_text("数字化能力促进组织学习与流程创新。" * 12, encoding="utf-8")
        chunked_index = MarkdownIndex()
        expect(chunked_index.ingest([long_chinese_source], words_per_chunk=10) > 1, "long unspaced Chinese prose should be chunked")
    checks.append("rag/ingest-save-load-search")
    checks.append("rag/chinese-tokenization-and-chunking")

    def literature_handler(task: AgentTask) -> AgentResult:
        return AgentResult(task.task_id, task.role, "pass", output="bounded metadata report", capability="Verified")

    tasks = [AgentTask("literature", "literature", "find metadata"), AgentTask("method", "method", "diagnose", ["literature"])]
    ordered, errors = validate_tasks(tasks)
    results, run_errors = SerialAgentRunner({"literature": literature_handler, "method": literature_handler}).run(tasks)
    expect([task.task_id for task in ordered] == ["literature", "method"] and not errors and not run_errors and all(item.status == "pass" for item in results), "serial dependency runner failed")
    checks.append("agents/serial-dependency-runner")
    _, cycle_errors = validate_tasks([AgentTask("a", "a", "", ["b"]), AgentTask("b", "b", "", ["a"])])
    expect(cycle_errors, "agent cycle should be rejected")
    checks.append("agents/cycle-rejection")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        tasks_path = temp / "tasks.json"
        tasks_path.write_text(json.dumps({"tasks": [{"task_id": "literature", "role": "literature", "prompt": "find"}, {"task_id": "audit", "role": "audit", "prompt": "check", "depends_on": ["literature"]}]}), encoding="utf-8")
        process = subprocess.run([*PYTHON_UTF8, str(ROOT / "scripts" / "run_agent_pipeline.py"), str(tasks_path), "--dry-run", "--json"], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        expect(process.returncode == 0, f"agent pipeline CLI dry-run failed: {process.stderr.strip()}")
        report = json.loads(process.stdout)
        expect(report["status"] == "pass" and report["order"] == ["literature", "audit"], "agent pipeline CLI dry-run failed")
    checks.append("agents/cli-dry-run")

    expected_names = {"did_zh.md", "iv_en.md", "rd_en.md", "survey_zh.md", "experiment_en.md", "qualitative_zh.md"}
    expect({path.name for path in FIXTURES.iterdir()} == expected_names, "expanded method fixture set is incomplete")
    checks.append("evals/method-fixture-coverage")

    crash_metrics = confusion(["fail", "pass"], ["error", "pass"])
    expect(crash_metrics["true_positive"] == 0 and crash_metrics["invalid"] == 1 and crash_metrics["accuracy"] == 0.5, "detector errors must not score as true positives")
    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_manifest = Path(temp_dir) / "invalid-gold.json"
        invalid_manifest.write_text(json.dumps({"cases": [{"id": "missing", "path": "evals/fixtures/does-not-exist.md", "expected": "fail"}]}), encoding="utf-8")
        invalid_metrics, invalid_details = run_gold(ROOT, invalid_manifest)
        expect(invalid_metrics["invalid"] == 1 and invalid_details[0]["observed"] == "error", "a crashed or invalid detector run must remain an error")
    checks.append("evals/detector-error-accounting")
    print(f"v3 extended tests passed ({len(checks)} checks)")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"v3 extended tests failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
