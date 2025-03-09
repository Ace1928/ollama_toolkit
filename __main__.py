#!/usr/bin/env python3
"""
Main entry point for running the Ollama Toolkit as a module.

This allows running the toolkit with 'python -m ollama_toolkit'
"""

import sys
import os
from typing import Callable, Optional, Union, cast

# Type definitions to help with type checking
CliMainType = Callable[[], Optional[int]]
QuickstartMainType = Callable[[], Optional[int]]

# Handle different execution contexts
if __name__ == "__main__":
    # Direct execution - add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        # Now import the CLI module using absolute import
        from ollama_toolkit.cli import main as cli_main
        from ollama_toolkit.examples.quickstart import main as quickstart_main
        # Cast to help with type checking
        cli_main = cast(CliMainType, cli_main)
        quickstart_main = cast(QuickstartMainType, quickstart_main)
    except ImportError as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)
else:
    # Module execution path
    try:
        # Try relative imports first
        from .cli import main as cli_main
        from .examples.quickstart import main as quickstart_main
        # Cast to help with type checking
        cli_main = cast(CliMainType, cli_main)
        quickstart_main = cast(QuickstartMainType, quickstart_main)
    except ImportError:
        try:
            # Fall back to absolute imports if relative imports fail
            # This helps in certain execution contexts
            from ollama_toolkit.cli import main as cli_main
            from ollama_toolkit.examples.quickstart import main as quickstart_main
            # Cast to help with type checking
            cli_main = cast(CliMainType, cli_main)
            quickstart_main = cast(QuickstartMainType, quickstart_main)
        except ImportError as e:
            print(f"Error importing modules: {e}")
            sys.exit(1)

def main() -> None:
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
        exit_code = cli_main() or 0  # Default to 0 if None is returned
        sys.exit(exit_code)
    else:
        # Launch the quickstart by default
        exit_code = quickstart_main() or 0  # Default to 0 if None is returned
        sys.exit(exit_code)
