# ScrapeGraph AI Integration Plan

## Context & Goals

### Current State
The MyCourses scraper currently uses:
- **Requests + BeautifulSoup**: Manual HTML parsing with CSS selectors and DOM navigation
- **Selenium + BeautifulSoup**: Browser automation for 2FA login, then manual parsing
- **Cookie Management**: Stores MoodleSession cookies for authentication
- **Manual Extraction**: Hardcoded logic to find sections, activities, announcements

### Problem
- Brittle scraping logic breaks when MyCourses updates their HTML structure
- Limited data extraction - only getting basic course structure
- Manual parsing requires deep knowledge of Moodle's DOM structure
- Hard to extend for new data types (assignments, deadlines, grades, etc.)

### Goal
Integrate **ScrapeGraph AI** to enable:
- AI-powered data extraction using natural language prompts
- Resilient scraping that adapts to HTML structure changes
- Easy extraction of complex nested data (assignment details, due dates, submission status, etc.)
- Structured output with type-safe schemas
- Maintain existing authentication mechanism (cookie-based)

## Proposed Architecture

### Component Overview

```
┌─────────────────────────────────────────────┐
│         MyCourses Planner                   │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ Auth Manager │◄─────┤  Config Store   │ │
│  │ (existing)   │      │  (config.json)  │ │
│  └───────┬──────┘      └─────────────────┘ │
│          │                                  │
│          ▼                                  │
│  ┌──────────────────────────────┐          │
│  │   ScrapeGraph AI Client      │          │
│  │  - Cookie injection          │          │
│  │  - Prompt-based extraction   │          │
│  │  - Schema validation         │          │
│  └──────────┬───────────────────┘          │
│             │                               │
│             ▼                               │
│  ┌──────────────────────────────┐          │
│  │   Data Extraction Modules    │          │
│  │  - Course overview           │          │
│  │  - Assignments & deadlines   │          │
│  │  - Materials & resources     │          │
│  │  - Grades & feedback         │          │
│  └──────────┬───────────────────┘          │
│             │                               │
│             ▼                               │
│  ┌──────────────────────────────┐          │
│  │   Output / Storage Layer     │          │
│  │  (JSON, structured data)     │          │
│  └──────────────────────────────┘          │
│                                             │
└─────────────────────────────────────────────┘
```

### Key Components

#### 1. ScrapeGraph AI Client Wrapper
- **Responsibility**: Manage ScrapeGraph AI client lifecycle and configuration
- **Key Features**:
  - Initialize client with API credentials (from environment or config)
  - Inject MoodleSession cookies into requests
  - Handle rate limiting and retries
  - Cache responses where appropriate

#### 2. Extraction Modules
Separate modules for different data types, each with:
- **Prompts**: Natural language descriptions of what to extract
- **Schemas**: Pydantic models defining expected output structure
- **URL builders**: Generate appropriate MyCourses URLs

Examples:
- `course_overview.py`: Course name, description, instructor, sections
- `assignments.py`: Assignment titles, due dates, submission status, points
- `materials.py`: Lecture notes, readings, videos
- `grades.py`: Current grades, feedback, rubrics

#### 3. Authentication Layer (Enhanced)
- Keep existing cookie management (already works well)
- Add API key management for ScrapeGraph AI
- Consider token refresh logic if needed

#### 4. Output Standardization
- Unified data format across all extraction modules
- Timestamping for cache invalidation
- Structured logging for debugging

## Integration Approach

### Phase 1: Proof of Concept
**Goal**: Validate ScrapeGraph AI works with MyCourses authentication

- Set up ScrapeGraph AI client with API credentials
- Test cookie injection with existing MoodleSession cookies
- Extract simple data (course title, sections) using natural language prompts
- Compare output with existing scraper results
- Document any limitations or issues

### Phase 2: Parallel Implementation
**Goal**: Build new extraction alongside existing scrapers

- Create new module structure (e.g., `extractors/`)
- Implement 2-3 key extraction modules (course overview, assignments)
- Define Pydantic schemas for structured output
- Keep existing scrapers as fallback
- Add configuration toggle between old/new approach

### Phase 3: Enhanced Extraction
**Goal**: Extract data that was difficult/impossible before

- Assignment details with complex nested data
- Calendar/timeline view of all deadlines
- Material categorization (readings vs videos vs slides)
- Grade trends and analytics data
- Discussion forum summaries

### Phase 4: Migration & Cleanup
**Goal**: Transition fully to new system

- Deprecate manual BeautifulSoup parsing
- Remove redundant code
- Keep Selenium script for initial cookie acquisition only
- Performance optimization and caching

## Key Technical Decisions

### Authentication Strategy
**Decision**: Continue using cookie-based authentication with existing infrastructure

