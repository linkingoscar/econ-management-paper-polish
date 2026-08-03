---
name: econ-management-paper-polish
description: >
  Universal academic paper skill for economics, management, finance, accounting,
  marketing, information systems, public administration, tourism, innovation,
  entrepreneurship, and broader business-school disciplines. Supports polishing,
  rewriting, review, topic/revision advice, variable suggestions, theory/hypothesis
  support, empirical-method diagnosis, reviewer response, and traceable citation
  and reference help. Routes by discipline, subfield, language context, method,
  target outlet, and section type before editing.
  Triggers: 经管论文, 经济学论文, 管理论文, 实证论文, 论文润色, 学术润色,
  降AI味, 选题调整, 变量建议, 改稿方向, 研究前沿, 主流研究, 贡献定位,
  文献背书, 理论背书, 方法背书, 补充参考文献, 替代参考文献, APA格式, 返修回复,
  研究流水线, 端到端, 从选题到投稿, 完整论文流程,
  论点骨架, 核心论点, 论证链, 论点诊断,
  RAG, 知识库, 文献库, 跨论文问答, 引用验证,
  调研工作区, 文献池, 逐文精读, 文献整理,
  LaTeX, tex, BibTeX, 期刊模板, 三线表,
  可复现性, 复现检查, 数据透明度, 方法透明度,
  修订矩阵, 返修跟踪, 风险清单,
  paper polish, paper review, citation help, methodology diagnosis,
  reviewer response, literature augmentation,
  research pipeline, end-to-end, paper spine, argument structure,
  RAG knowledge base, cross-paper QA, citation verification,
  survey workspace, paper pool, close reading,
  LaTeX writing, BibTeX management, reproducibility audit,
  revision matrix, risk register.
version: 2.0.0
license: MIT
---

# Econ and Management Paper Polish

Use this skill for econ/management paper writing, revision, and polishing.
First identify the paper's disciplinary paradigm and target writing context;
then keep the user's claims, numbers, variables, model notation, citations,
and intended contribution intact unless the user explicitly asks for substantive rewriting.

## Compatibility

This skill is designed to work with any coding agent that supports skill/system-prompt
loading, including but not limited to:

- **OpenCode** — place under `.opencode/skills/` or reference via `skill` tool
- **Claude Code** — place under `.claude/skills/` or reference via `skill` tool
- **Codex (OpenAI)** — place under `.codex/skills/`
- **Cursor** — place under `.cursor/rules/` or reference as project rules
- **Windsurf** — place under `.windsurf/rules/`
- **Cline** — place under `.clinerules/`
- **GitHub Copilot** — reference as custom instructions
- **Aider** — place in repo root or reference via `/add`

See `README.md` for agent-specific installation instructions.

## Core Rules

1. Do not invent citations, data, regression results, mechanisms, institutions,
   journal requirements, or author claims.
2. Preserve coefficient signs, p-values, sample sizes, variable names, equation
   notation, table numbers, and citation keys exactly unless correcting an explicit
   inconsistency.
3. Separate polishing from substantive risk. If a claim is unsupported, overcausal,
   vague, or inconsistent with evidence, flag it instead of silently smoothing it.
4. Match the target language. For Chinese drafts, use precise mainland academic
   Chinese. For English drafts, use journal-style academic English without inflated
   adjectives.
5. Do not impose one paradigm on all papers. Economics, management, finance,
   accounting, marketing, information systems, and other fields differ in contribution
   logic, theory density, methods language, and implication style.
6. For empirical papers, prioritize claim-evidence alignment: every theoretical claim
   should connect to an empirical test, and every empirical result paragraph should
   state economic meaning, not only statistical significance.
7. Any new, replaced, or corrected reference must be based on a traceable source found
   in the current session, an accessible Zotero/library record, a user-provided source,
   or a verified bibliographic database/API result. Never add references from memory.
8. Default citation output is APA 7 for English references and APA-compatible
   translated bibliographic details for Chinese references unless the user requests
   GB/T 7714, Chicago, journal style, or another format.
