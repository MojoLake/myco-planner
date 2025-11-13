# Ollama + Gemma3 Basic Test Plan

## Context & Goals

### Purpose

Before integrating ScrapeGraph AI with Ollama for MyCourses scraping, we need to verify that our local Ollama setup with Gemma3 is working correctly. This test will confirm:

- Ollama service is running and accessible
- Gemma3 model is properly installed
- Python can communicate with Ollama
- Basic text generation works as expected
- Response times are acceptable for our use case

### Success Criteria

✅ Python script successfully connects to Ollama  
✅ Gemma3 model responds to a simple prompt  
✅ Response is coherent and relevant  
✅ Response time is under 30 seconds (acceptable for local model)  
✅ No errors or warnings during execution

## Current State Assessment

### What We Have

- Ollama installed on macOS (darwin 25.1.0)
- Gemma3 model pulled/available
- Python 3.11+ environment

### What We Need to Test

- Direct connectivity to Ollama service (http://localhost:11434)
- Model availability and responsiveness
- Python integration approach (which library to use)

## Proposed Approach

### Test Script Design

Create a minimal Python script (`test_ollama.py`) that:

1. **Connects to Ollama** at default endpoint (http://localhost:11434)
2. **Sends a simple prompt** to Gemma3 model
3. **Displays the response** and timing information
4. **Reports success/failure** with clear error messages

All settings hardcoded for simplicity - no config file needed.

### Simple Test Prompt

Use a straightforward prompt that tests:

- Basic comprehension
- Structured output capability
- Relevance to our domain

Example: _"List 3 common elements found on an academic course website, formatted as JSON with 'name' and 'description' fields."_

This tests:

- Text generation
- JSON formatting (needed for extraction schemas)
- Domain relevance (academic/course context)

## Key Technical Decisions

### Choice of Python Library

**Options:**

1. **requests** - Direct HTTP calls to Ollama API
2. **ollama-python** - Official Ollama Python client
3. **langchain** - Full LLM framework (overkill for basic test)

**Decision**: Use **requests** for the basic test

**Rationale**:

- Already in dependencies
- Simple, transparent HTTP interaction
- No additional packages needed
- Easy to debug
- Shows exactly what's happening under the hood

**Alternative**: If we want more convenience, `ollama-python` could be added later for production code.

### Test Structure

**Decision**: Single standalone script with no external dependencies beyond requests

**Rationale**:

- Easy to run and understand
- Self-contained test
- No complex setup required
- Clear pass/fail output

## Implementation Overview

### Script Structure

```python
# test_ollama.py - Minimal test structure

1. Import required libraries (requests, json, time)
2. Define constants (endpoint, model, timeout)
3. Define Ollama API call function
4. Send test prompt to Gemma3
5. Validate response
6. Display results with timing
7. Report success or failure
```

### API Endpoint

Ollama REST API format:

- **Endpoint**: `http://localhost:11434/api/generate`
- **Method**: POST
- **Payload**: `{"model": "gemma3", "prompt": "...", "stream": false}`
- **Response**: JSON with `response` field containing generated text

### Error Handling

Handle common failure scenarios:

- Ollama service not running → Clear message to start Ollama
- Gemma3 model not found → Instruction to run `ollama pull gemma3`
- Connection timeout → Suggest checking if Ollama is running
- Invalid response → Display raw response for debugging

## Expected Output

### Success Case

```
=== Ollama + Gemma3 Test ===

Testing connection to http://localhost:11434
Model: gemma3

Sending test prompt...

Response (received in 8.3s):
[Generated JSON response from model]

✅ Test PASSED
   - Connection successful
   - Model responded
   - Response time acceptable (8.3s < 30s)
```

### Failure Cases

Clear error messages for each scenario:

- "❌ Connection failed: Ollama service not running at http://localhost:11434"
- "❌ Model not found: gemma3. Run: ollama pull gemma3"
- "❌ Timeout: Response took longer than 30s"

## Testing Checklist

Before running the test, verify:

- [ ] Ollama is installed: `ollama --version`
- [ ] Ollama service is running: `ollama list` (should not error)
- [ ] Gemma3 model is available: `ollama list | grep gemma3`

## Success Metrics

| Metric              | Target              | Why It Matters                     |
| ------------------- | ------------------- | ---------------------------------- |
| Connection success  | 100%                | Service must be accessible         |
| Response generation | Valid text          | Model must work                    |
| Response time       | <30s                | Usability threshold                |
| JSON parsing        | Valid JSON          | Needed for ScrapeGraph integration |
| Error clarity       | Actionable messages | Easy troubleshooting               |

## Next Steps After Test

### If Test Passes ✅

1. Document successful configuration
2. Proceed to ScrapeGraph AI integration POC
3. Test with actual MyCourses page extraction
4. Benchmark more complex prompts

### If Test Fails ❌

1. Debug based on error message
2. Verify Ollama installation: `brew reinstall ollama` (macOS)
3. Check service status: `ollama serve` (run in separate terminal)
4. Verify model: `ollama pull gemma3`
5. Test manually: `ollama run gemma3 "test prompt"`
6. Check port availability: `lsof -i :11434`

## Risks & Mitigations

| Risk                  | Mitigation                                                         |
| --------------------- | ------------------------------------------------------------------ |
| Ollama not running    | Script provides clear start instructions                           |
| Model not downloaded  | Script checks and instructs to pull model                          |
| Slow response         | Set realistic timeout (30s), inform user it's normal for first run |
| Port conflict (11434) | Document how to check with `lsof -i :11434`                        |

## Why This Test Matters

This simple test is the **foundation** for the entire ScrapeGraph AI integration:

- ✅ **Validates environment setup** before complex integration
- ✅ **Catches configuration issues early** (wrong endpoint, missing model)
- ✅ **Establishes baseline performance** (response time for simple prompts)
- ✅ **Verifies JSON capability** (needed for structured extraction)
- ✅ **Provides debugging template** for future issues

**Time investment**: ~15 minutes to write and run  
**Potential time saved**: Hours of debugging integration issues

## References

- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Gemma3 Model Card](https://ollama.ai/library/gemma3)
- Integration plan: `planning/scrapegraph_ai_integration_plan.md`
