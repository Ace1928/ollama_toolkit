# Ollama Toolkit Python Client Documentation

Welcome to the documentation for the Ollama Toolkit Python client.

## Installation

```bash
pip install ollama-api
```

## Basic Usage

```python
from ollama_toolkit import OllamaClient

client = OllamaClient()
response = client.generate(model="llama2", prompt="Hello, world!")
print(response)
```

## API Reference

See the [API Reference](api_reference.md) section for detailed information about all available methods and classes.

## Examples

Check out the [Examples](examples.md) section for more usage examples.
