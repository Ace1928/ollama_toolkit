"""
Ollama Forge - Python client library and CLI for Ollama

This package provides a comprehensive set of helpers for interacting with Ollama,
following all ten Eidosian principles for elegant, efficient, and effective code.

Key Features:
- Complete API coverage
- Synchronous and asynchronous interfaces
- Smart model fallbacks
- CLI helpers
- Embedding utilities
"""

# First attempt to import from centralized config
try:
    from .config import (
        VERSION as __version__, 
        get_version_string,
        get_author_string,
        get_email_string,
        DEFAULT_OLLAMA_API_URL,
        DEFAULT_CHAT_MODEL,
        BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL,
        BACKUP_EMBEDDING_MODEL
    )
    __author__ = get_author_string()
    __email__ = get_email_string()
except ImportError:
    # Fallback to direct imports if config not available
    try:
        from version import __version__, get_version_string
    except ImportError:
        # Last resort fallback for standalone use
        try:
            from .version import __version__, get_version_string
        except ImportError:
            __version__ = "0.1.9"  # Fallback version
            get_version_string = lambda: __version__
        
    # Package metadata fallbacks
    __author__ = "Lloyd Handyside, Eidos"
    __email__ = "ace1928@gmail.com, syntheticeidos@gmail.com"
    
    # Critical constants with optimal defaults
    DEFAULT_OLLAMA_API_URL = "http://localhost:11434"
    
    # Optimal model defaults based on current benchmarks & availability
    DEFAULT_CHAT_MODEL = "deepseek-r1:1.5b"      # Best small model for chat
    BACKUP_CHAT_MODEL = "qwen2.5:0.5b-Instruct"  # Excellent fallback
    DEFAULT_EMBEDDING_MODEL = DEFAULT_CHAT_MODEL  # Using chat model for embeddings improves context
    BACKUP_EMBEDDING_MODEL = BACKUP_CHAT_MODEL

# License and URL information
__license__ = "MIT"
__url__ = "https://github.com/Ace1928/ollama_forge"
__description__ = "Python client library and CLI for Ollama"

# Core components that should always be available
try:
    from .client import OllamaClient
    from .async_client import AsyncOllamaClient
    from .exceptions import (
        OllamaAPIError, OllamaConnectionError, 
        OllamaModelNotFoundError, OllamaServerError,
        ConnectionError, TimeoutError, ModelNotFoundError, 
        ServerError, InvalidRequestError, StreamingError, ParseError
    )
except ImportError as e:
    import warnings
    warnings.warn(f"Ollama Forge components couldn't be imported: {e}. Ensure package is properly installed.")

# Define what's available when importing * from this package
__all__ = [
    'OllamaClient', 'AsyncOllamaClient', '__version__', 'get_version_string',
    'DEFAULT_OLLAMA_API_URL', 'DEFAULT_CHAT_MODEL', 'BACKUP_CHAT_MODEL',
    'DEFAULT_EMBEDDING_MODEL', 'BACKUP_EMBEDDING_MODEL',
    'OllamaAPIError', 'OllamaConnectionError', 'OllamaModelNotFoundError', 'OllamaServerError',
    'ConnectionError', 'TimeoutError', 'ModelNotFoundError', 'ServerError', 
    'InvalidRequestError', 'StreamingError', 'ParseError',
]

# Debug mode detection
import os
if os.environ.get('OLLAMA_FORGE_DEBUG') == '1':
    print(f"🔍 Ollama Forge v{__version__} loaded and ready")

