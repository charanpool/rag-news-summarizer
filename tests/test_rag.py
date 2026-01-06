"""
Tests for RAG News Summarizer components.
"""

import pytest
from datetime import datetime

# Import modules to test
from app.config import settings
from app.news_fetcher import Article, generate_article_id, fetch_feed
from app.embeddings import get_embedding_model, embed_text, get_text_splitter
from app.vector_store import articles_to_documents


class TestConfig:
    """Tests for configuration module."""
    
    def test_settings_loaded(self):
        """Test that settings are loaded correctly."""
        assert settings.EMBEDDING_MODEL is not None
        assert settings.OLLAMA_MODEL is not None
        assert settings.CHUNK_SIZE > 0
    
    def test_rss_feeds_configured(self):
        """Test that RSS feeds are configured."""
        assert len(settings.RSS_FEEDS) > 0
        for name, url in settings.RSS_FEEDS.items():
            assert name
            assert url.startswith("http")
    
    def test_data_directories_exist(self):
        """Test that data directories are created."""
        assert settings.DATA_DIR.exists()
        assert settings.CHROMA_DB_DIR.exists()


class TestNewsFetcher:
    """Tests for news fetcher module."""
    
    def test_article_creation(self):
        """Test Article dataclass creation."""
        article = Article(
            id="test123",
            title="Test Article",
            content="This is test content.",
            summary="Test summary.",
            source="Test Source",
            url="https://example.com/test",
            published_date=datetime.now(),
        )
        
        assert article.id == "test123"
        assert article.title == "Test Article"
        assert article.source == "Test Source"
    
    def test_article_to_dict(self):
        """Test Article to_dict conversion."""
        article = Article(
            id="test123",
            title="Test Article",
            content="This is test content.",
            summary="Test summary.",
            source="Test Source",
            url="https://example.com/test",
        )
        
        article_dict = article.to_dict()
        assert article_dict["id"] == "test123"
        assert article_dict["title"] == "Test Article"
        assert article_dict["published_date"] is None
    
    def test_generate_article_id(self):
        """Test article ID generation is consistent."""
        url = "https://example.com/article/123"
        id1 = generate_article_id(url)
        id2 = generate_article_id(url)
        
        assert id1 == id2
        assert len(id1) == 32  # MD5 hex length
    
    def test_different_urls_different_ids(self):
        """Test that different URLs generate different IDs."""
        id1 = generate_article_id("https://example.com/article/1")
        id2 = generate_article_id("https://example.com/article/2")
        
        assert id1 != id2


class TestEmbeddings:
    """Tests for embeddings module."""
    
    def test_embedding_model_loads(self):
        """Test that embedding model loads successfully."""
        model = get_embedding_model()
        assert model is not None
    
    def test_embed_text_returns_vector(self):
        """Test that embed_text returns a vector."""
        text = "This is a test sentence about artificial intelligence."
        embedding = embed_text(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embedding_dimensionality(self):
        """Test embedding dimensions for the default model."""
        embedding = embed_text("Test text")
        # all-MiniLM-L6-v2 produces 384-dimensional embeddings
        assert len(embedding) == 384
    
    def test_text_splitter_configuration(self):
        """Test text splitter is configured correctly."""
        splitter = get_text_splitter()
        
        assert splitter._chunk_size == settings.CHUNK_SIZE
        assert splitter._chunk_overlap == settings.CHUNK_OVERLAP


class TestVectorStore:
    """Tests for vector store module."""
    
    def test_articles_to_documents_conversion(self):
        """Test converting articles to documents."""
        articles = [
            Article(
                id="test1",
                title="Test Article 1",
                content="This is the content of test article one. " * 50,
                summary="Summary 1",
                source="Test Source",
                url="https://example.com/1",
                published_date=datetime.now(),
            )
        ]
        
        documents = articles_to_documents(articles)
        
        assert len(documents) >= 1
        assert documents[0].metadata["article_id"] == "test1"
        assert documents[0].metadata["source"] == "Test Source"
    
    def test_document_metadata_complete(self):
        """Test that document metadata is complete."""
        articles = [
            Article(
                id="test1",
                title="Test Title",
                content="Test content",
                summary="Summary",
                source="Source",
                url="https://example.com",
                published_date=datetime(2024, 1, 15),
            )
        ]
        
        documents = articles_to_documents(articles)
        metadata = documents[0].metadata
        
        assert "article_id" in metadata
        assert "title" in metadata
        assert "source" in metadata
        assert "url" in metadata
        assert "published_date" in metadata
        assert "chunk_index" in metadata


class TestIntegration:
    """Integration tests for the RAG pipeline."""
    
    @pytest.mark.slow
    def test_fetch_real_feed(self):
        """Test fetching from a real RSS feed."""
        # Using Hacker News as it's reliable
        articles = fetch_feed("Hacker News", "https://hnrss.org/frontpage")
        
        # Should fetch at least some articles (may be 0 if network issues)
        assert isinstance(articles, list)
        
        if articles:
            assert articles[0].title
            assert articles[0].url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

