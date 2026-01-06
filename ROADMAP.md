# 🗺️ Roadmap

> This document outlines the planned enhancements and future direction for the RAG News Summarizer project.

The project was **intentionally built as a minimal, functional implementation** to demonstrate core RAG concepts. The roadmap below describes how it can evolve into a more production-ready system.

---

## 📍 Current State (v1.0)

A simple, working RAG pipeline that:
- ✅ Fetches news from RSS feeds
- ✅ Generates embeddings using sentence-transformers
- ✅ Stores vectors in ChromaDB
- ✅ Retrieves relevant articles via semantic search
- ✅ Summarizes using local LLM (Ollama)
- ✅ Provides a Streamlit web interface

---

## 🎯 Near-Term Enhancements

### Improved News Ingestion
- [ ] Add more RSS feed sources (CNN, Al Jazeera, etc.)
- [ ] Support for custom RSS feed URLs via UI
- [ ] Scheduled/automatic news fetching (cron-like)
- [ ] Full article extraction using `newspaper3k` (beyond RSS summaries)
- [ ] Deduplication based on content similarity (not just URL)

### Enhanced RAG Pipeline
- [ ] Hybrid search (combine semantic + keyword search)
- [ ] Re-ranking of retrieved documents using cross-encoders
- [ ] Configurable chunk sizes via UI
- [ ] Support for different embedding models (multilingual, domain-specific)

### Better Summarization
- [ ] Multiple summarization styles (brief, detailed, bullet points)
- [ ] Topic clustering before summarization
- [ ] Comparative summaries across sources
- [ ] Fact extraction and entity recognition

### UI/UX Improvements
- [ ] Dark/light theme toggle
- [ ] Save and export summaries (PDF, Markdown)
- [ ] Search history and bookmarks
- [ ] Mobile-responsive design

---

## 🔮 Mid-Term Goals

### Alternative LLM Support
- [ ] OpenAI API integration (optional)
- [ ] Anthropic Claude support
- [ ] Groq for faster inference
- [ ] Model selection dropdown in UI

### Data Management
- [ ] SQLite metadata storage for articles
- [ ] Date range filtering for searches
- [ ] Source filtering (search only from specific outlets)
- [ ] Export/import of vector database

### API Layer
- [ ] FastAPI REST endpoints for programmatic access
- [ ] Swagger/OpenAPI documentation
- [ ] Rate limiting and basic auth
- [ ] Webhook support for new article notifications

### Observability
- [ ] Logging with structured output
- [ ] Performance metrics (latency, token usage)
- [ ] Query analytics dashboard

---

## 🚀 Long-Term Vision

### Production Readiness
- [ ] Docker containerization
- [ ] Docker Compose for full stack deployment
- [ ] Kubernetes Helm charts
- [ ] Environment-based configuration

### Advanced Features
- [ ] Multi-language news support
- [ ] Sentiment analysis per source
- [ ] Bias detection across outlets
- [ ] Custom fine-tuned summarization models
- [ ] Integration with news APIs (NewsAPI, GDELT)

### Collaboration Features
- [ ] User accounts and authentication
- [ ] Shared summaries and annotations
- [ ] Team workspaces
- [ ] Slack/Discord bot integration

---

## 🎯 Keeping It Simple

To keep things focused, these are probably not coming anytime soon:

- Real-time streaming news (websockets)
- Social media integration (Twitter/X, Reddit)
- Paid news source scrapers (WSJ, NYT paywalls)
- Mobile native apps
- Complex user management (roles, permissions)

But hey, if you really want one of these — feel free to build it!

---

## 💡 How to Contribute

If you'd like to work on any roadmap item:

1. Check the [Issues](https://github.com/charanpool/rag-news-summarizer/issues) for existing discussions
2. Open a new issue to propose your approach
3. Fork, implement, and submit a PR
4. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

## 📝 Notes

This roadmap is a living document and will evolve based on:
- Community feedback and contributions
- Changes in the LLM/RAG ecosystem
- Real-world usage patterns

**Last updated:** January 2026

