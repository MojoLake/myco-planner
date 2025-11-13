# Planning 101: Effective Software Planning Documentation

## Philosophy

Good planning documents strike a balance between **clarity** and **flexibility**. They should provide enough structure to guide implementation without becoming rigid specifications that slow down development.

## What Makes a Good Plan?

### Semi-High-Level Overview

- **Focus on WHAT and WHY, not HOW**: Describe what needs to be done and why it matters, not the exact implementation steps
- **System-level thinking**: Think about components, interactions, and data flow rather than line-by-line code
- **Leave room for discovery**: Implementation often reveals better approaches than what was initially planned

### When to Include Code and Implementation Details

Include code/implementation details ONLY when:

1. **Critical architectural decisions** need to be communicated (e.g., "we'll use OAuth 2.0 PKCE flow")
2. **API interfaces** need to be defined for coordination between teams/components
3. **Complex algorithms** require explanation before implementation
4. **External dependencies** have specific usage patterns that aren't obvious

## Structure of a Good Plan

### 1. Context & Goals (WHY)

- What problem are we solving?
- What are the success criteria?
- What constraints exist?

### 2. Current State Assessment

- What do we have now?
- What works? What doesn't?
- What can be reused?

### 3. Proposed Approach (WHAT)

- High-level architecture or approach
- Key components and their responsibilities
- Integration points
- Data flow

### 4. Key Decisions & Trade-offs

- Major technical choices
- Alternatives considered
- Trade-offs and rationale

### 5. Migration Path (if applicable)

- How do we get from current to future state?
- Backward compatibility concerns
- Rollout strategy

### 6. Open Questions & Risks

- What needs more investigation?
- What could go wrong?
- Dependencies on external factors

## Examples

### ❌ Too Detailed (Anti-pattern)

```
Step 1: Import the requests library
Step 2: Create a function called fetch_data() with parameters url and cookies
Step 3: Inside the function, add a try-catch block...
```

### ✅ Right Level (Good)

```
Calendar Ingestion Layer: A module responsible for fetching the MyCourses
personal iCal feed, handling token storage/refresh, and exposing normalized
events so other components can consume schedule data without worrying about
calendar parsing details.
```

### ✅ When Code Is Appropriate

```
Calendar Parsing: We'll read the authenticated iCal feed and normalize events:

    import ics

    calendar = ics.Calendar(requests.get(feed_url).text)
    for event in calendar.events:
        tasks.append({"title": event.name, "due": event.begin})

This clarifies how we transform MyCourses calendar data into structured tasks.
```

## Remember

- **Plans are living documents**: Update them as you learn
- **Plans guide, not dictate**: Be willing to deviate when it makes sense
- **Plans save time**: Good planning prevents rework and miscommunication
- **Plans aren't code**: Don't confuse planning with implementation
