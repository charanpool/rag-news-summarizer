# 🧠 Core Concepts

> Understanding the key concepts behind the RAG News Summarizer.

---

## What is RAG?

**RAG (Retrieval-Augmented Generation)** is an AI architecture that combines:

1. **Retrieval**: Finding relevant documents from a knowledge base
2. **Augmentation**: Adding retrieved context to the LLM prompt
3. **Generation**: Producing output grounded in the retrieved information

```
User Query → Retrieve Relevant Docs → Augment Prompt → Generate Response
```

### Why RAG?

| Problem with Plain LLMs | How RAG Solves It |
|-------------------------|-------------------|
| Knowledge cutoff date | Retrieves fresh, up-to-date information |
| Hallucinations | Grounds responses in actual documents |
| No source attribution | Can cite specific sources used |
| Context limitations | Only sends relevant context, not everything |

---

## Key Components

### 1. Embeddings

Embeddings are numerical representations of text that capture semantic meaning.

```
"AI technology is advancing" → [0.23, -0.45, 0.12, ...]
"Machine learning grows fast" → [0.21, -0.43, 0.15, ...]  # Similar!
"The weather is sunny"       → [-0.56, 0.78, -0.33, ...] # Different!
```

**In this project:** We use `sentence-transformers` with the `all-MiniLM-L6-v2` model, which produces 384-dimensional vectors.

### 2. Vector Database

A vector database stores embeddings and enables similarity search.

```
Query: "What's happening in AI?"
        ↓
   Embed query
        ↓
   Find similar vectors
        ↓
   Return top K documents
```

**In this project:** We use ChromaDB, a lightweight, local vector database.

### 3. Chunking

Long documents are split into smaller chunks for better retrieval.

```
Article (2000 words)
    ↓
Chunk 1 (500 words) → Embedding 1
Chunk 2 (500 words) → Embedding 2
Chunk 3 (500 words) → Embedding 3
Chunk 4 (500 words) → Embedding 4
```

**In this project:** We use 1000-character chunks with 200-character overlap.

### 4. Retrieval

When a user asks a question, we:

1. Convert the question to an embedding
2. Find the K most similar document chunks
3. Return those chunks as context

### 5. Generation

The LLM receives:

```
System: You are a news analyst...
Context: [Retrieved article chunks]
Question: What are the latest AI developments?

→ LLM generates grounded response
```

**In this project:** We use Ollama with Llama 3.2 for local inference.

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         INGESTION                                │
│                                                                  │
│   RSS Feeds → Parse Articles → Chunk Text → Embed → Store       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       VECTOR DATABASE                            │
│                                                                  │
│   ChromaDB stores embeddings + metadata for all article chunks   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          RETRIEVAL                               │
│                                                                  │
│   User Query → Embed → Similarity Search → Top K Documents       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         GENERATION                               │
│                                                                  │
│   Context + Query → LLM Prompt → Generated Summary               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Trade-offs in This Implementation

### Simplicity Over Optimization

| Choice | Trade-off |
|--------|-----------|
| Single embedding model | Simple, but no domain-specific optimization |
| Fixed chunk size | Easy to configure, but not adaptive |
| Top-K retrieval | Fast, but no re-ranking |
| Local LLM | Private, but requires local resources |

### What's Not Included (Intentionally)

- **Hybrid search**: Could combine keyword + semantic search
- **Re-ranking**: Could use cross-encoders for better relevance
- **Query expansion**: Could rephrase queries for better retrieval
- **Caching**: Could cache frequent queries

These are omitted to keep the codebase educational and approachable.

---

## Further Reading

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Ollama Documentation](https://ollama.ai/)

