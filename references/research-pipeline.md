# Research Pipeline (研究流水线)

Use this file when the user asks for end-to-end research workflow support, from topic selection to final submission. The pipeline organizes the research process into stages with clear gates and handoffs.

## When To Use

- User asks "帮我从选题到投稿走一遍完整流程"
- User asks to organize a research project systematically.
- User provides a topic and wants structured guidance.
- User asks "我现在处于哪个阶段？下一步该做什么？"

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    研究流水线 (Research Pipeline)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: 选题诊断                                              │
│  ├── 研究问题提炼                                               │
│  ├── 文献缺口识别                                               │
│  └── 贡献定位                                                   │
│      ↓                                                         │
│  Stage 2: 文献综述                                              │
│  ├── 文献检索策略                                               │
│  ├── 主题聚类                                                   │
│  └── 综述写作                                                   │
│      ↓                                                         │
│  Stage 3: 理论构建                                              │
│  ├── 理论框架选择                                               │
│  ├── 机制推导                                                   │
│  └── 假说提出                                                   │
│      ↓                                                         │
│  Stage 4: 研究设计                                              │
│  ├── 数据获取                                                   │
│  ├── 变量构造                                                   │
│  └── 识别策略                                                   │
│      ↓                                                         │
│  Stage 5: 写作执行                                              │
│  ├── 论点骨架构建                                               │
│  ├── 分节写作                                                   │
│  └── 整合润色                                                   │
│      ↓                                                         │
│  Stage 6: 自审自查                                              │
│  ├── 质量门控检查                                               │
│  ├── 可复现性审计                                               │
│  └── 风险清单更新                                               │
│      ↓                                                         │
│  Stage 7: 同行模拟审稿                                          │
│  ├── 审稿人视角审查                                             │
│  ├── 修改建议                                                   │
│  └── 返修路线图                                                 │
│      ↓                                                         │
│  Stage 8: 迭代完善                                              │
│  ├── 修订矩阵跟踪                                               │
│  ├── Response Letter                                            │
│  └── 最终检查                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Stage Definitions

### Stage 1: Topic Diagnosis (选题诊断)

**Goal**: Refine the research question and identify the contribution.

**Inputs**:
- User's initial topic or idea
- Target journal or field
- Available data (if any)

**Activities**:
1. Clarify the research question
2. Search for existing literature
3. Identify the gap (empirical, theoretical, methodological)
4. Position the contribution
5. Assess feasibility

**Outputs**:
- Refined research question
- Literature gap statement
- Preliminary contribution claim
- Feasibility assessment

**Gate**: Can the question be answered with available data and methods?

**Reference files**: `topic-revision-advisor.md`, `evidence-citation-workflow.md`

### Stage 2: Literature Review (文献综述)

**Goal**: Map the literature landscape and write a positioning review.

**Inputs**:
- Research question
- Key constructs and keywords

**Activities**:
1. Design search strategy
2. Collect and organize papers
3. Cluster into themes
4. Identify seminal and frontier work
5. Write thematic review

**Outputs**:
- Organized literature database
- Thematic literature review
- Clear positioning statement

**Gate**: Is the review comprehensive enough to justify the gap?

**Reference files**: `evidence-citation-workflow.md`, `section-patterns.md`

### Stage 3: Theory Building (理论构建)

**Goal**: Develop theoretical framework and derive hypotheses.

**Inputs**:
- Literature review findings
- Research question
- Institutional context

**Activities**:
1. Select theoretical lens
2. Derive mechanisms
3. Identify boundary conditions
4. State hypotheses
5. Consider competing explanations

**Outputs**:
- Theoretical framework
- Mechanism diagram (conceptual)
- Testable hypotheses

**Gate**: Does each hypothesis follow from a stated mechanism?

**Reference files**: `theory-backing-router.md`, `section-patterns.md`

### Stage 4: Research Design (研究设计)

**Goal**: Design the empirical strategy to test hypotheses.

**Inputs**:
- Hypotheses
- Available data
- Identification concerns

**Activities**:
1. Specify data sources
2. Define variables
3. Choose identification strategy
4. Plan robustness checks
5. Anticipate reviewer concerns

