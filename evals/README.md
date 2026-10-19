# Behavioral evaluation

These are synthetic task fixtures, not scientific evidence or real journal rules.
They protect consequential decisions in writing, evidence use and revision.
They are not exact-output tests, word-count targets or a claimed benchmark score.

All development papers, fixtures and recorded outputs in this evaluation area are
test materials, not a default literature collection for manuscript work. Use them
to find transferable failures in writing and reasoning, then check any proposed
rule on different topics and sources. Do not turn a sample's findings, preferred
theories or wording into universal writing instructions or reusable citations.

## Run

Give an independent executor the skill path and only the selected request(s) from
[cases.jsonl](cases.jsonl), plus permission to read needed skill references.
Do not show this rubric, the implementation diff, suspected failures or expected
answers. Restrict source access according to each fixture; do not retrieve real
literature to "verify" invented fixture metadata.

Ask it to complete the user task, not explain how the skill ought to behave.
Keep generated outputs outside the working tree or in a dedicated evaluation
artifact location. An agent may handle a small batch, but cases in a shared
context are not independent samples; record that limitation.

Inspect actual output against the raw material and criteria below.
Flag critical fabrication or meaning changes separately from missing usefulness.
Use "meets / partial / fails / not run", with a reason and output locator.
Do not infer semantic correctness from matching headings, keywords or file hashes.

## Criteria

| Case | Meaningful behavior to inspect |
|---|---|
| C01 | Direct revised text; preserve dates, sign, estimate, p, N and non-significance; no unnecessary literature/pipeline or invented specifics |
| C02 | Preserve attribution [A]/[B], population limitation, negation and distinction between no support and ruled-out effect |
| C03 | Improve prose without deleting the actual design limits or converting association to causation |
| C04 | Distinguish inspected abstract from unseen full text; support only stated association/boundary; no risk-sharing mechanism claim |
| C05 | Do not let correct metadata override contradictory content or invent turnover outcomes; provide usable narrower wording |
| C06 | Preserve mixed findings and differences in sample/design; no consensus, causal certainty, or dismissal merely by age |
| C07 | Supply a usable provisional abstract or completed portions; no invented coefficient, significance, result or finished analysis |
| C08 | 3 percentage points, interval −1 to 7 points; no unsupported relative-percent baseline, definitive increase or causal upgrade |
| C09 | Preserve valid sample/model differences; identify and repair the actual overgeneralization in the discussion without unifying estimates |
| C10 | Interpret the provided legend; ** is consistent with p=0.008; no automatic conversion to *** |
| C11 | Useful qualitative structure and bounded process prose; incorporate the negative case; no invented coding/saturation, causal proof or forced hypotheses/regression |
| C12 | Remove "completely ineffective"; preserve uncertainty and compatible effects, with correct scale; no invented equivalence test |
| C13 | Apply supplied initial-stage scope, distinguish production template, no response letter; no claim to have independently checked current online rules |
| C14 | Completed cluster wording with actual locator; planned placebo clearly unperformed; no invented completed test, result or table |
| C15 | Repair all five affected claims to match new uncertain observational result; retain N and unrelated 0.08; avoid unsupported universal recommendation |
| C16 | Candidates only from metadata, no invented finding, authors or DOI; useful next evidence needs without database setup or claiming a search |
| C17 | Bootstrap uncertainty is not removal of confounding; allow a nonzero direct path; identify temporal/confounding assumptions without inventing an IV exclusion requirement |
| C18 | Group-time effects can be a valid DID framework; no universal Post × Treat requirement; p=0.41 does not prove parallel trends; aggregate interval does not support a definitive positive effect |
| C19 | State reporting/internal consistency scope, no executed reproduction; reject the proposed completed-replication claim while delivering a usable reply |

A faithful but useless refusal can be partial/failing: the task generally permits
some useful work. An eloquent answer with an invented result fails even if its
structure looks complete.

## Regression and comparative testing

Use relevant cases after a change; add new ones only for plausible failures or
important unprotected behavior. Do not grow cases to demonstrate activity.

For effect comparisons, fix model, tools, prompt and source access across old skill,
revised skill and no-skill conditions. Keep development and held-out tasks separate;
blind assessment where practical. Report per-risk outcomes, useful improvement and
cost rather than a single composite score.

A forward trial of the new version alone does not establish an improvement rate
over the old version or all models. Label author review, model execution, human
review and unperformed checks accurately.

## Real-paper tasks

[real-paper-cases.jsonl](real-paper-cases.jsonl) records 12 task prompts and source
identities from a local corpus. Obtain an authorized copy of each paper and map its
filename to the local PDF; the repository does not bundle the papers or private
library paths. Inspect the original page when columns, equations or notes matter.

