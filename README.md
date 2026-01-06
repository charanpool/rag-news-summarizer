# 📰 RAG News Summarizer

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple.svg)](https://ollama.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **A Retrieval-Augmented Generation (RAG) system for fetching, indexing, and summarizing news articles using local AI models.**

RAG News Summarizer demonstrates a complete RAG pipeline — from data ingestion to semantic search to LLM-powered summarization — all running locally on your machine.

---

## 🌱 Why This Project Exists

This project was **intentionally built as a simple, educational implementation** of RAG concepts.

Modern AI applications increasingly rely on RAG architectures, but many tutorials are either:
- Too abstract (theory without working code)
- Too complex (production systems with overwhelming features)
- Cloud-dependent (requiring API keys and paid services)

**RAG News Summarizer** fills the gap by providing:

- ✅ A **complete, working implementation** you can run locally
- ✅ **Clean, readable code** that's easy to understand and modify
- ✅ **No API keys required** — uses local models only
- ✅ A **foundation to build upon** for your own projects

This is ideal for learning, portfolio projects, or as a starting point for production systems.

---

## ✨ Features

- 🔍 **Semantic Search** — Find relevant articles using vector similarity
- 📰 **Multi-Source Ingestion** — Fetches from BBC, Reuters, TechCrunch, and more
- 🤖 **Local LLM Integration** — Runs entirely on your machine with Ollama
- 💾 **Persistent Storage** — ChromaDB vector database for efficient retrieval
- 🎨 **Modern Web UI** — Beautiful Streamlit interface with real-time updates
- 🔒 **Privacy-First** — No data leaves your machine

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAG Pipeline (LangChain)                      │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────────┐  │
│  │ News Fetcher  │  │ Vector Store   │  │ LLM Chain          │  │
│  │ (RSS Parser)  │  │ (ChromaDB)     │  │ (Ollama)           │  │
│  └───────────────┘  └────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
   ┌──────────┐      ┌──────────────┐      ┌─────────────┐
   │ RSS Feeds│      │ Sentence     │      │ Ollama      │
   │ (Free)   │      │ Transformers │      │ (Llama 3.2) │
   └──────────┘      └──────────────┘      └─────────────┘
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/charanpool/rag-news-summarizer.git
cd rag-news-summarizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up Ollama (in a separate terminal)
ollama pull llama3.2
ollama serve

# 5. Run the application
streamlit run app/main.py
```

Open your browser at `http://localhost:8501` 🎉

### First Run

1. Click **"🔄 Fetch & Index News"** in the sidebar
2. Wait for articles to be fetched and indexed
3. Ask a question like *"What's the latest in AI?"*
4. View the AI-generated summary with source citations

---

## 📁 Project Structure

```
RAG_News_Summarizer/
├── app/                    # Application code
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── embeddings.py       # Embedding generation
│   ├── main.py             # Streamlit web interface
│   ├── news_fetcher.py     # RSS feed parser
│   ├── rag_chain.py        # RAG pipeline logic
│   └── vector_store.py     # ChromaDB operations
├── data/                   # Runtime data (gitignored)
│   └── chroma_db/          # Vector database storage
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # Technical architecture
│   └── CONCEPTS.md         # Core RAG concepts
├── tests/                  # Test suite
│   └── test_rag.py
├── .env.example            # Environment template
├── .gitignore
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
├── README.md               # This file
├── ROADMAP.md              # Future enhancement plans
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | LangChain | RAG pipeline framework |
| **Embeddings** | sentence-transformers | Text vectorization (local) |
| **Vector DB** | ChromaDB | Similarity search storage |
| **LLM** | Ollama (Llama 3.2) | Text generation (local) |
| **Web UI** | Streamlit | Interactive interface |
| **News Source** | RSS Feeds | Free news data |

---

## 📊 How It Works

### 1. Ingestion Phase

```
RSS Feeds → Parse Articles → Chunk Text → Generate Embeddings → Store in ChromaDB
```

### 2. Query Phase

```
User Query → Embed Query → Semantic Search → Retrieve Top-K Articles
```

### 3. Generation Phase

```
Retrieved Context + User Query → LLM Prompt → Generated Summary → Display
```

For a deeper dive, see [docs/CONCEPTS.md](docs/CONCEPTS.md).

---

## ⚙️ Configuration

Key settings in `app/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model |
| `OLLAMA_MODEL` | `llama3.2` | Local LLM model |
| `CHUNK_SIZE` | `1000` | Text chunk size (characters) |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K_RESULTS` | `5` | Documents to retrieve |

Override via `.env` file:

```bash
cp .env.example .env
# Edit .env with your preferences
```

---

## 📡 Supported News Sources

| Source | Category |
|--------|----------|
| BBC World | World News |
| BBC Tech | Technology |
| Reuters | World News |
| TechCrunch | Technology |
| Hacker News | Technology |
| Ars Technica | Technology |

Add custom sources in `app/config.py`:

```python
RSS_FEEDS = {
    "Your Source": "https://example.com/rss/feed.xml",
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🧩 Design Principles

This project follows intentionally **lean design principles**:

| Principle | Implementation |
|-----------|----------------|
| **Simplicity** | Minimal dependencies, clear code structure |
| **Local-First** | No external API calls required |
| **Educational** | Well-documented, easy to understand |
| **Extensible** | Clean abstractions for modification |
| **Stateless Core** | No database beyond vector store |

### Keeping It Simple

This project skips a few things on purpose to stay beginner-friendly:

- User authentication
- Cloud deployments
- Complex caching layers
- Microservices architecture
- Kubernetes configurations

Want to add these? Check out [ROADMAP.md](ROADMAP.md) for ideas!

---

## 🔧 Troubleshooting

### Ollama Not Running

```bash
# Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Model Not Found

```bash
# Pull the required model
ollama pull llama3.2
```

### Memory Issues

- Use a smaller embedding model in config
- Reduce `CHUNK_SIZE`
- Use a smaller Ollama model: `llama3.2:1b`

### Module Import Errors

Ensure you're running from the project root:

```bash
cd /path/to/RAG_News_Summarizer
source venv/bin/activate
streamlit run app/main.py
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [CONCEPTS.md](docs/CONCEPTS.md) | Core RAG concepts explained |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture details |
| [ROADMAP.md](ROADMAP.md) | Future enhancement plans |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where help is appreciated:
- Improving heuristic parsing
- Adding test fixtures
- Documentation improvements
- UI/UX enhancements

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features including:

- [ ] Hybrid search (semantic + keyword)
- [ ] Multiple LLM provider support
- [ ] REST API endpoints
- [ ] Docker containerization
- [ ] Enhanced UI features

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

- ✅ Free for personal and commercial use
- ✅ Modify and distribute freely
- ✅ Attribution required

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) — RAG framework
- [Ollama](https://ollama.ai/) — Local LLM inference
- [ChromaDB](https://www.trychroma.com/) — Vector storage
- [Sentence-Transformers](https://www.sbert.net/) — Embeddings
- [Streamlit](https://streamlit.io/) — Web interface

---

## ⭐ Support

If you find this project useful:

- ⭐ **Star** the repository
- 🐛 **Report** issues you encounter
- 💡 **Share** ideas for improvements
- 🧑‍💻 **Contribute** code or documentation

---

<p align="center">
  Built with ❤️ for learning and demonstration purposes
</p>