**Rationale**:
- Already solved the 2FA problem
- ScrapeGraph AI supports cookie injection
- No need to re-implement login flow
- Cookies can be refreshed when needed via Selenium script

**Implementation note**:
```python
client = Client(api_key=os.getenv("SCRAPEGRAPH_API_KEY"))
response = client.smartscraper(
    website_url=mycourses_url,
    user_prompt="Extract course assignments...",
    cookies={"MoodleSession": stored_cookie},
    output_schema=AssignmentSchema
)
```

### Schema Design
**Decision**: Use Pydantic models for all extracted data

**Rationale**:
- Type safety and validation
- Auto-documentation
- Easy serialization to JSON
- ScrapeGraph AI native support

**Benefits**:
- Catch extraction errors early
- Clear contracts between components
- Easy to extend/modify schemas

### Prompt Engineering
**Decision**: Store prompts as constants/configs, not hardcoded in logic

**Rationale**:
- Easy to iterate and improve prompts
- Version control for prompt changes
- A/B testing different prompts
- Reusable across similar extractions

**Example structure**:
```python
# prompts.py
COURSE_OVERVIEW_PROMPT = """
Extract the course information including:
- Course name and code
- Instructor names
- Course description
- List of all sections/modules with their titles
"""
```

### Error Handling & Fallbacks
**Decision**: Graceful degradation with informative errors

**Approach**:
- Log raw responses for debugging
- Validate schemas and report specific failures
- Consider keeping simple BeautifulSoup fallback for critical data
- Clear error messages for cookie expiration

## Migration Path

### Backward Compatibility
- Maintain existing `scraper.py` and `scraper_selenium.py` during transition
- New code lives in separate modules
- Configuration flag to switch between approaches
- Both can coexist until new system is validated

### Data Format Evolution
- Current output: Pretty-printed console output
- New output: Structured JSON files
- Add backward-compatible console output formatter
- Enable programmatic consumption of data

### Testing Strategy
- Compare outputs between old and new scrapers for same pages
- Manual verification of complex extractions
- Test with multiple courses to ensure generalization
- Monitor for cookie expiration and re-authentication

## Dependencies & Requirements

### New Dependencies
- `scrapegraph-py`: ScrapeGraph AI Python client
- `pydantic`: Schema validation (may already be included)
- Environment variable management for API key

### API Key Management
- Store ScrapeGraph API key in environment variable or config
- Never commit API keys to version control
- Update config.json.example with placeholder

### Cost Considerations
- ScrapeGraph AI is a paid service (understand pricing)
- Consider caching to minimize API calls
- Rate limiting to avoid unexpected costs
- Start with free tier if available for testing

## Open Questions & Risks

### Questions to Investigate
1. **API Limits**: What are the rate limits and quotas for ScrapeGraph AI?
2. **Cost**: What's the pricing model? Per request? Per page size?
3. **Response Time**: Is it fast enough for interactive use or only batch processing?
4. **JavaScript Handling**: Does it handle dynamically loaded content in MyCourses?
5. **Multi-page Extraction**: How to handle courses with many pages (e.g., all assignments)?

### Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API costs too high | High | Medium | Implement aggressive caching, batch operations |
| Service downtime | Medium | Low | Keep existing scraper as fallback |
| Extraction quality varies | Medium | Medium | Validate outputs, iterative prompt engineering |
| Cookie expiry mid-session | Low | Low | Detect and prompt for re-authentication |
| Rate limiting blocks usage | Medium | Medium | Implement backoff strategy, respect limits |

### Success Metrics
- **Extraction Accuracy**: >95% correct data extraction vs manual verification
- **Resilience**: Continues working after minor MyCourses UI updates
- **Feature Expansion**: Extract 3+ new data types not previously available
- **Development Speed**: New extractions take <30min instead of hours
- **Maintenance**: Reduce scraper maintenance time by 80%

## Next Steps

1. **Setup Phase** (~1-2 hours)
   - Obtain ScrapeGraph AI API key
   - Install `scrapegraph-py` package
   - Test basic connection and authentication

2. **POC Phase** (~2-4 hours)
   - Create minimal working example
   - Extract course title and sections
   - Validate cookie injection works
   - Document findings

3. **Decision Point**
   - Evaluate POC results
   - Assess cost/benefit
   - Decide: proceed, adjust approach, or abandon

4. **Implementation Phase** (if green-lit)
   - Build out extraction modules
   - Define comprehensive schemas
   - Implement proper error handling
   - Create test suite

## References

- [ScrapeGraph AI Documentation](https://scrapegraph-ai.readthedocs.io/en/latest/)
- [ScrapeGraph AI Cookie Authentication](https://scrapegraph-ai.readthedocs.io/en/latest/) (example provided by user)
- Current codebase: `scraper.py`, `scraper_selenium.py`

