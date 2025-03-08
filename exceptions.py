#!/usr/bin/env python3
"""
Custom exceptions for the Ollama Toolkit client.
"""

class OllamaAPIError(Exception):
    """Base exception class for all Ollama Toolkit errors."""
    pass

class OllamaConnectionError(OllamaAPIError):
    """Raised when a connection to the Ollama server fails."""
    pass

class OllamaModelNotFoundError(OllamaAPIError):
    """Raised when a requested model is not found."""
    pass

class OllamaServerError(OllamaAPIError):
    """Raised when the Ollama server returns an error."""
    pass

class EndpointNotFoundError(OllamaAPIError):
    """Exception raised when an API endpoint is not found."""
    pass

class ModelCompatibilityError(OllamaAPIError):
    """Exception raised when a model doesn't support a specific operation."""
    pass

# Aliases for backward compatibility
ConnectionError = OllamaConnectionError
TimeoutError = OllamaConnectionError  # Specific timeout errors inherit from connection errors
ModelNotFoundError = OllamaModelNotFoundError
ServerError = OllamaServerError
InvalidRequestError = OllamaAPIError

class StreamingError(OllamaAPIError):
    """Exception raised when there's an error during streaming responses."""
    pass

class ParseError(OllamaAPIError):
    """Exception raised when there's an error parsing API responses."""
    pass

class AuthenticationError(OllamaAPIError):
    """Exception raised when authentication fails."""
    pass

class TimeoutError(OllamaConnectionError):
    """Raised when a request times out."""
    pass

class StreamingTimeoutError(TimeoutError):
    """Raised when a streaming response times out."""
    pass