**Outputs**:
- Data description
- Variable definitions
- Model specification
- Robustness plan

**Gate**: Is the identification strategy credible for the research question?

**Reference files**: `empirical-method-router.md`, `method-decision-tree.md`

### Stage 5: Writing Execution (写作执行)

**Goal**: Write the complete manuscript.

**Inputs**:
- All previous stage outputs
- Target journal style

**Activities**:
1. Build paper spine
2. Write each section
3. Integrate tables and figures
4. Polish prose
5. Format references

**Outputs**:
- Complete draft
- All tables and figures
- Formatted references

**Gate**: Does the draft follow the paper spine consistently?

**Reference files**: `paper-spine.md`, `section-patterns.md`, `style-and-polish.md`

### Stage 6: Self-Review (自审自查)

**Goal**: Internal quality check before external review.

**Inputs**:
- Complete draft

**Activities**:
1. Run quality gates
2. Check reproducibility
3. Update risk register
4. Verify all numbers
5. Check citation completeness

**Outputs**:
- Quality gate report
- Reproducibility audit
- Updated risk register
- List of issues to fix

**Gate**: Are all critical issues identified and prioritized?

**Reference files**: `quality-gates.md`, `reproducibility-audit.md`, `risk-register.md`

### Stage 7: Simulated Peer Review (同行模拟审稿)

**Goal**: Simulate reviewer feedback to anticipate real reviews.

**Inputs**:
- Self-reviewed draft
- Target journal

**Activities**:
1. Review from economist perspective
2. Review from management perspective
3. Review from methods perspective
4. Prioritize issues
5. Create revision roadmap

**Outputs**:
- Simulated review report
- Prioritized issue list
- Revision roadmap

**Gate**: Are the most likely reviewer concerns identified?

**Reference files**: `quality-gates.md`, `risk-register.md`

### Stage 8: Iteration (迭代完善)

**Goal**: Revise based on feedback and prepare for submission.

**Inputs**:
- Simulated review feedback
- Actual reviewer comments (if R&R)

**Activities**:
1. Build revision matrix
2. Execute revisions
3. Write response letter
4. Final quality check
5. Format for submission

**Outputs**:
- Revised manuscript
- Response letter
- Revision matrix
- Submission-ready files

**Gate**: Have all critical issues been addressed?

**Reference files**: `revision-matrix.md`, `section-patterns.md`

## Stage Transitions

Users can enter the pipeline at any stage. The skill should:

1. **Diagnose current stage** based on what the user provides.
2. **Check prerequisites** from earlier stages.
3. **Recommend missing steps** if earlier stages are incomplete.
4. **Proceed** if the user wants to focus on the current stage.

Example:
```
User: 帮我写这篇论文的引言
Skill: [Diagnoses: Stage 5, but Stage 1-3 may be incomplete]
       我可以帮你写引言。首先让我确认几个问题：
       1. 研究问题是否已经明确？
       2. 文献综述是否已完成？
       3. 理论框架和假说是否确定？
       如果这些都已就绪，我将按照论点骨架来构建引言。
```

## Pipeline State Tracking

When working through the pipeline, maintain a state card:

```markdown
## 流水线状态

| 阶段 | 状态 | 关键输出 | 备注 |
|------|------|---------|------|
| 选题诊断 | ✅ 完成 | RQ + 贡献定位 | — |
| 文献综述 | 🔄 进行中 | 部分完成 | 需补充2020年后文献 |
| 理论构建 | ⏳ 待开始 | — | — |
| 研究设计 | ⏳ 待开始 | — | — |
| 写作执行 | ⏳ 待开始 | — | — |
| 自审自查 | ⏳ 待开始 | — | — |
| 模拟审稿 | ⏳ 待开始 | — | — |
| 迭代完善 | ⏳ 待开始 | — | — |
```

## Integration With Other Modules

- **intake-and-modes.md**: Task mode selection maps to pipeline stages.
- **paper-spine.md**: Built in Stage 5, used throughout.
- **quality-gates.md**: Used in Stage 6.
- **reproducibility-audit.md**: Used in Stage 6.
- **revision-matrix.md**: Used in Stage 8.
- **risk-register.md**: Updated throughout.
