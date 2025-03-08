"""
Ollama API client package for Python.

This package provides a convenient interface to interact with the Ollama API.
"""

# Import version info
__version__ = "0.1.0"
__author__ = "Lloyd Handyside"
__email__ = "ace1928@gmail.com"

# Import directly from local directories
from .utils.common import (
    print_header, print_success, print_error, print_warning,
    print_info, print_json, make_api_request, DEFAULT_OLLAMA_API_URL
)

# Import client
from .client import OllamaClient

# Import exceptions
from .exceptions import (
    OllamaAPIError, ConnectionError, TimeoutError,
    ModelNotFoundError, ServerError, InvalidRequestError
)

__all__ = [
    # Common utilities
    "print_header", "print_success", "print_error", "print_warning",
    "print_info", "print_json", "make_api_request", "DEFAULT_OLLAMA_API_URL",
    
    # Client class
    "OllamaClient",
    
    # Exceptions
    "OllamaAPIError", "ConnectionError", "TimeoutError",
    "ModelNotFoundError", "ServerError", "InvalidRequestError"
]
