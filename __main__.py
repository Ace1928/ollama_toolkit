#!/usr/bin/env python3
"""
Main entry point for running the Ollama Toolkit as a module.

This allows running the toolkit with 'python -m ollama_toolkit'
"""

import sys
from .cli import main as cli_main

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

if __name__ == "__main__":
    # If arguments are provided, pass them to the CLI
    if len(sys.argv) > 1:
        sys.exit(cli_main())
    else:
        # Otherwise show the help menu
        main()
