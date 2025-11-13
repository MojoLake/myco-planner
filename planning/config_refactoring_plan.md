# Configuration Refactoring Plan

## Context & Goals

### Current State

The `test_ollama.py` script currently has:

- **Hardcoded configuration**: Ollama model name (`gemma3`) is hardcoded in the script
- **Default endpoint**: Assumes Ollama is at default `localhost:11434`
- **No flexibility**: Users must edit code to test different models or endpoints
- **No example/template**: New users don't have a reference for configuration

### Problem

- Testing different models requires code changes
- Cannot easily test different Ollama endpoints (custom ports, remote instances)
- No clear separation between code and configuration
- Missing `.cookie` and `config.json` infrastructure for the broader system

### Goal

Refactor the testing and configuration infrastructure to:

- Move all configuration to `config.json` (Ollama URL and model name)
- Create `.cookie` file for storing MyCourses authentication cookie
- Provide `config.json.example` as a template for users
- Update `test_ollama.py` to read from configuration file
- Enable easy switching between models and endpoints without code changes
- Follow best practices for configuration management

## Proposed Approach

### Configuration File Structure

Create a centralized `config.json` with clear sections:

```json
{
  "ollama": {
    "url": "http://localhost:11434",
    "model": "gemma3"
  }
}
```

**Design Principles**:

- **Flat but organized**: Group related settings under keys (e.g., `ollama`)
- **Sensible defaults**: Default values work out-of-the-box for standard setup
- **Extensible**: Easy to add new sections (e.g., `scraping`, `output`)
- **No secrets**: Sensitive data (cookies) stored in separate files

### Cookie File Structure

Create a simple `.cookie` file for authentication:

```
your_moodle_session_cookie_value_here
```

**Design Principles**:

- **Simple text file**: Just the cookie value, no JSON or formatting
- **Git-ignored**: Listed in `.gitignore` to prevent accidental commits
- **Separate from config**: Security best practice (config can be committed as example)
- **Easy to update**: Users can manually edit or script can write to it

### Example/Template Files

Create `config.json.example` as a template:

```json
{
  "ollama": {
    "url": "http://localhost:11434",
    "model": "gemma3"
  }
}
```

**Purpose**:

- Safe to commit to version control
- Shows all available configuration options
- Documents expected structure and defaults
- Users copy to `config.json` and customize

## Implementation Tasks

### Task 1: Create Configuration Files

**Files to create**:

1. **`config.json`** - Active configuration (git-ignored)

   - Contains actual Ollama settings
   - User-specific, not committed to repo

2. **`config.json.example`** - Template (committed)

   - Same structure as `config.json`
   - Documents all available options
   - Includes comments/descriptions in surrounding README

3. **`.cookie`** - Cookie storage (git-ignored)
   - Single line with MoodleSession cookie value
   - Used by scrapers for authentication

**Deliverable**: Three new files with appropriate content

### Task 2: Update `.gitignore`

Add entries to prevent committing sensitive files:

```
config.json
.cookie
```

**Rationale**: Prevent accidental exposure of:

- User-specific configurations (Ollama URLs)
- Authentication cookies (sensitive credentials)

### Task 3: Refactor `test_ollama.py`

**Changes required**:

1. **Add configuration loading**:

   - Import `json` module
   - Load `config.json` at script startup
   - Extract `ollama.url` and `ollama.model`
   - Handle missing file gracefully with helpful error

2. **Replace hardcoded values**:

   - Remove `MODEL_NAME = "gemma3"` constant
   - Use `config["ollama"]["model"]` instead
   - Use `config["ollama"]["url"]` if setting custom endpoint

3. **Add validation**:

   - Check if `config.json` exists
   - Validate required keys are present
   - Provide helpful error messages if misconfigured

4. **Update error messages**:
   - Reference config file in troubleshooting suggestions
   - Show how to modify `config.json` for different models

**Example refactoring**:

