#!/usr/bin/env python3
"""
Configuration module for Ollama Forge.

This module serves as the central source of truth for all configuration
parameters and versioning information used throughout the package.
It embodies the Eidosian principles of Structure as Control and Contextual Integrity.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

# Package metadata - single source of truth
PACKAGE_NAME = "Ollama Forge"
PACKAGE_NAME_NORMALIZED = "ollama_forge"
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 9
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
VERSION_RELEASE_DATE = "2025-01-15"

# Default API configuration
DEFAULT_OLLAMA_API_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_RETRIES = 3

# Model defaults - critical for cross-module consistency
DEFAULT_CHAT_MODEL = "deepseek-r1:1.5b"  # Optimal balance of speed and quality
BACKUP_CHAT_MODEL = "qwen2.5:0.5b-Instruct"  # Excellent small model fallback
DEFAULT_EMBEDDING_MODEL = DEFAULT_CHAT_MODEL  # Using chat model for embeddings improves context
BACKUP_EMBEDDING_MODEL = BACKUP_CHAT_MODEL

# Context window configurations
DEFAULT_MIN_CONTEXT = 2048
RECOMMENDED_CONTEXT = 4096

# Package authors
AUTHORS = [
    {"name": "Lloyd Handyside", "email": "ace1928@gmail.com"},
    {"name": "Eidos", "email": "syntheticeidos@gmail.com"}
]

# Environment variable control flags
DEBUG_MODE = os.environ.get("OLLAMA_FORGE_DEBUG") == "1"
VERBOSE_MODE = os.environ.get("OLLAMA_FORGE_VERBOSE") == "1"
LOG_LEVEL = os.environ.get("OLLAMA_FORGE_LOG_LEVEL", "INFO").upper()
DISABLE_PROGRESS_BARS = os.environ.get("OLLAMA_FORGE_NO_PROGRESS") == "1"

# User and system paths
USER_CONFIG_DIR = os.path.expanduser(os.path.join("~", ".config", "ollama_forge"))
USER_CACHE_DIR = os.path.expanduser(os.path.join("~", ".cache", "ollama_forge"))
USER_DATA_DIR = os.path.expanduser(os.path.join("~", ".local", "share", "ollama_forge"))

# API endpoints mapping - centralizes all endpoint definitions
API_ENDPOINTS = {
    "version": "/api/version",
    "generate": "/api/generate",
    "chat": "/api/chat",
    "embedding": "/api/embed",
    "tags": "/api/tags",
    "pull": "/api/pull",
    "push": "/api/push",
    "delete": "/api/delete",
    "copy": "/api/copy",
    "create": "/api/create",
}

# Function getters for consistent access throughout the package
def get_version_string() -> str:
    """Return the full version string."""
    return VERSION

def get_version_tuple() -> Tuple[int, int, int]:
    """Return version as a tuple of (major, minor, patch)."""
    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_release_date() -> str:
    """Return the release date of the current version."""
    return VERSION_RELEASE_DATE

def get_author_string() -> str:
    """Return a formatted author string."""
    return ", ".join(author["name"] for author in AUTHORS)

def get_email_string() -> str:
    """Return a formatted email string."""
    return ", ".join(author["email"] for author in AUTHORS)

def get_default_api_endpoint(operation: str) -> str:
    """Get the API endpoint for a specific operation."""
    return API_ENDPOINTS.get(operation, "")

def is_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return DEBUG_MODE

# Dynamic configuration based on environment and capabilities
try:
    import rich
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Platform-specific configurations
import platform
SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_MACOS = SYSTEM == "darwin"
IS_LINUX = SYSTEM == "linux"

# Create user directories if they don't exist
for directory in [USER_CONFIG_DIR, USER_CACHE_DIR, USER_DATA_DIR]:
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        pass  # Silent pass if directory creation fails

# Runtime configuration that may be modified during execution
runtime_config = {
    "api_url": DEFAULT_OLLAMA_API_URL,
    "timeout": DEFAULT_TIMEOUT,
    "max_retries": DEFAULT_MAX_RETRIES,
    "chat_model": DEFAULT_CHAT_MODEL,
    "embedding_model": DEFAULT_EMBEDDING_MODEL,
}

def update_runtime_config(key: str, value: Any) -> None:
    """Update a runtime configuration value."""
    if key in runtime_config:
        runtime_config[key] = value

def get_runtime_config(key: str, default: Any = None) -> Any:
    """Get a runtime configuration value."""
    return runtime_config.get(key, default)

def reset_runtime_config() -> None:
    """Reset runtime configuration to defaults."""
    runtime_config.update({
        "api_url": DEFAULT_OLLAMA_API_URL,
        "timeout": DEFAULT_TIMEOUT,
        "max_retries": DEFAULT_MAX_RETRIES,
        "chat_model": DEFAULT_CHAT_MODEL,
        "embedding_model": DEFAULT_EMBEDDING_MODEL,
    })

# Package initialization banner for debug mode
if DEBUG_MODE:
    print(f"🔍 Ollama Forge v{VERSION} configuration loaded")
    print(f"📂 User config directory: {USER_CONFIG_DIR}")
    print(f"🔧 Default API URL: {DEFAULT_OLLAMA_API_URL}")
    print(f"🤖 Default models: chat={DEFAULT_CHAT_MODEL}, embedding={DEFAULT_EMBEDDING_MODEL}")
