#!/usr/bin/env python3
"""
Example script for checking Ollama and client versions.

This example demonstrates version checking, compatibility validation,
and proper error handling for version-related operations.
"""

import os
import sys
from typing import Dict, Any, Tuple

# Add parent directory to path for direct script execution
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ollama_forge import OllamaClient
from ollama_forge.helpers.common import print_header, print_success, print_error, print_info
from version import is_compatible_ollama_version, __version__ as client_version

def check_versions() -> Tuple[Dict[str, str], bool]:
    """
    Check and validate Ollama and client versions.
    
    Returns:
        Tuple containing version information dict and compatibility status
    """
    client = OllamaClient()
    
    try:
        # Get Ollama version
        version_info = client.get_version()
        ollama_version = version_info.get("version", "unknown")
        
        # Create version information dictionary
        versions = {
            "client": client_version,
            "ollama_server": ollama_version,
        }
        
        # Check compatibility
        is_compatible = is_compatible_ollama_version(ollama_version)
        
        return versions, is_compatible
        
    except Exception as e:
        print_error(f"Error checking versions: {e}")
        return {"client": client_version, "ollama_server": "unavailable"}, False

def main() -> None:
    """Main function to demonstrate version checking."""
    print_header("Ollama Forge Version Example")
    
    print_info("Checking Ollama Forge and Ollama versions...")
    versions, is_compatible = check_versions()
    
    print("\nVersion Information:")
    print(f"• Ollama Forge client: v{versions['client']}")
    print(f"• Ollama server: v{versions['ollama_server']}")
    
    if is_compatible:
        print_success("\nVersions are compatible! ✅")
    else:
        print_error("\nWarning: Versions might not be compatible! ⚠️")
        print_info("Consider upgrading Ollama to ensure full compatibility.")
    
    print("\nAdditional Version Operations:")
    print("1. To update Ollama: Run 'curl -fsSL https://ollama.com/install.sh | sh'")
    print("2. To update Ollama Forge: Run 'pip install --upgrade ollama-forge'")

if __name__ == "__main__":
    main()
