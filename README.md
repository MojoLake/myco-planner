# MyCourses Web Scraper

A Python-based web scraper for Aalto University's MyCourses platform that handles two-factor authentication (2FA) using session cookies.

## Overview

This tool provides two methods to scrape content from MyCourses:

1. **Cookie-based scraper** (`scraper.py`) - Fast, uses saved session cookies
2. **Browser automation** (`scraper_selenium.py`) - Interactive login with Selenium

## Configuration

The project keeps runtime configuration in `config.json` at the repository root. The committed defaults point to a local Ollama instance and the `gemma3` model:

```json
{
  "ollama": {
    "url": "http://localhost:11434",
    "model": "gemma3"
  }
}
```

Update the fields to match your environment:

- `ollama.url` &mdash; the base URL where Ollama is reachable (use custom ports or remote hosts as needed).
- `ollama.model` &mdash; the model name to load when running the test script.

### Session Cookie

Store your Moodle session cookie in the `.cookie` file located at the repository root. This file is git-ignored. Paste the raw cookie value (no JSON formatting) to authenticate the cookie-based scraper.

## Testing Ollama Connectivity

Use `test_ollama.py` to confirm Ollama is reachable before running scrapers:

```bash
python test_ollama.py
```

The script reads configuration from `config.json`, connects to the configured endpoint, and reports helpful guidance if configuration issues are detected. Update the config file to try different models or endpoints without touching the code.
