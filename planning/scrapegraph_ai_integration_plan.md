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

Integrate **ScrapeGraph AI** with **Ollama (local Gemma3 model)** to enable:

- AI-powered data extraction using natural language prompts
- Resilient scraping that adapts to HTML structure changes
- Easy extraction of complex nested data (assignment details, due dates, submission status, etc.)
- Structured output with type-safe schemas
- Maintain existing authentication mechanism (cookie-based)
- **Local processing** - no data sent to external APIs, free to use

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
│  │  - Prompt-based extraction   │◄─────┐   │
│  │  - Schema validation         │      │   │
│  └──────────┬───────────────────┘      │   │
│             │                           │   │
│             ▼                           │   │
│  ┌──────────────────────────────┐      │   │
│  │   Data Extraction Modules    │      │   │
│  │  - Course overview           │      │   │
│  │  - Assignments & deadlines   │      │   │
│  │  - Materials & resources     │      │   │
│  │  - Grades & feedback         │      │   │
│  └──────────┬───────────────────┘      │   │
│             │                           │   │
│             ▼                           │   │
│  ┌──────────────────────────────┐      │   │
│  │   Output / Storage Layer     │      │   │
│  │  (JSON, structured data)     │      │   │
│  └──────────────────────────────┘      │   │
│                                         │   │
└─────────────────────────────────────────┼───┘
                                          │
                    ┌─────────────────────▼───┐
                    │  Local Ollama Service   │
                    │  (localhost:11434)      │
                    │  - Gemma3 Model         │
                    │  - Local inference      │
                    │  - No external calls    │
                    └─────────────────────────┘
```

### Key Components

#### 1. ScrapeGraph AI Client Wrapper (Local Ollama)

- **Responsibility**: Manage ScrapeGraph AI client with local Ollama backend
- **Key Features**:
  - Initialize client to use local Ollama endpoint
  - Configure Gemma3 model for extraction tasks
  - Inject MoodleSession cookies into requests
  - Cache responses where appropriate
  - No API key management needed (local execution)

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
- Configure Ollama endpoint (typically http://localhost:11434)
- No API keys needed - fully local processing

#### 4. Output Standardization

- Unified data format across all extraction modules
- Timestamping for cache invalidation
- Structured logging for debugging

## Integration Approach

### Phase 1: Proof of Concept

**Goal**: Validate ScrapeGraph AI with local Ollama works with MyCourses authentication

- Set up Ollama with Gemma3 model
- Configure ScrapeGraph AI client to use local Ollama endpoint
- Test cookie injection with existing MoodleSession cookies
- Extract simple data (course title, sections) using natural language prompts
- Compare output with existing scraper results
- Benchmark performance and extraction quality with local model
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

**Decision**: Continue using cookie-based authentication with existing infrastructure + local Ollama

**Rationale**:

- Already solved the 2FA problem
- ScrapeGraph AI supports cookie injection
- No need to re-implement login flow
- Cookies can be refreshed when needed via Selenium script
- **Local Ollama means no API keys, no external data transmission, no costs**

**Implementation note**:

```python
from scrapegraph_py import Client

# Configure for local Ollama with Gemma3
client = Client(
    api_url="http://localhost:11434",  # Local Ollama endpoint
    model="gemma3"  # Local model
)

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

### Ollama Configuration

**Decision**: Make Ollama endpoint and model configurable

**Rationale**:

- Allow switching between different local models (Gemma3, Llama3, etc.)
- Support custom Ollama installations (different ports)
- Easy to test different models without code changes

**Configuration example** (`config.json`):

```json
{
  "MoodleSession": "your_session_cookie",
  "ollama": {
    "endpoint": "http://localhost:11434",
    "model": "gemma3",
    "timeout": 30
  }
}
```

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

