"""
RAG News Summarizer - Streamlit Web Interface
==============================================
A beautiful, modern UI for the RAG-powered news summarization system.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports to work with Streamlit
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime

from app.config import settings
from app.news_fetcher import fetch_all_feeds
from app.vector_store import index_articles, search_similar, get_collection_stats, clear_collection
from app.rag_chain import summarize_news, check_ollama_available


# Page configuration
st.set_page_config(
    page_title="RAG News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Theme configurations
THEMES = {
    "dark": {
        "primary": "#6366f1",
        "primary_dark": "#4f46e5",
        "accent": "#f59e0b",
        "bg": "#0f172a",
        "bg_card": "#1e293b",
        "text_primary": "#f1f5f9",
        "text_secondary": "#94a3b8",
        "border": "#334155",
        "gradient_start": "#6366f1",
        "gradient_end": "#a855f7",
    },
    "light": {
        "primary": "#4f46e5",
        "primary_dark": "#4338ca",
        "accent": "#d97706",
        "bg": "#f8fafc",
        "bg_card": "#ffffff",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "border": "#e2e8f0",
        "gradient_start": "#4f46e5",
        "gradient_end": "#7c3aed",
    }
}

# Get current theme
current_theme = THEMES[st.session_state.theme]

# Custom CSS for a modern, polished look
st.markdown(f"""
<style>
    /* Import custom font */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables */
    :root {{
        --primary: {current_theme["primary"]};
        --primary-dark: {current_theme["primary_dark"]};
        --accent: {current_theme["accent"]};
        --bg-dark: {current_theme["bg"]};
        --bg-card: {current_theme["bg_card"]};
        --text-primary: {current_theme["text_primary"]};
        --text-secondary: {current_theme["text_secondary"]};
    }}
    
    /* Main container styling */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Theme-aware body background */
    .stApp {{
        background-color: {current_theme["bg"]};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        color: {current_theme["text_primary"]} !important;
    }}
    
    /* Custom header */
    .main-header {{
        background: linear-gradient(135deg, {current_theme["gradient_start"]} 0%, #8b5cf6 50%, {current_theme["gradient_end"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    .sub-header {{
        text-align: center;
        color: {current_theme["text_secondary"]};
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
    
    /* Cards */
    .stat-card {{
        background: linear-gradient(145deg, {current_theme["bg_card"]} 0%, {current_theme["border"]} 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid {current_theme["border"]};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {current_theme["primary"]};
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    .stat-label {{
        color: {current_theme["text_secondary"]};
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Source cards */
    .source-card {{
        background: {current_theme["bg_card"]};
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid {current_theme["primary"]};
    }}
    
    .source-title {{
        font-weight: 600;
        color: {current_theme["text_primary"]};
        margin-bottom: 0.25rem;
    }}
    
    .source-meta {{
        color: {current_theme["text_secondary"]};
        font-size: 0.85rem;
    }}
    
    /* Status badges */
    .status-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }}
    
    .status-success {{
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }}
    
    .status-warning {{
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
    }}
    
    .status-error {{
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {current_theme["bg"]} 0%, {current_theme["bg_card"]} 100%);
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: {current_theme["text_primary"]};
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {current_theme["primary"]} 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }}
    
    /* Text input styling */
    .stTextInput > div > div > input {{
        background: {current_theme["bg_card"]};
        border: 1px solid {current_theme["border"]};
        border-radius: 8px;
        color: {current_theme["text_primary"]};
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {current_theme["primary"]};
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: {current_theme["bg_card"]};
        border-radius: 8px;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">📰 RAG News Summarizer</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">AI-powered news analysis using Retrieval-Augmented Generation</p>',
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render the sidebar with controls and status."""
    with st.sidebar:
        # Theme toggle at the top
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("## ⚙️ Controls")
        with col2:
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            if st.button(theme_icon, key="theme_toggle", help="Toggle dark/light theme"):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
        
        # System status
        st.markdown("### 📊 System Status")
        
        # Ollama status
        ollama_ok, ollama_msg = check_ollama_available()
        if ollama_ok:
            st.success(f"✅ {ollama_msg}")
        else:
            st.warning(f"⚠️ {ollama_msg}")
        
        # Collection stats
        stats = get_collection_stats()
        doc_count = stats.get("document_count", 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📄 Documents", doc_count)
        with col2:
            st.metric("🔍 Model", settings.EMBEDDING_MODEL[:10] + "...")
        
        st.divider()
        
        # Data management
        st.markdown("### 📥 Data Management")
        
        if st.button("🔄 Fetch & Index News", use_container_width=True):
            with st.spinner("Fetching news from RSS feeds..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress, message):
                    progress_bar.progress(progress)
                    status_text.text(message)
                
                # Fetch articles
                articles = fetch_all_feeds(progress_callback=update_progress)
                
                if articles:
                    status_text.text("Indexing articles...")
                    indexed = index_articles(articles, progress_callback=update_progress)
                    progress_bar.progress(1.0)
                    st.success(f"✅ Indexed {indexed} new chunks from {len(articles)} articles")
                else:
                    st.warning("No articles fetched")
                
                progress_bar.empty()
                status_text.empty()
        
        if st.button("🗑️ Clear Database", use_container_width=True):
            if clear_collection():
                st.success("Database cleared!")
                st.rerun()
        
        st.divider()
        
        # News sources
        st.markdown("### 📡 News Sources")
        for source in settings.RSS_FEEDS.keys():
            st.markdown(f"• {source}")
        
        st.divider()
        
        # About section
        st.markdown("### ℹ️ About")
        st.markdown("""
        This project demonstrates a **RAG (Retrieval-Augmented Generation)** 
        pipeline for news summarization.
        
        **Tech Stack:**
        - 🔤 Embeddings: Sentence-Transformers
        - 🗄️ Vector DB: ChromaDB
        - 🤖 LLM: Ollama (Local)
        - 🎨 UI: Streamlit
        """)


def render_main_content():
    """Render the main content area."""
    # Query input
    st.markdown("### 🔍 Ask about the news")
    
    query = st.text_input(
        "Enter your question or topic",
        placeholder="e.g., What are the latest developments in AI?",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        num_results = st.selectbox("Results", [3, 5, 7, 10], index=1)
    with col2:
        search_clicked = st.button("🚀 Summarize", use_container_width=True)
    
    if search_clicked and query:
        with st.spinner("Analyzing news articles..."):
            result = summarize_news(query, k=num_results)
        
        # Display status
        status = result.get("status", "unknown")
        if status == "success":
            st.markdown('<span class="status-badge status-success">✓ Analysis Complete</span>', 
                       unsafe_allow_html=True)
        elif status == "llm_unavailable":
            st.markdown('<span class="status-badge status-warning">⚠ LLM Unavailable - Showing Retrieved Articles</span>', 
                       unsafe_allow_html=True)
        elif status == "no_data":
            st.markdown('<span class="status-badge status-error">✗ No Data</span>', 
                       unsafe_allow_html=True)
        
        # Display summary
        st.markdown("### 📝 Summary")
        st.markdown(result.get("summary", "No summary available."))
        
        # Display sources
        sources = result.get("sources", [])
        if sources:
            st.markdown("### 📚 Sources")
            for source in sources:
                with st.container():
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-title">{source.get('title', 'Untitled')}</div>
                        <div class="source-meta">
                            📰 {source.get('source', 'Unknown')} • 
                            📅 {source.get('date', 'No date')[:10] if source.get('date') else 'No date'}
                        </div>
                        <a href="{source.get('url', '#')}" target="_blank">🔗 Read full article</a>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif search_clicked and not query:
        st.warning("Please enter a question or topic to search.")
    
    # Show quick actions if no search
    if not search_clicked:
        st.markdown("### 💡 Quick Topics")
        
        topics = [
            ("🤖 AI & Technology", "What are the latest developments in artificial intelligence?"),
            ("🌍 World News", "Summarize the major world news and international events"),
            ("💰 Business & Finance", "What's happening in the business and financial world?"),
            ("🔬 Science", "What are the recent scientific discoveries and breakthroughs?"),
        ]
        
        cols = st.columns(2)
        for idx, (label, topic_query) in enumerate(topics):
            with cols[idx % 2]:
                if st.button(label, key=f"topic_{idx}", use_container_width=True):
                    st.session_state["quick_query"] = topic_query
                    st.rerun()
        
        # Handle quick query
        if "quick_query" in st.session_state:
            query = st.session_state.pop("quick_query")
            with st.spinner("Analyzing news articles..."):
                result = summarize_news(query, k=5)
            
            st.markdown("### 📝 Summary")
            st.markdown(result.get("summary", "No summary available."))
            
            sources = result.get("sources", [])
            if sources:
                with st.expander(f"📚 View {len(sources)} Sources"):
                    for source in sources:
                        st.markdown(f"**{source.get('title', 'Untitled')}**")
                        st.caption(f"{source.get('source', 'Unknown')} • [Read more]({source.get('url', '#')})")


def main():
    """Main application entry point."""
    render_header()
    render_sidebar()
    render_main_content()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; padding: 1rem;">
            Built with ❤️ using LangChain, ChromaDB, Ollama & Streamlit<br>
            <small>RAG News Summarizer v1.0</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

