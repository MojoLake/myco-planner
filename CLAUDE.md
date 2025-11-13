# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MyCo Planner ingests the authenticated calendar export from Aalto University's MyCourses platform, then analyzes the resulting events with a local LLM to generate personalized todo lists for students.

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

- **Calendar Feed Client**: Fetches the private MyCourses iCal feed
- **ICS Parser**: Normalizes calendar events into structured data
- **Local LLM**: Transforms events into prioritized todo lists

### Data Flow

```
MyCourses Calendar Export → ICS Parser → Structured Events → Local LLM → Todo List
```

## Configuration

**Calendar Feed URL:**

- Private tokenized link stored in `calendar_feed_url.txt` (git-ignored)

## Key Dependencies

- `ics`: Calendar parsing library
- `pydantic`: Data validation and schemas
- `requests`: HTTP client for authentication setup

## Development Notes

- **Authentication**: Relies on personalized calendar export token stored locally
- **Calendar Parsing**: ICS feed provides lectures, deadlines, and events
- **Local Processing**: Todo list generation happens locally for privacy
- **Target Platform**: Aalto University MyCourses (Moodle-based LMS)
