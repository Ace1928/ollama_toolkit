"""
Utility modules for the Ollama Toolkit client.
"""

# Import common utilities directly using relative imports
from .common import (
    DEFAULT_OLLAMA_API_URL,
    async_make_api_request,
    check_ollama_installed,
    check_ollama_running,
    ensure_ollama_running,
    install_ollama,
    make_api_request,
    print_error,
    print_header,
    print_info,
    print_json,
    print_success,
    print_warning,
)

# Import model constants if available
try:
    from .model_constants import (
        BACKUP_CHAT_MODEL,
        BACKUP_EMBEDDING_MODEL,
        DEFAULT_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL,
        resolve_model_alias,
    )
except ImportError:
    # Define default values if module doesn't exist
    DEFAULT_CHAT_MODEL = "llama2"
    BACKUP_CHAT_MODEL = "qwen2.5:0.5b"
    DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
    BACKUP_EMBEDDING_MODEL = "mxbai-embed-large"

    def resolve_model_alias(model_name):
        return model_name


__all__ = [
    # Common utilities
    "print_header",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_json",
    "make_api_request",
    "async_make_api_request",
    "check_ollama_installed",
    "check_ollama_running",
    "install_ollama",
    "ensure_ollama_running",
    "DEFAULT_OLLAMA_API_URL",
    # Model constants
    "DEFAULT_CHAT_MODEL",
    "BACKUP_CHAT_MODEL",
    "DEFAULT_EMBEDDING_MODEL",
    "BACKUP_EMBEDDING_MODEL",
    "resolve_model_alias",
]
