#!/usr/bin/env python3
"""
Custom exceptions for the Ollama Forge.
"""

class OllamaAPIError(Exception):
    """Base class for all Ollama API errors."""
    pass

class OllamaConnectionError(OllamaAPIError):
    """Raised when there is a connection error."""
    pass

class OllamaModelNotFoundError(OllamaAPIError):
    """Raised when a requested model is not found."""
    pass

class OllamaServerError(OllamaAPIError):
    """Raised when there is a server error."""
    pass

class ConnectionError(OllamaAPIError):
    """Raised when there is a connection error."""
    pass

class TimeoutError(OllamaAPIError):
    """Raised when a request times out."""
    pass

class ModelNotFoundError(OllamaAPIError):
    """Raised when a requested model is not found."""
    pass

class ServerError(OllamaAPIError):
    """Raised when there is a server error."""
    pass

class InvalidRequestError(OllamaAPIError):
    """Raised when a request is invalid."""
    pass

class StreamingError(OllamaAPIError):
    """Raised when there is an error in streaming response."""
    pass

class ParseError(OllamaAPIError):
    """Raised when there is an error parsing the response."""
    pass
