# Generate a Chat Completion

Generate the next message in a chat with a provided model. This is a streaming endpoint, so there will be a series of responses. Streaming can be disabled using "stream": false. The final response object will include statistics and additional data from the request.

## Endpoint

## Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| model | string | The model name | Yes |
| messages | array | The messages of the chat, used to keep chat memory | Yes |
| tools | array | List of tools in JSON for the model to use if supported | No |

### Message Object

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| role | string | The role of the message: "system", "user", "assistant", or "tool" | Yes |
| content | string | The content of the message | Yes |
| images | array | A list of images to include in the message (for multimodal models) | No |
| tool_calls | array | A list of tools in JSON that the model wants to use | No |

### Advanced Parameters (Optional)

| Parameter | Type | Description |
|-----------|------|-------------|
| format | string/object | The format to return a response in. Can be "json" or a JSON schema |
| options | object | Additional model parameters (temperature, etc.) |
| stream | boolean | If false, the response will be returned as a single object rather than a stream |
| keep_alive | string | Controls how long the model will stay loaded into memory (default: 5m) |

## Response

The API returns a stream of JSON objects by default. Each object contains:

| Field | Type | Description |
|-------|------|-------------|
| model | string | The model name |
| created_at | string | The timestamp when the response was created |
| message | object | Contains role, content, and other message data |
| done | boolean | Whether the generation is complete |

The final response in the stream includes additional statistics:

| Field | Type | Description |
|-------|------|-------------|
| total_duration | number | Time spent generating the response (nanoseconds) |
| load_duration | number | Time spent loading the model (nanoseconds) |
| prompt_eval_count | number | Number of tokens in the prompt |
| prompt_eval_duration | number | Time spent evaluating the prompt (nanoseconds) |
| eval_count | number | Number of tokens in the response |
| eval_duration | number | Time spent generating the response (nanoseconds) |

## Examples

### Chat Request (Streaming)

#### Request

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    },
    {
      "role": "assistant",
      "content": "due to rayleigh scattering."
    },
    {
      "role": "user",
      "content": "how is that different than mie scattering?"
    }
  ]
}'
```

#### Response

```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T08:52:19.385406455-07:00",
  "message": {
    "role": "assistant",
    "content": "The",
    "images": null
  },
  "done": false
}
```

```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "done": true,
  "total_duration": 4883583458,
  "load_duration": 1334875,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 342546000,
  "eval_count": 282,
  "eval_duration": 4535599000
}
```


