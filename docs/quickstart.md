# Quickstart Guide

This guide will help you get started with Ollama Forge in minutes—following Eidosian principles of efficiency and elegance.

## 🚀 Installation

Install from PyPI with a single command:

```bash
pip install ollama-forge
```

## 🔍 Verify Installation

Ensure everything is working correctly:

```python
from ollama_forge import OllamaClient, __version__

# Print version
print(f"Ollama Forge version: {__version__}")

# Initialize client
client = OllamaClient()

# Check Ollama connection
try:
    version = client.get_version()
    print(f"Connected to Ollama {version['version']}!")
except Exception as e:
    print(f"Connection failed: {e}")
```

## 💬 Generate Text

Here's a minimal example to generate text:

```python
from ollama_forge import OllamaClient

# Initialize client
client = OllamaClient()

# Generate text with the default model
response = client.generate(
    model="llama2",
    prompt="Explain what APIs are in simple terms.",
    stream=False
)

print(response["response"])
```

## 🔄 Complete Example

This example showcases automatic installation, model listing, and text generation:

```python
from ollama_forge import OllamaClient
from ollama_forge.helpers.common import ensure_ollama_running

# Ensure Ollama is running (will attempt to install if not found)
is_running, message = ensure_ollama_running()
if not is_running:
    print(f"Error: {message}")
    exit(1)

print(f"Ollama status: {message}")

# Initialize client
client = OllamaClient()

# List models
models = client.list_models()
model_names = [model["name"] for model in models.get("models", [])]

if not model_names:
    print("No models available. Pulling a small model...")
    client.pull_model("llama2")
    models = client.list_models()
    model_names = [model["name"] for model in models.get("models", [])]

# Generate text
if model_names:
    model = model_names[0]
    print(f"Using model: {model}")
    
    response = client.generate(
        model=model,
        prompt="What are three key principles of good API design?",
        stream=False
    )
    
    print(f"\nResponse: {response['response']}")
```

## 🔗 Next Steps

- Dive into [detailed examples](examples.md)
- Learn about the [API reference](api_reference.md)
- Explore [chat completion](chat.md) and [embeddings](embed.md)
