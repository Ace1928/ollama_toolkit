"""
Example scripts for using the ollama_toolkit package.

This module contains ready-to-run examples demonstrating the features
and capabilities of the Ollama Toolkit.
"""

# Import the main functions from example scripts for direct access
try:
    from .quickstart import main as quickstart_main
    from .basic_usage import main as basic_usage_main
    from .chat_example import main as chat_example_main
    from .embedding_example import main as embedding_example_main
    from .generate_example import main as generate_example_main
    from .version_example import main as version_example_main
    
    # Import the modules themselves for namespace access
    from . import quickstart
    from . import basic_usage
    from . import chat_example
    from . import embedding_example
    from . import generate_example
    from . import version_example
    
    __all__ = [
        # Main entry points
        "quickstart_main",
        "basic_usage_main",
        "chat_example_main",
        "embedding_example_main", 
        "generate_example_main",
        "version_example_main",
        
        # Modules
        "quickstart",
        "basic_usage",
        "chat_example",
        "embedding_example",
        "generate_example",
        "version_example",
    ]
    
except ImportError as e:
    # Fail gracefully if some examples are missing
    import sys
    import logging
    logging.debug(f"Some example modules couldn't be imported: {e}")
    
    __all__ = []
