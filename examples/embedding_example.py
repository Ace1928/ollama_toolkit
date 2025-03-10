#!/usr/bin/env python3
"""
Example script to create embeddings using the Ollama API.
"""

# Standard library imports first
import os
import sys
import argparse
import json
import logging
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import requests
from colorama import init

# Initialize colorama for cross-platform colored terminal output
init()

# Try to import as a package first, then try relative imports
try:
    from ollama_forge.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error,
        print_header,
        print_info,
        print_success,
    )
    from ollama_forge.utils.model_constants import (
        DEFAULT_CHAT_MODEL,
        BACKUP_CHAT_MODEL,
    )
except ImportError:
    # Add parent directory to path for direct execution
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from ollama_forge.utils.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error,
            print_header,
            print_info,
            print_success,
        )
        from ollama_forge.utils.model_constants import (
            BACKUP_EMBEDDING_MODEL,
            DEFAULT_EMBEDDING_MODEL,
        )
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install the package using: pip install -e /path/to/ollama_forge")
        sys.exit(1)

from ollama_forge import OllamaClient
from ollama_forge.utils.model_constants import DEFAULT_EMBEDDING_MODEL

def main() -> None:
    """Main entry point for the script."""
    client = OllamaClient()

    # Create embedding
    embedding = client.create_embedding(
        model=DEFAULT_EMBEDDING_MODEL,
        prompt="This is a sample text for embedding."
    )
    print("Created embedding:")
    print(embedding["embedding"])

    # Batch embeddings
    embeddings = client.batch_embeddings(
        model=DEFAULT_EMBEDDING_MODEL,
        prompts=["Text one", "Text two", "Text three"]
    )
    print("Created batch embeddings:")
    for i, emb in enumerate(embeddings):
        print(f"Embedding {i+1}: {emb['embedding']}")

if __name__ == "__main__":
    main()
