#!/usr/bin/env python3
"""
Core client functionality for interacting with Ollama Toolkit
"""

import asyncio
import logging
import time
from typing import (
    Any, Dict, List, Optional, Iterator, Union, 
    Callable, TypeVar, Awaitable, AsyncIterator, 
    AsyncGenerator, cast, Tuple, Generator  # Add Generator here
)
import os
import json

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
    Client for interacting with the Ollama Toolkit.
    
    This class provides a convenient interface for all Ollama Toolkit endpoints,
    including model management, generation, embeddings, and more.
    
    Attributes:
        base_url: The base URL of the Ollama Toolkit server
        timeout: Default timeout for API requests in seconds
        max_retries: Maximum number of retry attempts for failed requests
        retry_delay: Delay between retry attempts in seconds
    """
    
    def __init__(
        self, 
        base_url: str = DEFAULT_OLLAMA_API_URL,
        timeout: int = 300,  # Increased from 60 to 300 seconds (5 minutes)
        max_retries: int = 3,
        retry_delay: float = 1.0,
        cache_enabled: bool = False,
        cache_ttl: float = 300.0  # 5 minutes in seconds
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: The base URL of the Ollama Toolkit
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

    def _with_retry(self, func: Callable[[], T]) -> T:
        """
        Execute a function with retry logic.
        
        Args:
            func: The function to execute
            
        Returns:
            The result of the function
        """
        for attempt in range(self.max_retries):
            try:
                return func()
            except (ConnectionError, TimeoutError) as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise e

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
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Generate a response from the model.
        
        Args:
            model: The model to use
            prompt: The prompt to send
            options: Additional model parameters
            stream: Whether to stream the response
            
        Returns:
            Response dictionary or generator for streaming responses
        """
        data = {"model": model, "prompt": prompt, "stream": stream}
        
        # Add options to data if provided
        if isinstance(options, dict):
            for key, value in options.items():
                data[key] = value
        
        if stream:
            # Handle streaming response
            response = self._with_retry(lambda: requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                stream=True,
                timeout=self.timeout
            ))
            
            def response_generator():
                for line in response.iter_lines():
                    if line:
                        yield json.loads(line)
            
            return response_generator()
        else:
            # Handle non-streaming response using make_api_request
            response = make_api_request(
                "POST", 
                "/api/generate", 
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            return response.json()
            
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
        stream: bool = True,
        options: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Send a chat request to the model with robust anti-hanging protection.
        
        Args:
            model: The model to use
            messages: List of message dictionaries
            stream: Whether to stream the response
            options: Additional model parameters
            
        Returns:
            Response dictionary or generator for streaming responses
        """
        # Create a copy of options to avoid modifying the input
        opt = dict(options or {})
        
        # Set reasonable timeouts
        timeout = min(opt.get("timeout", self.timeout), 600)  # Max 10 minutes
        
        # Check if this is potentially an embedding-only model
        if self._is_likely_embedding_model(model):
            error_msg = f"Model '{model}' appears to be an embedding-only model and doesn't support chat"
            logger.error(error_msg)
            if stream:
                return self._error_generator(error_msg)
            else:
                return {"error": error_msg, "code": "model_compatibility_error"}
        
        # Basic data payload
        data = {"model": model, "messages": messages, "stream": stream}
        if opt:
            data.update(opt)
        
        # Attempt the request with aggressive anti-hanging measures
        if stream:
            # Stream mode - use a safer streaming approach
            try:
                # Create session with explicit socket timeout
                session = requests.Session()
                
                # Configure session with timeouts at every level
                session.mount('http://', requests.adapters.HTTPAdapter(
                    max_retries=1  # Only retry once
                ))
                
                # Use POST with carefully controlled timeouts
                response = session.post(
                    f"{self.base_url.rstrip('/')}/api/chat",
                    json=data,
                    stream=True,
                    timeout=(30.0, timeout - 30.0)
                )
                
                # Handle 400 error explicitly for better feedback
                if response.status_code == 400:
                    error_message = "Bad request - the model may not support chat functionality"
                    try:
                        # Try to get more specific error from response
                        error_data = json.loads(response.content)
                        if "error" in error_data:
                            error_message = error_data["error"]
                    except:
                        pass
                    logger.error(f"Chat API error: {error_message}")
                    return self._error_generator(error_message)
                
                # Check other response codes
                if response.status_code != 200:
                    logger.error(f"Chat API error: {response.status_code}")
                    return self._error_generator(f"HTTP error {response.status_code}")
                
                # Return a carefully controlled generator that can't hang
                return self._safe_stream_generator(response, timeout)
                
            except Exception as e:
                logger.error(f"Chat request error: {str(e)}")
                return self._error_generator(str(e))
        else:
            # Non-streaming mode - use make_api_request for better test compatibility
            try:
                response = make_api_request(
                    "POST", 
                    "/api/chat", 
                    data=data,
                    base_url=self.base_url,
                    timeout=min(timeout, 300)
                )
                return response.json()
            except Exception as e:
                logger.error(f"Chat request error: {str(e)}")
                return {"error": str(e)}
    
    def _is_likely_embedding_model(self, model_name: str) -> bool:
        """
        Check if a model is likely to be an embedding-only model based on name patterns.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            True if the model is likely embedding-only, False otherwise
        """
        # Common patterns in embedding model names
        embedding_patterns = [
            "embed", "embedding", "text-embedding", "nomic-embed", 
            "all-minilm", "e5-", "bge-", "instructor-", "sentence-"
        ]
        
        model_name_lower = model_name.lower()
        for pattern in embedding_patterns:
            if pattern in model_name_lower:
                return True
        
        return False
        
    def _error_generator(self, error_msg: str) -> Generator[Dict[str, Any], None, None]:
        """
        Create a generator that reports an error and completes.
        
        Args:
            error_msg: The error message
            
        Returns:
            Generator yielding an error and completion
        """
        yield {"error": error_msg}
        yield {"done": True}

    def _safe_stream_generator(self, response, timeout: int) -> Generator[Dict[str, Any], None, None]:
        """
        Process a streaming response with anti-hanging protection.
        
        Args:
            response: The streaming response
            timeout: Maximum time to wait (seconds)
            
        Returns:
            Generator yielding processed chunks
        """
        start_time = time.time()
        error_reported = False
        
        try:
            # Get the raw response iterator
            raw_iter = response.iter_lines(chunk_size=8192, decode_unicode=False)
            
            # Process with timeout protection
            for i, line in enumerate(raw_iter):
                # Emergency timeout check - only check every 20 chunks to allow longer processing
                if i % 20 == 0 and (time.time() - start_time) > timeout:
                    yield {"error": "Response timeout exceeded", "timeout": True}
                    return
                    
                # Skip empty lines
                if not line:
                    continue
                    
                # Process the line
                try:
                    chunk = json.loads(line)
                    yield chunk
                    
                    # Exit if done to avoid hanging
                    if chunk.get("done", False):
                        return
                        
                except json.JSONDecodeError:
                    # Handle non-JSON content
                    try:
                        text = line.decode('utf-8', errors='replace')
                        yield {"message": {"content": text}, "raw": True}
                    except Exception as e:
                        if not error_reported:  # Only report once to avoid spam
                            logger.error(f"Stream decoding error: {str(e)}")
                            error_reported = True
                
                # Add heartbeat timeout check every 20 chunks instead of every 5
                if i % 20 == 0 and (time.time() - start_time) > timeout:
                    yield {"error": "Response timeout exceeded", "timeout": True}
                    return
                    
        except Exception as e:
            # Catch and report any errors in the iterator
            yield {"error": f"Stream processing error: {str(e)}"}
            
        # Always yield final done message to prevent hanging in consumer code
        yield {"done": True}
        
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert chat messages to a unified prompt string for models that don't support chat format.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            A formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "").lower()
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"[SYSTEM]: {content}")
            elif role == "user":
                prompt_parts.append(f"[USER]: {content}")
            elif role == "assistant":
                prompt_parts.append(f"[ASSISTANT]: {content}")
            else:
                prompt_parts.append(f"[{role.upper()}]: {content}")
        
        # Add final assistant prompt
        prompt_parts.append("[ASSISTANT]:")
        
        return "\n\n".join(prompt_parts)
    
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
        Create embeddings for the given prompt.
        
        Args:
            model: The model to use
            prompt: The text to embed
            options: Additional model parameters
            
        Returns:
            Response dictionary with embeddings
        """
        data = {"model": model, "prompt": prompt}
        
        # Add options to data if provided
        if isinstance(options, dict):
            data.update(options)
        
        response = make_api_request(
            "POST", 
            "/api/embed", 
            data=data,
            base_url=self.base_url,
            timeout=self.timeout
        )
        return response.json()
    
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
        data = {"model": model}
        
        if stream:
            # Handle streaming response
            try:
                response = self._with_retry(lambda: requests.post(
                    f"{self.base_url}/api/pull",
                    json=data,
                    stream=True,
                    timeout=self.timeout
                ))
                
                def response_generator():
                    try:
                        for line in response.iter_lines():
                            if line:
                                try:
                                    yield json.loads(line)
                                except json.JSONDecodeError as e:
                                    # Skip invalid JSON lines instead of failing
                                    logger.warning(f"Skipping invalid JSON in stream: {e}")
                                    yield {"status": "parsing_error", "error": str(e)}
                    except Exception as ex:
                        # Catch any errors during iteration
                        logger.error(f"Error in pull stream: {str(ex)}")
                        yield {"status": "error", "error": str(ex)}
                
                return response_generator()
            except Exception as e:
                logger.error(f"Error pulling model {model}: {str(e)}")
                # Return a generator with error information
                def error_generator():
                    yield {"status": "error", "error": str(e)}
                return error_generator()
        else:
            try:
                response = make_api_request(
                    "POST", 
                    "/api/pull", 
                    data=data,
                    base_url=self.base_url,
                    timeout=self.timeout
                )
                return response.json()
            except Exception as e:
                logger.error(f"Error pulling model {model}: {str(e)}")
                return {"status": "error", "error": str(e)}
    
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
