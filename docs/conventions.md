# Ollama Toolkit Conventions

This document outlines the conventions used across the Ollama Toolkit.

## Model Names

Model names follow a `model:tag` format, where `model` can have an optional namespace such as `example/model`. 

Examples:
- `orca-mini:3b-q4_1`
- `llama3:70b`

The tag is optional and, if not provided, will default to `latest`. The tag is used to identify a specific version.

## Durations

All durations are returned in nanoseconds.

## Streaming Responses

Certain endpoints stream responses as JSON objects. Streaming can be disabled by providing `{"stream": false}` for these endpoints.
