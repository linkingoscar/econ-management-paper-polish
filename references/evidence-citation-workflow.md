# Evidence And Citation Workflow

Use this file whenever the task involves adding, replacing, verifying, formatting, or strengthening references; adding policy background; supporting theory and hypotheses; justifying methods; or finding alternative references. If source access is uncertain, read `source-access-policy.md` first. For theory and hypotheses, pair it with `theory-backing-router.md`. For every added, replacement, or candidate reference, use `evidence-grading.md`.

## Non-Negotiable Rule

No new reference enters the text or bibliography unless it is traceable to at least one current-session source:

- User-provided PDF, manuscript, Zotero item, BibTeX, RIS, note, or link.
- Publisher or journal landing page.
- DOI resolver, Crossref, OpenAlex, Semantic Scholar, Web of Science, Scopus, CNKI, CSSCI source, Google Scholar page, SSRN, NBER, CEPR, arXiv, RePEc, OSF, or institutional repository.
- Official government, regulator, standards body, statistical bureau, exchange, central bank, or international organization page for policy/background claims.

If only a memory-based citation seems relevant, search it first. If verification fails, do not cite it.

## Source Priority By Claim Type

### Policy Or Background Claims

Preferred sources:

1. Official policy text, laws, regulations, government notices, central bank/regulator releases, statistical bureau data.
2. Authoritative institutional reports from OECD, World Bank, IMF, BIS, ILO, UN agencies, central banks, exchanges, or industry regulators.
3. Peer-reviewed empirical papers or working papers analyzing the policy/event.
4. Reputable news only for dates and event facts when primary sources are not available.

For Chinese CSSCI papers, policy background may be useful, but it must be tied to the research question rather than used as decorative opening material.

### Theory And Hypothesis Claims

Preferred sources:

1. Seminal theory articles/books in the target field.
2. Top or field-journal papers that operationalize the theory in a similar setting.
3. Recent review/meta-analysis papers when mapping a literature stream.
4. Chinese CSSCI literature only when the target is Chinese or China-specific and the theory use is recognized in that literature.

Every theory citation should support a mechanism, boundary condition, construct definition, or hypothesis direction. Do not cite a paper merely because it shares keywords.

### Empirical Method Or Identification Claims

Preferred sources:

1. Econometrics/statistics/methodology articles or books.
2. Recent applied papers in the target journal family that use the same method.
3. Software/package documentation only for implementation details, not methodological validity.
4. Working papers when they are the current method reference and widely used.

When recommending methods, distinguish "methodologically appropriate" from "currently fashionable."

### Measurement Or Proxy Claims

Preferred sources:

1. Original scale, construct, or proxy paper.
2. Field-standard applications in the same discipline.
3. Validation studies or robustness papers.
4. Database documentation for variable construction.

Do not relabel a proxy as the construct itself.

### Topic, Frontier, Or Variable Recommendation Claims

Preferred sources:

1. Recent review articles, editorials, special issues, calls for papers, and target-journal clusters.
2. Recent top/field-journal papers in the routed subfield.
3. Citation networks from seminal work to recent applications.
4. Verified CNKI/CSSCI literature for Chinese topics and China-specific debates.
5. Official datasets, policy documents, database manuals, or user-provided data documentation for variable feasibility.

Do not label a direction as mainstream, frontier, or promising based only on intuition or search-result snippets.

## Retrieval Workflow

1. Identify available source access using `source-access-policy.md` when needed.
2. Parse the sentence or section into citation needs.
3. Generate search queries by discipline, construct, method, and target outlet.
4. Search at least two source channels when adding important references: e.g., Zotero/CNKI/school database plus Crossref/OpenAlex/publisher page when available.
5. Prefer sources with full text or DOI, stable URL, journal venue, complete metadata, and clear relevance.
6. Verify metadata: author names, year, title, journal, volume/issue/pages, DOI/URL.
7. Check support: confirm what claim the source supports.
8. Grade the evidence using `evidence-grading.md`.
9. Add in-text citation and reference-list entry only when grade threshold is met.
10. Report uncertain or weaker candidates separately, with source-access limits.

## Evidence Pack Format

When adding or replacing references, include a compact evidence pack:

| Use | Source | Supports | Trace |
| --- | --- | --- | --- |
| Theory | Author (Year), Title, Venue | Mechanism or construct | DOI/URL/CNKI/Zotero key |
| Method | Author (Year), Title, Venue | Identification or estimation choice | DOI/URL |
| Policy | Institution (Year), Document | Policy fact or institutional setting | Official URL |

Then list complete references in the requested style. Default: APA 7.

## Alternative Reference Search

When the user asks for alternative references:

- Preserve the claim's exact function: seminal theory, recent evidence, Chinese context, top-journal method exemplar, or policy fact.
- Return 3-8 candidates, grouped by function.
- For each candidate, state why it is a substitute and what it cannot support.
- Do not replace a seminal citation with a recent empirical citation unless the claim changes.

## APA Defaults

Use APA 7 style by default:

- Journal article: Author, A. A., & Author, B. B. (Year). Title of article. *Journal Title, volume*(issue), pages. https://doi.org/...
- Working paper: Author, A. A. (Year). Title. *Series or repository*. URL/DOI.
- Government document: Institution. (Year). *Title of document*. URL.
- Chinese sources: preserve Chinese title and institution names unless the target manuscript requires translation. If translating, include the original title when useful.

If metadata is incomplete, mark missing fields explicitly rather than guessing.

## Output Rules

For citation-augmentation tasks, default output:

1. Revised text.
2. Evidence pack.
3. Added/replaced references in APA.
4. Sources rejected or needing user confirmation.

If the user only asked for polished prose and did not request reference expansion, do not add references unless an unsupported claim is severe. Flag the need instead.
