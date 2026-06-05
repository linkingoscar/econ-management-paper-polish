# RAG Retrieval (RAG检索策略)

Use this file for detailed retrieval strategies when querying a RAG knowledge base. This covers how to formulate queries, select search methods, and rank results.

## Query Formulation

### From User Question to Search Query

| User Question Type | Query Strategy | Example |
|-------------------|----------------|---------|
| "哪些文献支持X？" | Semantic search for claim | "X is supported by evidence" |
| "谁用了Y方法？" | Keyword + semantic | "method: DID difference-in-differences" |
| "Z的定义是什么？" | Keyword search | "definition of Z construct" |
| "A和B什么关系？" | Semantic search | "relationship between A and B" |
| "这个引用对不对？" | Exact match | Direct quote verification |

### Query Decomposition

Complex questions should be decomposed:

**Original**: "数字金融如何通过信贷渠道影响农村贫困？"

**Decomposed**:
1. "digital financial inclusion credit access" (数字金融与信贷)
2. "rural poverty reduction mechanism" (农村减贫机制)
3. "credit channel poverty" (信贷渠道与贫困)

**Strategy**: Run each subquery, then merge results.

## Search Methods

### Method 1: Semantic Search

**How it works**: Embed query and chunks, find nearest neighbors.

**Best for**:
- Conceptual questions
- Finding related ideas
- Cross-language search

**Limitations**:
- May miss exact keywords
- Embedding quality varies
- Computationally expensive

**Parameters**:
- Top-K: 5-10 results
- Similarity threshold: 0.7-0.8 (cosine)

### Method 2: Keyword Search

**How it works**: Exact or fuzzy matching on text.

**Best for**:
- Specific terms, names, methods
- Finding exact quotes
- Fast retrieval

**Limitations**:
- Misses synonyms
- No semantic understanding
- Language-dependent

**Parameters**:
- Fuzzy matching: Levenshtein distance ≤ 2
- Boost title and abstract fields

### Method 3: Hybrid Search

**How it works**: Combine semantic and keyword, then re-rank.

**Best for**:
- General queries
- Balancing precision and recall
- Production systems

**Process**:
1. Run semantic search (top-20)
2. Run keyword search (top-20)
3. Merge results (deduplicate)
4. Re-rank by combined score
5. Return top-K

**Scoring**:
```
Final Score = α × Semantic Score + (1-α) × Keyword Score
```
Where α = 0.6-0.7 typically.

### Method 4: Filtered Search

**How it works**: Apply filters before or after search.

**Common filters**:
| Filter | Example |
|--------|---------|
| Year | Published after 2015 |
| Journal | Only AER, QJE, JPE |
| Method | Papers using DID |
| Field | Labor economics |
| Sample | China-specific |

**Implementation**: Pre-filter or post-filter with metadata.

## Result Ranking

### Ranking Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Semantic similarity | High | How related to query |
| Keyword match | Medium | Exact term matches |
| Recency | Low | More recent papers upranked |
| Citation count | Low | Highly cited papers upranked |
| Journal quality | Low | Top journal papers upranked |
| Section relevance | Medium | Abstract/introduction upranked |

### Re-ranking Strategies

**Cross-Encoder Re-ranking**:
1. Take query + each candidate passage
2. Score relevance with cross-encoder model
3. Sort by cross-encoder score

**Advantage**: More accurate than bi-encoder
**Disadvantage**: Slower (N forward passes)

## Result Presentation

### Standard Output

```markdown
## 检索结果

### 查询
[Original query]

### 搜索策略
- 方法: [Semantic/Keyword/Hybrid]
- 参数: [Top-K, threshold, etc.]
- 过滤: [Any filters applied]

### 结果 (共 N 条)

#### 1. [Author (Year)] - [Paper Title]
> "[Relevant passage]"

- **来源**: [Section name], p.[X]
- **相关度**: [High/Medium/Low]
- **匹配原因**: [Why this result matches]

#### 2. ...

### 统计
- 搜索文献总数: [Total]
- 匹配结果数: [Matched]
- 相关度分布: High [N], Medium [N], Low [N]
```

## Query Optimization

### Improving Recall

If too few results:
1. Broaden query terms
2. Lower similarity threshold
3. Add synonyms to search
4. Use keyword search as fallback

### Improving Precision

If too many irrelevant results:
1. Add specific terms
2. Raise similarity threshold
3. Add filters (year, journal, method)
4. Use cross-encoder re-ranking

### Handling Ambiguity

If query is ambiguous:
1. Ask user to clarify
2. Run multiple interpretations
3. Present results grouped by interpretation

## Special Queries

### Method Search

**Query**: "哪些文献用了事件研究法？"

**Strategy**:
1. Keywords: "event study", "event study design", "event-study"
2. Semantic: "empirical method for causal inference using event timing"
3. Filter: Method-related sections

### Construct Search

**Query**: "数字普惠金融怎么测量？"

**Strategy**:
1. Keywords: "digital financial inclusion index", "measurement", "proxy"
2. Semantic: "how to measure digital financial inclusion"
3. Filter: Data/method sections

### Theory Search

**Query**: "资源基础理论的核心观点"

**Strategy**:
1. Keywords: "resource-based view", "RBV", "theory"
2. Semantic: "core arguments of resource-based theory"
3. Filter: Theory/literature sections

## Integration With Other Modules

- **rag-workflow.md**: Overall RAG architecture.
- **rag-verification.md**: Verifying search results.
- **evidence-citation-workflow.md**: Using results for citations.
- **evidence-grading.md**: Grading search results.
