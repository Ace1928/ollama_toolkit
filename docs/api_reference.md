# API Reference

This page documents the key classes and methods provided by the Ollama Toolkit client.

## OllamaClient

The main class for interacting with the Ollama Toolkit.

```python
from ollama_toolkit import OllamaClient

client = OllamaClient(
    base_url="http://localhost:11434/",
    timeout=60,
    max_retries=3,
    retry_delay=1.0,
    cache_enabled=False
)
```

### Constructor Parameters

- `base_url` (str): The base URL of the Ollama Toolkit server. Default: "http://localhost:11434/"
- `timeout` (int): Default timeout for API requests in seconds. Default: 60
- `max_retries` (int): Maximum number of retry attempts for failed requests. Default: 3
- `retry_delay` (float): Delay between retry attempts in seconds. Default: 1.0
- `cache_enabled` (bool): Whether to cache API responses. Default: False
- `cache_ttl` (float): Cache time-to-live in seconds. Default: 300.0 (5 minutes)

### Methods

#### Text Generation

##### generate

Generate a completion for the given prompt.

```python
response = client.generate(
    model="llama2",
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7},
    stream=False
)
```

**Parameters**:
- `model` (str): The model name to use for generation
- `prompt` (str): The prompt to generate a response for
- `options` (dict, optional): Additional model parameters
- `stream` (bool, optional): Whether to stream the response. Default: False

**Returns**:
- If `stream=False`: A dictionary containing the response
- If `stream=True`: An iterator yielding response chunks

##### agenerate

Asynchronous version of `generate`.

```python
response = await client.agenerate(
    model="llama2",
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7},
    stream=False
)
```

**Returns**:
- If `stream=False`: A dictionary containing the response
- If `stream=True`: An async iterator yielding response chunks

#### Chat Completion

##### chat

Generate a chat response for the given messages.

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about neural networks."}
]
response = client.chat(
    model="llama2",
    messages=messages,
    options={"temperature": 0.7},
    stream=False
)
```

**Parameters**:
- `model` (str): The model name to use for generation
- `messages` (list): List of message dictionaries with 'role' and 'content' keys
- `options` (dict, optional): Additional model parameters
- `stream` (bool, optional): Whether to stream the response. Default: False

**Returns**:
- If `stream=False`: A dictionary containing the response
- If `stream=True`: An iterator yielding response chunks

##### achat

Asynchronous version of `chat`.

```python
response = await client.achat(
    model="llama2",
    messages=messages,
    options={"temperature": 0.7},
    stream=False
)
```

#### Embeddings

##### create_embedding

Create an embedding vector for the given text.

```python
embedding = client.create_embedding(
    model="nomic-embed-text",
    prompt="This is a sample text for embedding."
)
```

**Parameters**:
- `model` (str): The model name to use for embedding
- `prompt` (str): The text to create an embedding for
- `options` (dict, optional): Additional model parameters

**Returns**:
- A dictionary containing the embedding vector

##### acreate_embedding

Asynchronous version of `create_embedding`.

```python
embedding = await client.acreate_embedding(
    model="nomic-embed-text",
    prompt="This is a sample text for embedding."
)
```

##### batch_embeddings

Create embeddings for multiple prompts efficiently.

```python
embeddings = client.batch_embeddings(
    model="nomic-embed-text",
    prompts=["Text one", "Text two", "Text three"]
)
```

**Parameters**:
- `model` (str): The model name to use for embedding
- `prompts` (list): List of texts to create embeddings for
- `options` (dict, optional): Additional model parameters

**Returns**:
- A list of dictionaries containing embeddings

#### Model Management

##### list_models

List available models.

```python
models = client.list_models()
```

**Returns**:
- A dictionary containing the list of available models

##### get_model_info

Get information about a specific model.

```python
model_info = client.get_model_info("llama2")
```

**Parameters**:
- `model` (str): The model name

**Returns**:
- A dictionary containing model information

##### pull_model

Pull a model from the Ollama registry.

```python
# Non-streaming
result = client.pull_model("llama2", stream=False)

# Streaming with progress updates
for update in client.pull_model("llama2", stream=True):
    print(f"Progress: {update.get('status')}")
```

**Parameters**:
- `model` (str): The model name to pull
- `stream` (bool, optional): Whether to stream the download progress. Default: False

**Returns**:
- If `stream=False`: A dictionary with the status
- If `stream=True`: An iterator of status updates

##### delete_model

Delete a model.

```python
success = client.delete_model("llama2")
```

**Parameters**:
- `model` (str): The model name to delete

**Returns**:
- A boolean indicating success or failure

##### copy_model

Copy a model to a new name.

```python
result = client.copy_model("llama2", "my-llama2-copy")
```

**Parameters**:
- `source` (str): The source model name
- `destination` (str): The destination model name

**Returns**:
- A dictionary containing the status

#### Miscellaneous

##### get_version

Get the Ollama version.

```python
version = client.get_version()
print(f"Ollama version: {version['version']}")
```

**Returns**:
- A dictionary containing version information

##### aget_version

Asynchronous version of `get_version`.

```python
version = await client.aget_version()
```

## Exception Classes

The package provides several exception types for better error handling:

- `OllamaAPIError`: Base exception class for all Ollama Toolkit errors
- `ConnectionError`: Raised when connection to the API fails
- `TimeoutError`: Raised when an API request times out
- `ModelNotFoundError`: Raised when a requested model is not found
- `ServerError`: Raised when the API server returns a 5xx error
- `InvalidRequestError`: Raised when the API server returns a 4xx error
- `StreamingError`: Raised when there's an error during streaming responses
- `ParseError`: Raised when there's an error parsing API responses
- `AuthenticationError`: Raised when authentication fails

## Utility Functions

The package provides several utility functions in `ollama_toolkit.utils.common`:

- `print_header(title)`: Print a formatted header
- `print_success(message)`: Print a success message
- `print_error(message)`: Print an error message
- `print_warning(message)`: Print a warning message
- `print_info(message)`: Print an information message
- `print_json(data)`: Print formatted JSON data
- `make_api_request(method, endpoint, data=None, base_url=DEFAULT_OLLAMA_API_URL, timeout=60)`: Make an API request
- `async_make_api_request(method, endpoint, data=None, base_url=DEFAULT_OLLAMA_API_URL, timeout=60)`: Make an async API request
- `check_ollama_installed()`: Check if Ollama is installed
- `check_ollama_running()`: Check if Ollama server is running
- `install_ollama()`: Attempt to install Ollama
- `ensure_ollama_running()`: Ensure Ollama is installed and running
