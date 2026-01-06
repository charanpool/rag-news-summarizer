# 🤝 Contributing to RAG News Summarizer

First off, thank you for considering contributing! This project was built as a learning tool and portfolio piece, and contributions from the community make it even better.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

Just be kind and have fun! We're all here to learn and build cool things together. 🙂

---

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? No worries — just open an issue and include:

1. What happened vs what you expected
2. Steps to reproduce (if you can)
3. Any error messages or screenshots

### 💡 Suggesting Features

Got an idea? We'd love to hear it! Feel free to:

1. Check [ROADMAP.md](ROADMAP.md) to see if it's already planned
2. Open an issue describing your idea
3. Share why it would be useful

### 📝 Improving Documentation

Documentation improvements are always appreciated:

- Fix typos or unclear explanations
- Add examples or use cases
- Improve code comments
- Translate documentation

### 🧑‍💻 Contributing Code

Code contributions are welcome for:

- Bug fixes
- New features (check roadmap first)
- Performance improvements
- Test coverage improvements
- Refactoring (with justification)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- [Ollama](https://ollama.ai/) (for local LLM)

### Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/charanpool/rag-news-summarizer.git
cd rag-news-summarizer

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run tests to verify setup
pytest tests/ -v
```

---

## 🔄 Development Workflow

### 1. Create a Branch

```bash
# For features
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-description

# For documentation
git checkout -b docs/what-you-changed
```

### 2. Make Your Changes

Just try to keep things readable and consistent with the existing code style. Tests are appreciated but not mandatory for small fixes!

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run with coverage (optional)
pytest tests/ --cov=app --cov-report=html
```

### 4. Commit Your Changes

Follow conventional commit messages:

```bash
# Format: <type>: <description>

git commit -m "feat: add support for custom RSS feeds"
git commit -m "fix: resolve embedding dimension mismatch"
git commit -m "docs: update installation instructions"
git commit -m "refactor: simplify vector store logic"
git commit -m "test: add tests for news fetcher"
```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
git push origin your-branch-name
```

Then open a Pull Request on GitHub.

---

## 🎨 Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) conventions
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use f-strings for string formatting

### Docstrings

Use Google-style docstrings:

```python
def fetch_articles(source: str, limit: int = 10) -> list[Article]:
    """
    Fetch articles from a news source.

    Args:
        source: Name of the news source
        limit: Maximum number of articles to fetch

    Returns:
        List of Article objects

    Raises:
        ConnectionError: If the source is unreachable
    """
```

### Type Hints

Use type hints for function signatures:

```python
def summarize_news(query: str, k: int = 5) -> dict[str, Any]:
    ...
```

### Imports

Organize imports in this order:

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import os
from datetime import datetime

# Third-party
import streamlit as st
from langchain.schema import Document

# Local
from app.config import settings
from app.vector_store import search_similar
```

---

## 📥 Pull Request Process

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] All tests pass locally
- [ ] New code has appropriate tests
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventions

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How did you test these changes?

## Related Issues
Fixes #(issue number)
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

---

## 🆘 Need Help?

- Open an issue for questions
- Check existing issues and discussions
- Review the [README.md](README.md) and [docs/](docs/)

---

## 🙏 Recognition

Contributors will be recognized in:
- The repository's contributor list
- Release notes for significant contributions

Thank you for helping make this project better! 🎉

