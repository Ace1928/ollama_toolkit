#!/usr/bin/env python3
"""
Basic example showing how to use the Ollama Toolkit client.
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
    from ollama_toolkit.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error, print_header, print_info, print_success
    )
    from ollama_toolkit.utils.model_constants import (
        DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL
    )
except ImportError:
    # Add parent directory to path for direct execution
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from ollama_toolkit.utils.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error, print_header, print_info, print_success
        )
        from ollama_toolkit.utils.model_constants import (
            DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL
        )
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install the package using: pip install -e /path/to/ollama_toolkit")
        sys.exit(1)

from ollama_toolkit import OllamaClient

def main():
    """Run a basic example of the Ollama Toolkit client."""
    # Initialize the client
    client = OllamaClient()
    
    # Get the version
    version = client.get_version()
    print(f"Connected to Ollama version: {version['version']}")
    
    # List available models
    models = client.list_models()
    print("\nAvailable models:")
    for model in models.get("models", []):
        print(f"- {model.get('name')}")
    
    # Check if we have any models before continuing
    if not models.get("models"):
        print("No models found. Please pull a model using: ollama pull llama2")
        return
        
    # Use the first available model
    model_name = models["models"][0]["name"]
    
    # Generate a completion
    print(f"\nGenerating completion with {model_name}...")
    response = client.generate(
        model=model_name,
        prompt="Explain what an API is in simple terms.",
        options={"temperature": 0.7},
        stream=False
    )
    
    print("\nResponse:")
    print(response["response"])

if __name__ == "__main__":
    main()
