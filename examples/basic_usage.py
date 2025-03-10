#!/usr/bin/env python3
"""
Basic usage example for the Ollama Forge.
"""

# Standard library imports first
import os
import sys
import argparse
import json
import logging
from typing import Dict, List, Optional, Tuple

# Try to import as a package first, then try relative imports
try:
    from ollama_forge.helpers.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error, print_header, print_info, print_success
    )
    from ollama_forge.helpers.model_constants import (
        DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL
    )
except ImportError:
    # Add parent directory to path for direct execution
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from ollama_forge.helpers.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error, print_header, print_info, print_success
        )
        from ollama_forge.helpers.model_constants import (
            DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL
        )
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install the package using: pip install -e /path/to/ollama_forge")
        sys.exit(1)

from ollama_forge import OllamaClient

def main() -> None:
    """Main entry point for the script."""
    client = OllamaClient()

    # Get version
    version = client.get_version()
    print(f"Ollama API version: {version['version']}")

    # List models
    models = client.list_models()
    print("Available models:")
    for model in models["models"]:
        print(f" - {model['name']}")

    # Generate text
    response = client.generate(
        model="llama2",
        prompt="Explain quantum computing in simple terms",
        options={"temperature": 0.7}
    )
    print("Generated text:")
    print(response["response"])

if __name__ == "__main__":
    main()
