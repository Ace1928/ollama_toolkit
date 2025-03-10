# Ollama Forge Python Client

[![PyPI version](https://badge.fury.io/py/ollama-forge.svg)](https://badge.fury.io/py/ollama-forge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Welcome to the Ollama Forge Python Client! This toolkit provides a comprehensive Python client library and command-line tools for interacting with the [Ollama](https://ollama.ai/) API. 🚀

## Features

- **High-level client** (`OllamaClient`) for making API requests
- **Command-line interface** for interacting with Ollama models
- **Utility functions** for common operations
- **Comprehensive error handling** with precise exception types
- **Detailed examples and documentation** for easy onboarding

## EIDOSIAN Excellence
Every part of this toolkit embraces Eidosian Principles, ensuring:
- Precision for style, humor for clarity
- A seamless flow in usage
- Self-awareness to continually refine your process

## Why Use Ollama Forge?

Ollama Forge provides a comprehensive and efficient interface to interact with the Ollama API, following Eidosian principles of elegance, efficiency, and contextual integrity. It offers robust error handling, seamless integration, and extensive documentation to ensure a smooth development experience.

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

## Verifying Installation

After installation, you can verify everything is working by running:

```bash
# Run all tests
python -m pytest ollama_forge/tests

# Run specific test modules
python -m pytest ollama_forge/tests/test_client.py
```

You can also run a quick import test to ensure the package is accessible:

```bash
python -c "import ollama_forge; print(f'Ollama Forge version: {ollama_forge.__version__}')"
```

## Quick Start

```python
from ollama_forge import OllamaClient
from ollama_forge.utils.model_constants import DEFAULT_CHAT_MODEL

# Initialize the client
client = OllamaClient()

# Get Ollama version
version = client.get_version()
print(f"Ollama version: {version['version']}")

# Generate text (non-streaming)
response = client.generate(
    model=DEFAULT_CHAT_MODEL,
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7}
)

print(response["response"])

# Generate text (streaming)
for chunk in client.generate(
    model=DEFAULT_CHAT_MODEL, 
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
from ollama_forge import OllamaClient

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
from ollama_forge.utils.common import ensure_ollama_running

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
python -m ollama_forge.tools.install_ollama

# Check only, don't install or start
python -m ollama_forge.tools.install_ollama --check

# Install Ollama if not already installed
python -m ollama_forge.tools.install_ollama --install

# Start Ollama if not already running
python -m ollama_forge.tools.install_ollama --start

# Restart Ollama server
python -m ollama_forge.tools.install_ollama --restart
```

## Command-Line Interface

The package includes a comprehensive CLI:

```bash
# Main CLI command with subcommands
python -m ollama_forge.cli --help

# List available models
python -m ollama_forge.cli list-models

# Generate text
python -m ollama_forge.cli generate llama2 "Explain quantum computing"

# Chat with a model
python -m ollama_forge.cli chat llama2 "Tell me a joke" --system "You are a comedian"

# Create embeddings
python -m ollama_forge.cli embedding llama2 "This is a test sentence"

# Model management
python -m ollama_forge.cli pull llama2
python -m ollama_forge.cli model-info llama2
python -m ollama_forge.cli copy llama2 llama2-backup
python -m ollama_forge.cli delete llama2-backup

# Get Ollama version
python -m ollama_forge.cli version
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
from ollama_forge import ModelNotFoundError, OllamaAPIError

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
black ollama_forge
isort ollama_forge

# Run type checking
mypy ollama_forge

# Run tests
pytest ollama_forge/tests
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
python -m ollama_forge.examples.basic_usage
```

Use the scripts in the examples folder:
```bash
python -m ollama_forge.examples.quickstart
python -m ollama_forge.examples.basic_usage
python -m ollama_forge.examples.generate_example
python -m ollama_forge.examples.chat_example
python -m ollama_forge.examples.embedding_example
```

Review each example for the latest usage patterns, including fallback mechanisms, streaming modes, and updated model names (e.g. `deepseek-r1:1.5b`).

## Project Structure

```
ollama_forge/
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

If you're working within a larger repository and want to initialize `ollama_forge` as its own Git repository:

```bash
# Navigate to the ollama_forge directory
cd /path/to/ollama_forge

# Initialize a new Git repository
git init

# Add all files
git add .

# Create an initial commit
git commit -m "Initial commit of ollama_forge"

# Add a remote repository (replace with your repository URL)
git remote add origin https://github.com/Ace1928/ollama_forge.git

# Push to your repository
git push -u origin main
```

To avoid tracking this directory in the parent repository, add it to the parent's `.gitignore` file:

## Overview

The `ollama_forge` package provides a convenient interface to interact with the Ollama Forge. It includes:

- A high-level client (`OllamaClient`) for making API requests
- Command-line interface for interacting with Ollama models
- Utility functions for common operations
- Comprehensive error handling
- Detailed examples and documentation

## Automated Documentation

To build the documentation locally:
1. Install or update documentation tools:
   ```bash
   pip install sphinx sphinx-autobuild sphinx-rtd-theme
   ```
2. Navigate into the docs folder (or project root if you have a docs/ directory there).
3. Build the docs (for example with Sphinx):
   ```bash
   sphinx-build -b html . _build/html
   ```
4. Open the generated HTML files under `_build/html` in your browser.

Our docstrings follow a Google-style or reStructuredText format (compatible with autodoc systems). For more advanced usage, you can integrate with other popular doc generators (MkDocs, pdoc, etc.).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Format your code (`black ollama_forge && isort ollama_forge`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Contact

- Lloyd Handyside (Biological) - [ace1928@gmail.com](mailto:ace1928@gmail.com)
- Eidos (Digital) - [syntheticeidos@gmail.com](mailto:syntheticeidos@gmail.com)

Project Link: [https://github.com/Ace1928/ollama_forge](https://github.com/Ace1928/ollama_forge)
