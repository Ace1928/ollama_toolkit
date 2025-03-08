#!/usr/bin/env python3
"""
Custom exceptions for the Ollama API client.
"""

class OllamaAPIError(Exception):
    """Base exception class for all Ollama API errors."""

    pass


class ConnectionError(OllamaAPIError):
    """Exception raised when connection to the API fails."""

    pass


class TimeoutError(OllamaAPIError):
    """Exception raised when an API request times out."""

    pass


class ModelNotFoundError(OllamaAPIError):
    """Exception raised when a requested model is not found."""

    pass


class ServerError(OllamaAPIError):
    """Exception raised when the API server returns a 5xx error."""

    pass


class InvalidRequestError(OllamaAPIError):
    """Exception raised when the API server returns a 4xx error."""

    pass


class StreamingError(OllamaAPIError):
    """Exception raised when there's an error during streaming responses."""

    pass


class ParseError(OllamaAPIError):
    """Exception raised when there's an error parsing API responses."""

    pass


class AuthenticationError(OllamaAPIError):
    """Exception raised when authentication fails."""
    
    pass
