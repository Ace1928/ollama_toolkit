# Generate a Completion

Generate a response for a given prompt with a provided model. This is a streaming endpoint, so there will be a series of responses. The final response object will include statistics and additional data from the request.

## Endpoint

## Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| model | string | The model name | Yes |
| prompt | string | The prompt to generate a response for | Yes |
| suffix | string | The text after the model response | No |
| images | array | A list of base64-encoded images (for multimodal models like llava) | No |

### Advanced Parameters (Optional)

| Parameter | Type | Description |
|-----------|------|-------------|
| format | string/object | The format to return a response in. Can be "json" or a JSON schema |
| options | object | Additional model parameters listed in the documentation for the Modelfile such as temperature |
| system | string | System message (overrides what is defined in the Modelfile) |
| template | string | The prompt template to use (overrides what is defined in the Modelfile) |
| stream | boolean | If false, the response will be returned as a single response object, rather than a stream of objects |
| raw | boolean | If true, no formatting will be applied to the prompt |
| keep_alive | string | Controls how long the model will stay loaded into memory following the request (default: 5m) |

## Response

The API returns a stream of JSON objects by default. The final response in the stream includes additional data:

| Field | Type | Description |
|-------|------|-------------|
| model | string | The model name |
| created_at | string | The timestamp when the response was created |
| response | string | The generated text (empty if streamed) |
| done | boolean | Whether the generation is complete |
| context | array | An encoding of the conversation used in this response |
| total_duration | number | Time spent generating the response (nanoseconds) |
| load_duration | number | Time spent loading the model (nanoseconds) |
| prompt_eval_count | number | Number of tokens in the prompt |
| prompt_eval_duration | number | Time spent evaluating the prompt (nanoseconds) |
| eval_count | number | Number of tokens in the response |
| eval_duration | number | Time spent generating the response (nanoseconds) |

## Examples

### Generate Request (Streaming)

#### Request

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'
```

#### Response

```json
{
  "model": "deepseek-r1:1.5b",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 10706818083,
  "load_duration": 6338219291,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 130079000,
  "eval_count": 259,
  "eval_duration": 4232710000
}
```

