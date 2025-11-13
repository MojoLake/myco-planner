#!/usr/bin/env python3
"""
Ollama + Gemma3 Basic Test Script

This script tests the local Ollama installation with Gemma3 model to verify:
- Ollama service is running and accessible
- Gemma3 model is properly installed
- Python can communicate with Ollama
- Basic text generation works as expected
- Response times are acceptable
"""

import json
import sys
import time
from pathlib import Path

try:
    import ollama
except ImportError:
    print("❌ Error: 'ollama' library not found.")
    print("Install it with: pip install ollama")
    sys.exit(1)

# Configuration
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load configuration from config.json with validation."""
    if not path.exists():
        print("❌ Error: config.json not found.")
        print(f"Expected path: {path}")
        print(
            "Create the file (see the committed config.json for defaults) and try again."
        )
        sys.exit(1)

    try:
        with path.open(encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as exc:
        print("❌ Error: Invalid JSON in config.json.")
        print(f"   {exc}")
        print("Fix the JSON syntax (a trailing comma is a common issue) and try again.")
        sys.exit(1)
    except OSError as exc:
        print("❌ Error: Unable to read config.json.")
        print(f"   {exc}")
        sys.exit(1)

    if "ollama" not in config or not isinstance(config["ollama"], dict):
        print("❌ Error: config.json is missing the 'ollama' section.")
        print("Expected structure:")
        print(
            json.dumps(
                {
                    "ollama": {
                        "url": "http://localhost:11434",
                        "model": "gemma3",
                    }
                },
                indent=2,
            )
        )
        sys.exit(1)

    ollama_config = config["ollama"]
    missing_keys = [key for key in ("url", "model") if key not in ollama_config]
    if missing_keys:
        print("❌ Error: config.json is missing required keys in the 'ollama' section.")
        print(f"Missing: {', '.join(missing_keys)}")
        print("Update config.json with the required keys and try again.")
        sys.exit(1)

    return config


CONFIG = load_config()
MODEL_NAME = CONFIG["ollama"]["model"]
OLLAMA_URL = CONFIG["ollama"]["url"]
TIMEOUT_SECONDS = 30

# Test prompt that checks JSON formatting and domain relevance
TEST_PROMPT = (
    "List 3 common elements found on an academic course website, "
    "formatted as JSON with 'name' and 'description' fields."
)


def test_ollama_connection():
    """Test connection to Ollama and generate response from Gemma3."""

    print("=" * 50)
    print("=== Ollama + Gemma3 Test ===")
    print("=" * 50)
    print()
    print(f"Testing connection to Ollama")
    print(f"Endpoint: {OLLAMA_URL}")
    print(f"Model: {MODEL_NAME}")
    print(f"Timeout: {TIMEOUT_SECONDS}s")
    print()

    print("Sending test prompt...")
    print(f'Prompt: "{TEST_PROMPT}"')
    print()

    # Measure response time
    start_time = time.time()

    try:
        client = ollama.Client(host=OLLAMA_URL)

        # Send request to Ollama using the official library
        response = client.generate(
            model=MODEL_NAME,
            prompt=TEST_PROMPT,
        )

        elapsed_time = time.time() - start_time

        # Extract generated text
        generated_text = response["response"]

        # Display results
        print(f"Response received in {elapsed_time:.1f}s:")
        print("-" * 50)
        print(generated_text)
        print("-" * 50)
        print()

        # Check success criteria
        print("✅ Test PASSED")
        print(f"   - Connection successful")
        print(f"   - Model responded")
        print(f"   - Response time: {elapsed_time:.1f}s", end="")

        if elapsed_time < TIMEOUT_SECONDS:
            print(f" (< {TIMEOUT_SECONDS}s ✓)")
        else:
            print(f" (>= {TIMEOUT_SECONDS}s ⚠)")

        print(f"   - Response length: {len(generated_text)} characters")
        print()

        return True

    except ollama.ResponseError as e:
        print("❌ Test FAILED")
        print(f"   Error: {e.error}")
        print()
        if e.status_code == 404:
            print("To fix this, run:")
            print(f"   ollama pull {MODEL_NAME}")
        return False

    except ConnectionError:
        print("❌ Test FAILED")
        print("   Error: Connection failed to Ollama")
        print()
        print("Possible causes:")
        print("   1. Ollama service is not running")
        print("   2. Ollama is running on a different port or host")
        print()
        print("To fix this:")
        print("   - Check if Ollama is running: ollama list")
        print("   - Start Ollama if needed: ollama serve")
        print(
            "   - Confirm the 'url' in config.json points to the correct Ollama endpoint"
        )
        print("   - Or simply run any ollama command: ollama --version")
        return False

    except ValueError as e:
        print("❌ Test FAILED")
        print(f"   Invalid configuration value: {e}")
        print()
        print(
            "Check the 'url' value in config.json and ensure it is a valid HTTP(S) URL."
        )
        return False

    except TimeoutError:
        elapsed_time = time.time() - start_time
        print("❌ Test FAILED")
        print(f"   Error: Request timed out after {elapsed_time:.1f}s")
        print()
        print("The model may be:")
        print("   - Still loading (first run can be slow)")
        print("   - Too slow for this timeout setting")
        print()
        print("Try:")
        print("   - Running the test again (subsequent runs are faster)")
        print("   - Testing manually: ollama run gemma3 'test prompt'")
        return False

    except Exception as e:
        print("❌ Test FAILED")
        print(f"   Unexpected error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = test_ollama_connection()
    sys.exit(0 if success else 1)
