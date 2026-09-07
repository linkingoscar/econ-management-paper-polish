# Writing And Style Pack

## Invariants

For a line polish, preserve numbers, signs, p-values, sample sizes, variable names,
equation notation, table/figure numbers, citation keys, and causal strength. Improve
clarity, order, precision, and discipline-appropriate tone; do not use inflated
adjectives or erase a limitation.

## Choose one detailed writing guide

These maintained detail files are explicitly part of the v3 loading route.
Open the selected guide; the table alone is not the writing instruction.

| Route | Read | Emphasis |
|---|---|---|
| Chinese economics | [Chinese economics](../cn-economics-style.md) | economic question, useful institutional context, design, magnitude |
| English economics | [English economics](../en-economics-style.md) | question, identifying variation, evidence, contribution |
| Chinese management | [Chinese management](../cn-management-style.md) | construct, theory mechanism, evidence, contribution and implications |
| English management | [English management](../en-management-style.md) | theoretical puzzle, construct distinctions, mechanism, boundary conditions |

For an adjacent field, read only its section in [field styles](../field-style-packs.md).
Use [economics subfields](../subfields-economics.md) or
[management subfields](../subfields-management.md) when the subfield changes the
argument. The target research paradigm takes priority over a broad discipline
label: quantitative marketing and behavioral marketing need different emphases.
Theory, structural, qualitative, and descriptive papers must not be forced into
an applied-causal template. Chinese does not imply a policy-slogan introduction;
English management does not imply hypotheses for every type of article.

For a passage-level model, read the relevant section of
[worked writing examples](writing-examples.md). These synthetic examples teach
decisions; they are not reusable findings, mandatory templates, or quality data.

## Editing order

1. Repair logical subject and claim-evidence alignment.
2. Remove repetition, vague AI-sounding transitions, and unsupported intensifiers.
3. Make economic or practical meaning explicit after statistical results.
4. Preserve uncertainty: use association language when identification is incomplete.
5. Run `scripts/check_numeric_consistency.py` for meaning-fixed revisions.

Keep unsupported additions out of the revised paragraph. If a result needs a
baseline mean to express economic magnitude, ask for that mean only when needed
or mark the missing benchmark; do not infer it from the coefficient.

## Translation and bilingual editing

1. Write in the requested target language and preserve the research claim.
   Reorder prose for the audience; do not introduce a stronger contribution,
   identification design, mechanism, or causal verb during translation.
2. Retain a short in-context term mapping for recurring constructs and institutions.
   Use supplied definitions and established names; explain a local institution
   functionally on first mention when needed. Do not invent its official English
   name or require a glossary file for a paragraph.
3. Keep citation keys, author identities, variable names, estimands, equation
   notation, and table/figure links. Retain the supplied author spelling unless
   a verified bibliographic source supports another form; do not invent pinyin or
   translate a surname to make the citation detector pass.
4. Prefer keeping numbers and units. For customary target-language equivalents,
   record the concrete conversion, e.g. CNY 1.5亿元 → RMB 150 million.
   Distinguish percent from percentage points and coefficients from marginal
   effects. Do not convert currencies without a supplied rate/date and instruction.
5. Run the bounded verifier to locate protected-field changes, but inspect its
   components: same-language lexical counts and string-based sentence alignment
   are not a cross-language acceptance test. For an explicitly established CNY
   context, use the optional numeric check below on corresponding short passages.
   It also supports percent, percentage points, and basis points.

Run from the skill root:

    python scripts/check_numeric_consistency.py original.md translated.md --economic-units --json

The report shows recognized original and translated amounts and their canonical
values, alongside the strict numeric result. It checks an inventory, not which
claim owns each amount. Inspect the aligned source/target sentences, signs,
negation, uncertainty, citation attachment, and claim direction yourself.
Unrecognized units and translated author names need explicit comparison to the
source; they are not validated by a numeric pass. 元/yuan is treated as CNY only
when that currency context has been established.

Translation authorization covers faithful translation and transparent equivalent
notation; it is not authorization to change the research. Do not ask again merely
because translated words changed a lexical count. Deliver the inspected translation
and any concrete unresolved issue without claiming the strict patch gate passed.
The optional numeric check does not relax bounded apply or overwrite protections.

## Output that can be used immediately

- Same-language polish: revised text first; explain only consequential edits.
- Translation: target-language prose first. Include a back-translation or term
  table only when requested or needed to resolve ambiguity.
- Word-oriented text: clean paragraphs, ordinary percent signs and author-year
  references; no code fences, Markdown headings, or LaTeX escaping in the prose.
- LaTeX: preserve commands, math delimiters, citations, labels, and references;
  escape plain-text special characters without double-escaping existing commands.
- Missing evidence: finish supported portions and locate the gap. A language
  edit cannot establish an unsupported hypothesis or repair a research design.

For a native DOCX/PDF edit, use an available document tool and inspect the output;
plain text is not evidence that formatting, comments, or tracked changes survived.
