"""
Ollama Toolkit client package for Python.

This package provides a comprehensive interface to interact with the Ollama API,
following Eidosian principles of elegance, efficiency, and contextual integrity.
"""

__version__ = "0.1.9"
__author__ = "Lloyd Handyside, Eidos"
__email__ = "ace1928@gmail.com, eidos@gmail.com"

# Re-export core components for convenient top-level imports
from .client import OllamaClient
from .utils.common import (
    print_header, print_success, print_error, 
    print_warning, print_info, print_json,
    make_api_request, async_make_api_request,
    DEFAULT_OLLAMA_API_URL,
    ensure_ollama_running, check_ollama_installed, 
    check_ollama_running, install_ollama
)
from .exceptions import (
    OllamaAPIError, OllamaConnectionError, 
    OllamaModelNotFoundError, OllamaServerError,
    ConnectionError, TimeoutError, ModelNotFoundError, 
    ServerError, InvalidRequestError, StreamingError, ParseError
)
from .utils.model_constants import (
    DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL,
    resolve_model_alias, get_fallback_model
)

# Package structure imports - allow accessing modules as namespaces
from . import utils
from . import tools
from . import cli

# Make examples importable both ways
try:
    from . import examples
except ImportError:
    # Allow the package to be imported even if examples aren't available
    pass

__all__ = [
    # Core client
    "OllamaClient",
    
    # Constants
    "DEFAULT_OLLAMA_API_URL",
    "DEFAULT_CHAT_MODEL", "BACKUP_CHAT_MODEL",
    "DEFAULT_EMBEDDING_MODEL", "BACKUP_EMBEDDING_MODEL",
    
    # Utility functions
    "print_header", "print_success", "print_error", 
    "print_warning", "print_info", "print_json",
    "make_api_request", "async_make_api_request",
    "ensure_ollama_running", "check_ollama_installed", 
    "check_ollama_running", "install_ollama",
    "resolve_model_alias", "get_fallback_model",
    
    # Exceptions
    "OllamaAPIError", "OllamaConnectionError", 
    "OllamaModelNotFoundError", "OllamaServerError",
    "ConnectionError", "TimeoutError", "ModelNotFoundError", 
    "ServerError", "InvalidRequestError", "StreamingError", "ParseError",
    
    # Namespaces
    "utils", "tools", "cli", "examples",
    
    # Version info
    "__version__",
]
