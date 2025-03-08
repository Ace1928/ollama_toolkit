# Version API

Retrieve the Ollama version information.

## Endpoint

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
  "version": "0.5.1"
}
```

