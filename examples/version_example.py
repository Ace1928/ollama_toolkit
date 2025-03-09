#!/usr/bin/env python3
"""
Ollama Toolkit: Version Example

This script demonstrates how to fetch the Ollama version.
"""

# Standard library imports first
import os
import sys
import argparse
import json
import logging
from typing import Dict, List, Optional, Tuple, Any

import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init()

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


def get_ollama_version(
    base_url: str = DEFAULT_OLLAMA_API_URL,
) -> Optional[Dict[str, Any]]:
    """
    Get the current Ollama version

    Args:
        base_url: The base URL for the Ollama Toolkit

    Returns:
        The version information as a dictionary or None if failed
    """
    print_header("Fetching Ollama version")
    print_info(f"Connecting to Ollama Toolkit at {base_url}")

    try:
        # Make the API request
        response = requests.get(f"{base_url}/api/version")
        response.raise_for_status()
        result = response.json()
        print_success(
            f"Successfully connected to Ollama v{result.get('version', 'unknown')}"
        )
        return result
    except requests.exceptions.RequestException as e:
        print_error(f"Error connecting to Ollama Toolkit: {e}")
        return None


def main() -> None:
    # Get and display the version
    version_info = get_ollama_version()

    if version_info:
        print_info("\nVersion details:")
        print(f"  {Fore.GREEN}Version:{Style.RESET_ALL} {version_info['version']}")

        # Pretty print the full response
        print(f"\n{Fore.BLUE}Full Response:{Style.RESET_ALL}")
        print(json.dumps(version_info, indent=2))
    else:
        print_error("Failed to retrieve Ollama version.")
        print_info("Make sure Ollama is running on the specified URL.")


if __name__ == "__main__":
    main()