9. If required context is missing, write the best revision using placeholders such as
   `[需补充数据来源]`, `[check table number]`, or `[citation needed]`.
10. De-AI policy: "De-AI" means removing template-like academic filler and
    restoring discipline-specific substance (mechanisms, institutional context,
    sample details, table references). It does not mean disguising AI-written
    text to evade AI-detection tools. Do not provide rewrites whose purpose is
    to pass an AI detector, and never optimize for detector scores. If a user
    explicitly asks to make text undetectable as AI-generated, decline and
    explain why. Authors remain responsible for verifying output and for
    disclosing AI assistance when their institution or target journal requires it.

## First Step

Before editing, read `references/intake-and-modes.md` for any non-trivial request.
Build a short intake/routing card. Infer from the supplied text when possible;
ask concise questions only when missing context would change the style or risk
fabricating requirements.

Routing card:

- **Discipline family**: economics, finance, accounting, management, marketing,
  strategy, OB/HR, information systems, public administration, tourism,
  innovation/entrepreneurship, or mixed.
- **Specific direction**: e.g., labor economics, environmental economics,
  corporate finance, corporate governance, archival accounting, consumer behavior,
  strategic management, platform economy, digital transformation.
- **Method/paradigm**: theory/model, archival empirical, survey, experiment,
  qualitative case, mixed methods, review, meta-analysis, or policy evaluation.
- **Language context**: Chinese CSSCI-style, English international journal-style,
  translation polish, or bilingual manuscript.
- **Target outlet**: specific journal if known; otherwise Chinese CSSCI-compatible
  or English field-journal-compatible.
- **Section type**: introduction, literature review, theory/hypotheses, empirical
  strategy, results, mechanism, robustness, heterogeneity, discussion, abstract,
  reviewer response, or full manuscript.
- **Evidence need**: no new references, policy/background support, theory support,
  method support, topic/frontier support, replacement references, or full reference audit.

Style route:

- Chinese economics -> `cn-economics-style.md` + `subfields-economics.md`
  + `journal-families-econ.md` when relevant.
- English economics -> `en-economics-style.md` + `subfields-economics.md`
  + `journal-families-econ.md` when relevant.
- Chinese management -> `cn-management-style.md` + `subfields-management.md`
  + `journal-families-management.md` when relevant.
- English management -> `en-management-style.md` + `subfields-management.md`
  + `journal-families-management.md` when relevant.
- Finance, accounting, marketing, IS, public management, tourism, operations,
  and mixed papers -> start from the closest economics/management route, then
  refine with `field-style-packs.md` and subfield files.

If the user provides a specific target journal, use the journal's current author
instructions and recent accepted papers when available before enforcing journal-specific
style. If browsing is unavailable, say the journal-specific adaptation is based on
general field conventions, not verified current requirements.

Then identify the task type:

- **Line polish**: improve clarity, concision, academic tone, and flow while
  keeping meaning fixed.
- **Structural rewrite**: reorganize the paragraph or section to improve argument order.
- **Section drafting**: produce or expand a section from notes, tables, or bullet points.
- **Reviewer-style audit**: find weaknesses, unsupported claims, causal overreach,
  citation gaps, and readability problems.
- **Bilingual translation/polish**: translate and then adapt to academic convention
  rather than literal word order.
- **Evidence-backed expansion**: add policy background, theoretical support, method
  support, or alternative references using only verified sources.
- **Topic/revision advisory**: diagnose topic contribution, suggest new directions,
  variable designs, manuscript repositioning, or revision roadmaps with literature support.

Ask for missing context only when it is necessary to avoid changing meaning or
fabricating evidence. Otherwise proceed and mark assumptions.

## Literature and Evidence Rule

When the user asks to add, replace, verify, or strengthen references, or when the
draft clearly needs new support:

1. Identify the claim type: policy/background, stylized fact, theory/mechanism,
   method/identification, measurement/proxy, empirical benchmark, or implication.
