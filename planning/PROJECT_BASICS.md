# Project Basics

## Package Management

**uv** is used for both package and environment management:

```bash
uv sync              # Install dependencies and create virtual environment
uv add <package>     # Add new dependency
uv run python main.py # Run commands in the managed environment
```

## High-Level Overview

**MyCo Planner** extracts academic data from Aalto University's MyCourses platform and generates personalized todo lists.

### Architecture
1. **ScrapeGraph AI** → Extract structured data from MyCourses HTML
2. **Local Ollama LLM** → Analyze scraped data and generate todo lists  
3. **Cookie Authentication** → Bypass 2FA using stored session cookies

### Key Files
- `.cookie` → MoodleSession cookie for authentication
- `config.json` → Ollama server URL and model configuration
- `pyproject.toml` → Dependencies managed by uv

### Data Flow
```
MyCourses → ScrapeGraph AI → Structured Data → Local LLM → Todo Lists
```

**Privacy-first**: All processing happens locally, no external APIs.