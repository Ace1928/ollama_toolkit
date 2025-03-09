# System API

This document details system-related endpoints in Ollama Toolkit v0.1.8 for checking server status, version information, and system operations.

## Endpoints Overview

- **GET /api/version** - Get Ollama version
- **GET /api/health** - Check system health
- **GET /api/metrics** - Retrieve performance metrics

## Endpoint: /api/version

Retrieve version information for the Ollama server.

### Method
`GET`

### Response

```json
{
  "version": "0.1.14"
}
```

## Endpoint: /api/health

Check the health status of the Ollama server.

### Method
`GET`

### Response
A status code 200 OK response with no body indicates the server is healthy.

## Endpoint: /api/metrics

Retrieve performance metrics for the Ollama server (if enabled).

### Method
`GET`

### Response

```json
{
  "total_requests": 243,
  "total_tokens_predicted": 18965,
  "total_tokens_input": 4382,
  "requests_per_minute": 12.4,
  "tokens_per_second": 24.8,
  "active_requests": 1,
  "memory_usage": {
    "ram": 1073741824,
    "gpu": 536870912
  }
}
```

## Client Implementation

The Ollama Toolkit client provides utility functions for interacting with these system endpoints:

```python
from ollama_toolkit import OllamaClient
from ollama_toolkit.utils.common import (
    check_ollama_installed,
    check_ollama_running,
    ensure_ollama_running,
    install_ollama
)

# Get Ollama version
client = OllamaClient()
version_info = client.get_version()
print(f"Ollama version: {version_info.get('version', 'unknown')}")

# Check if Ollama is installed
installed, install_path = check_ollama_installed()
if installed:
    print(f"Ollama is installed at: {install_path}")
else:
    print("Ollama is not installed")
    
    # Install Ollama if not already installed
    success, message = install_ollama()
    print(message)

# Check if Ollama server is running
running, server_info = check_ollama_running()
if running:
    print(f"Ollama server is running: {server_info}")
else:
    print("Ollama server is not running")
    
    # Ensure Ollama is both installed and running
    success, message = ensure_ollama_running()
    print(message)
```

## Installation Process

The Ollama Toolkit can install and manage the Ollama server with zero friction:

1. **Detection**: Check if Ollama binary exists in standard paths
2. **Installation**: Download and install Ollama from official sources
3. **Verification**: Confirm installation with mathematical certainty  
4. **Startup**: Launch Ollama server process with optimal configuration
5. **Validation**: Verify server responds with correct API signature

## Server Management

Controlling the Ollama server lifecycle:

```python
from ollama_toolkit.utils.common import (
    start_ollama_server,
    stop_ollama_server,
    restart_ollama_server
)

# Start the Ollama server
success, message = start_ollama_server()
print(f"Start result: {message}")

# Restart the Ollama server
success, message = restart_ollama_server()
print(f"Restart result: {message}")

# Stop the Ollama server
success, message = stop_ollama_server()
print(f"Stop result: {message}")
```

## Eidosian Integration

The System API embodies Eidosian principles:

- **Self-Awareness as Foundation**: The system knows its own state with certainty
- **Structure as Control**: Server management follows precise architectural patterns
- **Recursive Refinement**: Each operation builds upon the previous with mathematical precision
- **Velocity as Intelligence**: Optimized for rapid state transitions with minimal overhead

By maintaining awareness of the system state, Ollama Toolkit creates a foundationally sound basis for all higher-level operations.

## Platform Compatibility

The System API handles platform-specific behaviors with recursive elegance:

| Platform | Installation | Process Management | Configuration |
|----------|--------------|-------------------|--------------|
| Linux    | Package manager or direct binary | Systemd or direct process | User-specific paths |
| macOS    | Homebrew or direct binary | launchd or direct process | User-specific paths |
| Windows  | Direct binary | Windows services or direct process | User-specific paths |

Each platform implementation maintains the same mathematical interface while adapting to platform-specific constraints.