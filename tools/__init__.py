"""
Tools for working with Ollama.

This package provides command-line tools and utilities for installing,
managing, and interacting with Ollama.
"""

# Re-export the main entry point for the install tool
try:
    from .install_ollama import (
        main as install_ollama_main,
        install_ollama,
        run_ollama,
        stop_ollama,
        check_ollama_installed,
        check_ollama_running,
    )
    
    # Make submodules directly importable
    from . import install_ollama
    
    __all__ = [
        # Main functions
        "install_ollama_main",
        "install_ollama",
        "run_ollama", 
        "stop_ollama",
        "check_ollama_installed",
        "check_ollama_running",
        
        # Submodules
        "install_ollama",
    ]
except ImportError as e:
    import logging
    logging.debug(f"Failed to import tool modules: {e}")
    __all__ = []
