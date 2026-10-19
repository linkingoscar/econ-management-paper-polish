# Retrieve relevant and competing evidence

Use when a literature collection or search tool is available.
Retrieval finds candidates; [rag-verification](rag-verification.md) decides support.

## Form the query from the research question

Identify constructs, relationship, population, time, design and evidential role.
Use synonyms and relevant language variants without silently changing construct
meaning. Search neutral formulations as well as contrary/null findings when relevant.
"Find support for X" should not suppress material evidence against X.

Break a compound claim into parts if different sources would support them.
Search a method's actual methodological section or a variable's definition rather
than assuming keywords in an abstract establish those details.

## Choose available search

- Exact text/keywords: source identity, quotations, variable names, methods.
- Semantic retrieval: conceptual paraphrases, when such a tool exists.
- Combined search: useful when either approach misses relevant material.
- Metadata filters: apply only to the real scope; explain exclusions that matter.

Do not impose universal cosine cutoffs, retrieval counts or weighting formulas.
Scores are system-dependent and do not measure claim support.
A highly cited, newer or prestigious paper is not automatically a better source
for the particular claim; ranking should preserve relevant contrary evidence.

## Read and refine

Inspect candidates and surrounding passages. Broaden terms when recall is weak;
narrow by the actual question when results are irrelevant.
Track search scope enough to explain the answer; avoid repeated equivalent searches
once the necessary evidence is found and unresolved limits are clear.

Distinguish no retrieved match from absence of relevant research.
Deduplicate versions carefully; a changed paper may have changed findings.
Return source locators and why each item matters, not only scores or paper counts.
