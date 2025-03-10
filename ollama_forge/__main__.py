#!/usr/bin/env python3
"""
Main entry point for running the Ollama Forge as a module.

This allows running the toolkit with 'python -m ollama_forge'
"""

import sys
import os
import shutil
import importlib.util
from typing import Callable, Optional, Union, cast

# Type definitions to help with type checking
CliMainType = Callable[[], Optional[int]]
QuickstartMainType = Callable[[], Optional[int]]

def supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    return sys.stdout.isatty() and os.name != 'nt' or (os.name == 'nt' and shutil.which("tput") is not None)

def import_module(module_path: str) -> Optional[Callable]:
    """Safely import a module and return the main function."""
    try:
        module_spec = importlib.util.find_spec(module_path)
        if module_spec is None:
            print(f"Could not find module: {module_path}")
            return None
            
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            return module.main
        else:
            print(f"Module {module_path} does not have a main function")
            return None
    except Exception as e:
        print(f"Error importing {module_path}: {e}")
        return None

def main() -> None:
    """Entry point for the module."""
    if supports_color():
        print("\033[1;36m╔══════════════════════════════════╗\033[0m")
        print("\033[1;36m║        \033[1;33mOllama Forge\033[1;36m          ║\033[0m")
        print("\033[1;36m╚══════════════════════════════════╝\033[0m\n")
    else:
        print("Ollama Forge\n")
    
    print("Available commands:")
    print("• python -m ollama_forge.cli - Use the command-line interface")
    print("• python -m ollama_forge.examples.quickstart - Run the interactive quickstart")
    print("• python -m ollama_forge.tools.install_ollama - Install/manage Ollama\n")
    print("Full documentation: https://github.com/Ace1928/ollama_forge")

# Handle execution
if __name__ == "__main__":
    # If arguments are provided, pass them to the CLI
    if len(sys.argv) > 1:
        cli_main = import_module("ollama_forge.cli")
        if cli_main:
            exit_code = cli_main() or 0  # Default to 0 if None is returned
            sys.exit(exit_code)
        else:
            sys.exit(1)
    else:
        # Launch the quickstart by default
        quickstart_main = import_module("ollama_forge.examples.quickstart")
        if quickstart_main:
            exit_code = quickstart_main() or 0  # Default to 0 if None is returned
            sys.exit(exit_code)
        else:
            # If quickstart fails to import, show help and exit
            main()
            sys.exit(1)
