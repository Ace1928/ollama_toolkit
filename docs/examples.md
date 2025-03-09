# Examples

This page contains examples of how to use the Ollama Toolkit client for various tasks.

## Basic Usage

Here's a simple example of getting the version and listing available models:

```python
from ollama_toolkit import OllamaClient

# Initialize the client
client = OllamaClient()

# Get the version
version = client.get_version()
print(f"Connected to Ollama version: {version['version']}")

# List available models
models = client.list_models()
print("\nAvailable models:")
for model in models.get("models", []):
    print(f"- {model.get('name')}")
```

## Text Generation

### Non-streaming Generation

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
response = client.generate(
    model="llama2",
    prompt="Explain quantum computing in simple terms",
    options={
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500
    },
    stream=False
)

print(response["response"])
```

### Streaming Generation

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
for chunk in client.generate(
    model="llama2",
    prompt="Write a short story about AI",
    options={"temperature": 0.9},
    stream=True
):
    if "response" in chunk:
        print(chunk["response"], end="", flush=True)
```

## Async Examples

### Async Generation

```python
import asyncio
from ollama_toolkit import OllamaClient

async def main():
    client = OllamaClient()
    
    # Async generation
    response = await client.agenerate(
        model="llama2",
        prompt="Explain how neural networks work"
    )
    print(response["response"])

asyncio.run(main())
```

### Async Streaming

```python
import asyncio
from ollama_toolkit import OllamaClient

async def main():
    client = OllamaClient()
    
    # Async streaming
    async for chunk in client.agenerate(
        model="llama2",
        prompt="Write a haiku about programming",
        stream=True
    ):
        if "response" in chunk:
            print(chunk["response"], end="", flush=True)

asyncio.run(main())
```

## Generate a Completion

Here's a complete example of generating text using the synchronous API:

```python
from ollama_toolkit import OllamaClient

client = OllamaClient(timeout=300)  # Increased timeout for larger responses

# Non-streaming example (get complete response at once)
response = client.generate(
    model="llama2",
    prompt="Write a short poem about artificial intelligence.",
    options={
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 200
    },
    stream=False
)

print(f"Complete response: {response['response']}")

# Streaming example (get tokens as they're generated)
print("\nStreaming response:")
for chunk in client.generate(
    model="llama2",
    prompt="Explain the concept of machine learning to a 10-year old.",
    stream=True
):
    if "response" in chunk:
        print(chunk["response"], end="", flush=True)
    if chunk.get("done", False):
        print("\n\nGeneration complete!")
```

## Chat Completion

The chat interface is robust and fully implemented:

```python
from ollama_toolkit import OllamaClient

client = OllamaClient(timeout=300)

# Prepare chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant who speaks like a pirate."},
    {"role": "user", "content": "Tell me about the solar system."}
]

# Non-streaming example
response = client.chat(
    model="llama2",
    messages=messages,
    stream=False,
    options={"temperature": 0.8}
)

print(f"Assistant: {response['message']['content']}")

# Streaming example
messages.append({"role": "user", "content": "What's the largest planet?"})

print("\nStreaming response:")
print("Assistant: ", end="", flush=True)

for chunk in client.chat(
    model="llama2",
    messages=messages,
    stream=True
):
    if "message" in chunk and "content" in chunk["message"]:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
    
    if chunk.get("done", False):
        print("\n\nChat complete!")
```

## Embeddings

Generate embeddings for semantic search and similarity:

```python
from ollama_toolkit import OllamaClient
import numpy as np

client = OllamaClient()

# Create embedding for a single text
embedding1 = client.create_embedding(
    model="nomic-embed-text",  # Use an embedding-specific model
    prompt="Artificial intelligence is transforming industries worldwide."
)

embedding2 = client.create_embedding(
    model="nomic-embed-text",
    prompt="AI technologies are changing how businesses operate globally."
)

# Calculate cosine similarity
def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Get the actual embedding vectors from the response
vec1 = embedding1["embedding"]
vec2 = embedding2["embedding"]

# Calculate similarity (higher value means more similar)
similarity = cosine_similarity(vec1, vec2)
print(f"Similarity score: {similarity:.4f}")
```

## Working with Models

Manage models with the toolkit:

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()

# List all available models
models = client.list_models()
print("Available models:")
for model in models.get("models", []):
    name = model.get("name", "Unknown")
    size_bytes = model.get("size", 0)
    size_gb = size_bytes / (1024**3) if size_bytes else "Unknown"
    print(f"- {name} ({size_gb:.2f} GB)" if isinstance(size_gb, float) else f"- {name} (size: {size_gb})")

# Pull a new model with progress updates
print("\nPulling tinyllama model...")
for update in client.pull_model("tinyllama", stream=True):
    status = update.get("status", "")
    if status == "downloading":
        progress = update.get("completed", 0) / update.get("total", 1) * 100
        print(f"\rDownloading: {progress:.1f}%", end="", flush=True)
    elif status == "success":
        print("\nDownload complete!")
        
# Delete a model (if needed)
# Uncomment to test deletion:
# result = client.delete_model("tinyllama")
# print(f"Model deleted: {result}")
```

## Error Handling

Proper error handling with Ollama Toolkit:

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.exceptions import (
    ModelNotFoundError, 
    ConnectionError, 
    TimeoutError,
    OllamaAPIError
)

client = OllamaClient()

def safe_generate():
    try:
        # Try with a model that may not exist
        return client.generate(
            model="nonexistent-model-123",
            prompt="This won't work",
            stream=False
        )
    except ModelNotFoundError as e:
        print(f"Model not found: {e}")
        # Fallback to a model we know exists
        return client.generate(
            model="llama2",
            prompt="This is a fallback prompt",
            stream=False
        )
    except ConnectionError as e:
        print(f"Connection error: {e}")
        print("Please ensure Ollama server is running")
        return None
    except TimeoutError as e:
        print(f"Request timed out: {e}")
        return None
    except OllamaAPIError as e:
        print(f"API error: {e}")
        return None

response = safe_generate()
if response:
    print(f"Response: {response.get('response', '')}")
```

## Automatic Ollama Installation

```python
from ollama_toolkit.utils.common import ensure_ollama_running, check_ollama_installed

# Check if Ollama is installed
is_installed, install_message = check_ollama_installed()
if is_installed:
    print(f"Ollama is installed: {install_message}")
else:
    print(f"Ollama is not installed: {install_message}")

# Ensure Ollama is running
is_running, message = ensure_ollama_running()
if is_running:
    print(f"Ollama is running: {message}")
else:
    print(f"Ollama setup failed: {message}")
```

For more examples, check out the example scripts in the `/examples` directory of the package.
