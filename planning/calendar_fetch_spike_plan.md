# Calendar Data Fetch Spike Plan

## Goal

Build a simple URL → data pipeline that fetches the MyCourses calendar export and prints the parsed events. This is a proof-of-concept to verify we can access and understand the data before building the full integration.

## What We're Building

A standalone script that:
1. Reads the calendar export URL from a config file
2. Fetches the ICS data via HTTP
3. Parses the calendar events
4. Prints the events in a readable format

## Success Criteria

- Script successfully fetches data from the calendar URL
- Events are parsed and printed with key details (title, date, type)
- No credentials or tokens committed to git
- Clear error messages if the URL is invalid or unreachable

## Implementation Approach

### 1. URL Storage

Store the calendar export URL in `calendar_feed_url.txt` (gitignored):

```
# .gitignore
calendar_feed_url.txt
```

The file should contain just the URL:
```
https://mycourses.aalto.fi/calendar/export_execute.php?userid=...&authtoken=...
```

### 2. Fetch Component

Use `requests` to fetch the ICS data:
- Simple GET request (URL already contains auth token)
- Add timeout to handle slow connections
- Handle common HTTP errors (404, 401, network issues)

### 3. Parse Component

Use the `ics` library to parse calendar events:
- Parse the ICS text into event objects
- Extract key fields: summary, start time, end time, description
- Handle timezone conversions (MyCourses likely uses UTC)

### 4. Display Component

Print events in a human-readable format:
- Sort by date (upcoming first)
- Show event type/category if available
- Format dates clearly
- Group by course if that info is available

## File Structure

```
myco_planner/
├── calendar_feed_url.txt          # Gitignored, contains the export URL
├── fetch_calendar.py              # The spike script
└── .gitignore                     # Updated to exclude URL file
```

## Dependencies

Add to project:
```bash
uv add ics requests
```

Both are lightweight and commonly used for this purpose.

## Sample Output

```
Fetching calendar from MyCourses...
Found 23 events

=== Upcoming Events ===

📅 Mon Nov 18, 2024 09:00
   Design Patterns - Lecture 5
   Location: U123

📝 Wed Nov 20, 2024 23:59
   Software Engineering - Assignment 3 Due
   Description: Submit UML diagrams...

📅 Thu Nov 21, 2024 14:15
   Algorithms - Exercise Session
   Location: U456

[... more events ...]
```

## Error Handling

Handle these common scenarios:
- Missing `calendar_feed_url.txt` → Clear instructions on how to create it
- Invalid URL → Show the error and check URL format
- Network errors → Suggest checking connection
- Parse errors → Save raw ICS to file for debugging

## Next Steps After Spike

Once this works:
1. Add caching to avoid repeated fetches
2. Filter events by date range (e.g., next 2 weeks)
3. Categorize events (assignments vs lectures vs exams)
4. Feed structured data to the LLM for task generation

## Why This Approach?

✅ **Start simple**: Get something working end-to-end first  
✅ **Validate assumptions**: Confirm the URL works and data is parseable  
✅ **Fast feedback**: See real data quickly to inform next steps  
✅ **Low risk**: Standalone script won't break existing functionality  
✅ **Easy debugging**: Can inspect raw ICS and parsed output separately

## Security Notes

- The export URL contains an auth token - treat it like a password
- Never commit `calendar_feed_url.txt` to git
- If token expires, simply update the file with a new URL from MyCourses
- Consider adding `.txt` files to `.gitignore` globally if not already done

## Time Estimate

- Setup dependencies: 5 minutes
- Basic fetch + parse: 15-20 minutes
- Error handling + formatting: 10-15 minutes
- Testing with real data: 10 minutes

**Total: ~1 hour** for a working proof-of-concept

