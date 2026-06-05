# RAG Verification (RAG引用验证)

Use this file when verifying that RAG search results actually support the claims they are cited for. This prevents "hallucinated citations" where a paper appears relevant but doesn't actually support the specific claim.

## When To Use

- After retrieving results from RAG knowledge base.
- Before adding any citation from RAG to a manuscript.
- When user asks "这个引用对不对？"
- When cross-checking existing citations against original text.

## Verification Process

### Step 1: Relevance Check (相关性检查)

**Question**: Is this paper generally relevant to the topic?

| Check | Description | Pass |
|-------|-------------|------|
| Topic match | Paper is about the same topic | Yes |
| Construct match | Paper uses same constructs | Yes |
| Method match | Paper uses relevant method | If applicable |
| Sample match | Paper studies similar context | If applicable |

**If failed**: Reject citation. Paper is not relevant.

### Step 2: Claim Match Check (主张匹配检查)

**Question**: Does the original text support the specific claim?

| Check | Description | Pass |
|-------|-------------|------|
| Direct support | Text explicitly states the claim | Yes |
| Implied support | Text implies the claim | Acceptable |
| No mention | Text doesn't address the claim | Reject |
| Contradicts | Text contradicts the claim | Reject |

**Verification method**:
1. Find the most relevant passage in the original text.
2. Compare the passage with the claim.
3. Determine if the passage supports, contradicts, or is neutral.

### Step 3: Strength Check (强度检查)

**Question**: How strongly does the text support the claim?

| Strength | Description | Citation Use |
|----------|-------------|--------------|
| Strong | Explicit, direct statement | Primary citation |
| Moderate | Implied or indirect | Supporting citation |
| Weak | Tangentially related | Background only |
| None | No support | Do not cite |

### Step 4: Context Check (上下文检查)

**Question**: Is the claim taken out of context?

| Check | Description | Pass |
|-------|-------------|------|
| Qualifiers preserved | "Under condition X" not dropped | Yes |
| Scope maintained | "In sample Y" not generalized | Yes |
| Direction correct | Positive/negative not flipped | Yes |
| Magnitude correct | Numbers not distorted | Yes |

**Common errors**:
- Paper says "in China" but cited for global claim.
- Paper says "for SMEs" but cited for all firms.
- Paper says "may affect" but cited as "affects".

## Verification Output

### Verified Citation

```markdown
## 引用验证: ✅ 通过

### 引用信息
- 文献: [Author (Year)]
- 被引主张: [The claim being made]
- 原文位置: [Section, page]

### 原文段落
> "[Exact quote from original text]"

### 验证结果
- 相关性: ✅ 高度相关
- 主张匹配: ✅ 直接支持
- 支持强度: 强
- 上下文: ✅ 无断章取义

### 建议
可以作为主要引用使用。
```

### Failed Verification

```markdown
## 引用验证: ❌ 未通过

### 引用信息
- 文献: [Author (Year)]
- 被引主张: [The claim being made]
- 原文位置: [Section, page]

### 原文段落
> "[Exact quote from original text]"

### 验证结果
- 相关性: ✅ 主题相关
- 主张匹配: ❌ 不支持该主张
- 原因: 原文讨论的是[X]，而非[Y]
- 上下文: ⚠️ 可能存在断章取义

### 建议
1. 不应作为该主张的引用
2. 可用于其他主张: [suggestion]
3. 替代文献建议: [alternatives]
```

### Partial Verification

```markdown
## 引用验证: ⚠️ 部分通过

### 引用信息
- 文献: [Author (Year)]
- 被引主张: [The claim being made]
- 原文位置: [Section, page]

### 原文段落
> "[Exact quote from original text]"

### 验证结果
- 相关性: ✅ 主题相关
- 主张匹配: ⚠️ 部分支持
- 原因: 原文支持[X]，但不支持[Y]部分
- 上下文: ⚠️ 需要限定范围

### 建议
1. 修改主张为: "[More precise claim]"
2. 添加限定语: "在[条件]下"
3. 补充其他文献支持[Y]部分
```

## Common Verification Failures

### 1. Topic Match but Claim Mismatch

**Scenario**: Paper is about digital finance, but doesn't support the specific claim about poverty reduction.

**Detection**: Read the abstract and conclusion for the paper's actual findings.

**Fix**: Find a different paper that actually supports the claim.

### 2. Outdated Finding

**Scenario**: Paper's finding has been contradicted by newer research.

**Detection**: Check publication date and search for recent papers.

**Fix**: Cite both, or use the newer finding.

### 3. Different Sample/Context

**Scenario**: Paper studies US firms but cited for China claim.

**Detection**: Check sample description in the paper.

**Fix**: Find China-specific paper, or acknowledge the difference.

### 4. Method Mismatch

**Scenario**: Paper uses correlation but cited for causal claim.

**Detection**: Check the method section.

**Fix**: Soften the claim or find a causal study.

### 5. Out-of-Context Quote

**Scenario**: Quote is from a limitation section, not the main finding.

**Detection**: Check where the quote appears in the paper.

**Fix**: Use the main finding section instead.

## Batch Verification

When verifying multiple citations:

```markdown
## 批量引用验证报告

### 统计
- 总引用数: [N]
- ✅ 通过: [X]
- ⚠️ 部分通过: [Y]
- ❌ 未通过: [Z]

### 详细结果

| # | 文献 | 主张 | 结果 | 原因 |
|---|------|------|------|------|
| 1 | Author1 (Year) | [Claim] | ✅ | 直接支持 |
| 2 | Author2 (Year) | [Claim] | ❌ | 不支持该主张 |
| 3 | Author3 (Year) | [Claim] | ⚠️ | 需限定范围 |
| ... | ... | ... | ... | ... |

### 需要处理的问题
1. [Citation 2]: 替换或删除
2. [Citation 3]: 添加限定语
3. ...
```

## Integration With Other Modules

- **rag-workflow.md**: RAG search results feed into verification.
- **rag-retrieval.md**: Retrieval strategies affect result quality.
- **evidence-citation-workflow.md**: Verified citations enter citation workflow.
- **evidence-grading.md**: Verification results affect evidence grade.
- **quality-gates.md**: Citation Gate uses verification rules.
