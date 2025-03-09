"""
Utility modules for the Ollama Toolkit client.

This package provides essential utility functions, constants, and tools
for working with Ollama.
"""

# Import and re-export common utilities
from .common import (
    # Formatting utilities
    print_header, print_success, print_error,
    print_warning, print_info, print_json,
    
    # API utilities
    make_api_request, async_make_api_request,
    
    # Ollama management
    check_ollama_installed, check_ollama_running,
    install_ollama, ensure_ollama_running,
    
    # Constants
    DEFAULT_OLLAMA_API_URL,
)

# Import and re-export model constants
try:
    from .model_constants import (
        # Default models
        DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
        
        # Model utilities
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

# Make submodules directly importable
from . import common
try:
    from . import model_constants
except ImportError:
    pass

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
