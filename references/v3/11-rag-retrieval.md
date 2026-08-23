# RAG And Retrieval Pack

## Retrieval stages

1. normalize the question and claim type;
2. choose keyword, semantic, or hybrid retrieval;
3. retrieve bounded candidates with source metadata;
4. rerank by claim fit, authority, recency, and access level;
5. verify the exact support and limitations;
6. write the Claim ID into the evidence ledger or mark the source candidate.

The default degradation path is **full index → local/manual index → BibTeX/metadata
search → user-guided search → no external source**. The output must state which path
was actually available. Retrieval similarity is not evidence of claim support.

## Chunk and citation rules

Keep title, authors, year, venue, DOI/URL, page/section, and source access tier with
each chunk. Prefer claim-sized excerpts and preserve enough context to detect scope
or causal-language changes. Never cite a retrieved title without verification.

The adapter contract lives in `adapters/rag/`; this pack defines behavior and safety,
not a mandatory vector database or embedding vendor.

The dependency-free lexical adapter emits overlapping 2–4 character n-grams for
continuous Han text and applies character-budget chunking when whitespace word
boundaries are absent. This is a deterministic fallback, not a substitute for
domain-aware Chinese segmentation or semantic retrieval.

Legacy sources merged: `rag-workflow.md`, `rag-retrieval.md`, `rag-verification.md`.
