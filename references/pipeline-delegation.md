# Pipeline Delegation (流水线子代理委派)

Use this file when the research pipeline needs to delegate subtasks to specialized agents or parallel workflows. This enables efficient handling of complex research tasks.

## When To Use

- User provides a full manuscript and wants comprehensive review.
- Pipeline stage requires multiple parallel activities.
- Task is complex enough to benefit from specialization.
- User asks to "全面审查" or "系统分析" the paper.

## Delegation Architecture

```
主代理 (Orchestrator)
├── 文献检索代理 (Literature Search Agent)
│   └── 任务: 检索、验证、格式化参考文献
├── 方法诊断代理 (Method Diagnosis Agent)
│   └── 任务: 评估实证策略、识别问题、建议改进
├── 风格润色代理 (Style Polish Agent)
│   └── 任务: 中英文润色、降AI味、学术化
├── 质量审计代理 (Quality Audit Agent)
│   └── 任务: 运行质量门控、可复现性检查
└── 同行模拟代理 (Peer Review Agent)
    └── 任务: 模拟审稿人视角、生成审稿报告
```

## Delegation Rules

### When to Delegate

| Scenario | Delegation Strategy |
|----------|---------------------|
| Full manuscript audit | Parallel: all agents |
| Literature augmentation | Single: literature agent |
| Method diagnosis | Single: method agent |
| Style polish | Single: style agent |
| Reviewer response | Sequential: audit → revision → response |
| End-to-end pipeline | Orchestrated: stage by stage |

### When NOT to Delegate

| Scenario | Reason |
|----------|--------|
| Simple line edit | Overhead exceeds benefit |
| Single citation check | Direct execution faster |
| Clarification question | No subtask needed |
| User specifies approach | Follow user's instruction |

## Subtask Specifications

### Literature Search Agent

**Input**: Research question, constructs, keywords, target field

**Task**:
1. Search for relevant papers using available sources.
2. Verify each paper's relevance and quality.
3. Organize by theme (theory, method, empirical, policy).
4. Format in APA 7.
5. Grade evidence quality.

**Output**:
```markdown
## 文献检索结果

### 核心文献 (Must Cite)
| # | 引用 | 主题 | 相关性 | 证据等级 |
|---|------|------|--------|---------|
| 1 | Author (Year) | [Topic] | 高 | A |

### 扩展文献 (Consider Citing)
...

### 边缘文献 (Optional)
...

### 检索策略
- 数据库: [List]
- 关键词: [List]
- 时间范围: [Period]
```

### Method Diagnosis Agent

**Input**: Manuscript text, tables, research question

**Task**:
1. Identify the empirical method used.
2. Check method appropriateness for the research question.
3. Evaluate identification strategy.
4. Assess robustness checks.
5. Suggest improvements.

**Output**:
```markdown
## 方法诊断报告

### 当前方法
- 方法: [OLS/FE/IV/DID/RD/...]
- 适用性: [适当/部分适当/不适当]

### 识别策略评估
- 策略: [描述]
- 可信度: [强/中/弱]
- 主要威胁: [List]

### 稳健性评估
- 已有检验: [List]
- 缺失检验: [List]
- 建议补充: [List]

### 改进建议
1. [Specific recommendation]
2. ...
```

### Style Polish Agent

**Input**: Manuscript text, target language, target journal

**Task**:
1. Identify style issues (AI-tone, vagueness, inconsistency).
2. Polish prose to journal standard.
3. Preserve meaning and claims.
4. Improve flow and readability.

**Output**:
```markdown
## 风格润色结果

### 问题类型统计
- AI味语句: [N] 处
- 模糊表述: [N] 处
- 逻辑不清: [N] 处
- 术语不一致: [N] 处

### 润色后文本
[Revised text]

### 主要修改
1. [Change 1 with reason]
2. ...

### 待确认项
1. [Item that needs user decision]
```

### Quality Audit Agent

**Input**: Complete manuscript

