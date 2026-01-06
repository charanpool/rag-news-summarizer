"""
Configuration settings for the RAG News Summarizer.
Uses pydantic-settings for type-safe configuration management.
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with sensible defaults for local development."""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    CHROMA_DB_DIR: Path = DATA_DIR / "chroma_db"

    # Embedding model (runs locally via sentence-transformers)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Ollama settings (local LLM)
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # ChromaDB settings
    COLLECTION_NAME: str = "news_articles"
    
    # RAG settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    
    # News sources (RSS feeds)
    RSS_FEEDS: dict = {
        "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "BBC Tech": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "Reuters World": "https://feeds.reuters.com/Reuters/worldNews",
        "TechCrunch": "https://techcrunch.com/feed/",
        "Hacker News": "https://hnrss.org/frontpage",
        "ArsTechnica": "https://feeds.arstechnica.com/arstechnica/index",
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


# Global settings instance
settings = Settings()

# Ensure data directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

