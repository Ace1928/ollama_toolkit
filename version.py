"""
Version information for the Ollama Forge package.

This file now imports from the centralized config module when available,
following Eidosian principles of "Structure as Control" and "Self-Awareness as Foundation".

Client version: 0.1.9
Minimum Ollama server version: 0.1.11
"""

# Import from centralized config if available (for installed package)
try:
    from ollama_forge.config import (
        VERSION as __version__,
        VERSION_MAJOR,
        VERSION_MINOR, 
        VERSION_PATCH,
        VERSION_RELEASE_DATE,
        MINIMUM_OLLAMA_VERSION,
        get_version_string,
        get_version_tuple
    )
except ImportError:
    # Fallback for direct use from repository root
    # Current version of the Ollama Forge package
    __version__ = "0.1.9"  # Ollama Forge client version

    # Minimum compatible Ollama server version
    MINIMUM_OLLAMA_VERSION = "0.1.11"  # Confirmed minimum Ollama server version

    # Version release date (YYYY-MM-DD)
    VERSION_RELEASE_DATE = "2025-01-15"

    # Version components for programmatic access
    VERSION_MAJOR = 0
    VERSION_MINOR = 1
    VERSION_PATCH = 9

    def get_version_tuple():
        """Return version as a tuple of (major, minor, patch)."""
        return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

    def get_version_string():
        """Return the full version string."""
        return __version__

    def get_release_date():
        """Return the release date of the current version."""
        return VERSION_RELEASE_DATE

try:
    from packaging.version import parse as parse_version
except ImportError:
    # Fallback implementation if packaging is not available
    import re
    
    class SimpleVersion:
        def __init__(self, version_str):
            match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version_str)
            if not match:
                self.major = self.minor = self.patch = 0
            else:
                self.major = int(match.group(1))
                self.minor = int(match.group(2))
                self.patch = int(match.group(3))
        
        def __lt__(self, other):
            if self.major != other.major:
                return self.major < other.major
            if self.minor != other.minor:
                return self.minor < other.minor
            return self.patch < other.patch
        
        def __eq__(self, other):
            return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
        
        def __gt__(self, other):
            return other < self
        
        def __ge__(self, other):
            return self > other or self == other
    
    def parse_version(version_str):
        """Simple version parser fallback."""
        return SimpleVersion(version_str)

def is_compatible_ollama_version(version_str):
    """
    Check if the given Ollama version is compatible with this toolkit version.
    
    Args:
        version_str (str): Version string to check against minimum requirements
        
    Returns:
        bool: True if version is compatible, False otherwise
    
    Example:
        >>> is_compatible_ollama_version("0.1.11")
        True
        >>> is_compatible_ollama_version("0.1.10")
        False
    """
    try:
        min_version = parse_version(MINIMUM_OLLAMA_VERSION)
        current_version = parse_version(version_str)
        return current_version >= min_version
    except Exception:
        # If there's any error parsing the version, assume incompatible
        return False

def update_version_universally(new_version: str) -> None:
    """
    Scans the repository for references to the old version and replaces them
    with new_version, ensuring everything is kept consistent.
    
    Args:
        new_version (str): New version string to use across the codebase
        
    Returns:
        None
    """
    import os
    import re
    
    global __version__, VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH
    current_version = __version__
    
    if current_version == new_version:
        print(f"No version change needed. Current version is already {new_version}.")
        return

    # Parse the new version components
    version_match = re.match(r'^(\d+)\.(\d+)\.(\d+)', new_version)
    if not version_match:
        print(f"Invalid version format: {new_version}. Expected format: X.Y.Z")
        return
        
    new_major = int(version_match.group(1))
    new_minor = int(version_match.group(2))
    new_patch = int(version_match.group(3))
    
    replaced_any = False
    files_updated = []

    for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(__file__))):
        # Skip hidden/system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ["__pycache__", "dist", "build"]]
        
        for name in files:
            if name.startswith('.') or not any(name.endswith(ext) for ext in [".py", ".md", ".rst", ".txt", ".toml", ".yaml", ".yml", ".cfg"]):
                continue
                
            filepath = os.path.join(root, name)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace version strings
                new_content = re.sub(
                    r'(version\s*=\s*["\'])' + re.escape(current_version) + r'(["\'])',
                    r'\g<1>' + new_version + r'\g<2>',
                    content
                )
                new_content = re.sub(
                    r'(__version__\s*=\s*["\'])' + re.escape(current_version) + r'(["\'])',
                    r'\g<1>' + new_version + r'\g<2>',
                    new_content
                )
                
                # Replace version components
                new_content = re.sub(
                    r'(VERSION_MAJOR\s*=\s*)' + str(VERSION_MAJOR),
                    r'\g<1>' + str(new_major),
                    new_content
                )
                new_content = re.sub(
                    r'(VERSION_MINOR\s*=\s*)' + str(VERSION_MINOR),
                    r'\g<1>' + str(new_minor),
                    new_content
                )
                new_content = re.sub(
                    r'(VERSION_PATCH\s*=\s*)' + str(VERSION_PATCH),
                    r'\g<1>' + str(new_patch),
                    new_content
                )
                
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    replaced_any = True
                    files_updated.append(filepath)
            except Exception as e:
                print(f"Error processing file {filepath}: {str(e)}")

    if replaced_any:
        # Update in-memory version variables
        __version__ = new_version
        VERSION_MAJOR = new_major
        VERSION_MINOR = new_minor
        VERSION_PATCH = new_patch
        
        print(f"Updated version from {current_version} to {new_version} in {len(files_updated)} files.")
        for file in files_updated:
            print(f"  - {file}")
    else:
        print("No version references found. Nothing updated.")
