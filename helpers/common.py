#!/usr/bin/env python3
"""
Common utilities for Ollama Toolkit examples and client.
"""
from typing import Any, Dict, Optional, Tuple, TypeVar, cast
import os
import sys
import json
import logging
import platform
import subprocess
import requests
import asyncio
import aiohttp
from colorama import Fore, Style

try:
    import numpy as np
except ImportError:
    np = None

# Configure logger
logger = logging.getLogger(__name__)

# Default Ollama Toolkit URL
DEFAULT_OLLAMA_API_URL = "http://localhost:11434/"

# Default model to use across the package
DEFAULT_MODEL = "deepseek-r1:1.5b"
ALTERNATIVE_MODEL = "qwen2.5:0.5b"

# Type variable for generic return types
T = TypeVar("T")


def print_header(title: str) -> None:
    """Print a formatted header with the given title."""
    print(f"\n{Fore.CYAN}=== {title} ==={Style.RESET_ALL}\n")


def print_success(message: str) -> None:
    """Print a success message with a green checkmark."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message with a red X."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message: str) -> None:
    """Print a warning message with a yellow warning symbol."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print an informational message with a blue info symbol."""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def print_json(data: Any) -> None:
    """Print JSON data in a formatted, readable way."""
    print(json.dumps(data, indent=2, default=str))


def make_api_request(
    method: str, 
    endpoint: str, 
    data: Optional[Dict[str, Any]] = None, 
    base_url: str = DEFAULT_OLLAMA_API_URL, 
    timeout: int = 60
) -> Any:
    """
    Make a request to the Ollama API with elegant error handling.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint to call
        data: JSON data to send (for POST, PUT, etc.)
        base_url: Base URL for the API
        timeout: Request timeout in seconds
        
    Returns:
        Parsed JSON response or raw response object
    """
    url = f"{base_url.rstrip('/')}{endpoint}"
    session = requests.Session()
    
    try:
        headers = {"Content-Type": "application/json"}
        response = session.request(
            method=method,
            url=url,
            json=data if data else None,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Transform into a structured error response
        error_data = {
            "error": error_type,
            "message": error_msg,
            "url": url,
            "method": method
        }
        
        # For timeouts, add specific error data
        if isinstance(e, requests.exceptions.Timeout):
            error_data["timeout"] = timeout
            error_data["suggestion"] = "Consider increasing the timeout value"
            
        logger.debug(f"Structured error: {error_data}")
        return error_data


async def async_make_api_request(
    method: str, 
    endpoint: str, 
    data: Optional[Dict[str, Any]] = None, 
    base_url: str = DEFAULT_OLLAMA_API_URL, 
    timeout: int = 60
) -> Any:
    """
    Make an asynchronous request to the Ollama API.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint to call
        data: JSON data to send
        base_url: Base URL for the API
        timeout: Request timeout in seconds
        
    Returns:
        Parsed JSON response or raw response object
    """
    url = f"{base_url.rstrip('/')}{endpoint}"
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    
    try:
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            async with session.request(
                method=method,
                url=url,
                json=data if data else None,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    error_data = {
                        "error": f"HTTP {response.status}",
                        "message": error_text,
                        "url": url,
                        "method": method
                    }
                    return error_data
                    
                try:
                    return await response.json()
                except ValueError:
                    return response
    except aiohttp.ClientError as e:
        logger.error(f"Async API request failed: {e}")
        error_data = {
            "error": type(e).__name__,
            "message": str(e),
            "url": url,
            "method": method
        }
        return error_data


def check_ollama_installed() -> bool:
    """
    Check if Ollama is installed on the system.
    
    Returns:
        True if installed, False otherwise
    """
    system = platform.system().lower()
    
    try:
        if system == "windows":
            # Check for Ollama in Program Files or AppData
            paths = [
                os.path.expandvars(r'%ProgramFiles%\Ollama'),
                os.path.expandvars(r'%LOCALAPPDATA%\Ollama')
            ]
            return any(os.path.exists(path) for path in paths)
        else:
            # For Unix-based systems, check binary in PATH
            result = subprocess.run(
                ["which", "ollama"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0
    except Exception as e:
        logger.warning(f"Error checking Ollama installation: {e}")
        return False


def check_ollama_running() -> Tuple[bool, str]:
    """
    Check if the Ollama server is running.
    
    Returns:
        Tuple of (is_running, message)
    """
    try:
        response = requests.get(
            f"{DEFAULT_OLLAMA_API_URL.rstrip('/')}/api/version",
            timeout=2.0
        )
        if response.status_code == 200:
            version_info = response.json()
            version = version_info.get("version", "unknown")
            return True, f"Ollama server is running (version {version})"
        return False, f"Ollama server returned status code {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to Ollama server"
    except requests.exceptions.Timeout:
        return False, "Connection to Ollama server timed out"
    except Exception as e:
        return False, f"Error checking Ollama server: {str(e)}"


def install_ollama(target_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Install Ollama on the system if not already installed.
    
    Args:
        target_dir: Optional directory to install Ollama into
        
    Returns:
        Tuple of (success, message)
    """
    system = platform.system().lower()
    
    if check_ollama_installed():
        return True, "Ollama is already installed"
    
    try:
        if system == "linux":
            # Use the official install script for Linux
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True, "Successfully installed Ollama"
            
        elif system == "darwin":  # macOS
            # Use the official install script for macOS
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True, "Successfully installed Ollama"
            
        elif system == "windows":
            # Windows installation requires manual steps or a more complex approach
            return False, "Windows installation must be done manually from https://ollama.com/download"
        
        else:
            return False, f"Unsupported platform: {system}"
            
    except subprocess.CalledProcessError as e:
        return False, f"Installation failed: {e.stderr}"
    except Exception as e:
        return False, f"Installation failed: {str(e)}"


def ensure_ollama_running() -> Tuple[bool, str]:
    """
    Ensure that Ollama is installed and running.
    Attempts to install if not found and start the service if not running.
    
    Returns:
        Tuple of (is_ready, message)
    """
    # First check if already running
    is_running, message = check_ollama_running()
    if is_running:
        return True, "Ollama is ready"
    
    # If not running, check if installed
    if not check_ollama_installed():
        # Try to install Ollama
        success, install_message = install_ollama()
        if not success:
            return False, f"Ollama not installed and installation failed: {install_message}"
    
    # Try to start Ollama
    system = platform.system().lower()
    try:
        if system in ("linux", "darwin"):
            # Start the Ollama service
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            # Wait for it to be ready
            for _ in range(5):  # Try 5 times
                is_running, msg = check_ollama_running()
                if is_running:
                    return True, "Ollama started successfully"
                # Wait a bit before checking again
                import time
                time.sleep(2)
                
            return False, "Started Ollama but service did not become ready"
            
        elif system == "windows":
            return False, "Starting Ollama on Windows must be done manually"
        
    except Exception as e:
        return False, f"Error starting Ollama: {str(e)}"
    
    return False, "Could not ensure Ollama is running"