**Task**:
1. Run all quality gates.
2. Check reproducibility.
3. Update risk register.
4. Verify numbers and citations.

**Output**:
```markdown
## 质量审计报告

### 门控检查
| 门控 | 状态 | 关键问题 |
|------|------|---------|
| 范式适配 | ✅ | — |
| 期刊适配 | ⚠️ | 需补充XX |
| 主张-证据 | ❌ | 3处无支持 |
| ... | ... | ... |

### 可复现性
- 数据透明度: [⭐⭐⭐⭐⭐]
- 方法透明度: [⭐⭐⭐⭐⭐]
- 结果一致性: [通过/有疑问]

### 风险清单
| 风险 | 严重度 | 建议 |
|------|--------|------|
| ... | ... | ... |
```

### Peer Review Agent

**Input**: Complete manuscript, target journal

**Task**:
1. Review from target journal perspective.
2. Identify strengths and weaknesses.
3. Simulate likely reviewer comments.
4. Prioritize issues by severity.

**Output**:
```markdown
## 模拟审稿报告

### 总体评价
[2-3 sentence summary]

### 优点
1. [Strength 1]
2. [Strength 2]

### 主要问题
1. **[Issue 1]**: [Description] → [Suggestion]
2. **[Issue 2]**: [Description] → [Suggestion]

### 次要问题
1. [Minor issue 1]
2. [Minor issue 2]

### 建议决定
- [Accept / Minor Revision / Major Revision / Reject]

### 修改优先级
1. [Most critical]
2. [Second priority]
3. ...
```

## Orchestration Patterns

### Parallel Review

When doing a full audit, run agents in parallel:

```
User: 全面审查这篇论文
Orchestrator:
  1. 同时启动 [Quality Audit] + [Method Diagnosis] + [Peer Review]
  2. 等待所有结果
  3. 整合结果，消除重复
  4. 输出综合报告
```

### Sequential Pipeline

When following the research pipeline, run agents sequentially:

```
User: 帮我从选题到完稿
Orchestrator:
  1. Stage 1-3: 自己处理（需要交互）
  2. Stage 4: 启动 [Method Diagnosis] 辅助设计
  3. Stage 5: 自己处理 + 启动 [Style Polish] 润色
  4. Stage 6: 启动 [Quality Audit]
  5. Stage 7: 启动 [Peer Review]
  6. Stage 8: 自己处理返修
```

### Focused Delegation

When user asks for specific help:

```
User: 帮我检查实证方法是否合适
Orchestrator:
  1. 启动 [Method Diagnosis]
  2. 接收结果
  3. 补充自己的判断
  4. 输出给用户
```

## Output Integration

When combining agent outputs:

1. **Remove duplicates**: Same issue found by multiple agents.
2. **Reconcile conflicts**: Different severity assessments.
3. **Prioritize**: Critical issues first.
4. **Maintain traceability**: Note which agent found each issue.

## Limitations

- Agents work from text only; they cannot access external databases.
- Parallel agents may give conflicting advice; orchestrator must reconcile.
- Delegation adds latency; skip for simple tasks.
- Agent quality depends on input quality.

## Integration With Other Modules

- **research-pipeline.md**: Defines stages that use delegation.
- **pipeline-stage-gates.md**: Gates may trigger delegation for thorough checks.
- **quality-gates.md**: Quality Audit Agent uses these gates.
- **reproducibility-audit.md**: Quality Audit Agent uses these checks.
- **risk-register.md**: All agents contribute to risk identification.

## Step-by-Step Execution Mode (分步执行模式)

When parallel execution is not available (single-threaded agents, no subagent support), use this sequential mode.

### Mode Selection

| Agent Capability | Recommended Mode | Fallback |
|-----------------|------------------|----------|
| Supports parallel subagents | Parallel Review | Sequential |
| Supports sequential subagents | Sequential Pipeline | Step-by-Step |
| Single-threaded only | Step-by-Step | Integrated |
| No subagent support | Integrated | — |

