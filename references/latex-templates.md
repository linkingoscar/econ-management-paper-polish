# Select a real template for the actual submission

Use when a manuscript needs a LaTeX template or a template conversion.
Do not maintain guessed class names or fixed journal word/page limits here.

## Source and stage

1. Identify journal, article type and submission stage.
2. Check the journal's current official instructions and the template they link.
3. Distinguish initial manuscript preparation from accepted-article production.
4. Inspect supplied project files before replacing an existing class or bibliography.
5. Record the source/date and apply only the relevant requirements.

Starting points, not stored requirements:
- [American Economic Review submissions](https://www.aeaweb.org/journals/aer/submissions)
- [Quarterly Journal of Economics instructions](https://academic.oup.com/qje/pages/Instructions_To_Authors)

Follow current links from the official page for any actual template; these URLs do
not guarantee a particular class, package, word limit or file-format requirement.
Do not infer an economics or management journal's current rules from its reputation,
another journal's template, or a published article.

## When a template is not required or available

Preserve a working user template. For a new general draft, use a simple available
article setup appropriate to language and compiler; label it a general draft.
Do not call a generic article "AER-compliant" or invent an aer package/class.

Choose a bibliography system compatible with the project and actual style.
natbib is a citation package, not a bibliography style file; apalike is not a
guarantee of APA 7 compliance. Do not mix incompatible systems to imitate a journal.

## Convert conservatively

Inspect class options, local style files, bibliography backend, commands,
cross-references, equations, figures and table notes before conversion.
Preserve citation/label keys and content. Replace only what the target needs.
Do not insert fake DOI examples or dummy results into the manuscript.

Use [latex-support](latex-support.md) for content preservation and
[latex-audit](latex-audit.md) for compilation and rendered inspection.
If a required class/compiler is unavailable, preserve editable sources and state
the specific limitation; do not claim the deliverable was compiled.
