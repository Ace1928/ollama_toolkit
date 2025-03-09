"""
Version information for the Ollama Toolkit package.

This file contains version constants and version-related utilities
to ensure consistency across the project.
"""

# Current version of the Ollama Toolkit package
__version__ = "0.1.8"

# Minimum compatible Ollama server version
MINIMUM_OLLAMA_VERSION = "0.1.11"

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
