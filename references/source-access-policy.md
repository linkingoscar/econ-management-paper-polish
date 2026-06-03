# Source Access Policy

Use before literature-backed writing, citation augmentation, topic/frontier scans, variable recommendations, journal-style adaptation, or method support when source access is uncertain.

## Access Tiers

### Tier 1: User-Provided Or Local Library Sources

Includes user-provided PDFs, drafts, BibTeX/RIS, Zotero records, Zotero PDFs, notes, and project files.

Allowed claims:

- If the full text or user material is inspected, cite and summarize with high confidence.
- Grade with `evidence-grading.md`: usually Grade A for directly inspected and supportive sources.

### Tier 2: Authenticated Institutional Access

Includes school-library sessions, CNKI, Web of Science, Scopus, EBSCO, ScienceDirect, Springer, Wiley, Taylor & Francis, JSTOR, database portals, and publisher full text reached through the user's authorized login.

Rules:

- Use only authorized access.
- Do not store, request, or expose passwords.
- Let the user handle SSO, MFA, captcha, paywall decisions, and downloads when needed.
- Avoid bulk scraping or behavior that could violate database terms.

Allowed claims:

- If full text or official database records are inspected, cite with the corresponding evidence grade.

### Tier 3: Publisher, DOI, Metadata, And Working-Paper Sources

Includes DOI landing pages, publisher abstracts, Crossref, OpenAlex, Semantic Scholar, SSRN, NBER, CEPR, RePEc, arXiv, OSF, institutional repositories, and official working-paper series.

Allowed claims:

- Metadata/abstract-supported claims may be Grade B.
- Do not treat metadata as full-text verification.
- Use working papers carefully and label status when relevant.

### Tier 4: Public Web And Search Results

Includes search-result pages, public summaries, news, blogs, library guides, non-official pages, and secondary summaries.

Allowed claims:

- Use for discovery, event dates, candidate sources, or context.
- Usually Grade C unless source details are independently verified.
- Do not insert as core theory/method support unless it is an authoritative official source.

### Tier 5: Unavailable Or Blocked Sources

Use when databases, full texts, or target-journal samples cannot be accessed.

Allowed output:

- Candidate directions or references clearly labeled as unverified.
- `[citation needed]`, `[full text not checked]`, or `[database access needed]`.
- A recommended retrieval plan.

Not allowed:

- Claim systematic coverage.
- Claim a direction is mainstream/frontier.
- Add a reference to the manuscript as confirmed support.

## Search-Coverage Labels

Use transparent labels in outputs involving sources:

- **Full-text verified**: full text or user-provided source inspected.
- **Metadata/abstract verified**: DOI, database, publisher, or abstract metadata checked, but full text not read.
- **Public-source preliminary scan**: only public web or metadata sources checked.
- **Candidate only**: plausible but not verified enough for citation.
- **Access limited**: source access blocked or unavailable.

## Downgrade Rules

- Full text inspected and directly supportive -> Grade A.
- Official metadata or abstract supports relevance but not exact claim -> Grade B.
- Search result or secondary mention only -> Grade C.
- Incomplete, tangential, unverifiable, or unsafe source -> Grade D.

If source access is limited, downgrade confidence and state the limitation.

## Minimum Standards By Task

- **Adding an in-text citation**: Grade A or strong Grade B.
- **Theory/hypothesis backbone**: Grade A preferred; Grade B only with caution.
- **Method support**: canonical or field-accepted source verified at least by metadata/abstract; full text preferred.
- **Policy/background fact**: official source preferred.
- **Topic/frontier recommendation**: at least two source channels preferred; otherwise label as preliminary.
- **Target-journal style adaptation**: author guidelines or recent sample papers required for journal-specific claims.

## Output Requirement

For source-dependent tasks, include a brief source-access note when useful:

```text
Source access used: [full-text verified / metadata verified / public-source preliminary scan / access limited]
Coverage limit: [what was not checked]
```

Do not over-explain this note for ordinary light polishing tasks.

