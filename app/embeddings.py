"""
Embeddings Module
=================
Handles text embedding generation using sentence-transformers.
Runs entirely locally without API calls.
"""

from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import settings


# Cache the model to avoid reloading
_embedding_model = None


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Get or create the embedding model instance.
    Uses HuggingFace embeddings compatible with LangChain.
    
    Returns:
        HuggingFaceEmbeddings instance
    """
    global _embedding_model
    
    if _embedding_model is None:
        print(f"🔄 Loading embedding model: {settings.EMBEDDING_MODEL}")
        _embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✅ Embedding model loaded successfully")
    
    return _embedding_model


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create a text splitter for chunking documents.
    
    Returns:
        Configured RecursiveCharacterTextSplitter
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def embed_text(text: str) -> list[float]:
    """
    Generate embedding for a single text string.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    model = get_embedding_model()
    return model.embed_query(text)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple text strings.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    model = get_embedding_model()
    return model.embed_documents(texts)


if __name__ == "__main__":
    # Test embedding generation
    test_text = "This is a test sentence about artificial intelligence and machine learning."
    
    embedding = embed_text(test_text)
    print(f"Generated embedding with {len(embedding)} dimensions")
    print(f"First 5 values: {embedding[:5]}")

