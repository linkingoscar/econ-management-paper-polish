# Evidence Grading

Use this whenever adding, replacing, verifying, or recommending references. The goal is to distinguish "verified support" from "possibly relevant candidate."

## Evidence Grades

### Grade A: Directly Verified And Supportive

Use when:

- Full text, user-provided PDF, Zotero PDF, or official source has been inspected.
- The source directly supports the exact claim.
- Metadata is complete enough for the requested citation style.

Allowed use:

- Add to text and reference list.
- Use as main theoretical, empirical, policy, or method support.

### Grade B: Metadata Verified, Claim Support Plausible

Use when:

- DOI/publisher/CNKI/Crossref/OpenAlex/Zotero metadata is verified.
- Title, abstract, or source description strongly indicates relevance.
- Full text has not been inspected.

Allowed use:

- Use cautiously for background or candidate support.
- Prefer wording such as "related work suggests" only if claim support is clear from abstract/metadata.
- Mark as not fully read when important.

### Grade C: Candidate Source, Needs Confirmation

Use when:

- Source is found through search results or secondary references.
- Metadata or relevance is incomplete.
- It may be a good substitute but has not been verified.

Allowed use:

- List as candidate only.
- Do not insert into manuscript as a supporting citation.

### Grade D: Rejected Or Unsafe

Use when:

- Metadata cannot be verified.
- Source does not support the claim.
- Source is too tangential.
- Source appears predatory, non-authoritative, retracted, duplicated, or mismatched.

Allowed use:

- Report as rejected if useful.
- Do not cite.

## Source Authority Tags

Add one or more tags:

- **Seminal theory**
- **Recent top/field journal**
- **Method canonical**
- **Recent method application**
- **Official policy**
- **Dataset/manual**
- **Chinese CSSCI**
- **Working paper**
- **Review/meta-analysis**
- **Context-specific evidence**
- **Candidate only**

These tags help explain why a reference is included.

## Claim Fit Tags

Map every source to one claim function:

- Construct definition.
- Mechanism.
- Hypothesis direction.
- Boundary condition.
- Measurement/proxy.
- Method/estimator.
- Identification assumption.
- Policy/background fact.
- Empirical benchmark.
- Managerial/policy implication.

If one source cannot be mapped to a claim function, do not cite it.

## Evidence Pack With Grades

Use this format:

| Grade | Role | Source | Supports | Trace | Note |
| --- | --- | --- | --- | --- | --- |
| A | Theory | Author (Year) | Mechanism | DOI/URL/Zotero | Full text checked |
| B | Method | Author (Year) | Estimator choice | DOI/URL | Abstract/metadata checked |
| C | Alternative | Author (Year) | Possible substitute | Search result | Needs confirmation |

## Replacement Rules

When replacing a weak reference:

1. Identify the exact claim the old citation was supposed to support.
2. Find a replacement with the same claim function.
3. Prefer higher evidence grade and higher field authority.
4. Preserve seminal citations unless the user asks for recent alternatives.
5. Do not replace theory with empirical evidence or method references with software documentation unless the claim changes.

## Minimum Thresholds

- New in-text citation: Grade A or strong Grade B.
- Theory/hypothesis backbone: Grade A preferred; Grade B allowed only with explicit caution.
- Method justification: Grade A or Grade B from canonical method/source metadata; verify before strong wording.
- Policy fact: Grade A official source preferred.
- Reference list addition: Grade A or B only.
- Candidate list: Grade C allowed, clearly labeled.

## Output Wording

Use transparent wording:

- "已核验并可直接引用" for Grade A.
- "元数据/摘要已核验，建议进一步阅读全文" for Grade B.
- "候选文献，需确认" for Grade C.
- "不建议引用" for Grade D.

