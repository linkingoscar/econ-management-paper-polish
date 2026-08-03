# Integrations And Capability Pack

## Capability modes

- **Verified**: an adapter or deterministic check ran and returned evidence.
- **Documented**: the interface is available, but this session did not execute it.
- **Conceptual**: required infrastructure, credentials, data, or connector is absent.

Always report the mode and the output ceiling. A local text audit is not a database
search, RAG retrieval, source verification, or replication.

## Adapter boundaries

- Source adapters return normalized candidates with URL/DOI, metadata, access tier,
  retrieval timestamp, and an opaque provider ID. They do not directly edit prose.
- RAG adapters implement ingest, search, and retrieve-with-context; verification and
  Claim ID assignment remain a separate step.
- Agent adapters accept a bounded task, required inputs, output schema, and timeout;
  they return a diff/report plus capability and provenance. They must be replaceable
  by serial execution.

The reference implementations are dependency-free stubs in `adapters/`. Optional
providers are discovered through configuration and fail closed when credentials or
network access are absent. No source is treated as citable merely because an adapter
returned it.

Legacy sources merged: `v3-runtime-contract.md`, `v3-evidence-ledger.md`,
`v3-audit-contract.md`.