```python
# Before
MODEL_NAME = "gemma3"

# After
def load_config():
    """Load configuration from config.json"""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("❌ Error: config.json not found")
        print("Copy config.json.example to config.json and customize")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in config.json: {e}")
        sys.exit(1)

config = load_config()
MODEL_NAME = config["ollama"]["model"]
OLLAMA_URL = config["ollama"].get("url", "http://localhost:11434")
```

### Task 4: Update Documentation

**Files to update**:

1. **README.md** - Add configuration section:

   - How to set up `config.json` from example
   - Where to find MoodleSession cookie
   - How to populate `.cookie` file
   - Configuration options explained

2. **Planning documents** - Already updated to reference:
   - `.cookie` for authentication
   - `config.json` for Ollama settings

## Key Technical Decisions

### Configuration Format: JSON

**Decision**: Use JSON for configuration

**Alternatives considered**:

- YAML: More readable but requires extra dependency (`PyYAML`)
- TOML: Modern, but less familiar to users
- `.env`: Good for environment variables, awkward for nested config
- Python file: Too flexible, security concerns

**Rationale for JSON**:

- Built-in Python support (no dependencies)
- Widely understood format
- Good IDE support and validation
- Structured (nested objects)
- Safe to parse (unlike `eval()` of Python files)

### Cookie Storage: Separate File

**Decision**: Store cookie in separate `.cookie` file, not in `config.json`

**Rationale**:

- **Security**: Easier to exclude from version control
- **Rotation**: Cookie changes more frequently than config
- **Simplicity**: Single-line file is easy to update programmatically
- **Safety**: Reduces risk of accidentally committing credentials

**Alternative considered**: Storing in `config.json` was rejected because:

- Config file is more likely to be shared (as example)
- Cookie is highly sensitive credential
- Different lifecycle (config rarely changes, cookie expires)

### Configuration Defaults

**Decision**: Provide sensible defaults that work for standard setup

**Defaults chosen**:

- Ollama URL: `http://localhost:11434` (standard Ollama port)
- Model: `gemma3` (balance of speed and capability)

**Rationale**:

- New users should have working config out-of-the-box
- Standard Ollama installation uses port 11434
- Gemma3 is reasonable default (fast, capable, well-supported)

### Error Handling Strategy

**Decision**: Fail fast with helpful error messages

**Approach**:

- Check for `config.json` existence before loading
- Validate JSON structure
- Provide clear instructions to fix issues
- Reference example file in errors

**Example error message**:

```
❌ Error: config.json not found

To fix this:
  1. Copy the example: cp config.json.example config.json
  2. Edit config.json with your settings

For default setup, the example values should work as-is.
```

## Migration Path

### For Existing Users

Current users of `test_ollama.py` need to:

1. Create `config.json` from example template
2. Script continues to work with same defaults
3. No behavior changes if using default model/endpoint

### Backward Compatibility

**Approach**: Smooth transition with helpful messages

- Old script behavior: Hardcoded `gemma3` model
- New script behavior: Reads from `config.json`
- If config missing: Clear error with setup instructions
- Default values match old hardcoded values

## File Structure After Implementation

```
myco_planner/
├── config.json.example      # Template (committed)
├── config.json              # Active config (git-ignored)
├── .cookie                  # MoodleSession cookie (git-ignored)
├── .gitignore               # Updated to exclude config.json and .cookie
├── test_ollama.py           # Refactored to use config.json
├── README.md                # Updated with configuration instructions
└── planning/
    ├── config_refactoring_plan.md  # This document
    ├── ollama_gemma3_test_plan.md  # Updated references
    └── scrapegraph_ai_integration_plan.md  # Updated references
```

## Validation & Testing

### Test Cases

1. **Happy path**: `config.json` exists with valid settings

   - Script loads config successfully
   - Uses configured model and URL

2. **Missing config**: `config.json` doesn't exist

   - Script shows helpful error
   - References example file

3. **Invalid JSON**: `config.json` has syntax errors

   - Script shows parse error with line number
   - Suggests validation

4. **Missing keys**: `config.json` lacks required fields

   - Script shows which keys are missing
   - Shows expected structure

5. **Different model**: Change model to `llama3` in config

   - Script uses new model
   - No code changes required

