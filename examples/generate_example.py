#!/usr/bin/env python3
"""
Example script to generate text using the Ollama API.
"""

from ollama_forge import OllamaClient
from ollama_forge.utils.model_constants import DEFAULT_CHAT_MODEL

def main() -> None:
    """Main entry point for the script."""
    client = OllamaClient()

    # Generate text (non-streaming)
    response = client.generate(
        model=DEFAULT_CHAT_MODEL,
        prompt="Explain quantum computing in simple terms",
        options={"temperature": 0.7}
    )
    print("Generated text (non-streaming):")
    print(response["response"])

    # Generate text (streaming)
    print("Generated text (streaming):")
    for chunk in client.generate(
        model=DEFAULT_CHAT_MODEL, 
        prompt="Write a short poem about AI", 
        stream=True
    ):
        if "response" in chunk:
            print(chunk["response"], end="", flush=True)

if __name__ == "__main__":
    main()
