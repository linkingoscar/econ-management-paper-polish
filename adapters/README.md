# v3 Adapters

The adapters are standard-library only and deliberately fail closed:

- `providers/`: real Crossref and OpenAlex metadata search. Results are candidates
  with provenance, not automatically citable evidence.
- `rag/`: a persistent lexical local index for Markdown, text, and JSON notes. It is
  reproducible and inspectable, not a hidden vector database.
- `agents/`: dependency-aware multi-role orchestration, serial fallback, and an
  optional OpenAI-compatible HTTP provider controlled by environment variables.

Use the scripts rather than importing providers directly for normal workflows:

```bash
python scripts/search_literature.py "staggered difference in differences" --provider both --json
python scripts/rag_search.py --index .rag/index.json --ingest references --query "parallel trends" --json
python scripts/run_agent_pipeline.py tasks.json --dry-run --json
```

Network access, API credentials, and full-text access are separate capabilities and
must be reported independently.

Provider references: [Crossref REST API](https://api.crossref.org/swagger-ui/index.html)
and [OpenAlex works API](https://developers.openalex.org/api-reference/works).
