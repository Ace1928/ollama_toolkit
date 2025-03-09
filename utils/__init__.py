"""
Utility modules for the Ollama Toolkit client.

This package provides essential utility functions, constants, and tools
for working with Ollama.
"""

# Standard imports
import sys
import os
import logging

# Configure minimal logging - will be overridden if proper logging is imported
try:
    logging.basicConfig(level=logging.INFO)
except Exception:
    pass

# Import and re-export common utilities with universal compatibility
try:
    # Try normal relative import first (when imported as a package)
    from .common import (
        print_header, print_success, print_error,
        print_warning, print_info, print_json,
        make_api_request, async_make_api_request,
        check_ollama_installed, check_ollama_running,
        install_ollama, ensure_ollama_running,
        DEFAULT_OLLAMA_API_URL,
    )
except ImportError:
    # When run directly, try absolute import
    try:
        # Add parent directory to path for absolute imports
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
            
        from ollama_toolkit.utils.common import (
            print_header, print_success, print_error,
            print_warning, print_info, print_json,
            make_api_request, async_make_api_request,
            check_ollama_installed, check_ollama_running,
            install_ollama, ensure_ollama_running,
            DEFAULT_OLLAMA_API_URL,
        )
    except ImportError as e:
        logging.debug(f"Failed to import common utilities: {e}")
        # Define minimal fallbacks for critical functions
        DEFAULT_OLLAMA_API_URL = "http://localhost:11434/"
        
        def print_header(title): print(f"\n=== {title} ===\n")
        def print_success(msg): print(f"Success: {msg}")
        def print_error(msg): print(f"Error: {msg}")
        def print_warning(msg): print(f"Warning: {msg}")
        def print_info(msg): print(f"Info: {msg}")
        def print_json(data): print(data)
        
        # Let these raise ImportError if called - they're not fallbackable
        def make_api_request(*args, **kwargs): raise ImportError("API requests unavailable")
        def async_make_api_request(*args, **kwargs): raise ImportError("Async API requests unavailable")
        def check_ollama_installed(*args, **kwargs): return (False, "Import failed")
        def check_ollama_running(*args, **kwargs): return (False, "Import failed")
        def install_ollama(*args, **kwargs): return (False, "Import failed")
        def ensure_ollama_running(*args, **kwargs): return (False, "Import failed")

# Import and re-export model constants with similar fallback approach
try:
    from .model_constants import (
        DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
        resolve_model_alias, get_fallback_model,
    )
except ImportError:
    try:
        from ollama_toolkit.utils.model_constants import (
            DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
            DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
            resolve_model_alias, get_fallback_model,
        )
    except ImportError:
        # Fallback definitions if module is missing
        DEFAULT_CHAT_MODEL = "deepseek-r1:1.5b"
        BACKUP_CHAT_MODEL = "qwen2.5:0.5b"
        DEFAULT_EMBEDDING_MODEL = "deepseek-r1:1.5b"
        BACKUP_EMBEDDING_MODEL = "mxbai-embed-large"
        
        def resolve_model_alias(model_name):
            """Fallback resolver that returns the model name unchanged."""
            return model_name
            
        def get_fallback_model(model_name):
            """Fallback function that returns the backup chat model."""
            return BACKUP_CHAT_MODEL

# Make submodules directly importable with robust fallback handling
try:
    from . import common
except ImportError:
    try:
        import ollama_toolkit.utils.common as common
    except ImportError:
        import logging
        logging.debug("Could not import common module")

try:
    from . import model_constants
except ImportError:
    try:
        import ollama_toolkit.utils.model_constants as model_constants
    except ImportError:
        import logging
        logging.debug("Could not import model_constants module")

__all__ = [
    # Formatting utilities
    "print_header", "print_success", "print_error",
    "print_warning", "print_info", "print_json",
    
    # API utilities
    "make_api_request", "async_make_api_request",
    
    # Ollama management
    "check_ollama_installed", "check_ollama_running",
    "install_ollama", "ensure_ollama_running",
    
    # Constants
    "DEFAULT_OLLAMA_API_URL",
    "DEFAULT_CHAT_MODEL", "BACKUP_CHAT_MODEL", 
    "DEFAULT_EMBEDDING_MODEL", "BACKUP_EMBEDDING_MODEL",
    
    # Model utilities
    "resolve_model_alias", "get_fallback_model",
    
    # Submodules
    "common", "model_constants",
]
