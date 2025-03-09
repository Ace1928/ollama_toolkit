# Error Handling

This document details the error handling capabilities in Ollama Toolkit v0.1.8, following Eidosian principles of self-awareness and structural robustness.

## Exception Hierarchy

Ollama Toolkit provides a precise hierarchy of exception types for optimal error handling:

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

Each exception type serves a specific purpose, allowing for precise handling of different error scenarios.

## Basic Error Handling Pattern

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.exceptions import ModelNotFoundError, ConnectionError, TimeoutError, OllamaAPIError

client = OllamaClient()

try:
    response = client.generate(
        model="nonexistent-model",
        prompt="This won't work",
        stream=False
    )
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
    # Handle missing model (e.g., suggest alternatives)
except ConnectionError as e:
    print(f"Connection error: {e}")
    # Handle connection issues (e.g., check if server is running)
except TimeoutError as e:
    print(f"Request timed out: {e}")
    # Handle timeout (e.g., suggest using a smaller model)
except OllamaAPIError as e:
    print(f"API error: {e}")
    # Generic error handling
```

## Advanced Fallback Mechanisms

Version 0.1.8 introduces sophisticated fallback mechanisms that operate at multiple levels:

### Model Fallback

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.utils.model_constants import get_fallback_model

client = OllamaClient()

def generate_with_fallback(model, prompt):
    try:
        return client.generate(model=model, prompt=prompt)
    except ModelNotFoundError:
        fallback_model = get_fallback_model(model)
        print(f"Model '{model}' not found. Using fallback model: {fallback_model}")
        return client.generate(model=fallback_model, prompt=prompt)

# Example usage
response = generate_with_fallback("missing-model", "Hello, world!")
print(response.get("response", ""))
```

### Comprehensive Fallback Strategy

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.exceptions import *
from ollama_toolkit.utils.model_constants import get_fallback_model

client = OllamaClient()

def safe_generate(model, prompt, max_attempts=3):
    """Recursively refined error handling approach with multiple fallback levels"""
    attempts = 0
    current_model = model
    
    while attempts < max_attempts:
        try:
            return client.generate(model=current_model, prompt=prompt, stream=False)
        except ModelNotFoundError as e:
            print(f"Model not found: {e}")
            current_model = get_fallback_model(current_model)
            print(f"Trying fallback model: {current_model}")
        except ConnectionError as e:
            print(f"Connection error: {e}")
            print("Attempting to restart connection...")
            time.sleep(1)  # Brief pause before retry
        except TimeoutError as e:
            print(f"Request timed out: {e}")
            if "llama" in current_model or "deepseek" in current_model:
                current_model = "tinyllama"  # Try smaller model
                print(f"Trying lighter model: {current_model}")
            else:
                print("Reducing complexity and trying again...")
                prompt = prompt[:len(prompt)//2]  # Simplify prompt
        except OllamaAPIError as e:
            print(f"API error: {e}")
            return {"error": str(e), "response": "Error occurred during generation"}
        
        attempts += 1
    
    return {"error": "Maximum retry attempts reached", "response": "Failed to generate response"}
```

## Exception Details

### ModelNotFoundError

Raised when a requested model cannot be found in the Ollama server.

```python
try:
    client.generate(model="nonexistent-model", prompt="Hello")
except ModelNotFoundError as e:
    print(f"Error: {e}")  # "Error: Model 'nonexistent-model' not found"
    print(f"Available models: {[m['name'] for m in client.list_models().get('models', [])]}")
```

### ConnectionError

Raised when the client cannot connect to the Ollama server.

```python
try:
    client = OllamaClient(base_url="http://incorrect-url:11434")
    client.get_version()
except ConnectionError as e:
    print(f"Connection failed: {e}")
    print("Please ensure the Ollama server is running with: 'ollama serve'")
```

### TimeoutError

Raised when a request takes longer than the specified timeout.

```python
try:
    client = OllamaClient(timeout=1)  # Very short timeout
    client.generate(model="llama2", prompt="Write a novel", stream=False)
except TimeoutError as e:
    print(f"Request timed out: {e}")
    print("Try increasing the timeout or using a smaller model")
```

### StreamingError

Raised when there's an error during a streaming response.

```python
try:
    for chunk in client.generate(model="llama2", prompt="Hello", stream=True):
        print(chunk.get("response", ""), end="", flush=True)
except StreamingError as e:
    print(f"\nStreaming error: {e}")
```

## Error Logging

Ollama Toolkit provides comprehensive logging for error diagnosis:

```python
import logging
from ollama_toolkit import OllamaClient

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("ollama_debug.log"), logging.StreamHandler()]
)

client = OllamaClient()
try:
    client.generate(model="nonexistent-model", prompt="Test")
except Exception as e:
    logging.error(f"Generation failed: {e}", exc_info=True)
```

## Eidosian Error Messages

Following the principle of "Humor as Cognitive Leverage," error messages are designed to be informative and memorable:

- When a model isn't found: "Model 'nonexistent-model' not found. Like searching for unicorns—majestic but absent. Try 'llama2' instead."
- When a connection fails: "Connection refused—like knocking on a door with no one home. Is Ollama running with 'ollama serve'?"
- When a request times out: "Time waits for no one, and neither does your request. Consider a smaller model or a larger timeout."

## Best Practices

1. **Always handle specific exceptions before generic ones**
2. **Implement fallback mechanisms for critical operations**
3. **Use proper timeout values based on model size and task complexity**
4. **Log errors with sufficient context for debugging**
5. **Provide helpful feedback to users when errors occur**

By following these patterns, your applications will achieve a level of robustness and resilience that embodies the Eidosian principle of "Self-Awareness as Foundation."
