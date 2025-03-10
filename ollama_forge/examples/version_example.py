#!/usr/bin/env python3
"""
Example script to get the version of the Ollama API.
"""

from ollama_forge import OllamaClient

def main() -> None:
    """Main entry point for the script."""
    client = OllamaClient()
    version = client.get_version()
    print(f"Ollama API version: {version['version']}")

if __name__ == "__main__":
    main()
