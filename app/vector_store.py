"""
Vector Store Module
===================
Manages ChromaDB vector database for storing and retrieving article embeddings.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain.schema import Document
from typing import Optional

from app.config import settings
from app.embeddings import get_embedding_model, get_text_splitter
from app.news_fetcher import Article


# Singleton instances to avoid "different settings" error
_chroma_client: Optional[chromadb.PersistentClient] = None
_vector_store: Optional[Chroma] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Get or create a persistent ChromaDB client (singleton).
    
    Returns:
        ChromaDB PersistentClient instance
    """
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB_DIR),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
    return _chroma_client


def get_vector_store() -> Chroma:
    """
    Get the LangChain Chroma vector store wrapper (singleton).
    
    Returns:
        Chroma vector store instance
    """
    global _vector_store
    if _vector_store is None:
        embedding_model = get_embedding_model()
        client = get_chroma_client()
        
        _vector_store = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=embedding_model,
            client=client,
        )
    return _vector_store


def articles_to_documents(articles: list[Article]) -> list[Document]:
    """
    Convert Article objects to LangChain Document objects with chunking.
    
    Args:
        articles: List of Article objects
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = get_text_splitter()
    documents = []
    
    for article in articles:
        # Combine title and content for better context
        full_text = f"Title: {article.title}\n\n{article.content}"
        
        # Create metadata
        metadata = {
            "article_id": article.id,
            "title": article.title,
            "source": article.source,
            "url": article.url,
            "published_date": article.published_date.isoformat() if article.published_date else "",
        }
        
        # Split into chunks
        chunks = text_splitter.split_text(full_text)
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={**metadata, "chunk_index": i}
            )
            documents.append(doc)
    
    return documents


def index_articles(
    articles: list[Article],
    progress_callback: Optional[callable] = None
) -> int:
    """
    Index articles into the vector store.
    
    Args:
        articles: List of Article objects to index
        progress_callback: Optional callback for progress updates
        
    Returns:
        Number of document chunks indexed
    """
    if not articles:
        print("⚠️  No articles to index")
        return 0
    
    # Convert to documents
    if progress_callback:
        progress_callback(0.3, "Converting articles to documents...")
    
    documents = articles_to_documents(articles)
    print(f"📄 Created {len(documents)} document chunks from {len(articles)} articles")
    
    # Get vector store
    if progress_callback:
        progress_callback(0.5, "Loading vector store...")
    
    vector_store = get_vector_store()
    
    # Get existing IDs to avoid duplicates
    if progress_callback:
        progress_callback(0.6, "Checking for duplicates...")
    
    try:
        existing_data = vector_store.get()
        existing_ids = set(existing_data.get('ids', []))
    except Exception:
        existing_ids = set()
    
    # Filter out documents that already exist (based on article_id + chunk_index)
    new_documents = []
    for doc in documents:
        doc_id = f"{doc.metadata['article_id']}_{doc.metadata['chunk_index']}"
        if doc_id not in existing_ids:
            new_documents.append(doc)
    
    if not new_documents:
        print("ℹ️  All articles already indexed")
        return 0
    
    # Add new documents
    if progress_callback:
        progress_callback(0.8, f"Indexing {len(new_documents)} new chunks...")
    
    # Generate IDs for new documents
    ids = [f"{doc.metadata['article_id']}_{doc.metadata['chunk_index']}" for doc in new_documents]
    
    vector_store.add_documents(new_documents, ids=ids)
    
    print(f"✅ Indexed {len(new_documents)} new document chunks")
    return len(new_documents)


def search_similar(query: str, k: int = None) -> list[Document]:
    """
    Search for documents similar to the query.
    
    Args:
        query: Search query text
        k: Number of results to return (defaults to settings.TOP_K_RESULTS)
        
    Returns:
        List of relevant Document objects
    """
    if k is None:
        k = settings.TOP_K_RESULTS
    
    vector_store = get_vector_store()
    
    try:
        results = vector_store.similarity_search(query, k=k)
        return results
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []


def get_collection_stats() -> dict:
    """
    Get statistics about the vector store collection.
    
    Returns:
        Dictionary with collection statistics
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection(settings.COLLECTION_NAME)
        count = collection.count()
        
        return {
            "collection_name": settings.COLLECTION_NAME,
            "document_count": count,
            "embedding_model": settings.EMBEDDING_MODEL,
        }
    except Exception as e:
        return {
            "collection_name": settings.COLLECTION_NAME,
            "document_count": 0,
            "error": str(e),
        }


def clear_collection() -> bool:
    """
    Clear all documents from the collection.
    
    Returns:
        True if successful, False otherwise
    """
    global _vector_store
    try:
        client = get_chroma_client()
        client.delete_collection(settings.COLLECTION_NAME)
        # Reset vector store singleton so it gets recreated with fresh collection
        _vector_store = None
        print("🗑️  Collection cleared")
        return True
    except Exception as e:
        print(f"❌ Error clearing collection: {e}")
        return False


if __name__ == "__main__":
    # Test vector store
    stats = get_collection_stats()
    print(f"Collection stats: {stats}")
    
    # Test search
    results = search_similar("artificial intelligence news")
    print(f"\nSearch results: {len(results)} documents found")
    for doc in results[:2]:
        print(f"  - {doc.metadata.get('title', 'No title')[:50]}...")

