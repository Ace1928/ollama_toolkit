# Models API

This document details the model management endpoints in Ollama Toolkit v0.1.9, providing interfaces for listing, pulling, modifying, and deleting models.

## Endpoints Overview

- **GET /api/tags** - List available models
- **GET /api/show** - Get model information
- **POST /api/pull** - Download a model
- **POST /api/push** - Upload a model
- **POST /api/create** - Create a custom model
- **POST /api/copy** - Copy a model
- **DELETE /api/delete** - Delete a model
- **GET /api/ps** - List running models

## Endpoint: /api/tags

List all available models.

### Method
`GET`

### Response

```json
{
  "models": [
    {
      "name": "deepseek-r1:1.5b",
      "modified_at": "2025-02-15T21:26:11Z",
      "size": 1610612736,
      "digest": "sha256:a1b2c3...",
      "details": {
        "format": "gguf",
        "family": "deepseek",
        "parameter_size": "1.5B",
        "quantization_level": "Q4_0"
      }
    },
    {
      "name": "qwen2.5:0.5b",
      "modified_at": "2025-02-14T18:42:33Z",
      "size": 536870912,
      "digest": "sha256:d4e5f6..."
    }
  ]
}
```

## Endpoint: /api/show

Retrieve detailed information about a specific model.

### Method
`GET`

### Query Parameters
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| name | string | Name of model to retrieve information for | Yes |

### Response

```json
{
  "name": "deepseek-r1:1.5b",
  "modified_at": "2025-02-15T21:26:11Z",
  "size": 1610612736,
  "digest": "sha256:a1b2c3...",
  "format": "gguf",
  "family": "deepseek",
  "parameter_size": "1.5B",
  "quantization_level": "Q4_0",
  "model_file": "/path/to/model/file.gguf"
}
```

## Endpoint: /api/pull

Pull a model from the Ollama library.

### Method
`POST`

### Request Body
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| name | string | Name of model to pull | Yes |
| stream | boolean | Stream the response (for progress updates) | No |

### Response (non-streaming)

```json
{
  "status": "success"
}
```

### Response (streaming)
A stream of JSON objects showing download progress:

```text
{"status":"downloading","digest":"sha256:a1b2c3...","total":1610612736,"completed":104857600}
{"status":"downloading","digest":"sha256:a1b2c3...","total":1610612736,"completed":209715200}
// Additional download progress messages would appear here
{"status":"processing","digest":"sha256:a1b2c3..."}
{"status":"success","digest":"sha256:a1b2c3..."}
```

## Endpoint: /api/create

Create a custom model using a Modelfile.

### Method
`POST`

### Request Body
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| name | string | Name of the model to create | Yes |
| modelfile | string | Contents of the Modelfile | Yes |
| stream | boolean | Stream the response | No |

### Response (non-streaming)

```json
{
  "status": "success"
}
```

### Response (streaming)
A stream of JSON objects showing progress:

```json
{"status":"processing","digest":"sha256:a1b2c3..."}
{"status":"success","digest":"sha256:a1b2c3..."}
```

## Endpoint: /api/copy

Copy a model to a new name.

### Method
`POST`

### Request Body
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| source | string | Source model name | Yes |
| destination | string | Destination model name | Yes |

### Response

```json
{
  "status": "success"
}
```

## Endpoint: /api/delete

Delete a model.

### Method
`DELETE`

### Request Body
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| model | string | Name of model to delete | Yes |

### Response
Empty 200 OK response on success

## Endpoint: /api/ps

List running models.

### Method
`GET`

### Response

```json
{
  "running": [
    {
      "name": "deepseek-r1:1.5b",
      "status": "running",
      "pid": 12345
    }
  ]
}
```

## Endpoint: /api/push

Push a model to a registry.

### Method
`POST`

### Request Body
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| name | string | Name of model to push | Yes |
| stream | boolean | Stream the response | No |

### Response (non-streaming)

```json
{
  "status": "success"
}
```

### Response (streaming)
A stream of JSON objects showing upload progress:

```text
{"status":"pushing","digest":"sha256:a1b2c3...","total":1610612736,"completed":104857600}
{"status":"pushing","digest":"sha256:a1b2c3...","total":1610612736,"completed":209715200}
// Additional upload progress messages would appear here
{"status":"success","digest":"sha256:a1b2c3..."}
```

## Mathematical Precision

The Models API follows Eidosian principles of structural control, ensuring each operation is mathematically precise and recursively consistent:

- **Model Hierarchy**: Each model exists within a mathematically defined space
- **Operation Atomicity**: All operations (pull, copy, delete) are atomic
- **Idempotent Actions**: Repeated operations yield consistent results
- **Structural Integrity**: Model relationships maintain referential integrity
- **Recursive Discoverability**: Model information reveals its own structure

## Client Implementation

The Ollama Toolkit client implements these endpoints with both synchronous and asynchronous interfaces, maintaining structural integrity across the API surface.