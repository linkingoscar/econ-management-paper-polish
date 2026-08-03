# Contributing to Econ-Management Paper Polish

Thank you for your interest in improving this skill! Contributions are welcome from
anyone in the academic and AI-agent community.

## Ways to Contribute

### 1. Add a Subfield Module

If your discipline or subfield is not well covered (e.g., behavioral finance, supply
chain management, health economics, tourism economics), you can add a new reference
module:

1. Create a new `.md` file in `references/` following the naming convention:
   - `cn-{subfield}-style.md` for Chinese writing styles
   - `en-{subfield}-style.md` for English writing styles
   - `subfield-{name}.md` for subfield-specific routing
2. Register the new file in `SKILL.md` under the **Reference Files** section.
3. Submit a pull request with a clear description of what the module covers.

### 2. Improve Style Rules

If you notice style guidance that is inaccurate, outdated, or missing:

- Edit the relevant file in `references/`.
- Keep changes focused: one improvement per pull request.
- Cite the source of the style rule (e.g., journal author guidelines, published paper).

### 3. Add Journal Family Guidance

If you have expertise with a specific journal or journal family:

1. Edit or create entries in `references/journal-families-econ.md` or
   `references/journal-families-management.md`.
2. Include: journal scope, typical contribution logic, preferred methods,
   formatting quirks, and recent trends.
3. Cite the journal's author guidelines or recent accepted papers as evidence.

### 4. Fix Bugs or Improve Routing

If the discipline router, method decision tree, or intake mode selector has issues:

- Open an issue describing the problem with a concrete example.
- Or submit a pull request with the fix.

## Guidelines

### Writing Style for Reference Files

- Use **imperative voice** ("Use when...", "Do not...") for rules.
- Keep paragraphs short. Prefer bullet lists for actionable rules.
- Avoid vague language like "generally" or "usually" without context.
- Include examples where helpful.

### Evidence Standards

When adding claims about journal requirements, method conventions, or field norms:

- Cite the source: journal author guidelines, published paper, or official documentation.
- Do not write "according to recent research" without a specific source.
- If the claim is based on general field convention, say so explicitly.

### v3 Reliability Checks

Changes to the v3 contracts, scripts, schemas, or reference routing must pass the
dependency-free repository and smoke checks from the repository root:

```bash
python scripts/validate_v3.py .
python evals/run_smoke_tests.py
```

When adding a journal rule or methodological claim, include an official or primary
source URL, a verification date, the applicable manuscript stage, and a clear
status (`verified`, `inferred`, `stale`, or `unknown`). Do not mark candidate or
rejected evidence as directly citable. If a script cannot run because a connector,
database, or original data is unavailable, document that capability limitation
instead of reporting a successful check.

### v3 Reference Migration and Adapters

New guidance belongs in one of the 14 packs under `references/v3/`. If it replaces
or consolidates a legacy module, update `references/v3/legacy-index.md`; do not
silently create a second routing rule in the old path. Provider adapters must return
normalized metadata with provenance and must never mark a result as citable by
themselves. RAG adapters must preserve source paths and retrieval context. Agent
adapters must support bounded serial execution or an explicit documented fallback.

### Naming Conventions

- File names: lowercase, hyphen-separated, `.md` extension.
- Examples: `cn-environmental-economics.md`, `en-ob-hr-style.md`
- Avoid spaces, uppercase, or special characters in file names.

### What NOT to Contribute

- Personal opinions without evidence.
- Specific journal requirements that are not sourced from official guidelines.
- Content that duplicates existing modules without adding value.
- Proprietary or copyrighted material.

## Pull Request Process

1. Fork the repository.
2. Create a feature branch: `git checkout -b add-tourism-economics-style`
3. Make your changes.
4. Ensure `SKILL.md` references any new files.
5. Submit a pull request with:
   - Clear description of what changed and why.
   - Links to sources if adding journal/field knowledge.
   - Examples of how the new module improves output (if applicable).

## Code of Conduct

Be respectful, evidence-based, and constructive. This project serves the academic
community — accuracy and intellectual honesty are paramount.

## Questions?

Open an issue on GitHub for questions, suggestions, or discussion.
