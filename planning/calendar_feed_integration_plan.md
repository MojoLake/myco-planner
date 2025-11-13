# MyCourses Calendar Integration Plan

## 🎯 Current Status

**✅ Ollama Setup Complete** – Local Gemma3 model installed and verified working  
**✅ Calendar Export Available** – Authenticated MyCourses iCal feed URL confirmed  
**⚠️ Next Task** – Build ingestion pipeline that fetches, parses, and normalizes calendar data

See [Next Steps](#next-steps) for immediate action items.

---

## Context & Goals

### Current State

The planner currently relies on ad-hoc scraping and manual data entry to track course deadlines. HTML scraping has proven fragile and time-consuming to maintain.

### Goal

Leverage the official MyCourses calendar export to obtain authoritative deadlines, lectures, and milestone data, then transform those events into actionable tasks for downstream processing with the local LLM.

Benefits:

- Stable, supported data format (iCalendar)
- Reduced maintenance compared to brittle DOM scraping
- Automatically scoped to enrolled courses via MyCourses preferences
- Compatible with fully offline processing (local fetch + local LLM)

---

## Proposed Architecture

### Component Overview

```
┌─────────────────────────────────────────────┐
│                 MyCo Planner                │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ Config Store │◄─────┤  Secret Vault   │ │
│  │ (config.json)│      │ (feed URL/token)│ │
│  └───────┬──────┘      └─────────────────┘ │
│          │                                  │
│          ▼                                  │
│  ┌──────────────────────────────┐          │
│  │ Calendar Feed Client         │          │
│  │ - Fetches ICS feed           │          │
│  │ - Handles caching            │          │
│  └───────┬──────────────────────┘          │
│          │                                  │
│          ▼                                  │
│  ┌──────────────────────────────┐          │
│  │ ICS Parser                   │          │
│  │ - Parses events              │          │
│  │ - Normalizes timezones       │          │
│  │ - Deduplicates occurrences   │          │
│  └───────┬──────────────────────┘          │
│          │                                  │
│          ▼                                  │
│  ┌──────────────────────────────┐          │
│  │ Event Normalization          │          │
│  │ - Categorizes event types    │          │
│  │ - Maps to planner schema     │          │
│  └───────┬──────────────────────┘          │
│          │                                  │
│          ▼                                  │
│  ┌──────────────────────────────┐          │
│  │ Task Generator               │          │
│  │ - Sends structured context   │          │
│  │   to local LLM (Ollama)      │          │
│  │ - Produces todo items        │          │
│  └──────────────────────────────┘          │
│                                             │
└─────────────────────────────────────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Local Ollama Service    │
          │ - Gemma3 model          │
          │ - Fully offline         │
          └─────────────────────────┘
```

### Key Components

#### 1. Calendar Feed Client

- Stores the personalized export URL securely (tokenized link)
- Fetches the ICS payload via HTTPS using `requests`
- Implements caching/backoff to avoid unnecessary downloads
- Supplies raw calendar text to parser

#### 2. ICS Parser

- Uses `ics` or `icalendar` library to parse events
- Handles timezones (UTC vs local) and daylight-saving adjustments
- Extracts metadata: `SUMMARY`, `DTSTART`, `DTEND`, `LOCATION`, `CATEGORIES`, `DESCRIPTION`
- Flags recurring events and exceptions

#### 3. Event Normalization Layer

- Maps MyCourses categories (e.g., assignment, lecture, quiz) to internal task types
- Performs deduplication and merges overlapping segments
- Adds derived fields (lead time, course code, urgency score)

#### 4. Task Generator (LLM Bridge)

- Bundles normalized events into context windows
- Prompts local Gemma3 model to suggest prioritized actions
- Produces todo entries with due dates, reminders, and suggested prep steps

#### 5. Storage & Output

- Persists normalized events to JSON for repeatable runs
- Provides CLI/Markdown summaries for users
- Future: optional calendar re-export or reminders integration

---

## Integration Approach

### Phase 1: Feed Retrieval & Parsing

- Store calendar export URL in `calendar_feed_url.txt` (gitignored)
- Implement fetch utility with caching and updated timestamp tracking
- Parse ICS payload into event objects; log parsing statistics
- Write golden sample JSON for regression checks

### Phase 2: Event Normalization

- Define internal event schema (course, title, start, end, category, metadata)
- Map MyCourses `CATEGORIES` to planner categories
- Handle all-day vs timed events; compute due dates for deadlines
- Implement deduplication for recurring entries

### Phase 3: Task Generation

- Curate prompt template for Gemma3 to convert event bundles into action plans
- Build evaluation harness comparing generated tasks with expectations
- Add configuration switches for prompt tuning and grouping logic

### Phase 4: Migration & Cleanup

- Replace legacy scraping references in documentation and scripts
- Deprecate unused scraping modules after validation
- Document operational playbook (refresh feed, handle token rotation)

---

## Key Technical Decisions

### Feed Authentication & Storage

**Decision**: Treat the calendar URL as a secret token stored in `calendar_feed_url.txt` (gitignored).

**Rationale**:

- URL contains authentication token; treat like a password
- Simple file-based storage keeps setup lightweight
- Easy to rotate by replacing file contents

### Parser Choice

**Decision**: Start with the `ics` Python library (already lightweight) and fall back to `icalendar` if advanced features (recurrence rules, alarms) are required.

**Rationale**:

- `ics` has a straightforward API for common fields
- Works well with timezone-aware `arrow` objects
- Swappable if requirements grow

### Timezone Handling

**Decision**: Normalize all timestamps to local timezone with UTC backup.

**Rationale**:

- Aligns with student expectations (campus schedule)
- Avoids confusion around daylight-saving transitions
- UTC retained for deterministic storage/testing

### Data Persistence

**Decision**: Emit canonical JSON snapshots of parsed events (`data/calendar_events.json`).

**Rationale**:

- Supports regression tests and offline inspection
- Enables downstream consumers beyond the LLM
- Facilitates caching and diffing between updates

### Prompt Strategy for LLM

**Decision**: Group events by course and timeframe (e.g., upcoming week) before prompting Gemma3.

**Rationale**:

- Keeps prompt size manageable
- Encourages course-specific todos
- Allows targeted re-prompts for a single course

---

## Migration Path

- Maintain existing manual notes until calendar pipeline validated
- Introduce feature flag to toggle between legacy data and calendar-derived tasks
- Document process for refreshing the feed URL if token rotates
- Provide script to backfill historical events if desired

---

## Dependencies & Requirements

### Already Available ✅

- `requests` for HTTP fetches
- Local Ollama service with Gemma3 model (`test_ollama.py` verified)

### New/Updated Dependencies

- `ics` (via `uv add ics`) for calendar parsing
- `python-dateutil` (if needed for timezone/recurrence support)
- Optional: `pydantic` models for validated event schema (already in project)

### Operational Notes

- Respect MyCourses rate limits (cache for at least 15 minutes)
- Monitor feed size; handle incremental updates vs full refresh
- Ensure `calendar_feed_url.txt` excluded from version control/backups

---

## Open Questions & Risks

| Topic             | Question                                          | Mitigation                                                        |
| ----------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| Token longevity   | How often does the MyCourses export token expire? | Add validation step; surface clear errors; support quick re-entry |
| Recurrence rules  | Are recurring lectures encoded as RRULEs?         | Verify with sample feed; ensure parser handles exceptions         |
| Event metadata    | Are deadlines always tagged in `CATEGORIES`?      | Fallback heuristics based on keywords in `SUMMARY`/`DESCRIPTION`  |
| Timezones         | Does feed always use UTC offsets?                 | Normalize with `pytz`/`dateutil`; log discrepancies               |
| Data completeness | Are grades/exams included?                        | Identify gaps and plan complementary data sources if needed       |

---

## Success Metrics

- **Parsing Coverage**: ≥ 99% of events successfully parsed without errors
- **Categorization Accuracy**: ≥ 95% correct mapping of events to planner categories
- **Latency**: Calendar fetch + parse < 3 seconds after caching warm-up
- **LLM Output Quality**: Actionable tasks generated for 100% of upcoming deadlines
- **Operational Reliability**: Zero token leaks; easy rotation workflow documented

---

## Next Steps

1. **Secure the Feed URL**

   - Store link in `calendar_feed_url.txt` with clear instructions
   - Update `.gitignore` if needed

2. **Prototype Parser**

   - Fetch feed once and persist raw ICS sample
   - Build quick parser spike to print upcoming events

3. **Define Event Schema**

   - Draft Pydantic model for normalized event
   - Capture optional fields (location, notes)

4. **Connect to LLM**
   - Adapt `test_ollama.py` to accept structured event context
   - Measure latency and output quality

---

## Why Calendar Export?

✅ **Official Source**: Data curated by MyCourses, reduces drift  
✅ **Low Maintenance**: No brittle HTML parsing or selector updates  
✅ **Security**: Token-based link avoids storing credentials in scripts  
✅ **Automation Friendly**: Easy to schedule periodic syncs  
✅ **Consistency**: Single feed aggregates all enrolled courses  
✅ **Offline Ready**: Once fetched, entire pipeline works without internet

---

## References

- [RFC 5545: Internet Calendaring and Scheduling Core Object Specification (iCalendar)](https://datatracker.ietf.org/doc/html/rfc5545)
- [ics.py Documentation](https://icspy.readthedocs.io/en/latest/)
- MyCourses calendar export URL (private token stored locally)
