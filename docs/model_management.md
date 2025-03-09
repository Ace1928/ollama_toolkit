# Model Management

This document details the model management capabilities in Ollama Toolkit v0.1.8, following Eidosian principles of structural control and recursive refinement.

## Overview

Ollama Toolkit provides a comprehensive set of functions for managing models:
- Listing available models
- Retrieving model information
- Pulling new models
- Copying models
- Deleting models
- Creating custom models

## Listing Models

Retrieve a list of all available models with their metadata:

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()

# Get all available models
models = client.list_models()

# Display model information
print("Available models:")
for model in models.get("models", []):
    name = model.get("name", "Unknown")
    size_bytes = model.get("size", 0)
    size_gb = size_bytes / (1024**3) if size_bytes else "Unknown"
    modified = model.get("modified_at", "Unknown")
    
    print(f"- {name}:")
    print(f"  Size: {size_gb:.2f} GB" if isinstance(size_gb, float) else f"  Size: {size_gb}")
    print(f"  Last modified: {modified}")
```

## Retrieving Model Information

Get detailed information about a specific model:

```python
model_info = client.get_model_info("llama2")
print(f"Model: {model_info.get('name')}")
print(f"Size: {model_info.get('size', 0) / (1024**3):.2f} GB")
print(f"Modified: {model_info.get('modified_at')}")
print(f"Format: {model_info.get('format')}")
print(f"Family: {model_info.get('family')}")
print(f"Parameter size: {model_info.get('parameter_size')}")
print(f"Quantization level: {model_info.get('quantization_level')}")
```

## Pulling Models

Download a model from the Ollama library:

### Non-streaming (Simple)

```python
result = client.pull_model("deepseek-r1:1.5b", stream=False)
print(f"Pull completed: {result}")
```

### Streaming with Progress Updates

```python
print("Pulling model with progress updates:")
for update in client.pull_model("qwen2.5:0.5b", stream=True):
    status = update.get("status", "")
    
    if status == "downloading":
        completed = update.get("completed", 0)
        total = update.get("total", 1)
        progress = (completed / total) * 100 if total else 0
        print(f"\rDownloading: {progress:.1f}% ({completed}/{total} bytes)", end="", flush=True)
    
    elif status == "processing":
        print(f"\rProcessing model...", end="", flush=True)
    
    elif status == "success":
        print("\nModel successfully pulled!")
        
    elif "error" in update:
        print(f"\nError: {update['error']}")
```

## Copying Models

Create a copy of an existing model with a new name:

```python
result = client.copy_model("llama2", "my-custom-llama")
print(f"Copy result: {result}")
```

## Deleting Models

Remove a model from the system:

```python
success = client.delete_model("my-custom-llama")
print(f"Model deleted: {success}")
```

## Creating Custom Models

Create a custom model using a Modelfile:

```python
modelfile = """
FROM deepseek-r1:1.5b
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM You are a helpful AI assistant specialized in Python programming.
"""

for update in client.create_model("python-assistant", modelfile, stream=True):
    status = update.get("status", "")
    print(f"Status: {status}")
    
    if "error" in update:
        print(f"Error: {update['error']}")
```

## Running Models

Check which models are currently loaded and running:

```python
running_models = client.list_running_models()
print("Currently running models:")
for model in running_models.get("running", []):
    name = model.get("name", "Unknown")
    status = model.get("status", "Unknown")
    pid = model.get("pid", "Unknown")
    
    print(f"- {name}:")
    print(f"  Status: {status}")
    print(f"  PID: {pid}")
```

## Pushing Models

Push a local model to the Ollama library (requires authentication):

```python
for update in client.push_model("my-custom-model", stream=True):
    status = update.get("status", "")
    print(f"Push status: {status}")
    
    if "error" in update:
        print(f"Error: {update['error']}")
```

## Recommended Models

Ollama Toolkit v0.1.8 recommends these models for different use cases:

| Purpose | Model | Size | Description |
|---------|-------|------|-------------|
| General text | `deepseek-r1:1.5b` | ~1.5GB | Balanced performance and quality |
| Chat | `qwen2.5:0.5b` | ~0.5GB | Optimized for conversations |
| Embeddings | `nomic-embed-text` | ~250MB | Efficient vector representations |
| Minimal | `tinyllama` | ~100MB | Ultra-lightweight option |

## Model Constants

The toolkit provides constants for commonly used models:

```python
from ollama_toolkit.utils.model_constants import (
    DEFAULT_CHAT_MODEL,
    BACKUP_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    BACKUP_EMBEDDING_MODEL
)

print(f"Default chat model: {DEFAULT_CHAT_MODEL}")
print(f"Backup chat model: {BACKUP_CHAT_MODEL}")
print(f"Default embedding model: {DEFAULT_EMBEDDING_MODEL}")
print(f"Backup embedding model: {BACKUP_EMBEDDING_MODEL}")
```

## Utility Functions

Helper functions for model management:

```python
from ollama_toolkit.utils.model_constants import resolve_model_alias, get_fallback_model

# Resolve a model alias to its full name
model_name = resolve_model_alias("chat")  # Returns DEFAULT_CHAT_MODEL
print(f"Resolved model: {model_name}")

# Get a fallback model when the primary is unavailable
fallback = get_fallback_model("deepseek-r1:1.5b")  # Returns a suitable fallback
print(f"Fallback model: {fallback}")
```

## Best Practices

1. **Check model availability** before operations to prevent errors
2. **Use streaming for large models** to provide user feedback
3. **Implement fallback mechanisms** using `get_fallback_model()`
4. **Consider resource constraints** when selecting models
5. **Use model constants** for consistency across your application

By following these patterns, you'll achieve a level of model management that embodies the Eidosian principle of "Structure as Control."
