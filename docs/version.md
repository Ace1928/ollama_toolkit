# Version API

Retrieve the Ollama version information.

## Endpoint

```
GET /api/version
```

This endpoint returns version information about the running Ollama instance. It doesn't require any parameters and is useful for checking API compatibility.

## Response

Returns a JSON object containing the current Ollama version.

### Response Fields

| Field    | Type   | Description          |
|----------|--------|----------------------|
| version  | string | The Ollama version   |

## Example

### Request

```bash
curl http://localhost:11434/api/version
```

### Response

```json
{
  "version": "0.1.8"
}
```

### Python Usage Example

```python
from ollama_toolkit import OllamaClient

# Initialize the client - system verification foundation
client = OllamaClient()

# Get and display version information
version_info = client.get_version()
print(f"Connected to Ollama version: {version_info['version']}")
```

## Async Example

```python
import asyncio
from ollama_toolkit import OllamaClient

async def get_version_async():
    client = OllamaClient()
    version_info = await client.aget_version()
    print(f"Async - Connected to Ollama version: {version_info['version']}")

# Run the async function
asyncio.run(get_version_async())
```

