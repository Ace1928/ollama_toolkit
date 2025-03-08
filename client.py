#!/usr/bin/env python3
"""
Core client functionality for interacting with Ollama API
"""

import asyncio
import logging
import time
from typing import (
    Any, Dict, List, Optional, Iterator, Union, 
    Callable, TypeVar, Awaitable, AsyncIterator, 
    AsyncGenerator, cast, Tuple
)
import os

import requests
import aiohttp

from .utils.common import (
    DEFAULT_OLLAMA_API_URL, 
    make_api_request, 
    async_make_api_request
)
from .utils.model_constants import (
    resolve_model_alias, 
    get_fallback_model,
    DEFAULT_CHAT_MODEL, 
    BACKUP_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL, 
    BACKUP_EMBEDDING_MODEL
)
from .exceptions import (
    OllamaAPIError, 
    ModelNotFoundError, 
    InvalidRequestError,
    ConnectionError,
    TimeoutError,
    StreamingError,
    ParseError
)

# Configure logger
logger = logging.getLogger(__name__)

# Type variable for generic return types
T = TypeVar('T')
# Fixed tuple type annotation
CacheKey = str
CacheValue = Tuple[float, Any]

class OllamaClient:
    """
    Client for interacting with the Ollama API.
    
    This class provides a convenient interface for all Ollama API endpoints,
    including model management, generation, embeddings, and more.
    
    Attributes:
        base_url: The base URL of the Ollama API server
        timeout: Default timeout for API requests in seconds
        max_retries: Maximum number of retry attempts for failed requests
        retry_delay: Delay between retry attempts in seconds
    """
    
    def __init__(
        self, 
        base_url: str = DEFAULT_OLLAMA_API_URL,
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        cache_enabled: bool = False,
        cache_ttl: float = 300.0  # 5 minutes in seconds
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: The base URL of the Ollama API
            timeout: Default timeout for API requests in seconds
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Delay between retry attempts in seconds
            cache_enabled: Whether to cache API responses
            cache_ttl: Cache time-to-live in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self._response_cache: Dict[CacheKey, CacheValue] = {}

    def get_version(self) -> Dict[str, Any]:
        """
        Get the Ollama version.
        
        Returns:
            Dictionary containing version information
        """
        response = make_api_request(
            "GET",
            "/api/version",
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return response.json()

    async def aget_version(self) -> Dict[str, Any]:
        """
        Asynchronously get the Ollama version.
        
        Returns:
            Dictionary containing version information
        """
        return await async_make_api_request(
            "GET",
            "/api/version",
            base_url=self.base_url,
            timeout=self.timeout,
        )

    def generate(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Generate a completion for the prompt.
        
        Args:
            model: The model name to use for generation
            prompt: The prompt to generate a response for
            options: Additional model parameters
            stream: Whether to stream the response
            
        Returns:
            Either a dictionary with the response or an iterator of response chunks
        """
        # Implementation would go here
        pass
    
    async def agenerate(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """
        Asynchronously generate a completion for the prompt.
        
        Args:
            model: The model name to use for generation
            prompt: The prompt to generate a response for
            options: Additional model parameters
            stream: Whether to stream the response
            
        Returns:
            Either a dictionary with the response or an async iterator of response chunks
        """
        # Implementation would go here
        pass
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Generate a chat response for the given messages.
        
        Args:
            model: The model name to use for generation
            messages: List of message dictionaries with 'role' and 'content'
            options: Additional model parameters
            stream: Whether to stream the response
            
        Returns:
            Either a dictionary with the response or an iterator of response chunks
        """
        # Implementation would go here
        pass
    
    async def achat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """
        Asynchronously generate a chat response for the given messages.
        
        Args:
            model: The model name to use for generation
            messages: List of message dictionaries with 'role' and 'content'
            options: Additional model parameters
            stream: Whether to stream the response
            
        Returns:
            Either a dictionary with the response or an async iterator of response chunks
        """
        # Implementation would go here
        pass
    
    def create_embedding(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an embedding vector for the given text.
        
        Args:
            model: The model name to use for embedding
            prompt: The text to create an embedding for
            options: Additional model parameters
            
        Returns:
            Dictionary containing the embedding
        """
        # Implementation would go here
        pass
    
    async def acreate_embedding(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously create an embedding vector for the given text.
        
        Args:
            model: The model name to use for embedding
            prompt: The text to create an embedding for
            options: Additional model parameters
            
        Returns:
            Dictionary containing the embedding
        """
        # Implementation would go here
        pass
    
    def batch_embeddings(
        self,
        model: str,
        prompts: List[str],
        options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Create embeddings for multiple prompts efficiently.
        
        Args:
            model: The model name to use for embedding
            prompts: List of texts to create embeddings for
            options: Additional model parameters
            
        Returns:
            List of dictionaries containing embeddings
        """
        # Implementation would go here
        pass
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available models.
        
        Returns:
            Dictionary containing the list of models
        """
        response = make_api_request(
            "GET",
            "/api/tags",
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return response.json()
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model: The model name
            
        Returns:
            Dictionary containing model information
        """
        # Implementation would go here
        pass
    
    def pull_model(
        self,
        model: str,
        stream: bool = False
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Pull a model from the Ollama registry.
        
        Args:
            model: The model name to pull
            stream: Whether to stream the download progress
            
        Returns:
            Either a dictionary with the status or an iterator of status updates
        """
        # Implementation would go here
        pass
    
    def delete_model(self, model: str) -> bool:
        """
        Delete a model.
        
        Args:
            model: The model name to delete
            
        Returns:
            True if the model was deleted successfully
        """
        response = make_api_request(
            "DELETE",
            "/api/delete",
            data={"model": model},
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return response.status_code == 200
    
    def copy_model(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Copy a model to a new name.
        
        Args:
            source: The source model name
            destination: The destination model name
            
        Returns:
            Dictionary containing the status
        """
        # Implementation would go here
        pass
    
    # Additional helper methods would be defined here
