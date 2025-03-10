"""
Centralized configuration for Ollama Forge

This module provides a single source of truth for all configuration values
following the Eidosian principles of "Structure as Control" and "Contextual Integrity".
All important constants and settings are defined here to ensure consistency
across the entire project.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

# ========== VERSION INFORMATION ==========
VERSION = "0.1.9"
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 9
VERSION_RELEASE_DATE = "2025-01-15"
MINIMUM_OLLAMA_VERSION = "0.1.11"

# ========== PACKAGE METADATA ==========
PACKAGE_NAME = "ollama-forge"
PACKAGE_NAME_NORMALIZED = "ollama_forge"  # Python package name (no hyphens)
AUTHORS = [
    {"name": "Lloyd Handyside", "email": "ace1928@gmail.com"},
    {"name": "Eidos", "email": "syntheticeidos@gmail.com"},
]
LICENSE = "MIT"
REPOSITORY_URL = "https://github.com/Ace1928/ollama_forge"
DOCUMENTATION_URL = "https://ollama-forge.readthedocs.io"
COPYRIGHT_YEAR = "2025"

# ========== API DEFAULTS ==========
DEFAULT_OLLAMA_API_URL = "http://localhost:11434"
DEFAULT_API_TIMEOUT = 60.0  # seconds

# ========== MODEL DEFAULTS ==========
DEFAULT_CHAT_MODEL = "llama2"
BACKUP_CHAT_MODEL = "mistral"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
BACKUP_EMBEDDING_MODEL = "all-minilm"

# ========== FILE PATHS ==========
def get_package_root() -> Path:
    """Get the package root directory."""
    # Get the directory this file is in
    this_file = Path(__file__).resolve()
    # The package root is one level up from this file
    return this_file.parent.parent

def get_config_path() -> Path:
    """Get path for config files based on OS."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", "~/.ollama-forge"))
    elif sys.platform == "darwin":
        base = Path("~/Library/Application Support/ollama-forge")
    else:
        base = Path("~/.config/ollama-forge")
    return base.expanduser()

def get_cache_path() -> Path:
    """Get path for cache files based on OS."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", "~/.ollama-forge-cache"))
    elif sys.platform == "darwin":
        base = Path("~/Library/Caches/ollama-forge")
    else:
        base = Path("~/.cache/ollama-forge")
    return base.expanduser()

# ========== ENVIRONMENT VARIABLES ==========
def get_env_variable(name: str, default: Any = None) -> Any:
    """Get environment variable with specific prefix."""
    env_var = f"OLLAMA_FORGE_{name}"
    return os.environ.get(env_var, default)

def is_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return get_env_variable("DEBUG", "0") == "1"

# ========== CONVENIENCE FUNCTIONS ==========
def get_version_string() -> str:
    """Return the full version string."""
    return VERSION

def get_version_tuple() -> Tuple[int, int, int]:
    """Return version as a tuple of (major, minor, patch)."""
    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_author_string() -> str:
    """Return formatted author string."""
    return ", ".join(f"{author['name']}" for author in AUTHORS)

def get_email_string() -> str:
    """Return formatted email string."""
    return ", ".join(f"{author['email']}" for author in AUTHORS)

# Initialize paths on module import
CONFIG_PATH = get_config_path()
CACHE_PATH = get_cache_path()
PACKAGE_ROOT = get_package_root()

# Ensure directories exist
CONFIG_PATH.mkdir(parents=True, exist_ok=True)
CACHE_PATH.mkdir(parents=True, exist_ok=True)
