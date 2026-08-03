# Evidence And Sources Pack

## Claim workflow

Classify each requested or newly discovered claim as policy/background, stylized
fact, theory/mechanism, identification/method, measurement, empirical benchmark, or
implication. Search primary sources first. For every usable claim create a stable
`CLM-*` entry with title, authors/year/venue when available, URL/DOI, checked date,
support location, limitations, verification level, and allowed use.

`full_text` and `official_page` may support direct citation; `metadata` is cautious
background; `candidate` is not inserted; `rejected` is never cited. Run
`scripts/build_evidence_pack.py` before treating the ledger as complete.

## Source access and downgrade

1. user-provided/local full text or library record;
2. authenticated institutional or publisher full text;
3. official DOI/publisher page and trusted metadata;
4. public search result or working paper;
5. unavailable/blocked source.

Downgrade the claim when access is limited. Never fill an evidence gap from memory.
Separate source relevance from claim support and label adjacent sources as candidates.
Theory, mechanism, and measurement claims require a source that actually supports
that sentence, not merely a paper with a similar title.

Legacy sources merged: `source-access-policy.md`, `evidence-citation-workflow.md`,
`evidence-grading.md`, `theory-backing-router.md`.
