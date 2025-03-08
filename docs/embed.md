# Generate Embeddings

Generate embeddings from a model. Embeddings are vector representations of text that can be used for semantic search, clustering, and other NLP tasks.

## Endpoint

## Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| model | string | Name of model to generate embeddings from | Yes |
| input | string/array | Text or list of text to generate embeddings for | Yes |

### Advanced Parameters (Optional)

| Parameter | Type | Description |
|-----------|------|-------------|
| truncate | boolean | Truncates the end of each input to fit within context length. Returns error if false and context length is exceeded. Defaults to true |
| options | object | Additional model parameters listed in the documentation for the Modelfile |
| keep_alive | string | Controls how long the model will stay loaded into memory following the request (default: 5m) |

## Response

| Field | Type | Description |
|-------|------|-------------|
| model | string | The model name |
| embeddings | array | Array of embedding vectors (array of floats) |
| total_duration | number | Time spent generating the embeddings (nanoseconds) |
| load_duration | number | Time spent loading the model (nanoseconds) |
| prompt_eval_count | number | Number of tokens processed |

## Examples

### Single Input Request

#### Request

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "all-minilm",
  "input": "Why is the sky blue?"
}'
```

#### Response

```json
{
  "model": "all-minilm",
  "embeddings": [[
    0.010071029, -0.0017594862, 0.05007221, 0.04692972, 0.054916814,
    0.008599704, 0.105441414, -0.025878139, 0.12958129, 0.031952348
  ]],
  "total_duration": 14143917,
  "load_duration": 1019500,
  "prompt_eval_count": 8
}
```

### Multiple Input Request

#### Request

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "all-minilm",
  "input": ["Why is the sky blue?", "Why is the grass green?"]
}'
```

#### Response

```json
{
  "model": "all-minilm",
  "embeddings": [[
    0.010071029, -0.0017594862, 0.05007221, 0.04692972, 0.054916814,
    0.008599704, 0.105441414, -0.025878139, 0.12958129, 0.031952348
  ],[
    -0.0098027075, 0.06042469, 0.025257962, -0.006364387, 0.07272725,
    0.017194884, 0.09032035, -0.051705178, 0.09951512, 0.09072481
  ]]
}
```

