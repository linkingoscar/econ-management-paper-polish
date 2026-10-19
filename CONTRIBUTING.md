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
2. Link the new file from the appropriate task route in `SKILL.md` or a relevant reference; explain when to read it.
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
2. Separate observed conventions and editorial judgment from requirements.
   For binding requirements, record the official source, check date, article type
   and submission stage; sample articles alone do not establish rules.
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

### Naming Conventions

- File names: lowercase, hyphen-separated, `.md` extension.
- Examples: `cn-environmental-economics.md`, `en-ob-hr-style.md`
- Avoid spaces, uppercase, or special characters in file names.

### What NOT to Contribute

- Unsupported factual claims or unlabeled editorial judgments.
- Specific journal requirements that are not sourced from official guidelines.
- Content that duplicates existing modules without adding value.
- Proprietary or copyrighted material.

## Pull Request Process

1. Fork the repository.
2. Create an appropriately named feature branch, for example `codex/tourism-style`.
3. Make your changes.
4. Check frontmatter and reference links. For changed non-trivial behavior, use
   the relevant cases in `evals/README.md` or add a meaningful regression case.
   Do not treat phrase matching or a validator exit status as semantic validation.
5. Submit a pull request with:
   - Clear description of what changed and why.
   - Links to sources if adding journal/field knowledge.
   - Examples of how the new module improves output (if applicable).

## Code of Conduct

Be respectful, evidence-based, and constructive. This project serves the academic
community — accuracy and intellectual honesty are paramount.

## Questions?

Open an issue on GitHub for questions, suggestions, or discussion.
