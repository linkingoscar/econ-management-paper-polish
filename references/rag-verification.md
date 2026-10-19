# Verify retrieved evidence

Use before relying on passages retrieved from a library or search index.
The admission rule is [evidence-grading](evidence-grading.md); retrieval does not
create a second, weaker standard.

1. Resolve the result to its source/version and page, section or stable chunk locator.
2. Inspect the passage in context when available, including negation, qualifiers,
   population, time, design and whether the author is quoting another source.
3. Compare it with the exact manuscript claim. Record supports, partly supports,
   contradicts, background only, not addressed or undetermined.
4. Distinguish a retrieved excerpt from a checked full paper and from inferred meaning.
5. Integrate only the supported statement; carry material limits into the writing.

A high similarity score, same keywords or matching author/year is not verification.
Do not reject a contrary finding merely because it is contrary. Do not replace
an older finding with a newer one without examining their evidence and comparability.
A limitation passage may be exactly the relevant evidence for a limitation claim;
its section name does not make it unusable.

For OCR or extraction errors affecting coefficients, symbols, tables or quotations,
inspect the rendered page if available. Otherwise flag the uncertain reading.

Output can be brief:
claim → source and locator → material inspected → support relation → usable wording
or unresolved limit. Batch records should preserve this information without
turning "source exists" into a claim-support pass.
