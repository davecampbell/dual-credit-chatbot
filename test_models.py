#!/usr/bin/env python3
"""Test which Claude models are available with your API key."""

import os
import anthropic

# Models to test (in order of preference for Dec 2025)
MODELS_TO_TEST = [
    "claude-sonnet-4-20250514",    # Claude 4 Sonnet (if exists)
    "claude-3-7-sonnet-20250219",  # Claude 3.7 Sonnet (if exists)
    "claude-3-6-sonnet-20250115",  # Claude 3.6 Sonnet (if exists)
    "claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet (Oct 2024)
    "claude-3-5-sonnet-20240620",  # Claude 3.5 Sonnet (June 2024)
    "claude-3-opus-20240229",      # Claude 3 Opus (most capable 3.0)
    "claude-3-sonnet-20240229",    # Claude 3 Sonnet
    "claude-3-haiku-20240307",     # Claude 3 Haiku (cheapest/fastest)
]

def test_model(client, model_name):
    """Test if a model is available."""
    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        return True, "✅ Works!"
    except Exception as e:
        return False, f"❌ Error: {str(e)[:50]}"

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("Run: export ANTHROPIC_API_KEY='your-key-here'")
        return

    print("Testing Claude models with your API key...\n")

    client = anthropic.Anthropic(api_key=api_key)

    working_models = []

    for model in MODELS_TO_TEST:
        works, message = test_model(client, model)
        print(f"{model:40} {message}")
        if works:
            working_models.append(model)

    print("\n" + "="*60)
    if working_models:
        print(f"\n✅ Recommended model to use: {working_models[0]}")
        print(f"\nSet it with:")
        print(f"export CLAUDE_MODEL='{working_models[0]}'")
    else:
        print("\n❌ No models are working. Check your API key!")

if __name__ == "__main__":
    main()
