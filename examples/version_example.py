#!/usr/bin/env python3
"""
Ollama Toolkit: Version Example

This script demonstrates how to fetch the Ollama version.
"""

import json
import os
import sys
from typing import Any, Dict, Optional

import requests
from colorama import Fore, Style, init

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
