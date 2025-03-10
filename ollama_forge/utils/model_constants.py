"""
Model constants used throughout the Ollama Toolkit client.
"""

from typing import Dict, List

# Default models
DEFAULT_CHAT_MODEL = "deepseek-r1:1.5b"
BACKUP_CHAT_MODEL = "qwen2.5:0.5b-instruct"
DEFAULT_EMBEDDING_MODEL = "deepseek-r1:1.5b"
BACKUP_EMBEDDING_MODEL = "qwen2.5:0.5b-instruct"

# Aliases for convenience
MODEL_ALIASES: Dict[str, str] = {
    # Chat model aliases
    "llama": "llama2",
    "gpt": "llama2",
    "gemma": "gemma:2b",
    "qwen": "qwen2.5:0.5b-instruct",
    "qwen2": "qwen2.5:0.5b-instruct",
    "mistral": "mistral",
    "deepseek": "deepseek-r1:1.5b",
    # Embedding model aliases
    "embed": "nomic-embed-text",
    "embedding": "nomic-embed-text",
    # Additional convenience
    "chat": "deepseek-r1:1.5b",
}

# Lists for user selection
CHAT_MODELS: List[str] = [DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL, "mistral", "gemma:2b"]
EMBEDDING_MODELS: List[str] = [DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL]

def resolve_model_alias(alias: str) -> str:
    return MODEL_ALIASES.get(alias.lower(), alias)

def get_fallback_model(model_name: str) -> str:
    fallbacks = {
        DEFAULT_CHAT_MODEL: BACKUP_CHAT_MODEL,
        DEFAULT_EMBEDDING_MODEL: BACKUP_EMBEDDING_MODEL,
    }
    return fallbacks.get(model_name, BACKUP_CHAT_MODEL)
