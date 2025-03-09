.. Ollama Toolkit documentation master file

# Ollama Toolkit Documentation

Welcome to the Ollama Toolkit documentation—where precision meets possibility. This Python client provides a comprehensive interface to interact with Ollama, a framework for running large language models locally with **exceptional efficiency**.

## Overview

Ollama Toolkit gives you programmatic access to:

- Text generation with surgical precision
- Chat completion engineered for natural flow
- Embedding creation with mathematical elegance
- Model management (listing, pulling, copying, deleting) with controlled recursion
- Async operations for high-velocity performance applications
- Robust error handling with intuitive fallback mechanisms
- Automatic Ollama installation and startup with zero friction

## Key Features

- 🚀 **Complete API Coverage**: Support for all Ollama endpoints—nothing missing, nothing extra
- 🔄 **Recursive Async Support**: Both synchronous and asynchronous interfaces that build upon each other
- 🔧 **Structurally Perfect CLI**: Powerful command-line tools with intuitive architecture
- 🔌 **Zero-Friction Auto-Installation**: Install and start Ollama with mathematically minimal steps
- 💪 **Self-Aware Error Handling**: Comprehensive error types that explain precisely what went wrong
- 📊 **Velocity-Optimized Embeddings**: Create and manipulate embeddings with maximum efficiency
- 🧪 **Recursively Refined Testing**: Every function proven robust through iterative improvement
- 🔍 **Version-Aware**: Full compatibility with Ollama 0.1.8 and beyond

## Getting Started

```python
# This implementation follows Eidosian principles of contextual integrity and precision
from ollama_toolkit import OllamaClient, __version__
from ollama_toolkit.utils.common import ensure_ollama_running

# Display toolkit version – foundational awareness
print(f"Ollama Toolkit version: {__version__}")  # Should be 0.1.8

# Ensure Ollama is installed and running – structurally sound foundation
is_running, message = ensure_ollama_running()
if not is_running:
    print(f"Error: {message}")
    exit(1)

print(f"Ollama status: {message}")

# Initialize the client with optimal timeout
client = OllamaClient(timeout=600)  # 10-minute timeout

# Check Ollama server version – recommended minimum is v0.1.11
version = client.get_version()
print(f"Connected to Ollama server version: {version.get('version', 'unknown')}")

# List available models – structural awareness
models = client.list_models()
model_names = [model["name"] for model in models.get("models", [])]
print(f"Available models: {model_names}")

# Generate text with precision and flow
if model_names:  # Use first available model if any exist
    model_name = model_names[0]
    print("\nGenerating a short test response...")
    response = client.generate(model=model_name, prompt="Say hello!", stream=False)
    print(f"\nResponse: {response.get('response', 'No response generated')}")
else:
    print("No models available. Use client.pull_model() to download a model.")
```

## Installation Guide

- Install via PyPI: `pip install ollama-toolkit==0.1.8`
- Or install locally in editable mode:

```bash
pip install -e /path/to/ollama_toolkit
```

## Documentation Contents

```{toctree}
:maxdepth: 2
:caption: 📚 Getting Started

README
installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: 🛠️ Core Documentation

api_reference
examples
advanced_usage
```

```{toctree}
:maxdepth: 2
:caption: 🔄 Features & Capabilities

chat
generate
embed
model_management
error_handling
```

```{toctree}
:maxdepth: 2
:caption: 🧠 Guides & References

conventions
troubleshooting
eidosian_integration
version
contributing
changelog
```

```{toctree}
:maxdepth: 1
:caption: 🧩 API Endpoints
:hidden:

version
generate
chat
embed
models_api
system_api
```

## Examples

Check out these practical examples:

- [Basic Usage](examples.md) — Precision in simplicity  
- [Generate Text](generate.md) — Flow like a river  
- [Chat Completion](chat.md) — Universal yet personal  
- [Embeddings](embed.md) — Mathematical elegance
- [Model Management](model_management.md) — Structural control
- [Error Handling](error_handling.md) — Self-aware resilience

All examples can be run via:

```bash
python -m ollama_toolkit.examples.<example_file>
```
(e.g. `python -m ollama_toolkit.examples.quickstart`).

## Version History

- **0.1.8** (Current) - Enhanced embedding operations, improved async support, expanded CLI
- **0.1.7** - Added comprehensive error handling and model fallbacks
- **0.1.6** - Introduced caching and optimization for embeddings
- **0.1.5** - Initial public release with basic functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Lloyd Handyside (Biological) - [ace1928@gmail.com](mailto:ace1928@gmail.com)
- Eidos (Digital) - [eidos@gmail.com](mailto:eidos@gmail.com)

## Project Repository

Find the complete source code on GitHub: [https://github.com/Ace1928/ollama_toolkit](https://github.com/Ace1928/ollama_toolkit)
