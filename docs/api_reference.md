# API Reference

This document—a precision-engineered blueprint—details all classes and methods provided by the Ollama Forge client.

## OllamaClient

The main class for interacting with the Ollama Forge, designed with contextual integrity and recursive refinement.

```python
from ollama_forge import OllamaClient
from ollama_forge.utils.model_constants import DEFAULT_CHAT_MODEL, DEFAULT_EMBEDDING_MODEL

# Initialize with optimal defaults - each parameter carefully calibrated
client = OllamaClient(
    base_url="http://localhost:11434/",  # Foundational connection point
    timeout=300,                         # Generous yet bounded timeout window
    max_retries=3,                       # Optimal retry balance for resilience
    retry_delay=1.0,                     # Mathematically sound exponential backoff
    cache_enabled=False,                 # Toggle for performance optimization
    cache_ttl=300.0                      # Time-bounded memory efficiency
)

# Generate text
response = client.generate(
    model=DEFAULT_CHAT_MODEL,
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7}
)
print(response["response"])

# Create embedding
embedding = client.create_embedding(
    model=DEFAULT_EMBEDDING_MODEL,
    prompt="This is a sample text for embedding."
)
print(embedding["embedding"])
```

### Constructor Parameters

Each parameter precisely tuned for maximum effect:

- `base_url` (str): The base URL of the Ollama Forge server. Default: "http://localhost:11434/"
- `timeout` (int): Default timeout for API requests in seconds. Default: 300
- `max_retries` (int): Maximum number of retry attempts for failed requests. Default: 3
- `retry_delay` (float): Delay between retry attempts in seconds. Default: 1.0
- `cache_enabled` (bool): Whether to cache API responses. Default: False
- `cache_ttl` (float): Cache time-to-live in seconds. Default: 300.0 (5 minutes)

### Core Methods
- generate / agenerate — Text generation with precision
- chat / achat — Conversational flow with structure
- create_embedding / acreate_embedding — Vector transformation with mathematical elegance
- list_models / pull_model / delete_model — Model lifecycle management
- get_version / check_ollama_installed / ensure_ollama_running — System verification

For maximum compatibility with autodoc systems, each function uses a Google-style docstring format with a brief summary, argument descriptions, and return values.

#### Text Generation

##### generate

Generate a completion for the given prompt with recursive refinement.

