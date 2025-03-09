#!/usr/bin/env python3
"""
Main entry point for running the Ollama Toolkit as a module.

This allows running the toolkit with 'python -m ollama_toolkit'
"""

import sys
import os

# Handle different execution contexts
if __name__ == "__main__":
    # Direct execution - add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Now import the CLI module using absolute import
    from ollama_toolkit.cli import main as cli_main
    from ollama_toolkit.examples.quickstart import main as quickstart_main
else:
    # Module execution - use relative imports
    from .cli import main as cli_main
    from .examples.quickstart import main as quickstart_main

def main():
    """Entry point for the module."""
    print("\033[1;36m╔══════════════════════════════════╗\033[0m")
    print("\033[1;36m║        \033[1;33mOllama Toolkit\033[1;36m          ║\033[0m")
    print("\033[1;36m╚══════════════════════════════════╝\033[0m\n")
    print("Available commands:")
    print("\033[1;32m• python -m ollama_toolkit.cli\033[0m - Use the command-line interface")
    print("\033[1;32m• python -m ollama_toolkit.examples.quickstart\033[0m - Run the interactive quickstart")
    print("\033[1;32m• python -m ollama_toolkit.tools.install_ollama\033[0m - Install/manage Ollama\n")
    print("Full documentation: \033[1;34mhttps://github.com/Ace1928/ollama_toolkit\033[0m")

# Handle execution
if __name__ == "__main__":
    # If arguments are provided, pass them to the CLI
    if len(sys.argv) > 1:
        sys.exit(cli_main())
    else:
        # Launch the quickstart by default
        sys.exit(quickstart_main())
