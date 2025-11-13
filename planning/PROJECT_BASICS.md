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

1. **MyCourses Calendar Export** → Fetch iCalendar feed with course events and deadlines
2. **ICS Parser** → Normalize calendar events into structured tasks
3. **Local Ollama LLM** → Prioritize tasks and generate personalized todo lists

### Key Files

- `calendar_feed_url.txt` → Stores the authenticated MyCourses calendar export link
- `config.json` → Ollama server URL and model configuration
- `pyproject.toml` → Dependencies managed by uv

### Data Flow

```
MyCourses → Calendar Export (ICS) → Parser → Structured Events → Local LLM → Todo Lists
```

**Privacy-first**: All processing happens locally, no external APIs.
