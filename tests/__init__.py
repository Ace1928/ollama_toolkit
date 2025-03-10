"""
Test package for the ollama_forge package.

This package contains comprehensive tests for all ollama_forge functionality.
"""

# Standard imports
import sys
import os
import logging

# Ensure parent directory is in path for running tests
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import test modules for direct access with robust error handling
test_modules = {}

# Try to import all test modules safely
for module_name in [
    "test_client", "test_chat", "test_embedding", 
    "test_helpers", "test_coverage", "test_nexus", "conftest"
]:
    try:
        # Try relative import first (package context)
        module = __import__(f".{module_name}", globals(), locals(), ["*"], 1)
        test_modules[module_name] = module
    except ImportError:
        try:
            # Try absolute import next (direct execution context)
            module = __import__(f"ollama_forge.tests.{module_name}", fromlist=["*"])
            test_modules[module_name] = module
        except ImportError as e:
            logging.debug(f"Could not import {module_name}: {e}")

# Define classes for explicit exports
TestOllamaClient = getattr(test_modules.get("test_client", {}), "TestOllamaClient", None)
TestChat = getattr(test_modules.get("test_chat", {}), "TestChat", None)
TestEmbeddings = getattr(test_modules.get("test_embedding", {}), "TestEmbeddings", None)
TestHelpers = getattr(test_modules.get("test_helpers", {}), "TestHelpers", None)
TestCodeCoverage = getattr(test_modules.get("test_coverage", {}), "TestCodeCoverage", None)

# Convert available modules to namespace attributes
test_client = test_modules.get("test_client")
test_chat = test_modules.get("test_chat")
test_embedding = test_modules.get("test_embedding")
test_helpers = test_modules.get("test_helpers")
test_coverage = test_modules.get("test_coverage")
test_nexus = test_modules.get("test_nexus")
conftest = test_modules.get("conftest")

__all__ = [
    # Test classes (if available)
    name for name in [
        "TestOllamaClient", "TestChat", "TestEmbeddings", 
        "TestHelpers", "TestCodeCoverage"
    ] if locals().get(name) is not None
] + [
    # Test modules (if available)
    name for name in [
        "test_client", "test_chat", "test_embedding", "test_helpers",
        "test_coverage", "test_nexus", "conftest"
    ] if locals().get(name) is not None
]
