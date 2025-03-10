#!/usr/bin/env python3
"""
Example script to chat with a model using the Ollama API.
"""

from ollama_forge import OllamaClient
from ollama_forge.helpers.model_constants import DEFAULT_CHAT_MODEL

def main() -> None:
    """Main entry point for the script."""
    client = OllamaClient()

    # Chat (non-streaming)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me about neural networks."}
    ]
    response = client.chat(
        model=DEFAULT_CHAT_MODEL,
        messages=messages,
        options={"temperature": 0.7}
    )
    print("Chat response (non-streaming):")
    print(response["message"]["content"])

    # Chat (streaming)
    print("Chat response (streaming):")
    for chunk in client.chat(
        model=DEFAULT_CHAT_MODEL,
        messages=messages,
        stream=True
    ):
        if "message" in chunk:
            print(chunk["message"]["content"], end="", flush=True)

if __name__ == "__main__":
    main()
