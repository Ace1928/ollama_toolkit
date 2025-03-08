# Ollama Toolkit Python Client

[![PyPI version](https://badge.fury.io/py/ollama-api.svg)](https://badge.fury.io/py/ollama-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python client library and command-line tools for interacting with the [Ollama](https://ollama.ai/) API. This package provides easy access to all Ollama Toolkit endpoints with intuitive interfaces, complete type hints, and detailed documentation.

## Features

- 🚀 **Complete API Coverage**: Support for all Ollama Toolkit endpoints
- 🔄 **Async Support**: Both synchronous and asynchronous interfaces
- 🔧 **Built-in CLI**: Powerful command-line tools for Ollama interaction
- 🔌 **Auto-Installation**: Can automatically install and start Ollama if needed
- 💪 **Robust Error Handling**: Comprehensive error types and fallback mechanisms
- 📊 **Embeddings Support**: Easy creation and manipulation of embeddings
- 🧪 **Well-Tested**: Comprehensive test suite for reliability

## Installation

### Prerequisites

1. Ensure you have Python 3.8+ installed
2. Install [Ollama](https://ollama.com/download) on your system
3. Start the Ollama service by running `ollama serve` in a terminal

### Install from PyPI

```bash
pip install ollama-api
```

### Install from source

```bash
git clone https://github.com/lloydhd/ollama_toolkit.git
cd ollama_toolkit
pip install -e .
```

## Verifying Installation

After installation, you can verify everything is working by running:

```bash
# Run all tests
python -m pytest ollama_toolkit/tests

# Run specific test modules
python -m pytest ollama_toolkit/tests/test_client.py
```

You can also run a quick import test to ensure the package is accessible:

```bash
python -c "import ollama_toolkit; print(f'Ollama Toolkit version: {ollama_toolkit.__version__}')"
```

## Quick Start

```python
from ollama_toolkit import OllamaClient

# Initialize the client
client = OllamaClient()

# Get Ollama version
version = client.get_version()
print(f"Ollama version: {version['version']}")

# Generate text (non-streaming)
response = client.generate(
    model="llama2",
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7}
)

print(response["response"])

# Generate text (streaming)
for chunk in client.generate(
    model="llama2", 
    prompt="Write a short poem about AI", 
    stream=True
):
    if "response" in chunk:
        print(chunk["response"], end="", flush=True)
```

### Async Support

The library also supports async operations:

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

## Automatic Ollama Installation

This package can automatically check for Ollama installation and help you install it:

```python
from ollama_toolkit.utils.common import ensure_ollama_running

# Check and optionally install/start Ollama
is_running, message = ensure_ollama_running()
if is_running:
    print(f"Ollama is ready: {message}")
else:
    print(f"Ollama setup failed: {message}")
```

You can also use the provided CLI tool:

```bash
# Check if Ollama is installed and running, install if needed
python -m ollama_toolkit.tools.install_ollama

# Check only, don't install or start
python -m ollama_toolkit.tools.install_ollama --check

# Install Ollama if not already installed
python -m ollama_toolkit.tools.install_ollama --install

# Start Ollama if not already running
python -m ollama_toolkit.tools.install_ollama --start

# Restart Ollama server
python -m ollama_toolkit.tools.install_ollama --restart
```

## Command-Line Interface

The package includes a comprehensive CLI:

```bash
# Main CLI command with subcommands
python -m ollama_toolkit.cli --help

# List available models
python -m ollama_toolkit.cli list-models

# Generate text
python -m ollama_toolkit.cli generate llama2 "Explain quantum computing"

# Chat with a model
python -m ollama_toolkit.cli chat llama2 "Tell me a joke" --system "You are a comedian"

# Create embeddings
python -m ollama_toolkit.cli embedding llama2 "This is a test sentence"

# Model management
python -m ollama_toolkit.cli pull llama2
python -m ollama_toolkit.cli model-info llama2
python -m ollama_toolkit.cli copy llama2 llama2-backup
python -m ollama_toolkit.cli delete llama2-backup

# Get Ollama version
python -m ollama_toolkit.cli version
```

## API Documentation

### Core Client Methods

- **generate(model, prompt, options=None, stream=False)** - Generate text completions
- **chat(model, messages, options=None, stream=False)** - Generate chat completions
- **list_models()** - Get list of available models
- **get_model_info(model)** - Get detailed model information
- **pull_model(model, stream=False)** - Pull a model from Ollama library
- **delete_model(model)** - Delete a model
- **copy_model(source, destination)** - Copy a model
- **get_version()** - Get Ollama version
- **create_embedding(model, prompt)** - Generate embeddings
- **batch_embeddings(model, prompts)** - Generate multiple embeddings efficiently

All methods have async equivalents prefixed with 'a' (e.g., `agenerate`, `achat`).

## Error Handling

The package provides specific exception types for better error handling:

```python
from ollama_toolkit import ModelNotFoundError, OllamaAPIError

try:
    client.generate(model="non-existent-model", prompt="Hello")
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
except OllamaAPIError as e:
    print(f"API error: {e}")
```

## Development

This project uses a central virtual environment located at `/home/lloyd/Development/eidos_venv`. To set up your development environment:

```bash
# Initialize the development environment (creates and activates venv, installs dependencies)
source ./development.sh

# Format code
black ollama_toolkit
isort ollama_toolkit

# Run type checking
mypy ollama_toolkit

# Run tests
pytest ollama_toolkit/tests
```

For repository setup:

```bash
# Initialize as its own Git repository
./init_repo.sh

# Update parent repository .gitignore to exclude this package
./update_parent_gitignore.sh
```

## Examples

The package includes several example scripts to help you get started:

- **basic_usage.py** - Basic client usage with model listing and generation
- **version_example.py** - How to check the Ollama version
- **generate_example.py** - Text generation with both streaming and non-streaming modes
- **chat_example.py** - Chat completion with message history management
- **embedding_example.py** - Creating and comparing text embeddings

Run the examples directly from the examples directory:

```bash
python -m ollama_toolkit.examples.basic_usage
```

## Project Structure

```
ollama_toolkit/
├── __init__.py                  # Package initialization and exports
├── client.py                    # Main OllamaClient implementation
├── cli.py                       # Command-line interface
├── exceptions.py                # Custom exceptions
├── docs/                        # Documentation files
│   ├── index.md                 # Main documentation index
│   ├── api_reference.md         # API documentation
│   └── examples.md              # Example usage documentation
├── examples/                    # Example usage scripts
│   ├── __init__.py              # Package marker
│   ├── basic_usage.py           # Basic client usage example
│   ├── chat_example.py          # Chat API example
│   ├── embedding_example.py     # Embedding API example
│   ├── generate_example.py      # Generate API example
│   └── version_example.py       # Version API example
├── tests/                       # Test suite
│   ├── __init__.py              # Package marker
│   ├── test_client.py           # Client tests
│   ├── test_nexus.py            # Test runner utility
│   └── test_utils.py            # Utility tests
├── tools/                       # Development tools
│   ├── __init__.py              # Package marker
│   └── install_ollama.py        # Ollama installation tool
├── utils/                       # Utility functions
│   ├── __init__.py              # Package marker
│   ├── common.py                # Common utilities
│   └── model_constants.py       # Model name constants
└── wheelhouse/                  # Build artifacts
├── LICENSE                      # License file
├── pyproject.toml               # Project configuration
├── setup.py                     # Legacy setup script
├── README.md                    # Project documentation
└── publish.py                   # Script for publishing to PyPI
```

## Project Setup

### Initializing as a Standalone Repository

If you're working within a larger repository and want to initialize `ollama_toolkit` as its own Git repository:

```bash
# Navigate to the ollama_toolkit directory
cd /path/to/ollama_toolkit

# Initialize a new Git repository
git init

# Add all files
git add .

# Create an initial commit
git commit -m "Initial commit of ollama_toolkit"

# Add a remote repository (replace with your repository URL)
git remote add origin https://github.com/Ace1928/ollama_toolkit.git

# Push to your repository
git push -u origin main
```

To avoid tracking this directory in the parent repository, add it to the parent's `.gitignore` file:

## Overview

The `ollama_toolkit` package provides a convenient interface to interact with the Ollama Toolkit. It includes:

- A high-level client (`OllamaClient`) for making API requests
- Command-line interface for interacting with Ollama models
- Utility functions for common operations
- Comprehensive error handling
- Detailed examples and documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Format your code (`black ollama_toolkit && isort ollama_toolkit`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Contact

Lloyd Handyside - [ace1928@gmail.com](mailto:ace1928@gmail.com)

Project Link: [https://github.com/lloydhd/ollama_toolkit](https://github.com/lloydhd/ollama_toolkit)
