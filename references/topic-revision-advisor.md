# Topic And Revision Advisor

Use this when the user asks for 选题调整, 新方向, 变量建议, 改稿方向, 创新性不足, 文章没意思, 投稿前重构, 研究前沿, 主流研究, 贡献定位, or whether a manuscript can be repositioned.

## Non-Negotiable Rules

1. Treat topic and variable suggestions as scholarly options, not guaranteed publication strategies.
2. Do not claim a direction is "mainstream", "frontier", "hot", or "highly promising" without current-session evidence from literature, target journals, calls for papers, review articles, recent top/field papers, or the user's Zotero/library material.
3. Do not recommend variables or methods that the user's data cannot plausibly support. If data feasibility is unknown, mark it as a condition.
4. Any supporting reference must follow `evidence-citation-workflow.md` and `evidence-grading.md`.
5. Separate conservative revision paths from ambitious topic pivots.

## Intake

Ask or infer:

- Current title/topic.
- Core research question.
- Discipline route and quadrant route.
- Current independent variable, dependent variable, mediator, moderator, controls, and sample/data source.
- Current method and identification strategy.
- Target journal or journal family.
- User's goal: rescue current paper, improve novelty, change variables, target CSSCI/SSCI, build a new paper, or prepare a revise-and-resubmit.
- Constraints: available data, time, software, sample period, language, and whether new data collection is possible.

If the user provides only a rough idea, ask for title/abstract and available data. If the user wants brainstorming, proceed with explicit assumptions.

## Diagnose The Current Manuscript

Classify the current paper's main weakness:

- **Weak contribution**: the research question is common and the marginal contribution is unclear.
- **Weak theory**: constructs, mechanism, boundary condition, or hypothesis logic are thin.
- **Weak variable design**: focal variable, outcome, mediator, or moderator does not match the theoretical claim.
- **Weak identification**: method cannot support causal language or reviewer expectations.
- **Weak measurement**: proxy validity is questionable.
- **Weak literature positioning**: the paper is not connected to the right literature stream.
- **Weak target fit**: the manuscript's style and contribution do not fit the target outlet.
- **Overextended implications**: policy/management implications exceed evidence.

Do not jump to new directions before diagnosing the old one.

## Search And Frontier Scan

When the user wants mainstream/frontier directions or literature-supported topic advice, first read `source-access-policy.md`, then perform a targeted scan:

1. Use the routed discipline and subfield to form search queries.
2. Search or inspect at least two channels when possible: Zotero/library materials, CNKI/CSSCI, Web of Science/Scopus, Google Scholar, OpenAlex/Crossref, publisher pages, recent target-journal issues, review articles, special issues, calls for papers, NBER/CEPR/SSRN/RePEc for economics/finance.
3. Separate **mainstream** from **frontier**:
   - Mainstream: established literature stream with repeated use in field journals or reviews.
   - Frontier: recent emerging direction, new data/method, special issue/call, recent target-journal cluster, or active debate.
4. Build an evidence pack with grades before recommending.
5. Avoid using search-result snippets as decisive support for a theory or method claim.

If browsing, Zotero, CNKI, or database access is unavailable, use only user-provided materials and public/metadata sources. Label the result as a "public-source preliminary scan" or "candidate-only advice" rather than a complete field scan.

## Direction Types

### Contribution Reframing

Keep variables and data mostly unchanged, but reposition the paper:

- New literature stream.
- Stronger mechanism.
- More precise contribution.
- Different target outlet.
- Better policy/management implication.

Best when data are fixed and results are usable.

### Topic Pivot

Change the focal question while reusing part of the data or setting:

- New outcome.
- New explanatory variable.
- New policy/event angle.
- New mechanism.
- New unit of analysis.

Best when the current contribution is weak but the data/setting is valuable.

### Variable Redesign

Suggest or revise:

- Independent variable.
- Dependent variable.
- Mediator/mechanism variable.
- Moderator/boundary condition.
- Control variables.
- Alternative proxies.
- Heterogeneity dimensions.

Each variable suggestion must include role, theoretical reason, data source/proxy, timing, endogeneity risk, and literature support.

### Method Or Identification Upgrade

Use only when data support it:

- Improve fixed effects, clustering, controls, or dynamic tests.
- Add event study, DID, IV, RD, SCM, matching/weighting, sensitivity analysis, mediation, causal ML, or text/ML validation.
- Reframe causal claims as associative if design cannot support causality.

Pair with `method-decision-tree.md`.

### Literature Repositioning

Move the paper from a generic topic to a precise literature conversation:

- Economics: policy effect, mechanism, welfare, market response, institutional variation.
- Management: construct, theory, mechanism, boundary condition.
- Finance/accounting: market participant, information, incentives, governance, disclosure, risk.
- Marketing/IS: consumer/firm/platform/technology mechanism.

### Target-Journal Repositioning

If the target is unrealistic, suggest a better outlet family or a staged strategy:

- Current paper salvage for Chinese CSSCI.
- Reframe for English field journal.
- Build a new paper for higher-tier outlet.
- Split one overbroad paper into two focused papers.

Use `journal-style-card.md` for a named journal.

## Variable Suggestion Protocol

For each proposed variable, provide:

| Variable role | Candidate variable | Why it fits | Data/proxy | Timing/order | Literature support | Risk |
| --- | --- | --- | --- | --- | --- | --- |

Check:

- The variable maps to the theory or research question.
- Data are plausibly available.
- Temporal order supports interpretation.
- It is not a bad control or post-treatment control.
- Measurement has precedent or can be validated.
- Endogeneity risk is stated.

Do not recommend fashionable variables such as AI, ESG, digital transformation, green innovation, or attention unless they fit the mechanism and data.

## Direction Scoring

Score each direction qualitatively:

- **Novelty**: low/medium/high.
- **Theory fit**: weak/moderate/strong.
- **Data feasibility**: low/medium/high.
- **Identification credibility**: low/medium/high.
- **Literature support**: Grade A/B/C/D by `evidence-grading.md`.
- **Target fit**: weak/moderate/strong.
- **Revision cost**: low/medium/high.

Recommended paths should usually balance novelty and feasibility. High novelty with low data feasibility should be labeled as a new-paper idea rather than a revision path.

## Output Templates

### Topic/Direction Advice

```text
Current-paper diagnosis
- Current contribution:
- Main weakness:
- Salvage potential:
- Key constraints:

Direction options
| Option | Core idea | What changes | Why promising | Evidence | Feasibility | Risk |

Recommended path
- Best conservative revision:
- Best ambitious pivot:
- What to keep:
- What to drop:
- What to collect/check:

Literature support
- Evidence pack with grades.
- APA references.
```

### Variable Advice

```text
Variable diagnosis
- Current IV/DV/mechanism/moderator issue:
- Theoretical mismatch:
- Data/measurement risk:

Variable suggestions
| Role | Candidate | Theory link | Data/proxy | Expected sign or relation | Evidence grade | Risk |

Do-not-use variables
- Variable:
- Reason:
```

### Rewrite Plan

```text
Revision roadmap
1. Reposition the research question.
2. Rebuild theory/mechanism.
3. Adjust variable design.
4. Revise empirical strategy and robustness.
5. Update literature support.
6. Rewrite introduction and contribution.
7. Check target-journal fit.
```

## Reviewer Risk Lens

For each proposed direction, anticipate reviewer questions:

- Is this a real contribution or only a new context?
- Does the variable measure the construct?
- Can the method identify the claimed effect?
- Are the added references central or decorative?
- Does the target journal care about this question?
- Are implications too broad for the evidence?
