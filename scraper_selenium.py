#!/usr/bin/env python3
"""
MyCourses Web Scraper - Selenium Browser Automation
Alternative approach using browser automation with manual 2FA completion.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import time
import sys

CONFIG_FILE = "config.json"
TARGET_URL = "https://mycourses.aalto.fi/course/view.php?id=47384"


def load_config():
    """Load configuration from config.json file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(config):
    """Save configuration to config.json file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to {CONFIG_FILE}")


def save_cookies_to_config(driver):
    """Extract cookies from Selenium and save to config."""
    cookies = driver.get_cookies()

    # Find MoodleSession cookie
    moodle_session = None
    for cookie in cookies:
        if cookie["name"] == "MoodleSession":
            moodle_session = cookie["value"]
            break

    if moodle_session:
        config = load_config()
        config["MoodleSession"] = moodle_session
        save_config(config)
        print(f"\n✓ MoodleSession cookie saved to {CONFIG_FILE}")
        print("You can now use scraper.py for faster access!")
        return moodle_session
    else:
        print("\nWarning: MoodleSession cookie not found")
        return None


def setup_driver():
    """Setup and return Chrome WebDriver with appropriate options."""
    options = webdriver.ChromeOptions()

    # Add user agent
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    # Optional: Run in headless mode (commented out so you can see the browser)
    # options.add_argument('--headless')

    # Disable automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error: Could not start Chrome WebDriver: {e}")
        print("\nMake sure you have Chrome and ChromeDriver installed:")
        print("  brew install chromedriver  (on macOS)")
        print("  or download from: https://chromedriver.chromium.org/")
        sys.exit(1)


def scrape_with_browser():
    """Scrape using Selenium with interactive login."""
    print("MyCourses Web Scraper - Selenium Mode")
    print("=" * 60)
    print("\nStarting Chrome browser...")

    driver = setup_driver()

    try:
        # Navigate to target URL
        print(f"Navigating to: {TARGET_URL}")
        driver.get(TARGET_URL)

        # Check if we're on login page
        if "login" in driver.current_url.lower():
            print("\n" + "=" * 60)
            print("PLEASE LOG IN MANUALLY")
            print("=" * 60)
            print("\n1. Complete the Aalto login process in the browser")
            print("2. Complete 2FA authentication")
            print("3. Wait for the course page to load")
            print("\nPress Enter here once you've logged in and see the course page...")
            input()

        # Wait for the page to load
        print("\nWaiting for page to fully load...")
        time.sleep(3)

        # Verify we're on the course page
        current_url = driver.current_url
        if "login" in current_url.lower():
            print("\nError: Still on login page. Please ensure you're logged in.")
            driver.quit()
            sys.exit(1)

        print(f"✓ Successfully accessed: {current_url}")

        # Save cookies for future use
        save_cookies_to_config(driver)

        # Get page source
        html_content = driver.page_source

        # Parse and display content
        parse_and_display(html_content)

        print("\n✓ Scraping completed successfully!")

    except Exception as e:
        print(f"\nError during scraping: {e}")
        sys.exit(1)

    finally:
        # Keep browser open for a moment
        print("\nClosing browser in 3 seconds...")
        time.sleep(3)
        driver.quit()


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
    print("\nThis script will open Chrome and let you log in manually.")
    print("After login, it will save your session cookie for use with scraper.py\n")

    response = input("Continue? (y/n): ").strip().lower()
    if response != "y":
        print("Cancelled.")
        sys.exit(0)

    scrape_with_browser()


if __name__ == "__main__":
    main()
