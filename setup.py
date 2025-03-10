#!/usr/bin/env python3
"""
Legacy setup script for Ollama Forge.
This file exists for compatibility with older pip/setuptools versions.
The actual package configuration is in pyproject.toml.

Now imports configuration from the centralized config module when available.
"""

import setuptools
import os
import sys
from pathlib import Path

# Try most reliable import path first
try:
    # First try direct import from config.py if it exists
    config_path = Path(__file__).parent / "ollama_forge" / "config.py"
    if config_path.exists():
        sys.path.insert(0, str(config_path.parent))
        from config import (
            PACKAGE_NAME_NORMALIZED,
            get_version_string,
            get_author_string,
            get_email_string,
        )
        version = get_version_string()
        author = get_author_string()
        author_email = get_email_string()
        description = "Python client library and CLI for Ollama"
    else:
        # Try importing from the package
        sys.path.insert(0, os.path.abspath('.'))
        from ollama_forge.config import (
            PACKAGE_NAME_NORMALIZED,
            get_version_string,
            get_author_string,
            get_email_string,
        )
        version = get_version_string()
        author = get_author_string()
        author_email = get_email_string()
        description = "Python client library and CLI for Ollama"
except ImportError:
    # Fallback values if config module is not available
    version = "0.1.9"
    author = "Lloyd Handyside, Eidos" 
    author_email = "ace1928@gmail.com, syntheticeidos@gmail.com"
    description = "Python client library and CLI for Ollama"
    PACKAGE_NAME_NORMALIZED = "ollama_forge"

# Use setuptools.setup() with minimal configuration required
setuptools.setup(
    name=PACKAGE_NAME_NORMALIZED,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
)
