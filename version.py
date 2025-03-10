"""
Version information for the Ollama Toolkit package.

This file contains version constants and version-related utilities
to ensure consistency across the project.

Client version: 0.1.8
Minimum Ollama server version: 0.1.11
"""

# Current version of the Ollama Toolkit package
__version__ = "0.1.8"             # Ollama Toolkit client version

# Minimum compatible Ollama server version
MINIMUM_OLLAMA_VERSION = "0.1.11"  # Confirmed minimum Ollama server version

# Version release date (YYYY-MM-DD)
VERSION_RELEASE_DATE = "2023-10-15"

# Version components for programmatic access
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 8

def get_version_tuple():
    """Return version as a tuple of (major, minor, patch)."""
    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_version_string():
    """Return the full version string."""
    return __version__

def is_compatible_ollama_version(version_str):
    """Check if the given Ollama version is compatible with this toolkit version."""
    try:
        # Simple version comparison - can be expanded for more complex comparisons
        min_parts = MINIMUM_OLLAMA_VERSION.split('.')
        version_parts = version_str.split('.')
        
        # Compare major version
        if int(version_parts[0]) < int(min_parts[0]):
            return False
        
        # If major version is equal, compare minor version
        if int(version_parts[0]) == int(min_parts[0]) and int(version_parts[1]) < int(min_parts[1]):
            return False
            
        # If major and minor are equal, compare patch
        if (int(version_parts[0]) == int(min_parts[0]) and 
            int(version_parts[1]) == int(min_parts[1]) and 
            int(version_parts[2]) < int(min_parts[2])):
            return False
            
        return True
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
        global __version__
        __version__ = new_version
        print(f"Global __version__ updated to {new_version}")
    else:
        print("No version references found. Nothing updated.")
