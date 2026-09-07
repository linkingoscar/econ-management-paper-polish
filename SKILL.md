---
name: econ-management-paper-polish
description: >
  Write, polish, translate, and review Chinese and English economics, management,
  and related business-school papers. Preserve evidence and author intent; adapt
  argument and prose to the field, section, and audience. Use for 经管论文润色、
  中英学术翻译、引言与结果写作、方法表述诊断、期刊适配和审稿回复。
---

# Econ and Management Paper Polish

Deliver usable manuscript prose or a focused diagnosis from the material supplied.
Current release: v3.1.0-alpha.6. Installation and host compatibility are in
[README.md](README.md); script details are loaded only when needed.

## Start with the writing task

1. Infer the language, discipline, section, and requested depth from the text.
   Keep the route in context. Ask only when missing information would change the
   argument or require inventing evidence; finish independent parts meanwhile.
2. Read [writing and style](references/v3/02-writing-style.md), then the ONE
   matching Chinese/English economics/management guide it links. For finance,
   accounting, marketing, IS, or another adjacent field, also read the relevant
   section of the linked field guide. A named journal does not require a corpus
   project for a paragraph polish.
3. Revise or draft the requested passage. Lead with the revised text; preserve the
   author's terminology and voice. For a diagnosis, lead with located findings.
   Do not rewrite when the user asked only for a review.
4. Check facts and the relevant risks before delivery. For a same-language
   meaning-preserving edit, run `scripts/verify_bounded_patch.py` on original and
   candidate text; temporary files suffice. For translation, follow the distinct
   checks in the style pack rather than treating changed language as changed facts.

Default delivery is the finished text plus brief explanations only where useful.
Mention unresolved evidence or material risks specifically, not as a routine
checklist. A local evidence gap should not prevent polishing the rest of a passage.
A section draft uses supplied notes, tables, or claims; placeholders may mark
missing inputs, but must not disguise them as completed results.

Short polish, translation, section drafting, and a one-off reviewer response need
no workspace, JSON routing card, evidence ledger, or Agent panel by default.
Use the user's existing files and formats. For Word-oriented prose, return clean
paragraphs without Markdown syntax; for LaTeX, preserve commands and references.
Creating or redlining a native document requires a suitable document tool and
inspection of the result, not merely a plain-text response.

## Preserve the research

- Never invent data, results, citations, mechanisms, institutional facts, or current
  journal requirements. Separate what the material shows from what remains unknown.
- Preserve coefficients, signs, p-values, sample sizes, variable labels, equations,
  citations and their claims, limitations, and contribution positioning. A polish
  cannot silently change identification, theory, result interpretation, or causality.
- Respect explicit substantive instructions already given by the user. A lexical
  warning is a reason to inspect a change, not proof of a meaning change or a demand
  for repeated approval. Unsupported factual changes still require evidence.
- Distinguish statistical precision, economic/practical magnitude, and causality.
  Do not invent baseline means, scales, or benchmarks to interpret an estimate.
- Keep the existing citation style unless conversion is requested. For a new
  standalone bibliography with no specified style, use APA 7; follow requested
  GB/T 7714 or outlet style. New or corrected references need a traceable source
  inspected in the session or supplied by the user, not model memory.
- "De-AI" means clearer, less formulaic academic writing, not optimizing detector
  scores or concealing authorship. Preserve author responsibility and applicable
  disclosure requirements.
- A passing script checks only its stated scope. It is not semantic equivalence,
  evidence that a claim is true, a successful data replication, or publication approval.

## Load only what the task needs

| Task | Read and use |
|---|---|
| Polish, translation, bilingual terminology | [Style and output rules](references/v3/02-writing-style.md); its selected field guide and examples |
| Introduction, literature, theory, results, discussion | [Argument and section structure](references/v3/06-argument-structure.md), plus the relevant worked example linked from the style pack |
| Methods, identification, robustness, mediation | [Methods and identification](references/v3/05-methods-identification.md); inspect supplied design before prescribing checks |
| Add, replace, or verify sources | [Evidence sources](references/v3/04-evidence-sources.md); cite only material that supports the claim |
| Named outlet requirements or supplied reference papers | [Journal adaptation](references/v3/03-journal-adaptation.md); distinguish observed style from verified requirements |
| Reviewer response or tracked revision | [Revision and risk](references/v3/08-revision-risk.md); address the specific request and state actual changes |
| LaTeX or reproducibility audit | [LaTeX](references/v3/10-latex-typesetting.md) or [data and reproducibility](references/v3/13-reproducibility-data.md) |
| Sustained manuscript audit, corpus workflow, or integrations | [Pack index](references/v3/README.md) and [writing contract](references/v3-writing-contract.md) |
| Choose a script | [Command reference](references/v3-command-reference.md) |

For methods, follow data structure → identifying variation → estimand → assumptions
→ diagnostics → remaining threats. A method name alone establishes none of these.
Event-study leads do not prove parallel trends; matching and controls do not
automatically solve endogeneity; mediation does not by itself establish a causal
mechanism. Survey, experimental, qualitative, and review designs need their own
standards. Explain which supplied result supports each diagnostic; with no data or
code, diagnose reporting and design transparency without claiming a rerun.

The method-language screen separates known overclaim patterns from contextual
advisories. Inspect either in its paragraph before proposing a correction.
Conditional or negated discussion is not automatically an error, and a regex
cannot decide whether an identification argument is valid.

## Tracked and optional workflows

Use a workspace when the user needs sustained manuscript-wide audit or explicit
revision tracking. Read [routing](references/v3/01-intake-routing.md) and the
[writing contract](references/v3-writing-contract.md); persist only relevant state.
Existing provenance, source-snapshot, apply/rollback, issue-history, and protected
field gates still apply. Scripts do not silently overwrite the manuscript.

For a reusable corpus-derived style profile, follow the confirmation and
structural-only copy boundary in [the corpus contract](references/v3-corpus-and-style.md).
Do not require a profile to use ordinary field guidance or discuss supplied examples.
For optional comparative Agent evaluation, read
[the Agentic contract](references/v3-agentic-benchmark.md). Judge consensus cannot
authorize high-risk scholarly changes; same-model judgments are limited evidence.
Do not start a panel simply because a writing task is substantial.

In an audit, name the actual checks and their capability ceiling: Verified for a
performed check, Documented for an unexecuted workflow, Conceptual for unavailable
infrastructure. If TeX compilation cannot run, report structural checking only.
Repository fixtures test local behavior; they are not external-paper quality data.
