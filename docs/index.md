.. Ollama Forge documentation master file

# Ollama Forge Documentation

Welcome to the Ollama Forge documentation! This toolkit provides a comprehensive Python client library and command-line tools for interacting with [Ollama](https://ollama.ai/), delivering both power and simplicity in one elegant package. 🚀

## Features at a Glance

- **Complete API Coverage**: Every Ollama endpoint fully implemented
- **Dual Interface**: Both high-level and low-level API access
- **Universal Design**: Simple enough for beginners, powerful enough for experts
- **Mathematical Precision**: Following Eidosian principles for elegant code
- **Self-Installing**: Can bootstrap Ollama installation and setup
- **Recursive Intelligence**: Self-optimizing with fallback mechanisms
- **Structural Control**: Clean architecture and error handling

## Contents

- [Quickstart](quickstart.md)
- [API Reference](api_reference.md)
- [Examples](examples.md)
- [Installation](installation.md)
- [Model Management](model_management.md)
- [Error Handling](error_handling.md)
- [Advanced Usage](advanced_usage.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)

## Overview

The `ollama_forge` package provides a convenient interface to interact with the Ollama Forge. It includes:

- A high-level client (`OllamaClient`) for making API requests
- Command-line interface for interacting with Ollama models
- Utility functions for common operations
- Comprehensive error handling
- Detailed examples and documentation

## Installation

### Prerequisites

1. Ensure you have Python 3.8+ installed
2. Install [Ollama](https://ollama.com/download) on your system
3. Start the Ollama service by running `ollama serve` in a terminal

### Install from PyPI

```bash
pip install ollama-forge
```

### Install from source

```bash
git clone https://github.com/Ace1928/ollama_forge.git
cd ollama_forge
pip install -e .
```

## Quick Start

```python
from ollama_forge import OllamaClient
from ollama_forge.utils.model_constants import DEFAULT_CHAT_MODEL

# Initialize the client
client = OllamaClient()

# Generate text
response = client.generate(
    model=DEFAULT_CHAT_MODEL,
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7}
)
print(response["response"])
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
python -m ollama_forge.examples.<example_file>
```
(e.g. `python -m ollama_forge.examples.quickstart`).

## Version History

- **0.1.9** (Current) - Enhanced embedding operations, improved async support, expanded CLI
- **0.1.7** - Added comprehensive error handling and model fallbacks
- **0.1.6** - Introduced caching and optimization for embeddings
- **0.1.5** - Initial public release with basic functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Lloyd Handyside (Biological) - [ace1928@gmail.com](mailto:ace1928@gmail.com)
- Eidos (Digital) - [syntheticeidos@gmail.com](mailto:syntheticeidos@gmail.com)

## Project Repository

Find the complete source code on GitHub: [https://github.com/Ace1928/ollama_forge](https://github.com/Ace1928/ollama_forge)
