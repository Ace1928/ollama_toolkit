#!/usr/bin/env python3
"""
Main entry point for running the Ollama Toolkit as a module.

This allows running the toolkit with 'python -m ollama_toolkit'
"""

import sys

def main():
    """Entry point for the module."""
    print("Ollama Toolkit")
    print("Available commands:")
    print("  python -m ollama_toolkit.quickstart - Run the interactive quickstart wizard")

if __name__ == "__main__":
    main()
