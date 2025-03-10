# Version Endpoint

This document explains how to retrieve the current version of the Ollama server and confirms the Ollama Forge client is at v0.1.9.

## Endpoint

```
GET /api/version
```
Returns JSON containing the server's version details.

## Example

```bash
curl http://localhost:11434/api/version
```

Expected output:
```json
{
  "version": "0.1.11"
}
```

(Ollama Forge v0.1.9 is compatible with Ollama server >= 0.1.11.)

### Python Usage Example

```python
from ollama_forge import OllamaClient

client = OllamaClient()

version_info = client.get_version()
print(f"Connected to Ollama server version: {version_info['version']}")
```

## Async Example

```python
import asyncio
from ollama_forge import OllamaClient

async def get_version_async():
    client = OllamaClient()
    version_info = await client.aget_version()
    print(f"Async - Connected to Ollama version: {version_info['version']}")

# Run the async function
asyncio.run(get_version_async())
```

