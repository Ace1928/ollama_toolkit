# Examples

This page contains precision-engineered examples that demonstrate the Ollama Forge client's capabilities with Eidosian elegance.

## Basic Usage {#basic-usage}
- Demonstrates version checks, listing models, and generating completions.  
- Run:
  ```bash
  python -m ollama_forge.examples.basic_usage
  ```

Here's a simple example of getting the version and listing available models:

```python
from ollama_forge import OllamaClient

# Initialize the client - foundation of all operations
client = OllamaClient()

# Get the version - basic system awareness
version = client.get_version()
print(f"Connected to Ollama version: {version['version']}")

# List available models - structural knowledge acquisition
models = client.list_models()
print("\nAvailable models:")
for model in models.get("models", []):
    print(f"- {model.get('name')}")  # Precise formatting
```

Run with mathematical simplicity:
```bash
python -m ollama_forge.examples.basic_usage
```

## Text Generation {#text-generation}
- Non-streaming and streaming examples:
  ```python
  response = client.generate(model="deepseek-r1:1.5b", prompt="Explain quantum mechanics.")
  # ...
  ```

### Non-streaming Generation

```python
from ollama_forge import OllamaClient

client = OllamaClient()
# Single operation, complete result - maximum efficiency
response = client.generate(
    model="deepseek-r1:1.5b",  # Precision model selection
    prompt="Explain quantum computing in simple terms",
    options={
        "temperature": 0.7,  # Calibrated randomness
        "top_p": 0.9,        # Optimized diversity
        "max_tokens": 500    # Bounded output
    },
    stream=False
)

print(response["response"])
```

### Streaming Generation

```python
from ollama_forge import OllamaClient

client = OllamaClient()
# Flowing river of tokens - immediate feedback loop
for chunk in client.generate(
    model="llama2",
    prompt="Write a short story about AI",
    options={"temperature": 0.9},
    stream=True
):
    if "response" in chunk:
        print(chunk["response"], end="", flush=True)  # Seamless display
```

## Async Examples

### Async Generation

```python
import asyncio
from ollama_forge import OllamaClient

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
from ollama_forge import OllamaClient

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
from ollama_forge import OllamaClient

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

## Chat Completion {#chat-completion}
- Use message roles (system, user, assistant).
  ```bash
  python -m ollama_forge.examples.chat_example
  ```

The chat interface is robust and fully implemented:

```python
from ollama_forge import OllamaClient

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

## Embeddings {#embeddings}
- Demonstrates embedding creation and cosine similarity:
  ```bash
  python -m ollama_forge.examples.embedding_example --text "Hello world"
  ```

Generate embeddings for semantic search and similarity:

```python
from ollama_forge import OllamaClient
import numpy as np

client = OllamaClient()

# Create embedding with semantic precision
embedding1 = client.create_embedding(
    model="nomic-embed-text",  # Purpose-built model selection
    prompt="Artificial intelligence is transforming industries worldwide."
)

embedding2 = client.create_embedding(
    model="nomic-embed-text",
    prompt="AI technologies are changing how businesses operate globally."
)

# Calculate cosine similarity with mathematical elegance
def cosine_similarity(a, b):
    # Vector mathematics distilled to its essence
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Extract vectors with contextual awareness
vec1 = embedding1["embedding"]
vec2 = embedding2["embedding"]

# Calculate similarity—higher value means more similar concepts
similarity = cosine_similarity(vec1, vec2)
print(f"Similarity score: {similarity:.4f}")  # Precise formatting
```

Run with one simple command:
```bash
python -m ollama_forge.examples.embedding_example --text "Hello world"
```

## Working with Models
- Pull, list, or delete models:
  ```python
  client.pull_model("deepseek-r1:1.5b", stream=True)
  # ...
  ```

Manage models with the toolkit:

```python
from ollama_forge import OllamaClient

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
Includes fallback mechanisms and thorough exceptions—structural resilience in action:

```python
from ollama_forge import OllamaClient
from ollama_forge.exceptions import (
    ModelNotFoundError,  # Specific error classification
    ConnectionError, 
    TimeoutError,
    OllamaAPIError
)

client = OllamaClient()

def safe_generate():
    """Recursively refined error handling approach"""
    try:
        # Primary attempt - optimistic path
        return client.generate(
            model="nonexistent-model-123",
            prompt="This won't work",
            stream=False
        )
    except ModelNotFoundError as e:
        print(f"Model not found: {e}")  # Precise error communication
        # Fallback with graceful recovery - structural control
        return client.generate(
            model="llama2",
            prompt="This is a fallback prompt",
            stream=False
        )
    except ConnectionError as e:
        # System awareness
        print(f"Connection error: {e}")
        print("Please ensure Ollama server is running")
        return None
    except TimeoutError as e:
        # Velocity awareness
        print(f"Request timed out: {e}")
        return None
    except OllamaAPIError as e:
        # Generic error handling as final safety net
        print(f"API error: {e}")
        return None

response = safe_generate()
if response:
    print(f"Response: {response.get('response', '')}")
```

## Automatic Ollama Installation

```python
from ollama_forge.utils.common import ensure_ollama_running, check_ollama_installed

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

For more examples that embody Eidosian principles, explore the example scripts in the `/examples` directory.
