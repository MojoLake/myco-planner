#!/usr/bin/env python3
"""
MyCourses Web Scraper - Cookie-based authentication
Scrapes content from Aalto MyCourses using stored session cookies.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import sys

CONFIG_FILE = "config.json"
TARGET_URL = "https://mycourses.aalto.fi/course/view.php?id=47384"


def load_config():
    """Load configuration from config.json file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {CONFIG_FILE} exists but is not valid JSON.")
            return {}
    return {}


def save_config(config):
    """Save configuration to config.json file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to {CONFIG_FILE}")


def get_cookie():
    """Get MoodleSession cookie from config or prompt user."""
    config = load_config()

    # Check if cookie exists in config
    if "MoodleSession" in config and config["MoodleSession"]:
        print("Using stored MoodleSession cookie from config.json")
        return config["MoodleSession"]

    # Prompt user for cookie
    print("\n" + "=" * 60)
    print("MoodleSession cookie not found in config.json")
    print("=" * 60)
    print("\nTo get your session cookie:")
    print("1. Log into MyCourses in your browser (complete 2FA)")
    print("2. Press F12 to open DevTools")
    print("3. Go to Application/Storage → Cookies → https://mycourses.aalto.fi")
    print("4. Find and copy the 'MoodleSession' cookie value")
    print("\n" + "=" * 60 + "\n")

    cookie_value = input("Enter your MoodleSession cookie value: ").strip()

    if not cookie_value:
        print("Error: Cookie value cannot be empty.")
        sys.exit(1)

    # Save for future use
    config["MoodleSession"] = cookie_value
    save_config(config)

    return cookie_value


def scrape_page(url, cookie_value):
    """Scrape the target page using the provided cookie."""
    cookies = {"MoodleSession": cookie_value}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print(f"\nFetching: {url}")

    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        response.raise_for_status()

        # Check if we got redirected to login page
        if "login" in response.url.lower():
            print(
                "\nError: Session expired or invalid cookie. You were redirected to login."
            )
            print("Please obtain a fresh cookie and try again.")

            # Delete the invalid cookie from config
            config = load_config()
            if "MoodleSession" in config:
                del config["MoodleSession"]
                save_config(config)
                print(f"Removed invalid cookie from {CONFIG_FILE}")

            sys.exit(1)

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)


def parse_and_display(html_content):
    """Parse HTML and display relevant content."""
    soup = BeautifulSoup(html_content, "html.parser")

    print("\n" + "=" * 60)
    print("PAGE CONTENT")
    print("=" * 60 + "\n")

    # Try to get page title
    title = soup.find("title")
    if title:
        print(f"Page Title: {title.get_text().strip()}\n")

    # Try to get course name
    course_name = soup.find("h1") or soup.find("div", class_="page-header-headings")
    if course_name:
        print(f"Course Name: {course_name.get_text().strip()}\n")

    # Get main content area
    main_content = soup.find("div", id="region-main") or soup.find("main")

    if main_content:
        # Extract sections
        sections = main_content.find_all("li", class_="section")

        if sections:
            print(f"Found {len(sections)} course sections:\n")
            for i, section in enumerate(sections, 1):
                section_title = section.find("h3") or section.find(
                    "span", class_="sectionname"
                )
                if section_title:
                    print(f"  {i}. {section_title.get_text().strip()}")

        # Extract activities/resources
        activities = main_content.find_all("li", class_="activity")
        if activities:
            print(f"\nFound {len(activities)} activities/resources:\n")
            for i, activity in enumerate(activities[:10], 1):  # Limit to first 10
                activity_name = activity.find("span", class_="instancename")
                if activity_name:
                    print(f"  {i}. {activity_name.get_text().strip()}")
            if len(activities) > 10:
                print(f"  ... and {len(activities) - 10} more")

    # Get any announcements or news
    announcements = soup.find_all("div", class_="forum-post-display")
    if announcements:
        print(f"\nFound {len(announcements)} announcements")

    print("\n" + "=" * 60)
    print("Raw text content (first 500 chars):")
    print("=" * 60)

    # Get all text content
    text_content = soup.get_text(separator=" ", strip=True)
    print(text_content[:500] + "...")

    print("\n" + "=" * 60)
    print(f"Full HTML length: {len(html_content)} characters")
    print("=" * 60 + "\n")


def main():
    """Main function."""
    print("MyCourses Web Scraper")
    print("=" * 60)

    # Get cookie (from config or prompt)
    cookie_value = get_cookie()

    # Scrape the page
    html_content = scrape_page(TARGET_URL, cookie_value)

    # Parse and display content
    parse_and_display(html_content)

    print("\n✓ Scraping completed successfully!")


if __name__ == "__main__":
    main()
