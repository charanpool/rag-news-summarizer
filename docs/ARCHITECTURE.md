# 🏗️ Architecture

> Technical architecture and module overview for the RAG News Summarizer.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    Streamlit Web App                         │   │
│   │                      (app/main.py)                           │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│                                                                     │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐   │
│   │ News Fetcher │   │ RAG Chain    │   │ Vector Store         │   │
│   │              │   │              │   │                      │   │
│   │ • RSS Parse  │   │ • Retrieval  │   │ • Index articles     │   │
│   │ • Article    │   │ • Prompt     │   │ • Search similar     │   │
│   │   extraction │   │ • Generation │   │ • Manage collection  │   │
│   └──────────────┘   └──────────────┘   └──────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER                          │
│                                                                     │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐   │
│   │  Embeddings  │   │  ChromaDB    │   │  Ollama              │   │
│   │              │   │              │   │                      │   │
│   │ Sentence     │   │ Vector       │   │ Local LLM            │   │
│   │ Transformers │   │ Storage      │   │ (Llama 3.2)          │   │
│   └──────────────┘   └──────────────┘   └──────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Module Overview

### `app/config.py`

**Purpose:** Centralized configuration management.

```python
# Key settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2"
CHUNK_SIZE = 1000
TOP_K_RESULTS = 5
RSS_FEEDS = {...}
```

**Design decisions:**
- Uses `pydantic-settings` for type-safe config
- Supports `.env` file overrides
- Creates data directories on import

---

### `app/news_fetcher.py`

**Purpose:** Fetch and parse news articles from RSS feeds.

**Key components:**
- `Article` dataclass: Structured article representation
- `fetch_feed()`: Fetches single RSS feed
- `fetch_all_feeds()`: Fetches from all configured sources

**Data flow:**
```
RSS URL → feedparser → Article objects → List[Article]
```

---

### `app/embeddings.py`

**Purpose:** Generate text embeddings using sentence-transformers.

**Key components:**
- `get_embedding_model()`: Singleton model loader
- `embed_text()`: Single text embedding
- `embed_texts()`: Batch text embedding
- `get_text_splitter()`: Configurable text chunker

**Design decisions:**
- Model is cached to avoid reloading
- Uses HuggingFace embeddings for LangChain compatibility

---

### `app/vector_store.py`

**Purpose:** Manage ChromaDB vector database operations.

**Key components:**
- `get_vector_store()`: LangChain Chroma wrapper
- `articles_to_documents()`: Convert articles to chunked documents
- `index_articles()`: Add articles to vector store
- `search_similar()`: Semantic similarity search
- `get_collection_stats()`: Database statistics

**Data flow:**
```
Articles → Chunk → Embed → Store in ChromaDB
Query → Embed → Search → Return Documents
```

---

### `app/rag_chain.py`

**Purpose:** Orchestrate the RAG pipeline.

**Key components:**
- `check_ollama_available()`: Verify LLM availability
- `get_llm()`: Initialize Ollama LLM
- `format_documents()`: Prepare context for LLM
- `summarize_news()`: Main RAG function

**Prompt template:**
```
CONTEXT: [Retrieved articles]
QUESTION: [User query]
INSTRUCTIONS: Analyze, synthesize, cite sources...
```

---

### `app/main.py`

**Purpose:** Streamlit web interface.

**Key components:**
- `render_header()`: Page title and branding
- `render_sidebar()`: Controls and system status
- `render_main_content()`: Query input and results

**UI features:**
- Real-time Ollama status
- Progress indicators for indexing
- Source attribution with links
- Quick topic buttons

---

## Data Models

### Article

```python
@dataclass
class Article:
    id: str              # MD5 hash of URL
    title: str           # Article headline
    content: str         # Full text content
    summary: str         # RSS summary/description
    source: str          # News outlet name
    url: str             # Original article URL
    published_date: datetime  # Publication timestamp
```

### Document (LangChain)

```python
Document(
    page_content="Chunk of article text...",
    metadata={
        "article_id": "abc123",
        "title": "Article Title",
        "source": "BBC",
        "url": "https://...",
        "published_date": "2024-01-15T...",
        "chunk_index": 0
    }
)
```

---

## Directory Structure

```
RAG_News_Summarizer/
├── app/                    # Application code
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── embeddings.py       # Embedding generation
│   ├── main.py             # Streamlit UI
│   ├── news_fetcher.py     # RSS parsing
│   ├── rag_chain.py        # RAG pipeline
│   └── vector_store.py     # ChromaDB operations
├── data/                   # Runtime data
│   └── chroma_db/          # Vector database files
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # This file
│   └── CONCEPTS.md         # Core concepts
├── tests/                  # Test suite
│   └── test_rag.py
├── .env.example            # Environment template
├── .gitignore
├── CONTRIBUTING.md         # Contribution guide
├── LICENSE                 # MIT License
├── README.md               # Project overview
├── ROADMAP.md              # Future plans
└── requirements.txt        # Dependencies
```

---

## Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Framework** | LangChain | Industry standard, good abstractions |
| **Embeddings** | sentence-transformers | Local, fast, high quality |
| **Vector DB** | ChromaDB | Simple, no server needed |
| **LLM** | Ollama | Local, free, privacy-first |
| **UI** | Streamlit | Rapid prototyping, Python-native |
| **Config** | pydantic-settings | Type-safe, env file support |

---

## Extensibility Points

The architecture supports extension in several ways:

1. **Add news sources**: Modify `RSS_FEEDS` in config
2. **Change embedding model**: Update `EMBEDDING_MODEL`
3. **Switch LLM**: Modify `OLLAMA_MODEL` or integrate other providers
4. **Customize prompts**: Edit `SUMMARY_PROMPT` in rag_chain.py
5. **Add UI features**: Extend main.py Streamlit components

