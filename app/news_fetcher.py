"""
News Fetcher Module
===================
Fetches and parses news articles from RSS feeds.
"""

import feedparser
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import hashlib
import requests
from time import mktime

from app.config import settings


@dataclass
class Article:
    """Represents a news article with metadata."""
    
    id: str
    title: str
    content: str
    summary: str
    source: str
    url: str
    published_date: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert article to dictionary for storage."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "source": self.source,
            "url": self.url,
            "published_date": self.published_date.isoformat() if self.published_date else None,
        }


def generate_article_id(url: str) -> str:
    """Generate a unique ID for an article based on its URL."""
    return hashlib.md5(url.encode()).hexdigest()


def parse_rss_date(entry: dict) -> Optional[datetime]:
    """Parse the published date from an RSS entry."""
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime.fromtimestamp(mktime(entry.published_parsed))
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        return datetime.fromtimestamp(mktime(entry.updated_parsed))
    return None


def fetch_feed(source_name: str, feed_url: str, timeout: int = 10) -> list[Article]:
    """
    Fetch articles from a single RSS feed.
    
    Args:
        source_name: Human-readable name of the news source
        feed_url: URL of the RSS feed
        timeout: Request timeout in seconds
        
    Returns:
        List of Article objects
    """
    articles = []
    
    try:
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)
        
        if feed.bozo and feed.bozo_exception:
            print(f"⚠️  Warning parsing {source_name}: {feed.bozo_exception}")
        
        for entry in feed.entries:
            # Extract content - try different fields
            content = ""
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', '')
            elif hasattr(entry, 'description'):
                content = entry.description
            elif hasattr(entry, 'summary'):
                content = entry.summary
            
            # Get summary (usually shorter than content)
            summary = getattr(entry, 'summary', content[:500] if content else "")
            
            # Create article object
            article = Article(
                id=generate_article_id(entry.link),
                title=entry.title,
                content=content if content else summary,
                summary=summary,
                source=source_name,
                url=entry.link,
                published_date=parse_rss_date(entry),
            )
            articles.append(article)
            
    except Exception as e:
        print(f"❌ Error fetching {source_name}: {e}")
    
    return articles


def fetch_all_feeds(
    feeds: Optional[dict[str, str]] = None,
    progress_callback: Optional[callable] = None
) -> list[Article]:
    """
    Fetch articles from all configured RSS feeds.
    
    Args:
        feeds: Dictionary of {source_name: feed_url}. Uses config defaults if None.
        progress_callback: Optional callback for progress updates (for UI)
        
    Returns:
        List of all fetched Article objects
    """
    if feeds is None:
        feeds = settings.RSS_FEEDS
    
    all_articles = []
    total_feeds = len(feeds)
    
    for idx, (source_name, feed_url) in enumerate(feeds.items(), 1):
        if progress_callback:
            progress_callback(idx / total_feeds, f"Fetching {source_name}...")
        
        articles = fetch_feed(source_name, feed_url)
        all_articles.extend(articles)
        print(f"✅ Fetched {len(articles)} articles from {source_name}")
    
    # Remove duplicates based on article ID
    seen_ids = set()
    unique_articles = []
    for article in all_articles:
        if article.id not in seen_ids:
            seen_ids.add(article.id)
            unique_articles.append(article)
    
    print(f"\n📰 Total unique articles fetched: {len(unique_articles)}")
    return unique_articles


if __name__ == "__main__":
    # Test the news fetcher
    articles = fetch_all_feeds()
    for article in articles[:3]:
        print(f"\n{'='*50}")
        print(f"Title: {article.title}")
        print(f"Source: {article.source}")
        print(f"Date: {article.published_date}")
        print(f"URL: {article.url}")

