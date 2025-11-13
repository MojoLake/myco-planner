# MyCourses Web Scraper

A Python-based web scraper for Aalto University's MyCourses platform that handles two-factor authentication (2FA) using session cookies.

## Overview

This tool provides two methods to scrape content from MyCourses:

1. **Cookie-based scraper** (`scraper.py`) - Fast, uses saved session cookies
2. **Browser automation** (`scraper_selenium.py`) - Interactive login with Selenium

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) For Selenium Method

If you plan to use `scraper_selenium.py`, install ChromeDriver:

**macOS:**

```bash
brew install chromedriver
```

**Linux/Windows:**
Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/)

## Usage

### Method 1: Cookie-Based Scraper (Recommended)

The main scraper uses session cookies for authentication.

```bash
python scraper.py
```

**First Run:**

- If no cookie is found, you'll be prompted to enter your `MoodleSession` cookie
- The cookie will be saved to `config.json` for future use

**Subsequent Runs:**

- Automatically uses the stored cookie from `config.json`
- No need to log in again until the session expires

### Method 2: Browser Automation

Use this method if you want the script to handle login through browser automation:

```bash
python scraper_selenium.py
```

**How it works:**

1. Opens Chrome browser
2. Navigates to MyCourses
3. Waits for you to log in manually (including 2FA)
4. Extracts and saves the session cookie
5. Scrapes the page content

The saved cookie can then be used with `scraper.py` for faster access.

## Getting Your Session Cookie

### Option 1: Browser DevTools (Chrome/Firefox)

1. **Log into MyCourses** in your browser (complete 2FA)
2. **Open DevTools** - Press `F12` or right-click → Inspect
3. **Navigate to Cookies:**
   - Chrome: `Application` tab → `Storage` → `Cookies` → `https://mycourses.aalto.fi`
   - Firefox: `Storage` tab → `Cookies` → `https://mycourses.aalto.fi`
4. **Find `MoodleSession`** in the cookie list
5. **Copy the Value** (double-click to select, then copy)
6. **Paste** into `scraper.py` when prompted, or add to `config.json` manually

### Option 2: Browser Extension

Use a cookie export extension:

- [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/) (Chrome)
- [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) (Firefox)

Export cookies from `mycourses.aalto.fi` and extract the `MoodleSession` value.

### Option 3: Use Selenium Script

Simply run `scraper_selenium.py` and it will extract the cookie after you log in.

## Configuration

### config.json Format

The scraper stores cookies in `config.json`:

```json
{
  "MoodleSession": "your_session_cookie_value_here"
}
```

You can manually create or edit this file if needed.

## Features

Both scrapers will:

- ✅ Authenticate using session cookies
- ✅ Detect expired sessions
- ✅ Parse and display course information
- ✅ Extract course sections
- ✅ List activities and resources
- ✅ Show announcements
- ✅ Display page content

## Output Example

```
MyCourses Web Scraper
============================================================
Using stored MoodleSession cookie from config.json

Fetching: https://mycourses.aalto.fi/course/view.php?id=47384

============================================================
PAGE CONTENT
============================================================

Page Title: Course Name - MyCourses

Course Name: Introduction to Computer Science

Found 12 course sections:

  1. Week 1: Introduction
  2. Week 2: Python Basics
  3. Week 3: Data Structures
  ...

Found 45 activities/resources:

  1. Lecture Slides
  2. Assignment 1
  3. Reading Material
  ...

============================================================
Full HTML length: 125643 characters
============================================================

✓ Scraping completed successfully!
```

## Troubleshooting

### "Session expired or invalid cookie"

Your cookie has expired. Get a fresh one by:

- Logging into MyCourses again in your browser
- Extracting a new cookie using one of the methods above
- Or running `scraper_selenium.py` to automatically get a new cookie

### "Could not start Chrome WebDriver"

For `scraper_selenium.py`, ensure ChromeDriver is installed:

```bash
# macOS
brew install chromedriver

# Ubuntu/Debian
sudo apt install chromium-chromedriver

# Or download manually from:
# https://chromedriver.chromium.org/
```

### Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Cookie Lifespan

MyCourses session cookies typically last:

- **Active session:** Several hours while you're using it
- **Idle session:** May expire after 30-60 minutes of inactivity
- **Maximum:** Usually 24 hours

When your cookie expires, simply get a new one using any of the methods above.

## Security Notes

⚠️ **Important:**

- Your `config.json` contains your session cookie - **keep it private**
- Don't commit `config.json` to version control (it's in `.gitignore`)
- Session cookies give full access to your MyCourses account
- Only use this tool for personal/educational purposes
- Respect MyCourses terms of service and use responsibly

## Target URL

Currently scrapes: `https://mycourses.aalto.fi/course/view.php?id=47384`

To scrape a different course, edit the `TARGET_URL` variable in either script:

```python
TARGET_URL = "https://mycourses.aalto.fi/course/view.php?id=YOUR_COURSE_ID"
```

## License

This is an educational tool for personal use. Use responsibly and in accordance with Aalto University's policies.

## Support

If you encounter issues:

1. Check that your cookie is valid and not expired
2. Verify you have all dependencies installed
3. Try the alternative scraper method
4. Check your internet connection

For course ID 47384, ensure you have access to this course in your MyCourses account.
