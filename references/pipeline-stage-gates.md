# Pipeline Stage Gates (流水线阶段门控)

Use this file to define quality gates between pipeline stages. Each gate ensures prerequisites are met before proceeding.

## Gate Philosophy

- Gates prevent premature progression (e.g., writing before research design).
- Gates do not block; they warn and recommend.
- Users can override gates with explicit acknowledgment.
- Gates check minimum quality, not perfection.

## Gate Definitions

### Gate 1: Topic → Literature Review

**Prerequisites**: Stage 1 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Research question stated | Yes | Question is specific and answerable |
| Literature gap identified | Yes | Gap is meaningful, not trivial |
| Contribution positioned | Yes | Contribution is literature-linked |
| Feasibility assessed | Recommended | Data and methods are plausible |

**If failed**: Return to Stage 1 with specific diagnosis.

**Pass message**: "选题诊断完成，可以进入文献综述阶段。"

### Gate 2: Literature Review → Theory Building

**Prerequisites**: Stage 2 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Key themes identified | Yes | 2-4 literature streams mapped |
| Seminal work cited | Yes | Core references included |
| Gap justified | Yes | Gap is supported by literature |
| Positioning clear | Yes | "This paper differs by..." stated |

**If failed**: Return to Stage 2 with search recommendations.

**Pass message**: "文献综述完成，可以进入理论构建阶段。"

### Gate 3: Theory Building → Research Design

**Prerequisites**: Stage 3 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Theoretical lens chosen | Yes | Theory is named and applicable |
| Mechanism derived | Yes | Channel from X to Y is clear |
| Hypotheses stated | Yes | Each H is testable and directional |
| Boundary conditions | Recommended | Scope conditions identified |

**If failed**: Return to Stage 3 with theory recommendations.

**Pass message**: "理论框架构建完成，可以进入研究设计阶段。"

### Gate 4: Research Design → Writing Execution

**Prerequisites**: Stage 4 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Data source specified | Yes | Source is accessible and appropriate |
| Variables defined | Yes | DV, IV, controls are clear |
| Model specified | Yes | Equation is complete |
| Identification strategy | Yes | Strategy is credible |
| Robustness plan | Recommended | Key checks planned |

**If failed**: Return to Stage 4 with design recommendations.

**Pass message**: "研究设计完成，可以开始写作。"

### Gate 5: Writing Execution → Self-Review

**Prerequisites**: Stage 5 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| All sections drafted | Yes | Every required section exists |
| Paper spine followed | Yes | Argument is coherent |
| Tables integrated | Yes | All tables referenced in text |
| References formatted | Yes | Consistent style applied |

**If failed**: Return to Stage 5 with specific section feedback.

**Pass message**: "初稿完成，可以进入自审自查阶段。"

### Gate 6: Self-Review → Simulated Peer Review

**Prerequisites**: Stage 6 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Quality gates passed | Yes | No critical failures |
| Numbers verified | Yes | Text-table consistency |
| Citations complete | Yes | No [citation needed] remaining |
| Risk register updated | Yes | All identified risks listed |

**If failed**: Return to Stage 6 with specific issues.

**Pass message**: "自审完成，可以进行模拟同行审稿。"

### Gate 7: Simulated Peer Review → Iteration

**Prerequisites**: Stage 7 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| Review report complete | Yes | All sections reviewed |
| Issues prioritized | Yes | Critical/major/minor classified |
| Revision roadmap | Yes | Actionable plan exists |

**If failed**: Return to Stage 7 for more thorough review.

**Pass message**: "模拟审稿完成，可以开始迭代修改。"

### Gate 8: Iteration → Submission

**Prerequisites**: Stage 8 outputs

| Check | Required | Pass Condition |
|-------|----------|----------------|
| All critical issues fixed | Yes | No 🔴 risks remaining |
| Response letter ready | Yes | All reviewer concerns addressed |
| Format compliance | Yes | Matches target journal |
| Final consistency check | Yes | No internal contradictions |

**If failed**: Return to Stage 8 with specific issues.

**Pass message**: "论文已准备好投稿。"

## Gate Output Format

When running a gate check, output:

```markdown
## 阶段门控检查: [Stage X → Stage Y]

### 检查结果
- ✅ 通过: [N] 项
- ⚠️ 警告: [N] 项
- ❌ 未通过: [N] 项

### 详细检查
| 检查项 | 状态 | 详情 |
|--------|------|------|
| [Check 1] | ✅ | [Brief note] |
| [Check 2] | ⚠️ | [Issue description] |
| [Check 3] | ❌ | [Issue and recommendation] |

### 结论
[Pass/Fail decision with recommendation]

### 下一步
[If passed: proceed to Stage Y]
[If failed: specific actions to take]
```

## Override Rules

Users can override gates by:
1. Explicitly stating "跳过这个检查" or "我确认可以继续"
2. Acknowledging the risk in writing
3. Accepting responsibility for the gap

When overriding:
- Record the override in the pipeline state.
- Note the risk for later stages.
- Do not block the user.

## Integration With Other Modules

- **research-pipeline.md**: Defines the stages that gates connect.
- **quality-gates.md**: Provides detailed checks used by pipeline gates.
- **reproducibility-audit.md**: Provides data and method checks.
- **paper-spine.md**: Provides argument structure checks.
- **risk-register.md**: Tracks risks identified at gates.
