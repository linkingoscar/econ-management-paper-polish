# RAG Workflow (RAG知识库工作流)

Use this file when the user wants to build or query a local knowledge base from academic PDFs. RAG (Retrieval-Augmented Generation) enables intelligent search and citation from the user's own literature collection.

## When To Use

- User asks to search their PDF collection.
- User provides PDFs and asks "这些文献里哪些支持X观点？"
- User wants to build a local literature database.
- User asks cross-paper questions.
- User wants to verify citations against original text.

## RAG Architecture

```
用户文献库 (PDFs/BibTeX/Zotero)
        ↓
    文档处理层
    ├── PDF解析
    ├── 元数据提取
    ├── 分块索引
    └── 向量化
        ↓
    知识库存储
    ├── 向量数据库
    ├── 元数据索引
    └── 全文索引
        ↓
    查询层
    ├── 语义搜索
    ├── 关键词搜索
    └── 混合搜索
        ↓
    回答层
    ├── 引用溯源
    ├── 置信度评估
    └── 证据包生成
```

## Document Processing

### Input Formats

| Format | Processing | Output |
|--------|-----------|--------|
| PDF | Text extraction + OCR if needed | Chunks with metadata |
| BibTeX | Parse entries | Metadata records |
| RIS | Parse entries | Metadata records |
| Zotero export | Parse JSON/RIS | Metadata records |
| URL | Fetch + extract | Chunks with metadata |

### Metadata Extraction

For each document, extract:

| Field | Source | Required |
|-------|--------|----------|
| Title | PDF header/BibTeX | Yes |
| Authors | PDF header/BibTeX | Yes |
| Year | PDF header/BibTeX | Yes |
| Journal | PDF header/BibTeX | Yes |
| DOI | PDF/BibTeX | Recommended |
| Abstract | PDF/BibTeX | Recommended |
| Keywords | PDF/BibTeX | Recommended |

### Chunking Strategy

**By Section** (preferred for academic papers):
```
Abstract → Introduction → Literature Review → Theory → 
Data → Method → Results → Discussion → Conclusion
```

**By Paragraph** (fallback):
- Split at paragraph boundaries
- Maintain paragraph context
- Include section header as context

**Chunk Size**: 500-1000 tokens recommended
**Overlap**: 100-200 tokens for context continuity

## Query Types

### 1. Semantic Search (语义搜索)

Find passages semantically similar to the query.

**Example**: "What are the mechanisms of digital financial inclusion on poverty?"

**Process**:
1. Embed the query
2. Find nearest chunks by cosine similarity
3. Return top-K chunks with source info

### 2. Keyword Search (关键词搜索)

Exact or fuzzy keyword matching.

**Example**: "DID parallel trends test"

**Process**:
1. Parse keywords
2. Search full-text index
3. Rank by relevance

### 3. Hybrid Search (混合搜索)

Combine semantic and keyword search.

**Process**:
1. Run semantic search
2. Run keyword search
3. Merge and re-rank results
4. Return top-K

### 4. Cross-Paper Question (跨论文问答)

Answer questions that span multiple papers.

**Example**: "哪些文献用了工具变量研究数字金融？"

**Process**:
1. Parse question into search components
2. Search across all papers
3. Aggregate findings
4. Return structured answer with citations

### 5. Citation Verification (引用验证)

Check if a citation actually supports a claim.

**Example**: "Author (Year) 说数字金融减少贫困，原文怎么讲的？"

**Process**:
1. Find the paper in the database
2. Search for relevant passages
3. Compare claim with original text
4. Report match/mismatch

## Output Formats

### Search Results

```markdown
## 搜索结果: [Query]

### 最相关段落

#### 1. [Author (Year)] - [Section]
> "[Relevant passage from original text]"

**相关度**: 高
**支持观点**: [What this passage supports]

#### 2. [Author (Year)] - [Section]
> "[Relevant passage]"

**相关度**: 中
**支持观点**: [What this passage supports]

...

### 统计
- 搜索文献总数: [N]
- 返回结果数: [K]
- 相关度分布: 高[X], 中[Y], 低[Z]
```

### Cross-Paper Answer

```markdown
## 跨论文回答: [Question]

### 直接回答
[Concise answer to the question]

### 证据来源

| # | 文献 | 相关发现 | 原文位置 |
|---|------|---------|---------|
| 1 | Author1 (Year) | [Finding] | Section X, p.Y |
| 2 | Author2 (Year) | [Finding] | Section X, p.Y |
| ... | ... | ... | ... |

### 覆盖度评估
- 支持该观点的文献: [N] 篇
- 反对该观点的文献: [N] 篇
- 未明确表态的文献: [N] 篇

### 局限性
- [Any limitations of the search]
```

## Integration With Citation Workflow

When using RAG results for citations:

1. **Verify**: Always check the original passage matches the claim.
2. **Grade**: Apply evidence grading from `evidence-grading.md`.
3. **Format**: Format citation in required style.
4. **Trace**: Record the source passage for traceability.

**Do NOT**:
- Cite a paper just because it appears in search results.
- Assume search ranking equals relevance.
- Skip verification of the original text.

## Limitations

- RAG quality depends on PDF text extraction quality.
- Scanned PDFs may require OCR (not always accurate).
- Tables and figures are often poorly extracted.
- Semantic search may miss exact keyword matches.
- Cross-language search requires translation.

## User Setup Guidance

For users who want to build a RAG knowledge base:

