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

## Chat Completion

### Simple Chat

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about neural networks."}
]

response = client.chat(
    model="llama2",
    messages=messages,
    stream=False
)

print(response["message"]["content"])
```

### Interactive Chat

```python
from ollama_toolkit import OllamaClient
from typing import List, Dict

def chat_session(model: str = "llama2"):
    client = OllamaClient()
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    print(f"Chat session with {model} (type 'exit' to quit)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
            
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get response
        print("\nAssistant: ", end="", flush=True)
        
        # Stream response
        for chunk in client.chat(model, messages, stream=True):
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk["message"]["content"]
                print(content, end="", flush=True)
                
        # Add assistant response to history
        messages.append({"role": "assistant", "content": content})

if __name__ == "__main__":
    chat_session()
```

## Embeddings

### Create Embeddings

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
embedding = client.create_embedding(
    model="nomic-embed-text",
    prompt="This is a sample text for embedding."
)

print(f"Embedding dimension: {len(embedding['embedding'])}")
print(f"First few values: {embedding['embedding'][:5]}...")
```

### Compare Text Similarity

```python
import numpy as np
from ollama_toolkit import OllamaClient

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

client = OllamaClient()
model = "nomic-embed-text"

# Get embeddings for two texts
text1 = "Artificial intelligence is transforming the world."
text2 = "AI technology is changing how we live and work."

emb1 = client.create_embedding(model, text1)["embedding"]
emb2 = client.create_embedding(model, text2)["embedding"]

# Calculate similarity
similarity = cosine_similarity(emb1, emb2)
print(f"Similarity: {similarity:.4f}")
```

## Working with Models

### Pull a Model

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()

# Non-streaming
result = client.pull_model("llama2")
print(f"Model pulled: {result}")

# Streaming with progress updates
for update in client.pull_model("mistral", stream=True):
    if "status" in update:
        print(f"Progress: {update['status']}")
```

### Copy a Model

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
result = client.copy_model("llama2", "my-llama2-copy")
print(f"Model copied: {result}")
```

### Delete a Model

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
success = client.delete_model("my-llama2-copy")
print(f"Model deleted: {success}")
```

## Error Handling

```python
from ollama_toolkit import OllamaClient, ModelNotFoundError, OllamaAPIError, ConnectionError

client = OllamaClient()

try:
    # Try to use a model that doesn't exist
    client.generate(model="non-existent-model", prompt="Hello")
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}. Is Ollama server running?")
except OllamaAPIError as e:
    print(f"API error: {e}")
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
