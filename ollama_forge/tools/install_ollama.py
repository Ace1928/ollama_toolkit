#!/usr/bin/env python3
"""
Tool for checking, installing, and managing the Ollama backend.
"""

import argparse
import os
import platform
import subprocess
import sys
import time
import logging
from typing import Tuple

# Add parent directory to path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from ollama_forge.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        check_ollama_installed,
        check_ollama_running,
        ensure_ollama_running,
        print_error,
        print_header,
        print_info,
        print_success,
        print_warning,
    )
except ImportError:
    # When run directly or in development
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.common import (
        DEFAULT_OLLAMA_API_URL,
        check_ollama_installed,
        check_ollama_running,
        ensure_ollama_running,
        print_error,
        print_header,
        print_info,
        print_success,
        print_warning,
    )

def run_ollama() -> bool:
    """
    Start the Ollama service if it is not already running.

    Returns:
        bool: True if the Ollama server was successfully started or
              is already running, otherwise False.
    """
    print_header("Starting Ollama Server")

    # First check if already running
    is_running, message = check_ollama_running()
    if is_running:
        print_success(f"Ollama server is already running: {message}")
        return True

    # Check if installed
    is_installed, install_message = check_ollama_installed()
    if not is_installed:
        print_error(f"Ollama is not installed: {install_message}")
        print_info(
            "Install Ollama first with: python -m ollama_forge.tools.install_ollama --install"
        )
        return False

    # Start the server
    print_info("Starting Ollama server...")
    try:
        if platform.system() == "Windows":
            # Start process detached on Windows
            subprocess.Popen(
                ["ollama", "serve"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                shell=True,
            )
        else:
            # Start process in background on Unix-like systems
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

        # Wait for service to start
        for i in range(5):
            print_info(f"Waiting for server to start ({i+1}/5)...")
            time.sleep(2)
            is_running, message = check_ollama_running()
            if is_running:
                print_success(f"Ollama server started successfully: {message}")
                print_info(f"API available at: {DEFAULT_OLLAMA_API_URL}")
                return True

        print_error("Ollama server didn't start within the timeout period")
        return False

    except Exception as e:
        print_error(f"Error starting Ollama server: {e}")
        return False


def stop_ollama() -> bool:
    """Stop the Ollama service."""
    print_header("Stopping Ollama Server")

    # Check if running
    is_running, _ = check_ollama_running()
    if not is_running:
        print_info("Ollama server is not running")
        return True

    try:
        if platform.system() == "Windows":
            # Windows process management
            subprocess.run(
                ["taskkill", "/F", "/IM", "ollama.exe"],
                check=False,
                capture_output=True,
            )
        else:
            # Unix-like systems
            subprocess.run(
                ["pkill", "-f", "ollama serve"], check=False, capture_output=True
            )

        # Verify it's stopped
        time.sleep(2)
        is_running, _ = check_ollama_running()
        if not is_running:
            print_success("Ollama server stopped successfully")
            return True
        else:
            print_error("Failed to stop Ollama server")
            return False

    except Exception as e:
        print_error(f"Error stopping Ollama server: {e}")
        return False


def install_ollama() -> Tuple[bool, str]:
    """
    Install Ollama on the system.

    Returns:
        Tuple[bool, str]: A tuple containing:
          - A boolean indicating if the installation was successful
          - A message describing the result
    """
    system = platform.system().lower()

    try:
        if system == "linux":
            print_info("Installing Ollama on Linux...")
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "bash"],
                shell=True,
                check=False,
            )

            if result.returncode == 0:
                return True, "Ollama installed successfully"
            else:
                return False, f"Installation failed with exit code {result.returncode}"

        elif system == "darwin":  # macOS
            print_info("Installing Ollama on macOS...")
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "bash"],
                shell=True,
                check=False,
            )

            if result.returncode == 0:
                return True, "Ollama installed successfully"
            else:
                return False, f"Installation failed with exit code {result.returncode}"

        elif system == "windows":
            print_info(
                "For Windows, please download Ollama from https://ollama.com/download/windows"
            )
            return False, "Automatic installation not supported on Windows"

        else:
            return False, f"Unsupported operating system: {system}"

    except Exception as e:
        return False, f"Error during installation: {str(e)}"


def main() -> None:
    """Main entry point for Ollama installation and management."""
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Ollama installation and management tool"
    )

    # Add arguments
    parser.add_argument(
        "--check", action="store_true", help="Check if Ollama is installed and running"
    )
    parser.add_argument("--install", action="store_true", help="Install Ollama")
    parser.add_argument("--start", action="store_true", help="Start Ollama server")
    parser.add_argument("--stop", action="store_true", help="Stop Ollama server")
    parser.add_argument("--restart", action="store_true", help="Restart Ollama server")
    parser.add_argument("--version", action="store_true", help="Get Ollama version")

    args = parser.parse_args()

    # If no arguments provided, show status
    if len(sys.argv) == 1:
        args.check = True

    if args.check:
        print_header("Ollama Status Check")
        logging.info("Checking Ollama status...")

        # Check if installed
        is_installed, install_message = check_ollama_installed()
        if is_installed:
            print_success(f"Ollama is installed: {install_message}")
        else:
            print_error(f"Ollama is not installed: {install_message}")
            print_info(
                "To install Ollama, run: python -m ollama_forge.tools.install_ollama --install"
            )
            print_info("Or visit https://ollama.com/download")
            return

        # Check if running
        is_running, run_message = check_ollama_running()
        if is_running:
            print_success(f"Ollama server is running: {run_message}")
            print_info(f"API available at: {DEFAULT_OLLAMA_API_URL}")
        else:
            print_warning(f"Ollama server is not running: {run_message}")
            print_info(
                "To start Ollama server, run: python -m ollama_forge.tools.install_ollama --start"
            )

    elif args.install:
        print_header("Installing Ollama")
        success, message = install_ollama()
        if success:
            print_success(f"Ollama installed successfully: {message}")
            # Try to start it
            print_info("Starting Ollama server...")
            run_ollama()
        else:
            print_error(f"Failed to install Ollama: {message}")
            print_info(
                "You can download Ollama manually from https://ollama.com/download"
            )

    elif args.start:
        run_ollama()

    elif args.stop:
        stop_ollama()

    elif args.restart:
        print_header("Restarting Ollama Server")
        if stop_ollama():
            time.sleep(2)  # Give it time to fully stop
            run_ollama()

    elif args.version:
        print_header("Ollama Version")
        is_installed, install_message = check_ollama_installed()
        if is_installed:
            print_success(f"Ollama version: {install_message}")
        else:
            print_error("Ollama is not installed")


if __name__ == "__main__":
    main()
