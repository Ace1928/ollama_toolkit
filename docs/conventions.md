# Ollama Toolkit Conventions

This document outlines the conventions used across the Ollama Toolkit v0.1.8, following Eidosian principles of precision, clarity, and structural integrity.

## Model Names

### Recommended Models

Latest recommended default models for different purposes:

- **General text generation**: `deepseek-r1:1.5b` - Excellent balance of quality and efficiency
- **Chat**: `qwen2.5:0.5b` - Optimized for conversational flow
- **Embeddings**: `nomic-embed-text` - Mathematical precision for vector representations
- **Lightweight option**: `tinyllama` - Minimal resource usage for constrained environments

The tag is optional and, if not provided, will default to `latest`. The tag is used to identify a specific version of a model.

### Model Name Format

```
name[:tag]@owner/model
```

Examples:
- `llama2`
- `llama2:13b`
- `llama2:70b-q4_0`
- `stability.ai/stable-diffusion`

## API Versioning

Ollama Toolkit follows semantic versioning (MAJOR.MINOR.PATCH):
- Current version: 0.1.8
- Version information is accessible via `ollama_toolkit.__version__`
- All endpoints maintain backward compatibility within the same MAJOR version

## Durations

All durations in API responses are provided in nanoseconds for maximum precision.

## Streaming Responses

Several endpoints support streaming responses. Control streaming behavior by setting:

```json
{"stream": true}
```

or 

```json
{"stream": false}
```

in request JSON.

Streaming can be disabled by providing `{"stream": false}` for these endpoints:
- `/api/generate`
- `/api/chat`
- `/api/pull`
- `/api/push`

## Error Handling

All error responses follow a consistent format:

```json
{
  "error": "Descriptive error message"
}
```

HTTP status codes:
- 200: Success
- 400: Bad request (client error)
- 404: Not found
- 500: Server error

## Python Client Parameters

When using the Python client, parameters follow consistent naming:
- Use snake_case for parameter names
- Boolean flags use explicit names (e.g., `stream=True` not `stream`)
- Optional parameters default to Python's `None` where appropriate

## Documentation Style

All documentation follows these Eidosian principles:
- **Contextual Integrity**: Every section serves a precise purpose
- **Exhaustive But Concise**: Complete information presented efficiently
- **Flow Like a River**: Smooth transitions between related concepts
- **Precision as Style**: Clear, accurate information presented elegantly

## CLI Conventions

Command-line interface commands use consistent patterns:
- Main subcommands represent primary API functions
- Options follow GNU-style with both short and long forms (e.g., `-m/--model`)
- Global flags appear before subcommands, specific flags after
