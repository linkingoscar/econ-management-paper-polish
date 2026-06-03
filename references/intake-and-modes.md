# Intake And Modes

Use this file before any substantial editing. The goal is to choose the right intervention depth and avoid over-editing or under-editing.

## Intake Card

Build a compact intake card before working:

- **Task mode**: light polish, peer-style rewrite, structural rewrite, theory reconstruction, literature/evidence augmentation, topic/revision advisory, empirical-method diagnosis, journal adaptation, reviewer response, full-manuscript audit.
- **Preservation level**: preserve meaning only, preserve sentence order, preserve terminology and variables, preserve citations and all quantitative claims, or allow substantive restructuring.
- **Discipline route**: use `discipline-router.md`.
- **Language route**: Chinese CSSCI, Chinese non-CSSCI, English field journal, translation polish, bilingual.
- **Quadrant route**: Chinese economics, English economics, Chinese management, English management, or mixed/adjacent.
- **Target outlet**: specific journal, journal family, tier, or unspecified.
- **Evidence need**: none, flag only, add verified citations, replace weak citations, method support, policy support, topic/frontier support, full reference audit.
- **Output need**: revised text only, revised text plus notes, evidence pack, method diagnosis, or reviewer-risk list.

If the user gives an exact instruction that conflicts with the default workflow, follow the user's instruction unless it would require fabricating sources or changing data.

## Quadrant Selection

After intake, choose one of four primary writing routes:

- **Chinese economics**: use `cn-economics-style.md`, then `subfields-economics.md`.
- **English economics**: use `en-economics-style.md`, then `subfields-economics.md`.
- **Chinese management**: use `cn-management-style.md`, then `subfields-management.md`.
- **English management**: use `en-management-style.md`, then `subfields-management.md`.

If the paper is finance/accounting/marketing/IS/operations/public management/tourism:

- Choose the closest economics or management route by target outlet and argument logic.
- Add the relevant pack from `field-style-packs.md`.
- If the target journal is named, use `journal-style-card.md`.

If the manuscript is bilingual or translated:

- Diagnose the source language structure first.
- Rewrite into the target language's scholarly convention instead of literal translation.

## Mode Selection

### Light Polish

Use when the user asks for 润色, 降AI味, grammar, clarity, or tone without asking to change structure.

Rules:

- Preserve argument order and claims.
- Do not add new references unless a claim is clearly unsupported and risky.
- Keep notes brief.

### Peer-Style Rewrite

Use when the user asks for 同行化, 学术化, 投稿级, 顶刊风格, or more professional expression.

Rules:

- Improve paragraph logic, conceptual precision, and disciplinary tone.
- Preserve empirical claims and citations unless the user allows substantive changes.
- Add reviewer-risk notes when theory, identification, or evidence is weak.

### Structural Rewrite

Use when the section has weak order, repetition, unclear contribution, or mixed arguments.

Rules:

- Reorder sentences and paragraphs.
- Mark removed or merged claims when meaning could change.
- Use section templates from `section-patterns.md`.

### Theory Reconstruction

Use when mechanisms, constructs, hypotheses, or contribution logic are weak.

Rules:

- Read `theory-backing-router.md`.
- Identify construct definitions, theoretical lens, mechanism, boundary condition, and competing explanation.
- Add citations only after verification.
- If the user's theory is not yet defensible, produce a theory diagnosis before drafting.

### Literature Or Evidence Augmentation

Use when the user asks to 补文献, 找背书, 替代参考文献, 加政策背景, or strengthen citations.

Rules:

- Read `evidence-citation-workflow.md` and `evidence-grading.md`.
- Do not write new citations before retrieval.
- Default output includes revised text, evidence pack, and APA references.

### Topic Or Revision Advisory

Use when the user asks for 选题调整, 新方向, 变量建议, 改稿方向, 创新性不足, 主流研究, 前沿方向, 贡献定位, or article repositioning.

Rules:

- Read `topic-revision-advisor.md`.
- Diagnose the current manuscript before recommending a new direction.
- If claiming a direction is mainstream/frontier, search or inspect current literature, target journal papers, calls/special issues, or user-provided Zotero/library materials.
- Score each suggestion by novelty, theory fit, data feasibility, identification credibility, literature support, target fit, and revision cost.
- Do not recommend variables or methods unsupported by the user's data constraints.

### Empirical-Method Diagnosis

Use when the user asks whether a method is suitable, wants method upgrades, robustness, endogeneity, or empirical strategy text.

Rules:

- Read `empirical-method-router.md` and `method-decision-tree.md`.
- Diagnose data, treatment, identifying variation, and threats before recommending methods.
- Do not suggest advanced methods unless data and design support them.

### Journal Adaptation

Use when the user names a journal, journal family, CSSCI, SSCI, FT50, UTD, or a target tier.

Rules:

- Read `journal-style-card.md`.
- If current journal requirements or sample papers matter, browse or use user-provided sample papers.
- If not verified, label adaptation as general field style.

### Reviewer Response

Use for 返修, 审稿意见, response letter, rebuttal, or revise-and-resubmit.

Rules:

- Separate reviewer concern, manuscript action, evidence added, and response wording.
- Never overclaim that a change fully solves a problem when it only mitigates it.
- Preserve a respectful, non-defensive tone.

### Full-Manuscript Audit

Use when the user provides a full draft or asks for overall review.

Rules:

- Check contribution, theory, identification, results, references, consistency, and target-journal fit.
- Prioritize fatal and major issues before prose.
- Produce an action plan rather than rewriting everything at once.

## Ask Or Proceed

Ask one concise question only when missing information changes the correct route:

- Target journal/family for style adaptation.
- Discipline/subfield when text is too ambiguous.
- Whether new references may be added.
- Whether meaning and structure can be changed.

Otherwise proceed and state assumptions in the intake card.
