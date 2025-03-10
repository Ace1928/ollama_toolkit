#!/usr/bin/env python3
"""
Tool for setting up the Ollama Forge package for development or use.

This script:
1. Checks for proper Python environment
2. Installs the package in development mode
3. Runs basic sanity checks to ensure everything is working
"""

import os
import subprocess
import sys
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'=' * 80}\n{title.center(80)}\n{'=' * 80}")


def print_success(message):
    """Print a success message."""
    print(f"\033[92m✓ {message}\033[0m")


def print_error(message):
    """Print an error message."""
    print(f"\033[91m✗ {message}\033[0m")


def print_info(message):
    """Print an info message."""
    print(f"\033[94mi {message}\033[0m")


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    major, minor = sys.version_info[:2]
    print_info(f"Detected Python {major}.{minor}")
    
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Python 3.8+ is required, but you have {major}.{minor}")
        return False
    
    print_success(f"Python {major}.{minor} is compatible")
    return True


def install_package():
    """Install the package in development mode."""
    print_header("Installing Package")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print_success("Package installed successfully in development mode")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install package: {e}")
        return False


def run_sanity_check():
    """Run basic sanity checks to verify installation."""
    print_header("Running Sanity Checks")
    
    try:
        # Try importing the package
        import ollama_forge
        print_success(f"Successfully imported ollama_forge (version {ollama_forge.__version__})")
        
        # Check for key modules
        from ollama_forge import OllamaClient
        from ollama_forge.utils.model_constants import DEFAULT_CHAT_MODEL
        
        print_success("Key modules imported successfully")
        print_info(f"Default chat model: {DEFAULT_CHAT_MODEL}")
        
        return True
    except ImportError as e:
        print_error(f"Import error: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def main():
    """Main function."""
    print_header("Ollama Forge Setup")
    
    # Run checks and setup
    if not check_python_version():
        sys.exit(1)
    
    if not install_package():
        sys.exit(1)
    
    if not run_sanity_check():
        print_error("Sanity checks failed")
        sys.exit(1)
    
    print_header("Setup Complete")
    print_success("Ollama Forge is properly installed and ready to use")
    print_info("You can now run:")
    print("  python -m ollama_forge            # Interactive quickstart")
    print("  python -m ollama_forge.cli        # Command line interface")
    print("  python -m ollama_forge.examples   # Example scripts")


if __name__ == "__main__":
    main()
