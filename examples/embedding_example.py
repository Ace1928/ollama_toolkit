#!/usr/bin/env python3
"""
Ollama Toolkit: Embedding Example

This script demonstrates how to use the Ollama Embedding API to create text embeddings.
"""

import argparse
import os
import sys
from typing import Any, Dict, List, Optional

import numpy as np
import requests
from colorama import init

# Initialize colorama for cross-platform colored terminal output
init()

# Try to import as a package first, then try relative imports
try:
    from ollama_toolkit.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error,
        print_header,
        print_info,
        print_success,
        print_warning,
    )
    from ollama_toolkit.utils.model_constants import (
        BACKUP_EMBEDDING_MODEL,
        DEFAULT_EMBEDDING_MODEL,
    )
except ImportError:
    # Add parent directory to path for direct execution
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    )
    try:
        from ollama_toolkit.utils.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error,
            print_header,
            print_info,
            print_success,
            print_warning,
        )
        from ollama_toolkit.utils.model_constants import (
            BACKUP_EMBEDDING_MODEL,
            DEFAULT_EMBEDDING_MODEL,
        )
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install the package using: pip install -e /path/to/ollama_toolkit")
        sys.exit(1)


def create_embedding(
    model: str,
    text: str,
    options: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    use_fallback: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Create an embedding for the provided text.

    Args:
        model: The model name
        text: The text to create an embedding for
        options: Additional model parameters
        base_url: The base URL for the Ollama Toolkit
        use_fallback: Whether to try the backup model if primary fails

    Returns:
        The embedding response or None if failed
    """
    print_header(f"Creating embedding with {model}")
    print_info(f"Text: {text}\n")

    # Prepare the request data
    data: Dict[str, Any] = {
        "model": model,
        "prompt": text,
    }

    if options:
        # Add any provided options to the request
        data.update(options)

    response = None  # Initialize response variable
    try:
        # Send the request directly using requests
        print_info(f"Sending embedding request to {base_url}/api/embed")
        response = requests.post(f"{base_url}/api/embed", json=data)
        response.raise_for_status()

        # Parse the response
        result = response.json()

        # Get the embedding
        embedding = result.get("embedding", [])

        # Print embedding info
        print_info(f"Embedding dimension: {len(embedding)}")
        print_info(f"First few values: {embedding[:5]}...")
        print_info(f"Embedding norm: {np.linalg.norm(embedding):.4f}")
        print_success("Embedding created successfully!")

        return result
    except requests.exceptions.RequestException as e:
        print_error(f"Request error with model {model}: {str(e)}")

        # Try fallback model if enabled and not already using it
        if use_fallback and model != BACKUP_EMBEDDING_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_EMBEDDING_MODEL}")
            return create_embedding(
                BACKUP_EMBEDDING_MODEL, text, options, base_url, use_fallback=False
            )
        return None
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")

        # Try fallback for any error
        if use_fallback and model != BACKUP_EMBEDDING_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_EMBEDDING_MODEL}")
            return create_embedding(
                BACKUP_EMBEDDING_MODEL, text, options, base_url, use_fallback=False
            )
        return None


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Cosine similarity score (1 = most similar, -1 = most dissimilar)
    """
    # Verify inputs
    if not embedding1 or not embedding2:
        raise ValueError("Embeddings cannot be empty")

    if len(embedding1) != len(embedding2):
        raise ValueError(
            f"Embedding dimensions must match: {len(embedding1)} != {len(embedding2)}"
        )

    # Convert to numpy arrays
    v1 = np.array(embedding1)
    v2 = np.array(embedding2)

    # Calculate norms
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Calculate cosine similarity
    similarity = np.dot(v1, v2) / (norm1 * norm2)

    # Ensure result is in valid range [-1, 1]
    return max(min(similarity, 1.0), -1.0)


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ollama Embedding API Example")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help=f"Model name (default: {DEFAULT_EMBEDDING_MODEL}, backup: {BACKUP_EMBEDDING_MODEL})",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="This is a test sentence for embedding.",
        help="Text to embed",
    )
    parser.add_argument(
        "--compare", type=str, help="Optional second text to compare similarity"
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable automatic fallback to backup model",
    )
    args = parser.parse_args()

    # Create embedding for the main text
    result1 = create_embedding(
        args.model, args.text, use_fallback=not args.no_fallback
    )
    if not result1:
        return

    # If comparison text provided, calculate similarity
    if args.compare:
        print("\n")
        print_info(f"Comparing with: '{args.compare}'")

        result2 = create_embedding(
            args.model, args.compare, use_fallback=not args.no_fallback
        )
        if not result2:
            return

        # Calculate similarity between embeddings
        embedding1 = result1.get("embedding", [])
        embedding2 = result2.get("embedding", [])

        if not embedding1 or not embedding2:
            print_error("Could not extract embeddings from responses")
            return

        # Calculate similarity
        similarity = calculate_similarity(embedding1, embedding2)
        print("\n")
        print_info(f"Cosine similarity: {similarity:.4f}")

        # Interpret similarity
        if similarity > 0.9:
            print_success("The texts are very similar in meaning")
        elif similarity > 0.7:
            print_info("The texts are moderately similar")
        elif similarity > 0.5:
            print_info("The texts have some similarity")
        else:
            print_warning("The texts are not very similar")


if __name__ == "__main__":
    main()
