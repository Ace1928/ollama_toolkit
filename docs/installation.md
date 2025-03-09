# Installation Guide

This guide covers all aspects of installing and setting up Ollama Toolkit.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Ollama (version 0.1.11 or later recommended, will be automatically installed if not present)
- 2+ GB RAM for running small models
- 8+ GB RAM recommended for larger models

## Basic Installation

Install the package directly from PyPI:

```bash
pip install ollama-toolkit
```

## Development Installation

For development or to access the latest features:

```bash
# Clone the repository
git clone https://github.com/lloydhd/ollama_toolkit.git
cd ollama_toolkit

# Install in development mode
pip install -e .
```

## Automatic Ollama Setup

Ollama Toolkit can automatically install and manage Ollama for you:

```python
from ollama_toolkit.utils.common import ensure_ollama_running

# This will install Ollama if needed and start the server
is_running, message = ensure_ollama_running()
if is_running:
    print(f"Ollama is ready: {message}")
else:
    print(f"Could not start Ollama: {message}")
```

## Manual Ollama Installation

If you prefer to install Ollama manually:

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### macOS
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download the installer from: https://ollama.com/download/windows

## Verifying Installation

Verify the installation with:

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
version = client.get_version()
print(f"Connected to Ollama version: {version['version']}")

# List available models
models = client.list_models()
print("Available models:", [model.get("name") for model in models.get("models", [])])
```

## Dependencies

The package automatically installs these dependencies:
- `requests`: For HTTP communication
- `aiohttp`: For asynchronous requests
- `colorama`: For terminal coloring
- `numpy`: For array manipulation (optional, for embedding operations)

## Configuration

No configuration is necessary to get started, but you can customize the client:

```python
from ollama_toolkit import OllamaClient

# Custom configuration
client = OllamaClient(
    base_url="http://localhost:11434/",  # Custom Ollama API URL
    timeout=300,                         # Request timeout in seconds
    max_retries=3,                       # Connection retry attempts
    retry_delay=1.0,                     # Delay between retries
    cache_enabled=True,                  # Enable response caching
    cache_ttl=300.0                      # Cache time-to-live in seconds
)
```

## Troubleshooting Installation

If you encounter issues during installation:

1. **Ollama not found**: Ensure Ollama is installed and in your PATH
2. **Connection errors**: Check if the Ollama server is running (`ollama serve`)
3. **Python version**: Verify you're using Python 3.6+
4. **Permission issues**: Try installing with `sudo` or use a virtual environment

For more detailed troubleshooting, see the [Troubleshooting Guide](troubleshooting.md).
