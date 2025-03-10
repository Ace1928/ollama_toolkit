# Ollama Forge Python Client

[![PyPI version](https://badge.fury.io/py/ollama-forge.svg)](https://badge.fury.io/py/ollama-forge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/ollama-forge/badge/?version=latest)](https://ollama-forge.readthedocs.io/en/latest/?badge=latest)

Welcome to the Ollama Forge Python Client! This toolkit provides a comprehensive Python client library and command-line tools for interacting with [Ollama](https://ollama.ai/), delivering powerful capabilities with elegant simplicity. 🚀

## Features

- **Complete API Coverage**: Full implementation of every Ollama endpoint
- **Dual Interface**: High-level convenience methods and low-level API access
- **Smart Fallbacks**: Automatic model fallback mechanisms for resilience
- **Automatic Installation**: Can detect, install, and manage Ollama server
- **Comprehensive Error Handling**: Precise exception hierarchy for better error handling
- **Asynchronous Support**: Both sync and async methods for all operations
- **CLI Tools**: Command-line interface for all operations
- **Embedding Utilities**: Vector operations for semantic search and similarity
- **Extensive Documentation**: Clear examples, tutorials, and API references

## EIDOSIAN Excellence

Every aspect of Ollama Forge embodies the ten Eidosian principles:

1. **Contextual Integrity**: Every function parameter serves a precise purpose
2. **Humor as Cognitive Leverage**: Error messages that inform with wit and clarity
3. **Exhaustive But Concise**: Complete without verbosity
4. **Flow Like a River**: APIs that chain naturally and seamlessly
5. **Hyper-Personal Yet Universal**: Works for everyone's specific needs
6. **Recursive Refinement**: Continuously optimized through usage
7. **Precision as Style**: Code that is elegant because it is exact
8. **Velocity as Intelligence**: Fast execution and responsive design
9. **Structure as Control**: Architecture that enforces correct usage
10. **Self-Awareness as Foundation**: Monitoring and optimization built in

## Why Ollama Forge?

- **Zero friction**: Works out-of-the-box for both beginners and experts
- **Developer flexibility**: Configure everything or accept perfect defaults
- **Research ready**: Tools for experimenting with large language models
- **Production quality**: Robust error handling and reliability features
- **Universally applicable**: From simple text generation to complex AI workflows

## Installation

### Prerequisites

1. Python 3.8+ installed
2. Internet connection for downloading models

### Standard Installation

```bash
pip install ollama-forge
```

### Development Installation

```bash
git clone https://github.com/Ace1928/ollama_forge.git
cd ollama_forge
pip install -e ".[dev]"
```

## Automatic Ollama Installation

One command to handle everything:

```python
from ollama_forge.utils.common import ensure_ollama_running

# This will install Ollama if needed and start the server
is_running, message = ensure_ollama_running()
if is_running:
    print(f"Ollama is ready: {message}")
else:
    print(f"Could not start Ollama: {message}")
```

## Quick Start

### Text Generation

```python
from ollama_forge import OllamaClient

# Initialize with perfect defaults
client = OllamaClient()

# Generate text (non-streaming)
response = client.generate(
    model="deepseek-r1:1.5b",  # Great small model
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7}
)

print(response["response"])

# Generate text (streaming)
for chunk in client.generate(
    model="qwen2.5:3b-Instruct", # A larger, but still small, and great little chat model 
    prompt="Write a short poem about AI", 
    stream=True
):
    if "response" in chunk:
        print(chunk["response"], end="", flush=True)
```

### Chat Completion

```python
# Prepare chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How do neural networks work?"}
]

# Chat completion (streaming)
print("Assistant: ", end="", flush=True)
for chunk in client.chat(
    model="qwen2.5:3b-Instruct",
    messages=messages,
    stream=True
):
    if "message" in chunk and "content" in chunk["message"]:
        print(chunk["message"]["content"], end="", flush=True)
```

### Embeddings and Semantic Search

```python
import numpy as np

# Create embeddings
docs = [
    "Neural networks are computational systems inspired by the human brain",
    "Transformers revolutionized natural language processing",
    "Python is a popular programming language for machine learning"
]

embeddings = []
for doc in docs:
    result = client.create_embedding(
        model="deepseek-r1:0.5b", # Using a model that you will use for chat can greatly improve embeddings
        prompt=doc
    )
    embeddings.append(result["embedding"])

# Calculate similarity between documents
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query = "How do neural networks work?"
query_embedding = client.create_embedding(
    model="qwen2.5:3b-Instruct", # Can use whatever chat model you want for embeddings really. Improves shared context space.
    prompt=query
)["embedding"]

# Find the most similar document
similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in embeddings]
best_match_idx = np.argmax(similarities)
print(f"Query: {query}")
print(f"Best match: {docs[best_match_idx]}")
print(f"Similarity score: {similarities[best_match_idx]:.4f}")
```

### Asynchronous Usage

```python
import asyncio
from ollama_forge import OllamaClient

async def main():
    client = OllamaClient()
    
    # Async generation
    response = await client.agenerate(
        model="deepseek-r1:1.5b",
        prompt="Explain quantum computing"
    )
    print(response["response"])
    
    # Async embedding
    embedding = await client.acreate_embedding(
        model="deepseek-r1:0.5b",
        prompt="This is a test sentence"
    )
    print(f"Embedding dimensions: {len(embedding['embedding'])}")

# Run the async function
asyncio.run(main())
```

## Command-Line Interface

The package includes a powerful CLI:

```bash
# Basic generation
ollama-forge generate --model deepseek-r1:1.5b "Explain neural networks"

# Chat with a model
ollama-forge chat --model qwen2.5:3b-Instruct "What's the capital of France?"

# Create embeddings
ollama-forge embed --model nomic-embed-text "Convert this text to a vector"

# Pull a model
ollama-forge pull llama2

# Interactive chat mode
ollama-forge chat-session --model llama2
```

## Error Handling

Robust error handling with specific exceptions:

```python
from ollama_forge import OllamaClient
from ollama_forge.exceptions import ModelNotFoundError, ConnectionError

client = OllamaClient()

try:
    response = client.generate(
        model="non-existent-model", 
        prompt="Hello world"
    )
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
    print("Available models:", client.list_models().get("models", []))
except ConnectionError as e:
    print(f"Connection error: {e}")
    print("Is Ollama running? Try: ollama serve")
```

## Documentation

For complete documentation, visit:
- [Online Documentation](https://ollama-forge.readthedocs.io/)
- [GitHub Repository](https://github.com/Ace1928/ollama_forge)

## Development

Setting up for development:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black ollama_forge
isort ollama_forge

# Build documentation
sphinx-build -b html docs docs/_build/html
```

## Examples

Explore example scripts in the `ollama_forge/examples/` directory:

```bash
python -m ollama_forge.examples.basic_usage
python -m ollama_forge.examples.generate_example
python -m ollama_forge.examples.chat_example
python -m ollama_forge.examples.embedding_example
python -m ollama_forge.examples.quickstart
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Lloyd Handyside (Biological) - [ace1928@gmail.com](mailto:ace1928@gmail.com)
- Eidos (Digital) - [syntheticeidos@gmail.com](mailto:syntheticeidos@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