### Step-by-Step Full Audit

When user asks for "全面审查" but parallel execution is unavailable:

```
User: 全面审查这篇论文

Step 1: Quality Audit (质量审计)
Agent: 读取 quality-gates.md → 运行所有门控检查 → 输出报告
       读取 reproducibility-audit.md → 运行可复现性检查 → 输出报告

Step 2: Method Diagnosis (方法诊断)
Agent: 读取 empirical-method-router.md → 评估实证策略 → 输出报告

Step 3: Peer Review (模拟审稿)
Agent: 模拟审稿人视角 → 识别问题 → 输出报告

Step 4: Integration (整合)
Agent: 合并所有报告 → 消除重复 → 优先级排序 → 输出综合报告
```

### Step-by-Step Output Template

```markdown
## 全面审查报告 (分步执行)

### 执行模式
- 模式: 分步执行 (Step-by-Step)
- 原因: [Agent不支持并行/用户指定/其他]

### Step 1: 质量审计
[Quality Audit output]

### Step 2: 方法诊断
[Method Diagnosis output]

### Step 3: 模拟审稿
[Peer Review output]

### 综合评估
[Integrated assessment with prioritized issues]

### 执行说明
- 各步骤独立执行，结果可能存在重复
- 已消除重复项，保留最严重的版本
- 优先级按综合严重度排序
```

### Integrated Mode (集成模式)

When even step-by-step delegation is not available, integrate all checks into a single pass:

```
User: 全面审查这篇论文

Agent performs in single pass:
1. Read quality-gates.md → Run all gates
2. Read reproducibility-audit.md → Run reproducibility checks
3. Read empirical-method-router.md → Evaluate method
4. Simulate peer review perspective
5. Integrate all findings
6. Output comprehensive report
```

**Advantages**:
- No delegation overhead
- Consistent perspective
- Faster for small manuscripts

**Disadvantages**:
- May miss issues that benefit from specialized focus
- Single perspective may lack diversity
- Context window limits for large manuscripts

### Mode Comparison

| Capability | Parallel | Sequential | Step-by-Step | Integrated |
|-----------|----------|------------|--------------|------------|
| Speed | Fast | Medium | Slow | Medium |
| Specialization | High | High | Medium | Low |
| Consistency | Low | Medium | High | High |
| Resource usage | High | Medium | Low | Low |
| Setup complexity | High | Medium | Low | None |

### Practical Recommendations

**For most users**: Use Step-by-Step mode.

**Why**:
- Works with most agents (including single-threaded)
- Maintains specialization benefits
- Clear audit trail
- User can review each step

**When to use Integrated mode**:
- Small manuscripts (< 20 pages)
- Simple review requests
- Agent has large context window
- Speed is priority

**When to use Parallel mode**:
- Large manuscripts
- Time-sensitive reviews
- Agent supports true parallel execution
- Quality is priority over speed

### Step-by-Step Execution Checklist

When executing step-by-step:

- [ ] Step 1 completed: Quality Audit
  - [ ] All gates checked
  - [ ] Reproducibility assessed
  - [ ] Risk register updated
- [ ] Step 2 completed: Method Diagnosis
  - [ ] Method identified
  - [ ] Identification strategy evaluated
  - [ ] Robustness assessed
- [ ] Step 3 completed: Peer Review
  - [ ] Strengths identified
  - [ ] Weaknesses identified
  - [ ] Issues prioritized
- [ ] Step 4 completed: Integration
  - [ ] Duplicates removed
  - [ ] Conflicts reconciled
  - [ ] Final report generated

### Degradation Path

```
Parallel (理想)
    ↓ [Agent不支持并行]
Sequential (顺序执行子代理)
    ↓ [Agent不支持子代理]
Step-by-Step (分步执行，单一代理)
    ↓ [Agent上下文窗口不足]
Integrated (集成模式，单次完成)
```
