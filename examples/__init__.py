"""
Example scripts for using the ollama_toolkit package.
"""

# Import the main function from quickstart so it can be called directly
try:
    from .quickstart import main as quickstart_main
    __all__ = ["quickstart_main"]
except ImportError:
    # If it fails, don't crash on import
    __all__ = []