```python
response = client.generate(
    model=DEFAULT_CHAT_MODEL,
    prompt="Explain quantum computing in simple terms",
    options={"temperature": 0.7},  # Precisely tuned randomness
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

**Options Dictionary Parameters**:
- `temperature` (float): Controls randomness in generation. Higher values (e.g., 0.8) make output more random, lower values (e.g., 0.2) make it more deterministic
- `top_p` (float): Controls diversity via nucleus sampling. Default: 1.0
- `top_k` (int): Limits token selection to top K options. Default: -1 (disabled)
- `max_tokens` (int): Maximum number of tokens to generate. Default varies by model
- `presence_penalty` (float): Penalty for token repetition. Default: 0.0
- `frequency_penalty` (float): Penalty based on frequency in text. Default: 0.0
- `stop` (list): Sequences where the API will stop generating further tokens
- `seed` (int): Random number seed for reproducible outputs

##### agenerate

Asynchronous version of `generate`. *(Note: This method is planned but not fully implemented in the current version)*

```python
response = await client.agenerate(
    model=DEFAULT_CHAT_MODEL,
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
    model=DEFAULT_CHAT_MODEL,
    messages=messages,
    options={"temperature": 0.7},
    stream=False
)
```

**Parameters**:
- `model` (str): The model name to use for generation
- `messages` (list): List of message dictionaries with 'role' and 'content' keys
- `options` (dict, optional): Additional model parameters
- `stream` (bool, optional): Whether to stream the response. Default: True

**Returns**:
- If `stream=False`: A dictionary containing the response
- If `stream=True`: An iterator yielding response chunks

**Message Object Structure**:
- `role` (str): The role of the message - "system", "user", "assistant", or "tool"
- `content` (str): The content of the message
- `images` (list, optional): For multimodal models, a list of image data
- `tool_calls` (list, optional): For function calling, a list of tool call objects

##### achat

Asynchronous version of `chat`. *(Note: This method is planned but not fully implemented in the current version)*

```python
response = await client.achat(
    model=DEFAULT_CHAT_MODEL,
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
    model=DEFAULT_EMBEDDING_MODEL,
    prompt="This is a sample text for embedding."
)
```

**Parameters**:
- `model` (str): The model name to use for embedding
- `prompt` (str): The text to create an embedding for
- `options` (dict, optional): Additional model parameters

**Returns**:
- A dictionary containing the embedding vector

**Response Structure**:
- `model` (str): The model name
- `embedding` (list): The embedding vector (array of floats)
- `total_duration` (int): Time spent generating embeddings (nanoseconds)
- `prompt_eval_count` (int): Number of tokens processed

##### acreate_embedding

Asynchronous version of `create_embedding`. *(Note: This method is planned but not fully implemented in the current version)*

```python
embedding = await client.acreate_embedding(
    model=DEFAULT_EMBEDDING_MODEL,
    prompt="This is a sample text for embedding."
)
```

##### batch_embeddings

Create embeddings for multiple prompts efficiently. *(Note: This method is planned but not fully implemented in the current version)*

```python
embeddings = client.batch_embeddings(
    model=DEFAULT_EMBEDDING_MODEL,
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

**Response Structure**:
- `models` (list): A list of model objects containing:
  - `name` (str): The model name
  - `size` (int): Size in bytes
  - `modified_at` (str): Timestamp of last modification
  - `digest` (str): Model digest
  - `details` (object): Additional model details

##### get_model_info

Get information about a specific model. *(Note: This method is planned but not fully implemented in the current version)*

```python
model_info = client.get_model_info(DEFAULT_CHAT_MODEL)
```

**Parameters**:
- `model` (str): The model name

**Returns**:
- A dictionary containing model information

##### pull_model

Pull a model from the Ollama registry.

```python
# Non-streaming
result = client.pull_model(DEFAULT_CHAT_MODEL, stream=False)

# Streaming with progress updates
for update in client.pull_model(DEFAULT_CHAT_MODEL, stream=True):
    print(f"Progress: {update.get('status')}")
```

**Parameters**:
- `model` (str): The model name to pull
- `stream` (bool, optional): Whether to stream the download progress. Default: False

**Returns**:
- If `stream=False`: A dictionary with the status
- If `stream=True`: An iterator of status updates

**Stream Update Structure**:
- `status` (str): Status message like "downloading", "processing", "success"
- `completed` (int): Bytes downloaded (present during downloading)
- `total` (int): Total bytes to download (present during downloading)
- `digest` (str): Model digest (present during downloading)

##### delete_model

Delete a model.

```python
success = client.delete_model(DEFAULT_CHAT_MODEL)
```

**Parameters**:
- `model` (str): The model name to delete

**Returns**:
- A boolean indicating success or failure

##### copy_model

Copy a model to a new name. *(Note: This method is planned but not fully implemented in the current version)*

```python
result = client.copy_model(DEFAULT_CHAT_MODEL, "my-model-copy")
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

##### _messages_to_prompt

Convert chat messages to a unified prompt string for models that don't support chat format.

```python
prompt = client._messages_to_prompt(messages)
```

**Parameters**:
- `messages` (list): List of message dictionaries

**Returns**:
- A formatted prompt string

##### _is_likely_embedding_model

Check if a model is likely to be an embedding-only model based on name patterns.

```python
is_embedding = client._is_likely_embedding_model(DEFAULT_EMBEDDING_MODEL)
```

**Parameters**:
- `model_name` (str): Name of the model to check

**Returns**:
- `True` if the model is likely embedding-only, `False` otherwise

### Eidosian Note
We strive for recursive excellence:
- **Recursive Refinement:** Each function evolves toward perfection through rigorous testing and user feedback
- **Humor as Cognitive Leverage:** Error messages enlighten through carefully calibrated wit
- **Structure as Control:** Every parameter and return type forms a precise architectural blueprint
- **Velocity as Intelligence:** Functions optimized for lightning-fast execution without sacrificing depth

## Exception Classes

The package provides precisely engineered exception types for clear error handling:

- `OllamaAPIError`: Base exception class for all Ollama Forge errors
- `ConnectionError`: Raised when connection to the API fails
- `TimeoutError`: Raised when an API request times out
- `ModelNotFoundError`: Raised when a requested model is not found
- `ServerError`: Raised when the API server returns a 5xx error
- `InvalidRequestError`: Raised when the API server returns a 4xx error
- `StreamingError`: Raised when there's an error during streaming responses
- `ParseError`: Raised when there's an error parsing API responses
- `AuthenticationError`: Raised when authentication fails
- `EndpointNotFoundError`: Raised when an API endpoint is not found
- `ModelCompatibilityError`: Raised when a model doesn't support an operation
- `StreamingTimeoutError`: Raised when a streaming response times out

## Utility Functions

The package provides several utility functions in `ollama_forge.utils.common`:

### Display Functions

- `print_header(title)`: Print a formatted header
- `print_success(message)`: Print a success message in green
- `print_error(message)`: Print an error message in red
- `print_warning(message)`: Print a warning message in yellow
- `print_info(message)`: Print an information message in blue
- `print_json(data)`: Print formatted JSON data

### API Utilities

- `make_api_request(method, endpoint, data=None, base_url=DEFAULT_OLLAMA_API_URL, timeout=300)`: Make a synchronous API request
- `async_make_api_request(method, endpoint, data=None, base_url=DEFAULT_OLLAMA_API_URL, timeout=300)`: Make an asynchronous API request

### Ollama Management

- `check_ollama_installed()`: Check if Ollama is installed on the system
- `check_ollama_running()`: Check if Ollama server is running
- `install_ollama()`: Attempt to install Ollama
- `ensure_ollama_running()`: Ensure Ollama is installed and running
- `format_traceback(e)`: Format an exception traceback for logging or display

### Model Constants

The `ollama_forge.utils.model_constants` module provides:

- `DEFAULT_CHAT_MODEL`: Default model for chat completions
- `BACKUP_CHAT_MODEL`: Fallback model for chat completions
- `DEFAULT_EMBEDDING_MODEL`: Default model for embeddings
- `BACKUP_EMBEDDING_MODEL`: Fallback model for embeddings
- `resolve_model_alias(alias)`: Convert model alias to actual model name
- `get_fallback_model(model_name)`: Get the appropriate fallback model

Refer to the examples in `/examples` for real-world usage.