1. **Collect PDFs**: Gather all relevant papers.
2. **Organize**: Use consistent naming (Author_Year_Title.pdf).
3. **Export BibTeX**: From Zotero or reference manager.
4. **Process**: Run through document processing pipeline.
5. **Index**: Build vector and keyword indexes.
6. **Query**: Use the search interface.

## Integration With Other Modules

- **evidence-citation-workflow.md**: RAG feeds into citation verification.
- **rag-retrieval.md**: Detailed retrieval strategies.
- **rag-verification.md**: Citation verification rules.
- **survey-workspace.md**: RAG can power the literature pool.

## Degradation Modes (降级方案)

When RAG infrastructure (vector database, PDF parser, embedding model) is not available, use these fallback strategies.

### Mode 1: Full RAG (理想模式)

**Requirements**: Vector database, PDF parser, embedding model

**Capabilities**:
- Semantic search across PDF collection
- Automatic metadata extraction
- Cross-paper QA
- Citation verification against original text

**Setup**:
1. Install vector database (Chroma, FAISS, Pinecone, etc.)
2. Install PDF parser (PyPDF2, pdfplumber, etc.)
3. Install embedding model (OpenAI, sentence-transformers, etc.)
4. Run indexing pipeline

### Mode 2: Manual Index + Agent Search (手动索引模式)

**Requirements**: User provides structured index, agent can read files

**Capabilities**:
- Keyword search across indexed content
- Manual metadata management
- Basic cross-paper QA
- Citation verification with user help

**Setup**:

1. User creates a structured index file:

```markdown
# 文献索引: [Topic]

## Paper 1: Author1 (Year)
- **文件路径**: ./papers/author1_2024.pdf
- **标题**: [Full title]
- **期刊**: [Journal]
- **关键词**: [keyword1], [keyword2], [keyword3]
- **摘要**: [2-3 sentence summary]
- **关键发现**: [Key findings relevant to your research]
- **可引用段落**:
  - "[Quote 1]" (p.X, Section Y)
  - "[Quote 2]" (p.X, Section Y)

## Paper 2: Author2 (Year)
...
```

2. Agent searches the index file using keyword matching.
3. User verifies passages against original PDFs.

**Output**: Same as Full RAG mode, but with manual verification step.

### Mode 3: BibTeX + Metadata Search (元数据搜索模式)

**Requirements**: BibTeX file, agent can parse it

**Capabilities**:
- Search by author, year, title, keywords
- Filter by journal, field, method
- Basic literature mapping
- No full-text search

**Setup**:

1. Export BibTeX from Zotero/EndNote/Mendeley.
2. Agent parses BibTeX and builds metadata index.
3. Search by metadata fields.

**Example BibTeX**:
```bibtex
@article{author2024,
    author = {Author, First},
    title = {Digital Financial Inclusion and Poverty},
    journal = {Journal of Finance},
    year = {2024},
    keywords = {digital finance, poverty, credit access},
    abstract = {This paper examines...}
}
```

**Search capabilities**:
- "哪些文献研究了数字金融？" → Search keywords field
- "Author (Year) 的论文讲了什么？" → Search by author/year
- "JF上有哪些相关论文？" → Search by journal

### Mode 4: User-Guided Search (用户引导搜索)

**Requirements**: User provides PDF text or quotes

**Capabilities**:
- Verify user-provided quotes
- Analyze passages user shares
- Cross-check citations
- No autonomous search

**Process**:

1. User shares a passage: "这段话来自Author (Year)，讲的是..."
2. Agent analyzes the passage.
3. Agent checks if it supports the claim.
4. Agent provides verification result.

**Example**:
```
User: 这段来自Zhang (2023)："数字金融显著降低了农村贫困发生率，主要通过扩大信贷渠道实现。"
      这能支持我的论点吗？

Agent: [Analyzes the passage]
       ✅ 支持你的论点"数字金融通过信贷渠道减少贫困"
       - 直接支持: 是
       - 强度: 强（明确陈述因果机制）
       - 建议引用位置: 理论假说或机制检验部分
```

### Mode Selection Guide

| Scenario | Recommended Mode | Fallback |
|----------|-----------------|----------|
| Have vector DB + PDFs | Full RAG | Mode 2 |
| Have PDFs but no vector DB | Mode 2 | Mode 3 |
| Have BibTeX only | Mode 3 | Mode 4 |
| Have quotes only | Mode 4 | Direct analysis |
| No infrastructure | Mode 4 | Manual search |

### Mode Comparison

| Capability | Mode 1 | Mode 2 | Mode 3 | Mode 4 |
|-----------|--------|--------|--------|--------|
| Semantic search | ✅ | ❌ | ❌ | ❌ |
| Keyword search | ✅ | ✅ | ✅ | ❌ |
| Full-text search | ✅ | ✅ | ❌ | ❌ |
| Metadata search | ✅ | ✅ | ✅ | ❌ |
| Citation verification | ✅ | ✅ | ⚠️ | ✅ |
| Cross-paper QA | ✅ | ✅ | ⚠️ | ❌ |
| Setup complexity | High | Medium | Low | None |

### Practical Recommendations

**For most users**: Start with Mode 3 (BibTeX) or Mode 4 (User-Guided).

**Why**:
- Most researchers already have BibTeX files.
- Mode 4 requires no setup and works immediately.
- Full RAG requires significant technical setup.

**Upgrade path**:
1. Start with Mode 4 (immediate, no setup).
2. Export BibTeX → Mode 3 (metadata search).
3. Organize PDFs with consistent naming → Mode 2.
4. When ready, set up vector DB → Mode 1.
