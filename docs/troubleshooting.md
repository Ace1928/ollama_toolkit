# Troubleshooting Guide

This document provides structured solutions for common issues encountered when using Ollama Toolkit v0.1.8, organized by problem domain with Eidosian precision and recursion.

## Connection Issues

### Symptoms
- `ConnectionError` exceptions
- "Failed to connect" messages
- Timeout errors on initial connection

### Potential Causes & Solutions

#### 1. Ollama Server Not Running

**Diagnostic:**
```python
from ollama_toolkit.utils.common import check_ollama_running

is_running, message = check_ollama_running()
print(f"Ollama running: {is_running}, Message: {message}")
```

**Solution:**
Start the Ollama server with one of these approaches:
```python
# Method 1: Using toolkit utilities
from ollama_toolkit.utils.common import ensure_ollama_running
ensure_ollama_running()

# Method 2: Command line (execute in terminal)
ollama serve
```

## Model Loading Errors

When models fail to load...

## Performance Problems

If generation is too slow...