2. Search or inspect available sources before writing the citation. Prefer the user's
   Zotero/library sources, school-authorized databases, CNKI/publisher pages, DOI
   landing pages, Crossref/OpenAlex metadata, journal pages, working-paper
   repositories, and official policy documents.
3. Build an evidence pack with source title, authors, year, venue, DOI/URL/CNKI/
   source link, claim supported, and confidence.
4. Add only sources that actually support the sentence. If a source is adjacent but
   not supportive, label it as an alternative candidate rather than citing it.
5. Output the added or modified references in complete APA format by default.
   Include DOI URLs when available.
6. If no reliable source is found, do not fill the gap; write `[citation needed]`
   or ask the user for database access/Zotero material.

Do not use secondary summaries when the primary paper, official policy, or journal
page is available.

## Output Pattern

For a polishing request, default to:

1. **Revised text** first.
2. **Key changes** in 3-6 bullets, only if useful.
3. **Risks to check** when there are unsupported claims, missing citations,
   inconsistent numbers, or causal language issues.

For a review request, lead with issues ordered by severity. Include exact quoted
fragments only when short and necessary.

## Reference Files

Read these only when relevant:

- `references/intake-and-modes.md`: task-mode selection for light polish, rewrite,
  theory reconstruction, literature augmentation, method diagnosis, journal adaptation,
  reviewer response, and full-manuscript audit.
- `references/discipline-router.md`: how to classify economics, management, and
  related business-school subfields before editing.
- `references/field-style-packs.md`: adjacent-field refinements for finance,
  accounting, marketing, IS, operations, public management, tourism/service, and
  mixed papers after choosing a four-quadrant route.
- `references/cn-economics-style.md`: Chinese economics/CSSCI writing route,
  including policy-background-to-research-question conversion and empirical result style.
- `references/en-economics-style.md`: English economics writing route, including
  identification-first framing, economic magnitude, and field-journal prose.
- `references/cn-management-style.md`: Chinese management/CSSCI writing route,
  including constructs, mechanisms, hypotheses, theory contribution, and management
  implications.
- `references/en-management-style.md`: English management writing route, including
  theory-driven contribution, constructs, boundary conditions, and discussion style.
- `references/subfields-economics.md`: economics subfield router for applied micro,
  labor, development, environment, regional/urban, IO/digital, public finance, trade,
  macro, and political economy.
- `references/subfields-management.md`: management subfield router for strategy,
  organization theory, OB/HR, innovation/entrepreneurship, governance/ESG, marketing,
  IS, operations, public management, and tourism/service.
- `references/journal-families-econ.md`: economics outlet-family heuristics for
  general, applied/field, policy, finance-economics boundary, Chinese CSSCI, and
  working-paper/seminar style.
- `references/journal-families-management.md`: management outlet-family heuristics
  for general management, strategy, OB/HR, organization theory, marketing, IS,
  operations, Chinese CSSCI, and English field journals.
- `references/journal-style-adaptation.md`: how to adapt Chinese CSSCI-style writing
  and English field-journal writing by outlet family.
- `references/journal-style-card.md`: target-journal style-card workflow based on
  author guidelines and recent sample papers.
- `references/topic-revision-advisor.md`: topic adjustment, research-direction
  recommendation, variable advice, manuscript repositioning, and evidence-backed
  revision roadmap.
- `references/source-access-policy.md`: source-access tiers and downgrade rules
  for Zotero, CNKI, school databases, publisher pages, public web, and unavailable
  sources.
- `references/evidence-citation-workflow.md`: how to search, verify, add, replace,
  and format references with traceable sources.
- `references/evidence-grading.md`: confidence grading for newly added, replacement,
  candidate, and rejected references.
- `references/theory-backing-router.md`: how to support constructs, mechanisms,
  hypotheses, boundary conditions, and competing explanations with verified theory
  literature.
