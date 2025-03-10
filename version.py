"""
Version information for the Ollama Forge package.

This file contains version constants and version-related utilities
to ensure consistency across the project.

Client version: 0.1.9
Minimum Ollama server version: 0.1.11
"""

# Current version of the Ollama Forge package
__version__ = "0.1.9"             # Ollama Forge client version

# Minimum compatible Ollama server version
MINIMUM_OLLAMA_VERSION = "0.1.11"  # Confirmed minimum Ollama server version

# Version release date (YYYY-MM-DD)
VERSION_RELEASE_DATE = "2023-10-15"

# Version components for programmatic access
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 9  # Updated from 8 to 9 to match __version__

def get_version_tuple():
    """Return version as a tuple of (major, minor, patch)."""
    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_version_string():
    """Return the full version string."""
    return __version__

from packaging.version import parse as parse_version

def is_compatible_ollama_version(version_str):
    """Check if the given Ollama version is compatible with this toolkit version."""
    try:
        min_version = parse_version(MINIMUM_OLLAMA_VERSION)
        current_version = parse_version(version_str)
        return current_version >= min_version
    except (IndexError, ValueError):
        # If there's any error parsing the version, assume incompatible
        return False

import re
import os

def update_version_universally(new_version: str) -> None:
    """
    Scans the repository for references to the old version and replaces them
    with new_version, ensuring everything is kept consistent.
    """
    global __version__  # Moved to top of function before any usage of __version__
    current_version = __version__
    if current_version == new_version:
        print(f"No version change needed. Current version is already {new_version}.")
        return

    replaced_any = False

    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        # Skip hidden/system directories
        if any(ignored in root for ignored in [".git", "__pycache__"]):
            continue
        for name in files:
            if not any(name.endswith(ext) for ext in [".py", ".md", ".rst", ".txt"]):
                continue
            filepath = os.path.join(root, name)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = content.replace(current_version, new_version)
            if new_content != content:
                replaced_any = True
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated version in {filepath}")

    if replaced_any:
        # Also update our own __version__ in memory
        __version__ = new_version
        print(f"Global __version__ updated to {new_version}")
    else:
        print("No version references found. Nothing updated.")
