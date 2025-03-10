# Error Handling

This document details the error handling capabilities in Ollama Forge v0.1.9, following Eidosian principles of self-awareness and structural robustness.

## Exception Hierarchy

Ollama Forge provides a precise hierarchy of exception types for optimal error handling:

```
OllamaAPIError (base)
├── ConnectionError
├── TimeoutError
├── ModelNotFoundError
├── ServerError
├── InvalidRequestError
├── StreamingError
├── ParseError
├── AuthenticationError
├── EndpointNotFoundError
├── ModelCompatibilityError
└── StreamingTimeoutError
```

## Using Exceptions

### Basic Error Handling

```python
from ollama_forge import OllamaClient
from ollama_forge.exceptions import ModelNotFoundError, ConnectionError, TimeoutError

client = OllamaClient()

try:
    response = client.generate(model="non-existent-model", prompt="Hello")
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
    # Respond with available models
    models = client.list_models()
    print(f"Available models: {[m['name'] for m in models.get('models', [])]}")
except ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check if Ollama server is running with: ollama serve")
except TimeoutError as e:
    print(f"Request timed out: {e}")
    print("Try a shorter prompt or increase the timeout")
```

### Custom Error Handlers

Create reusable error handlers for consistent handling across your application:

```python
def handle_ollama_errors(func):
    """Decorator for handling common Ollama API errors."""
    from functools import wraps
    from ollama_forge.exceptions import (
        ModelNotFoundError, ConnectionError, 
        TimeoutError, StreamingError
    )
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ModelNotFoundError as e:
            print(f"Model not found: {e}")
            return {"error": "model_not_found", "message": str(e)}
        except ConnectionError as e:
            print(f"Connection error: {e}")
            return {"error": "connection_error", "message": str(e)}
        except TimeoutError as e:
            print(f"Request timed out: {e}")
            return {"error": "timeout", "message": str(e)}
        except StreamingError as e:
            print(f"Streaming error: {e}")
            return {"error": "streaming_error", "message": str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "unknown", "message": str(e)}
    
    return wrapper

# Usage
@handle_ollama_errors
def generate_text(client, prompt, model="deepseek-r1:1.5b"):
    return client.generate(model=model, prompt=prompt)
```

### Exception Reference

#### OllamaAPIError
Base exception for all Ollama API errors.

#### ConnectionError
Raised when connection to the Ollama API server fails.
- Common causes: Server not running, network issues, incorrect API URL

#### TimeoutError
Raised when an API request times out.
- Common causes: Large prompt, complex generation, server overload

#### ModelNotFoundError
Raised when the requested model is not available.
- Common causes: Typo in model name, model not downloaded

#### ServerError
Raised when the Ollama API server returns a 5xx error.
- Common causes: Server crash, internal server error

#### InvalidRequestError
Raised when the Ollama API server returns a 4xx error.
- Common causes: Invalid parameters, malformed request

#### StreamingError
Raised when there's an error during streaming responses.
- Common causes: Connection interruption, server timeout

#### ParseError
Raised when there's an error parsing API responses.
- Common causes: Malformed JSON, unexpected response format

#### AuthenticationError
Raised when authentication fails.
- Common causes: Invalid API key (for future use with secured APIs)

#### EndpointNotFoundError
Raised when an API endpoint is not found.
- Common causes: Using an API endpoint that doesn't exist, API version mismatch

#### ModelCompatibilityError
Raised when a model doesn't support the requested operation.
- Common causes: Using chat with an embedding-only model

#### StreamingTimeoutError
Raised when a streaming response times out.
- Common causes: Long generations, slow network connection

## Error Handling Best Practices

1. **Always catch specific exceptions first**, then broader ones
2. **Provide informative error messages** to users
3. **Implement appropriate fallbacks** for critical operations
4. **Log errors** with sufficient context for debugging
5. **Consider retry strategies** for transient errors like connection issues

## Example: Robust Client with Fallbacks

```python
from ollama_forge import OllamaClient
from ollama_forge.exceptions import ModelNotFoundError, ConnectionError
from ollama_forge.helpers.model_constants import get_fallback_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_robust_completion(prompt, model="deepseek-r1:1.5b", max_attempts=3):
    """Get completion with robust error handling and fallbacks."""
    client = OllamaClient()
    
    # Try primary model
    try:
        logger.info(f"Attempting generation with {model}")
        return client.generate(model=model, prompt=prompt)
    except ModelNotFoundError:
        fallback = get_fallback_model(model)
        logger.warning(f"Model {model} not found, falling back to {fallback}")
        return client.generate(model=fallback, prompt=prompt)
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        
        # Try to start Ollama service
        from ollama_forge.helpers.common import ensure_ollama_running
        is_running, message = ensure_ollama_running()
        
        if is_running:
            logger.info(f"Started Ollama service: {message}")
            # Retry with the original model
            return client.generate(model=model, prompt=prompt)
        else:
            logger.error(f"Failed to start Ollama: {message}")
            return {"error": "service_unavailable", "message": str(e)}
```

By using this structured approach to error handling, your applications will be more robust, user-friendly, and easier to maintain.
