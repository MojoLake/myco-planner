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

import sys
import time

try:
    import ollama
except ImportError:
    print("❌ Error: 'ollama' library not found.")
    print("Install it with: pip install ollama")
    sys.exit(1)

# Constants
MODEL_NAME = "gemma3"
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
    print(f"Model: {MODEL_NAME}")
    print(f"Timeout: {TIMEOUT_SECONDS}s")
    print()

    print("Sending test prompt...")
    print(f'Prompt: "{TEST_PROMPT}"')
    print()

    # Measure response time
    start_time = time.time()

    try:
        # Send request to Ollama using the official library
        response = ollama.generate(
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
        print("   2. Ollama is running on a different port")
        print()
        print("To fix this:")
        print("   - Check if Ollama is running: ollama list")
        print("   - Start Ollama if needed: ollama serve")
        print("   - Or simply run any ollama command: ollama --version")
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
