#!/usr/bin/env python3
"""
Legacy setup script for Ollama Forge.
This file exists for compatibility with older pip/setuptools versions.
The actual package configuration is in pyproject.toml.
"""

import setuptools

# Use setuptools.setup() with minimal configuration required.
# All actual configuration should be in pyproject.toml.
setuptools.setup(
    name="ollama_forge",
    author="Lloyd Handyside, Eidos",
    author_email="ace1928@gmail.com",
    description="Python client library and CLI for Ollama",
)