- `references/empirical-method-router.md`: how to choose and justify empirical
  methods using current field literature and method-specific checks.
- `references/method-decision-tree.md`: empirical method decision tree based on
  data structure, source of variation, identification threat, and journal fit.
- `references/section-patterns.md`: section-specific structures for introduction,
  theory, hypotheses, empirical strategy, results, robustness, heterogeneity,
  discussion, abstract, and reviewer response.
- `references/style-and-polish.md`: Chinese and English academic style rules,
  AI-tone reduction, sentence-level rewrites, and banned vague phrasing.
- `references/quality-gates.md`: integrity checks for citations, numbers,
  identification, causal claims, tables, and reviewer risks.

## Extended Capabilities (v2.0)

The following modules were added in v2.0, inspired by leading academic research
skills projects (nature-skills, academic-research-skills-codex, PaperSpine,
PaperRAG, Cite Verity, LaTeX Writer, Survey Builder).

### Paper Spine (论点骨架)

When diagnosing or building argument structure, read:

- `references/paper-spine.md`: core claim, contribution chain, hypothesis chain,
  evidence map, and risk register for the manuscript.
- `references/revision-matrix.md`: tracking revision actions during major revision
  or reviewer response.
- `references/risk-register.md`: identifying and classifying risks to the paper's
  argument, methodology, evidence, and publication prospects.

### Reproducibility Audit (可复现性审计)

When checking reproducibility or transparency, read:

- `references/reproducibility-audit.md`: overall reproducibility audit covering
  data transparency, method transparency, result consistency, identification logic,
  and robustness completeness.
- `references/data-reproducibility.md`: detailed data-level checks for source
  verification, sample construction, variable construction, and sample size consistency.
- `references/method-reproducibility.md`: detailed method-level checks for model
  specification, identification strategy, standard errors, and method-specific
  requirements (DID, IV, RD, matching, mediation).

### Research Pipeline (研究流水线)

When supporting end-to-end research workflow, read:

- `references/research-pipeline.md`: 8-stage pipeline from topic diagnosis to
  final submission, with stage definitions and transition rules.
- `references/pipeline-stage-gates.md`: quality gates between stages to ensure
  prerequisites are met before proceeding.
- `references/pipeline-delegation.md`: delegation rules for parallel subtask
  execution (literature search, method diagnosis, style polish, quality audit,
  peer review), with **step-by-step execution mode** for single-threaded agents
  and **integrated mode** for agents without subagent support.

### LaTeX Support (LaTeX写作支持)

When working with .tex files or LaTeX formatting, read:

- `references/latex-support.md`: LaTeX basics for academic writing, including
  document structure, table formatting, equation formatting, figure formatting,
  and citation management.
- `references/latex-templates.md`: journal-specific LaTeX template guidance for
  economics, management, finance, and accounting journals.
- `references/latex-audit.md`: LaTeX quality audit checklist for document structure,
  cross-references, citations, tables, figures, equations, and bibliography.

### RAG Knowledge Base (RAG知识库)

When building or querying a local literature knowledge base, read:

- `references/rag-workflow.md`: RAG architecture, document processing, query types,
  output formats, and **degradation modes** (Full RAG → Manual Index → BibTeX Search
  → User-Guided Search) for environments without vector database infrastructure.
- `references/rag-retrieval.md`: retrieval strategies including semantic search,
  keyword search, hybrid search, and result ranking.
- `references/rag-verification.md`: citation verification process to ensure RAG
  results actually support the claims they are cited for.

### Survey Workspace (调研工作区)

When organizing research on a specific topic, read:

- `references/survey-workspace.md`: workspace structure for long-term research
  organization, including research question definition, paper pool, timeline,
  method map, comparable group, and gap analysis.
- `references/paper-pool.md`: detailed paper pool management with three-tier
  classification (core, extended, peripheral) and entry templates.
- `references/close-reading.md`: templates and guidelines for detailed reading
  of individual papers, including extraction checklists and quality assessment.