- **Ollama**: Local LLM runtime (install via: https://ollama.ai)
- **Gemma3 model**: Download via `ollama pull gemma3`
- `scrapegraph-py`: ScrapeGraph AI Python client
- `pydantic`: Schema validation (may already be included)

### Ollama Setup

- Install Ollama on local machine
- Pull Gemma3 model: `ollama pull gemma3`
- Ensure Ollama is running (default: http://localhost:11434)
- Verify model availability: `ollama list`

### Cost Considerations

- ✅ **Zero API costs** - everything runs locally
- ✅ **No data privacy concerns** - course data stays on your machine
- ⚠️ **Hardware requirements**: Gemma3 needs sufficient RAM/CPU
- ✅ **Unlimited usage** - no rate limits or quotas
- Consider caching to avoid redundant processing and save computation time

## Open Questions & Risks

### Questions to Investigate

1. **Model Performance**: How well does Gemma3 extract structured data compared to larger models?
2. **Response Time**: What's the latency for local Gemma3 inference? Fast enough for interactive use?
3. **Hardware Requirements**: Will Gemma3 run smoothly on the target machine (RAM/CPU)?
4. **JavaScript Handling**: Does ScrapeGraph AI + Ollama handle dynamically loaded content in MyCourses?
5. **Multi-page Extraction**: How to handle courses with many pages (e.g., all assignments)?
6. **Extraction Quality**: Does a smaller local model (Gemma3) extract data as reliably as cloud models?

### Risks & Mitigations

| Risk                                   | Impact | Likelihood | Mitigation                                                     |
| -------------------------------------- | ------ | ---------- | -------------------------------------------------------------- |
| Gemma3 extraction quality insufficient | High   | Medium     | Test thoroughly, consider larger local models if needed        |
| Local model too slow                   | Medium | Medium     | Implement caching, batch processing, consider GPU acceleration |
| Hardware limitations (RAM/CPU)         | Medium | Low        | Monitor resource usage, optimize prompts for efficiency        |
| Extraction quality varies              | Medium | Medium     | Validate outputs, iterative prompt engineering                 |
| Cookie expiry mid-session              | Low    | Low        | Detect and prompt for re-authentication                        |
| Ollama service not running             | Low    | Medium     | Add health checks, clear error messages                        |

### Success Metrics

- **Extraction Accuracy**: >95% correct data extraction vs manual verification
- **Resilience**: Continues working after minor MyCourses UI updates
- **Feature Expansion**: Extract 3+ new data types not previously available
- **Development Speed**: New extractions take <30min instead of hours
- **Maintenance**: Reduce scraper maintenance time by 80%
- **Performance**: Page extraction completes in <10 seconds with Gemma3
- **Privacy**: Zero data transmitted to external services

## Next Steps

1. **Setup Phase** (~1-2 hours)

   - Install Ollama: `brew install ollama` (macOS) or download from ollama.ai
   - Pull Gemma3 model: `ollama pull gemma3`
   - Verify Ollama is running: `ollama list`
   - Install `scrapegraph-py` package
   - Test basic Ollama connection

2. **POC Phase** (~2-4 hours)

   - Create minimal working example with local Ollama
   - Configure ScrapeGraph AI client for local endpoint
   - Extract course title and sections using Gemma3
   - Validate cookie injection works
   - Benchmark extraction speed and quality
   - Document findings (especially Gemma3 performance)

3. **Decision Point**

   - Evaluate POC results (accuracy, speed, resource usage)
   - Assess if Gemma3 is sufficient or if larger local model needed
   - Decide: proceed, adjust model choice, or use hybrid approach

4. **Implementation Phase** (if green-lit)
   - Build out extraction modules
   - Define comprehensive schemas
   - Implement proper error handling
   - Add Ollama health checks
   - Create test suite
   - Optimize prompts for Gemma3's capabilities

## Why Local Ollama + Gemma3?

### Advantages

✅ **Privacy**: Course data never leaves your machine - critical for academic/sensitive information  
✅ **Cost**: Zero API costs - unlimited scraping without worrying about bills  
✅ **Speed**: No network latency once model is loaded (after first run)  
✅ **Reliability**: No dependency on external API availability or rate limits  
✅ **Offline**: Works without internet connection (after initial model download)  
✅ **Control**: Full control over model version and behavior

### Considerations

⚠️ **Initial Setup**: Requires installing Ollama and downloading model (~4-8GB)  
⚠️ **Hardware**: Needs sufficient RAM (8GB+ recommended) for Gemma3  
⚠️ **First Run**: Model loading takes time on first inference  
⚠️ **Model Size Trade-off**: Gemma3 is smaller/faster but may be less capable than GPT-4/Claude for complex extractions

### When This Approach Excels

- Regular scraping of multiple courses
- Sensitive academic data that shouldn't be sent to third parties
- Batch processing where initial model load time is amortized
- Budget-conscious projects
- Learning environments where experimenting is encouraged

## References

- [ScrapeGraph AI Documentation](https://scrapegraph-ai.readthedocs.io/en/latest/)
- [Ollama Documentation](https://ollama.ai)
- [Gemma3 Model](https://ollama.ai/library/gemma3)
- [ScrapeGraph AI Cookie Authentication](https://scrapegraph-ai.readthedocs.io/en/latest/) (example provided by user)
- Current codebase: `scraper.py`, `scraper_selenium.py`
