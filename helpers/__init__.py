"""
Ollama Forge Helpers

This package provides essential helper functions and constants for the Ollama Forge toolkit.
Following Eidosian principles, it offers elegantly structured helpers for common operations.

Modules:
    common: General utility functions
    embedding: Functions for working with embeddings
    install_ollama: Helpers for installing and managing Ollama
    model_constants: Constants and resolvers for models
"""

import os
import sys
import logging

# Configure minimal logging - will be overridden if proper logging is configured
logging.basicConfig(level=logging.INFO)

# Robust import system with elegant fallbacks
try:
    # Standard relative imports for package context
    from .common import (
        print_header, print_success, print_error, print_warning, print_info, print_json,
        make_api_request, async_make_api_request, check_ollama_installed, 
        check_ollama_running, install_ollama, ensure_ollama_running,
        DEFAULT_OLLAMA_API_URL,
    )
    from .model_constants import (
        DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
        resolve_model_alias, get_fallback_model, get_model_recommendation
    )
    from .embedding import (
        calculate_similarity, normalize_vector,
        batch_calculate_similarities, process_embeddings_response,
    )
except ImportError:
    # Alternative absolute imports for direct execution or out-of-package access
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        
    try:
        from ollama_forge.helpers.common import (
            print_header, print_success, print_error, print_warning, print_info, print_json,
            make_api_request, async_make_api_request, check_ollama_installed, 
            check_ollama_running, install_ollama, ensure_ollama_running,
            DEFAULT_OLLAMA_API_URL,
        )
        from ollama_forge.helpers.model_constants import (
            DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
            DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
            resolve_model_alias, get_fallback_model, get_model_recommendation
        )
        from ollama_forge.helpers.embedding import (
            calculate_similarity, normalize_vector,
            batch_calculate_similarities, process_embeddings_response,
        )
    except ImportError as e:
        # Elegant minimal fallbacks for critical functionality
        logging.debug(f"Failed to import helpers: {e}")
        DEFAULT_OLLAMA_API_URL = "http://localhost:11434/"
        DEFAULT_CHAT_MODEL = "deepseek-r1:1.5b"
        BACKUP_CHAT_MODEL = "qwen2.5:0.5b"
        DEFAULT_EMBEDDING_MODEL = "deepseek-r1:1.5b"
        BACKUP_EMBEDDING_MODEL = "mxbai-embed-large"
        
        # Minimal implementations of critical functions
        def print_header(title): print(f"\n=== {title} ===\n")
        def print_success(msg): print(f"✓ {msg}")
        def print_error(msg): print(f"✗ {msg}")
        def print_warning(msg): print(f"⚠ {msg}")
        def print_info(msg): print(f"ℹ {msg}")
        def print_json(data): print(data)
        
        # Function stubs that raise proper errors when called
        def make_api_request(*args, **kwargs): raise ImportError("API requests unavailable")
        def async_make_api_request(*args, **kwargs): raise ImportError("Async API requests unavailable")
        def check_ollama_installed(*args, **kwargs): return (False, "Import failed")
        def check_ollama_running(*args, **kwargs): return (False, "Import failed")
        def install_ollama(*args, **kwargs): return (False, "Import failed")
        def ensure_ollama_running(*args, **kwargs): return (False, "Import failed")
        def resolve_model_alias(model_name): return model_name
        def get_fallback_model(model_name): return BACKUP_CHAT_MODEL
        def get_model_recommendation(model_name): return BACKUP_CHAT_MODEL
        def calculate_similarity(vec1, vec2): return 0.0
        def normalize_vector(vector): return vector
        def batch_calculate_similarities(query_vector, comparison_vectors): return []
        def process_embeddings_response(response): return None

# Export submodules for direct access
try:
    import common
except ImportError:
    try:
        import ollama_forge.helpers.common as common
    except ImportError:
        pass

try:
    import model_constants
except ImportError:
    try:
        import ollama_forge.helpers.model_constants as model_constants
    except ImportError:
        pass

try:
    import embedding
except ImportError:
    try:
        import ollama_forge.helpers.embedding as embedding
    except ImportError:
        pass

# Define explicit exports with perfect precision
__all__ = [
    # Formatting utilities
    "print_header", "print_success", "print_error", "print_warning", "print_info", "print_json",
    
    # API utilities
    "make_api_request", "async_make_api_request",
    
    # Ollama management
    "check_ollama_installed", "check_ollama_running", "install_ollama", "ensure_ollama_running",
    
    # Constants
    "DEFAULT_OLLAMA_API_URL",
    "DEFAULT_CHAT_MODEL", "BACKUP_CHAT_MODEL", 
    "DEFAULT_EMBEDDING_MODEL", "BACKUP_EMBEDDING_MODEL",
    
    # Model utilities
    "resolve_model_alias", "get_fallback_model", "get_model_recommendation",
    
    # Embedding utilities
    "calculate_similarity", "normalize_vector", 
    "batch_calculate_similarities", "process_embeddings_response",
    
    # Submodules
    "common", "model_constants", "embedding",
]