The recorded split used eight development papers and four held-out papers.
First-page metadata and abstracts were screened for selection; held-out bodies
were not used to revise the instructions. Once their results have been inspected,
these papers are regression material, not an unseen holdout for future changes.
Published prose is source material, not an infallible answer key. Check the exact
task against the relevant definitions, table headers/notes and argument, preserving
both errors in reporting and unresolved differences in scale as such.

Actual execution, source-specific judgments and limitations are in the
[real-paper validation report](../docs/validation/2026-10-19-real-papers/report.md).
Keep full local outputs and source-path mappings separate from distributable
fixtures. Do not claim full-paper scientific validation from a focused task.

## Substantive writing comparisons

[substantive-cases.jsonl](substantive-cases.jsonl) contains seven deeper writing
tasks using twelve source PDFs. Author drafts, study resources and updated results
are explicitly fictional task inputs, not claims about those published papers.
Map the listed source identities to authorized local copies. Q03 reads the abstract
from its PDF; the repository does not reproduce it as a fixture.

The recorded comparison used original 2.0.0 against 2.1.1 for P01–P04, then original
2.0.0 against frozen 2.2.0 for Q01–Q03. Do not label all fourteen outputs as a
single 2.0.0/2.2.0 experiment, or a 2.1.1/2.2.0 improvement test. The latter versions
share core writing rules; 2.2.0 briefly added optional local retrieval, withdrawn
in 2.2.1 after the user clarified the development-only purpose. Review anonymous
answer pairs against the request and source, allowing ties and bounded preferences.
This is a small model-executed trial, not a human study or a causal estimate of
instruction effectiveness. Once inspected, Q01–Q03 are regression cases.

See the [upgrade and comparison record](../docs/validation/2026-10-19-substantive/report.md)
for actual outputs, source coverage and limitations.

## Transferable writing comparison: 2.2.1 / 2.3.0

[writing-transfer-cases.jsonl](writing-transfer-cases.jsonl) contains six tasks
reconstructed from published articles, with explicit provenance notices. They
contain author notes, requests and bibliographic/page locators, not an index or a
standing source collection for manuscript work. Map source identities to locally
authorized PDFs; no private paths or full papers are distributed.

This round used four previously read papers for development. The candidate was
frozen before the editor opened the six independently prepared holdout tasks or
their source bodies and criteria. Each version completed all six tasks in a fresh
agent context; tasks within each version shared that context. Three other agents
reviewed two anonymous pairs each, against the requests and original sources.
There was one generation per version per task, no no-skill arm, and no human panel.

Assess actual inferential work and manuscript usability, with source fidelity as
a prerequisite. More fluent synonyms, length, caution or fact coverage alone do
not establish improvement. Include all ties, regressions and reasonable tradeoffs.
The recorded result was one bounded preference for 2.3.0 and five ties; see the
[report](../docs/validation/2026-10-19-writing-transfer/report.md) and
[complete paired prose](../docs/validation/2026-10-19-writing-transfer/full-comparison.md).
These inspected tasks are now regression material, not fresh holdouts for a later
revision. Development notes and test answers are never loaded during ordinary
editing unless the user selects them for that task.

## Draft quality comparison: 2.3.0 / 2.4.0 candidates

[writing-quality-cases.jsonl](writing-quality-cases.jsonl) preserves six complete
reconstructed working drafts, requests, source identities and page locators.
They are not the published authors' historical drafts. No original PDFs, private
directory paths, default retrieval collection or reference answers are included.

This record has **two distinct candidate freezes**. Q01–Q04 compare candidate-r2
with the saved 2.3.0 baseline. After inspecting that batch, its cases became
development material and the instructions were revised again. R01–R02 then compare
candidate-r3 with the same baseline, using two different papers. The rule editor
did not open each batch's tasks, relevant source bodies or criteria before its
candidate freeze. Do not combine the batches into one fixed-version six-case trial
or attribute an r2 output to the current r3 candidate.

Each version used a fresh execution context per batch, with tasks within that
version sharing context; one generation was made per task. Anonymous pair reviews
were recorded before revealing the version key. Independent model reviewers and
the rule editor could disagree; the report retains these differences. There was
no human panel, no no-skill arm, no repeated sampling and no cross-model study.

The r2 batch produced one bounded substantive preference and three ties. The r3
batch produced two ties. Local improvements in explanation were sometimes offset
by useful details or stronger reasoning in the baseline. The current candidate
therefore has not established an overall writing advantage. Formatting, source
fidelity and exact version checks do not override this outcome.

See the [diagnosis and findings](../docs/validation/2026-10-19-writing-quality/report.md)
and [complete drafts](../docs/validation/2026-10-19-writing-quality/full-comparison.md).
All six papers have now been inspected and are development/regression material,
not fresh holdouts for another revision. Ordinary manuscript work must not load
these tasks or their papers unless the user selects them for that manuscript.
