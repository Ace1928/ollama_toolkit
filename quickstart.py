#!/usr/bin/env python3
"""
Ollama Toolkit Quickstart

This module provides an entry point to launch the quickstart wizard.
"""

import sys
import os

def main():
    """Entry point for the quickstart command."""
    try:
        # Try importing from the installed package
        from ollama_toolkit.examples.quickstart import main as quickstart_main
        return quickstart_main()
    except ImportError:
        # If not installed, try direct import by adding parent directory to path
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        try:
            from ollama_toolkit.examples.quickstart import main as quickstart_main
            return quickstart_main()
        except ImportError as e:
            print(f"Error: {e}")
            print("Cannot import the quickstart module. Make sure the package is correctly installed.")
            print("Try reinstalling with: pip install -e .")
            sys.exit(1)

if __name__ == "__main__":
    main()
