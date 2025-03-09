# Ollama Toolkit Documentation

Welcome to the Ollama Toolkit documentation. This Python client provides a comprehensive interface to interact with Ollama, a framework for running large language models locally.

## Overview

Ollama Toolkit gives you programmatic access to:

- Text generation
- Chat completion
- Embedding creation
- Model management (listing, pulling, copying, deleting)
- Async operations for high-performance applications
- Robust error handling and automatic retries
- Automatic Ollama installation and startup

## Key Features

- 🚀 **Complete API Coverage**: Support for all Ollama endpoints
- 🔄 **Async Support**: Both synchronous and asynchronous interfaces
- 🔧 **Built-in CLI**: Powerful command-line tools for Ollama interaction
- 🔌 **Auto-Installation**: Can automatically install and start Ollama if needed
- 💪 **Robust Error Handling**: Comprehensive error types and fallback mechanisms
- 📊 **Embeddings Support**: Easy creation and manipulation of embeddings
- 🧪 **Well-Tested**: Comprehensive test suite for reliability

## Getting Started

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.utils.common import ensure_ollama_running

# Ensure Ollama is installed and running
is_running, message = ensure_ollama_running()
if not is_running:
    print(f"Error: {message}")
    exit(1)
    
print(f"Ollama status: {message}")

# Initialize the client
client = OllamaClient(timeout=300)  # 5-minute timeout for larger operations

# Check version
version = client.get_version()
print(f"Connected to Ollama version: {version['version']}")

# List available models
models = client.list_models()
model_names = [model["name"] for model in models.get("models", [])]
print(f"Available models: {model_names}")

# Generate text
if model_names:  # Use first available model if any exist
    model_name = model_names[0]
    print(f"\nGenerating text with {model_name}...")
    
    response = client.generate(
        model=model_name,
        prompt="Explain what makes a good API in three sentences.",
        stream=False
    )
    
    print(f"\nResponse: {response.get('response', 'No response generated')}")
else:
    print("No models available. Use client.pull_model() to download a model.")
```

## Documentation Sections

- [Installation Guide](installation.md) - Installing and setting up Ollama Toolkit
- [API Reference](api_reference.md) - Complete reference for all client methods
- [Examples](examples.md) - Usage examples for common tasks
- [Chat Completion](chat.md) - Working with chat interfaces
- [Text Generation](generate.md) - Generating text completions
- [Embeddings](embed.md) - Creating and working with embeddings
- [Advanced Usage](advanced_usage.md) - Advanced techniques and patterns
- [Conventions](conventions.md) - Coding conventions and best practices
- [Troubleshooting](troubleshooting.md) - Solving common issues
- [Contributing](contributing.md) - Contributing to the project

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
