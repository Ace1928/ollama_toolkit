"""
Model constants used throughout the Ollama Toolkit client.
"""

from typing import Dict, List, Optional

# Default models that should be available in the Ollama Toolkit
DEFAULT_CHAT_MODEL = "llama2"
BACKUP_CHAT_MODEL = "qwen2.5:0.5b"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
BACKUP_EMBEDDING_MODEL = "mxbai-embed-large"

# Common model aliases for easier usage
MODEL_ALIASES: Dict[str, str] = {
    # Chat model aliases
    "llama": "llama2",
    "gpt": "llama2",
    "gemma": "gemma:2b",
    "qwen": "qwen2.5:0.5b",
    "qwen2": "qwen2.5:0.5b",
    "mistral": "mistral",
    "deepseek": "deepseek-r1:1.5b",
    # Embedding model aliases
    "embed": "nomic-embed-text",
    "embedding": "nomic-embed-text",
}

# Lists for user selection
CHAT_MODELS: List[str] = [DEFAULT_CHAT_MODEL, BACKUP_CHAT_MODEL, "mistral", "gemma:2b"]
EMBEDDING_MODELS: List[str] = [DEFAULT_EMBEDDING_MODEL, BACKUP_EMBEDDING_MODEL]


def resolve_model_alias(model_name: str) -> str:
    """
    Resolve model name aliases to their actual names.
    
    Args:
        model_name: The model name or alias
        
    Returns:
        The resolved model name
    """
    return MODEL_ALIASES.get(model_name.lower(), model_name)


def get_fallback_model(model_name: str) -> Optional[str]:
    """
    Get a fallback model for the specified model.
    
    Args:
        model_name: The model name that needs a fallback
        
    Returns:
        A suitable fallback model name, or None if no fallback is defined
    """
    # General fallback strategy based on model type
    if model_name == DEFAULT_CHAT_MODEL:
        return BACKUP_CHAT_MODEL
    elif model_name == DEFAULT_EMBEDDING_MODEL:
        return BACKUP_EMBEDDING_MODEL
    
    # More specific fallbacks based on model family
    if "llama" in model_name.lower():
        return BACKUP_CHAT_MODEL
    elif "embed" in model_name.lower():
        return BACKUP_EMBEDDING_MODEL
    
    # Default fallbacks if we can't determine model type
    return BACKUP_CHAT_MODEL
