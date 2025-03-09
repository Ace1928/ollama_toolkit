"""
Ollama Toolkit client package for Python.

This package provides a convenient interface to interact with the Ollama Toolkit,
elevated to peak Eidosian perfection.
"""

__version__ = "0.1.7"
__author__ = "Lloyd Handyside, Eidos"
__email__ = "ace1928@gmail.com, eidos@gmail.com"

# Utilities
from .utils.common import (
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_json,
    make_api_request,
    DEFAULT_OLLAMA_API_URL,
    ensure_ollama_running,
    check_ollama_installed,
    check_ollama_running,
    install_ollama
)

# Client
from .client import OllamaClient

# Exceptions
from .exceptions import (
    OllamaAPIError,
    OllamaConnectionError,
    OllamaModelNotFoundError,
    OllamaServerError,
    ConnectionError,
    TimeoutError,
    ModelNotFoundError,
    ServerError,
    InvalidRequestError,
    StreamingError,
    ParseError
)

__all__ = [
    "print_header",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_json",
    "make_api_request",
    "DEFAULT_OLLAMA_API_URL",
    "OllamaClient",
    "OllamaAPIError",
    "OllamaConnectionError",
    "OllamaModelNotFoundError",
    "OllamaServerError",
    "ConnectionError",
    "TimeoutError",
    "ModelNotFoundError",
    "ServerError",
    "InvalidRequestError",
    "ensure_ollama_running",
    "check_ollama_installed",
    "check_ollama_running",
    "install_ollama",
    "StreamingError",
    "ParseError"
]
