"""
RAG Chain Module
================
Implements the Retrieval-Augmented Generation pipeline for news summarization.
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.schema.runnable import RunnablePassthrough
from typing import Optional
import requests

from app.config import settings
from app.vector_store import search_similar, get_collection_stats


# Prompt template for news summarization
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful news analyst assistant. Your task is to provide accurate, 
well-structured summaries based on the news articles provided in the context.

CONTEXT (Retrieved News Articles):
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Analyze the provided news articles carefully
2. Synthesize information from multiple sources when available
3. Provide a clear, concise summary that answers the user's question
4. Mention the sources of information when relevant
5. If the context doesn't contain enough information, acknowledge this limitation
6. Use bullet points for key facts when appropriate

SUMMARY:"""
)


def check_ollama_available() -> tuple[bool, str]:
    """
    Check if Ollama is running and the required model is available.
    
    Returns:
        Tuple of (is_available, status_message)
    """
    try:
        # Check if Ollama server is running
        response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            return False, "Ollama server is not responding correctly"
        
        # Check if the required model is available
        models = response.json().get("models", [])
        model_names = [m.get("name", "").split(":")[0] for m in models]
        
        required_model = settings.OLLAMA_MODEL.split(":")[0]
        if required_model not in model_names:
            return False, f"Model '{settings.OLLAMA_MODEL}' not found. Run: ollama pull {settings.OLLAMA_MODEL}"
        
        return True, f"Ollama ready with model: {settings.OLLAMA_MODEL}"
        
    except requests.exceptions.ConnectionError:
        return False, "Ollama is not running. Start it with: ollama serve"
    except Exception as e:
        return False, f"Error checking Ollama: {str(e)}"


def get_llm() -> OllamaLLM:
    """
    Get the Ollama LLM instance.
    
    Returns:
        OllamaLLM instance
    """
    return OllamaLLM(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.3,  # Lower temperature for more factual responses
    )


def format_documents(docs: list[Document]) -> str:
    """
    Format retrieved documents into a context string.
    
    Args:
        docs: List of Document objects
        
    Returns:
        Formatted context string
    """
    if not docs:
        return "No relevant articles found."
    
    formatted_parts = []
    seen_titles = set()
    
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get("title", "Untitled")
        
        # Avoid duplicate titles in context
        if title in seen_titles:
            continue
        seen_titles.add(title)
        
        source = doc.metadata.get("source", "Unknown")
        date = doc.metadata.get("published_date", "")
        
        formatted_parts.append(
            f"[Article {i}]\n"
            f"Title: {title}\n"
            f"Source: {source}\n"
            f"Date: {date}\n"
            f"Content: {doc.page_content}\n"
        )
    
    return "\n---\n".join(formatted_parts)


def summarize_news(
    query: str,
    k: int = None,
    return_sources: bool = True
) -> dict:
    """
    Main RAG function: Retrieve relevant articles and generate a summary.
    
    Args:
        query: User's question or topic
        k: Number of documents to retrieve
        return_sources: Whether to include source information
        
    Returns:
        Dictionary with summary and optional source information
    """
    # Check if we have any indexed documents
    stats = get_collection_stats()
    if stats.get("document_count", 0) == 0:
        return {
            "summary": "No news articles have been indexed yet. Please fetch and index some articles first.",
            "sources": [],
            "status": "no_data"
        }
    
    # Retrieve relevant documents
    if k is None:
        k = settings.TOP_K_RESULTS
    
    docs = search_similar(query, k=k)
    
    if not docs:
        return {
            "summary": "No relevant articles found for your query. Try a different search term.",
            "sources": [],
            "status": "no_results"
        }
    
    # Format context
    context = format_documents(docs)
    
    # Check Ollama availability
    ollama_available, ollama_status = check_ollama_available()
    
    if not ollama_available:
        # Return just the retrieved context if LLM is not available
        return {
            "summary": f"⚠️ LLM not available: {ollama_status}\n\nRetrieved articles:\n\n{context}",
            "sources": _extract_sources(docs),
            "status": "llm_unavailable"
        }
    
    # Generate summary using LLM
    try:
        llm = get_llm()
        prompt = SUMMARY_PROMPT.format(context=context, question=query)
        summary = llm.invoke(prompt)
        
        result = {
            "summary": summary,
            "status": "success"
        }
        
        if return_sources:
            result["sources"] = _extract_sources(docs)
        
        return result
        
    except Exception as e:
        return {
            "summary": f"Error generating summary: {str(e)}\n\nRetrieved context:\n\n{context}",
            "sources": _extract_sources(docs),
            "status": "error"
        }


def _extract_sources(docs: list[Document]) -> list[dict]:
    """
    Extract unique source information from documents.
    
    Args:
        docs: List of Document objects
        
    Returns:
        List of source dictionaries
    """
    seen_urls = set()
    sources = []
    
    for doc in docs:
        url = doc.metadata.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            sources.append({
                "title": doc.metadata.get("title", "Untitled"),
                "source": doc.metadata.get("source", "Unknown"),
                "url": url,
                "date": doc.metadata.get("published_date", ""),
            })
    
    return sources


if __name__ == "__main__":
    # Test the RAG chain
    print("Testing RAG chain...")
    
    # Check Ollama
    available, status = check_ollama_available()
    print(f"Ollama status: {status}")
    
    # Test summarization
    result = summarize_news("What are the latest technology news?")
    print(f"\nSummary:\n{result['summary']}")
    print(f"\nSources: {len(result.get('sources', []))} articles")

