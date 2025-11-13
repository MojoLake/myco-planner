#!/usr/bin/env python3
"""
Calendar Fetch Spike Script

Fetches and parses MyCourses calendar export data.
This is a proof-of-concept to validate calendar data access.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

import requests
from ics import Calendar


def load_calendar_url() -> Optional[str]:
    """Load the calendar feed URL from the config file."""
    url_file = Path("calendar_feed_url.txt")
    
    if not url_file.exists():
        print("❌ Error: calendar_feed_url.txt not found")
        print("\nTo create this file:")
        print("1. Go to MyCourses (https://mycourses.aalto.fi)")
        print("2. Navigate to Calendar")
        print("3. Click 'Export calendar' or find the export option")
        print("4. Copy the export URL")
        print("5. Create a file named 'calendar_feed_url.txt' in this directory")
        print("6. Paste the URL into that file")
        print("\nSee calendar_feed_url.txt.template for more details")
        return None
    
    try:
        url = url_file.read_text().strip()
        if not url:
            print("❌ Error: calendar_feed_url.txt is empty")
            return None
        if not url.startswith(("http://", "https://")):
            print(f"❌ Error: Invalid URL format: {url}")
            print("URL should start with http:// or https://")
            return None
        return url
    except Exception as e:
        print(f"❌ Error reading calendar_feed_url.txt: {e}")
        return None


def fetch_calendar_data(url: str) -> Optional[str]:
    """Fetch ICS data from the calendar URL."""
    print("📡 Fetching calendar from MyCourses...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out")
        print("Please check your internet connection and try again")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("❌ Error: Unauthorized (401)")
            print("Your auth token may have expired. Get a new export URL from MyCourses")
        elif response.status_code == 404:
            print("❌ Error: URL not found (404)")
            print("Please check that your calendar export URL is correct")
        else:
            print(f"❌ HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("Please check your internet connection")
        return None


def parse_calendar_events(ics_data: str) -> Optional[Calendar]:
    """Parse ICS data into calendar events."""
    try:
        calendar = Calendar(ics_data)
        return calendar
    except Exception as e:
        print(f"❌ Error parsing calendar data: {e}")
        print("\nSaving raw ICS data to 'debug_calendar.ics' for inspection...")
        try:
            Path("debug_calendar.ics").write_text(ics_data)
            print("✅ Raw data saved to debug_calendar.ics")
        except Exception as save_error:
            print(f"Could not save debug file: {save_error}")
        return None


def format_datetime(dt: Optional[datetime]) -> str:
    """Format a datetime object for display."""
    if dt is None:
        return "No date"
    
    # Format: Mon Nov 18, 2024 09:00
    return dt.strftime("%a %b %d, %Y %H:%M")


def display_events(calendar: Calendar):
    """Display calendar events in a readable format."""
    events = list(calendar.events)
    
    if not events:
        print("\n📭 No events found in the calendar")
        return
    
    print(f"\n✅ Found {len(events)} event(s)")
    
    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e.begin if e.begin else datetime.min)
    
    # Filter to only upcoming/recent events (you can adjust this)
    now = datetime.now()
    
    print("\n" + "=" * 60)
    print("📅 CALENDAR EVENTS")
    print("=" * 60)
    
    for event in sorted_events:
        print(f"\n🗓️  {format_datetime(event.begin)}")
        
        # Event name/summary
        if event.name:
            print(f"   {event.name}")
        
        # End time if different from start
        if event.end and event.end != event.begin:
            print(f"   Ends: {format_datetime(event.end)}")
        
        # Location
        if event.location:
            print(f"   📍 Location: {event.location}")
        
        # Description preview (first 100 chars)
        if event.description:
            desc = event.description.strip()
            if len(desc) > 100:
                desc = desc[:97] + "..."
            if desc:
                print(f"   📝 {desc}")
    
    print("\n" + "=" * 60)


def main():
    """Main function to run the calendar fetch spike."""
    print("🚀 MyCourses Calendar Fetch Spike")
    print("=" * 60)
    
    # Step 1: Load URL
    url = load_calendar_url()
    if not url:
        sys.exit(1)
    
    # Step 2: Fetch data
    ics_data = fetch_calendar_data(url)
    if not ics_data:
        sys.exit(1)
    
    # Step 3: Parse events
    calendar = parse_calendar_events(ics_data)
    if not calendar:
        sys.exit(1)
    
    # Step 4: Display events
    display_events(calendar)
    
    print("\n✨ Spike complete!")


if __name__ == "__main__":
    main()