6. **Custom endpoint**: Change URL to `http://localhost:8080`
   - Script connects to custom port
   - Handles connection appropriately

### Validation Checklist

- [ ] `config.json.example` has all required fields
- [ ] `config.json.example` values work out-of-the-box
- [ ] `.gitignore` excludes sensitive files
- [ ] `test_ollama.py` loads config correctly
- [ ] Error messages are clear and actionable
- [ ] README documents configuration setup
- [ ] Config changes don't require code changes

## Security Considerations

### Sensitive Data Handling

**Files with sensitive data**:

- `.cookie` - Contains authentication credential
- `config.json` - May contain custom URLs (less sensitive)

**Mitigations**:

- Both files in `.gitignore`
- Example file has placeholder values
- README warns about not committing these files
- Clear naming (`.cookie` suggests secret)

### Configuration Validation

**Risks**:

- Malformed JSON could crash script
- Invalid URLs could cause connection errors
- Wrong model name leads to failed inference

**Mitigations**:

- Parse JSON with error handling
- Validate URL format (basic check)
- Catch model-not-found errors from Ollama
- Provide helpful error messages for each case

## Benefits of This Approach

### Developer Experience

✅ **Easy to test different models**: Edit config, run script  
✅ **Support custom Ollama setups**: Configure non-standard ports  
✅ **Clear separation**: Configuration vs. code  
✅ **Safe defaults**: Works out-of-the-box for standard setup  
✅ **Self-documenting**: Example file shows all options

### Maintenance

✅ **No code changes for config**: Update config file only  
✅ **Reusable config**: Other scripts can use same config  
✅ **Version control friendly**: Example committed, actual config ignored  
✅ **Easy troubleshooting**: Check config file first

### Security

✅ **Credentials separated**: `.cookie` file is distinct  
✅ **Git-safe**: Sensitive files automatically ignored  
✅ **Example safe to share**: No real credentials in example  
✅ **Audit trail**: Config changes tracked separately from code

## Implementation Timeline

**Estimated effort**: 1-2 hours

1. **Create files** (~15 min)

   - Write `config.json.example`
   - Copy to `config.json`
   - Create empty `.cookie` file
   - Update `.gitignore`

2. **Refactor script** (~30 min)

   - Add config loading function
   - Replace hardcoded values
   - Add validation and error handling
   - Test with various scenarios

3. **Documentation** (~15 min)

   - Update README with configuration section
   - Add inline comments in script
   - Verify planning docs are updated

4. **Testing** (~15 min)
   - Test happy path
   - Test error cases
   - Verify different models work
   - Check custom endpoints

## Success Criteria

✅ `config.json.example` exists and is documented  
✅ `config.json` and `.cookie` are git-ignored  
✅ `test_ollama.py` reads configuration from file  
✅ Script works with default configuration  
✅ Easy to change models without editing code  
✅ Clear error messages when config is missing/invalid  
✅ README documents configuration setup  
✅ All tests pass with new configuration system

## Future Enhancements

### Potential Extensions

1. **Environment variable overrides**:

   - `OLLAMA_URL` env var overrides config
   - Useful for CI/CD or containerized environments

2. **Configuration validation CLI**:

   - `python validate_config.py` to check config
   - Catch issues before running main scripts

3. **Multiple profiles**:

   - `config.dev.json`, `config.prod.json`
   - Switch with environment variable

4. **Extended settings**:
   - Timeout values
   - Retry policies
   - Output formatting options
   - Logging levels

### Not Included in This Phase

❌ **Advanced validation**: Schema validation with `jsonschema`  
❌ **Encrypted credentials**: Beyond scope for local development  
❌ **Dynamic reloading**: Watch config file for changes  
❌ **GUI configuration**: Command-line is sufficient

**Rationale**: Keep it simple for initial implementation. Add complexity only when needed.

## References

- Current script: `test_ollama.py`
- Related plans: `planning/ollama_gemma3_test_plan.md`
- Integration plan: `planning/scrapegraph_ai_integration_plan.md`
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Python JSON module](https://docs.python.org/3/library/json.html)
