# Results And Quality-Gates Pack

## Gates before release

1. Paradigm and outlet fit are explicit.
2. Every important claim has matching evidence or a limitation marker.
3. Citations are traceable and no placeholders are silently retained.
4. Numbers, variables, tables, figures, references, and equations are consistent.
5. Identification and causal language match the design and estimand.
6. The report distinguishes text transparency from code/data replication.

Use deterministic checks for exactness: numeric tokens, citation/BibTeX keys, LaTeX
references/packages/figures, and version comparison. A passing check proves only the
checked invariant. A model must not silently rewrite a failing artifact.

## Result language

Use “is associated with” when the design identifies association; reserve causal verbs
for an explicitly defended estimand. Report uncertainty and economic magnitude, not
only stars. Flag external-validity, measurement, specification, and inference risks.

## Triage

Classify findings as blocking, major, moderate, or cosmetic. A blocking integrity or
identification issue precedes stylistic polish.

Legacy source merged: `quality-gates.md`; cross-cutting audit rules are in
`v3-audit-contract.md`.
