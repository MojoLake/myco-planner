# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MyCo Planner uses ScrapeGraph AI to extract data from Aalto University's MyCourses platform, then analyzes this data with a local LLM to generate personalized todo lists for students.

## Development Commands

**Package Management (uv):**
```bash
uv sync              # Install dependencies
uv add <package>     # Add new dependency
```

**Running the Application:**
```bash
python main.py       # Main entry point
```

## Architecture

### Core Components
- **ScrapeGraph AI**: Web scraping with AI-powered data extraction
- **Local LLM**: Analyze scraped data to generate todo lists
- **Session Management**: MoodleSession cookie authentication via `.cookie` file

### Data Flow
```
MyCourses URL → ScrapeGraph AI + Cookie → Structured Data → Local LLM → Todo List
```

## Configuration

**Cookie Storage:**
- MoodleSession cookie stored in `.cookie` file as plain text

## Key Dependencies

- `scrapegraphai`: AI-powered web scraping framework
- `scrapegraph-py`: Python client for ScrapeGraph
- `pydantic`: Data validation and schemas
- `requests`: HTTP client for authentication setup

## Development Notes

- **Authentication**: Uses MoodleSession cookies stored in `.cookie` file
- **AI Scraping**: ScrapeGraph handles complex HTML extraction automatically
- **Local Processing**: Todo list generation happens locally for privacy
- **Target Platform**: Aalto University MyCourses (Moodle-based LMS)