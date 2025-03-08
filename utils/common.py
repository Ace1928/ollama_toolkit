#!/usr/bin/env python3
"""
Common utilities for Ollama Toolkit examples and client.
"""

import asyncio
import json
import logging
import platform
import subprocess
import time
from typing import Any, Dict, Optional, Tuple, TypeVar, cast

import aiohttp
import requests
from colorama import Fore, Style

from exceptions import (
    ConnectionError,
    InvalidRequestError,
    ModelNotFoundError,
    OllamaAPIError,
    ServerError,
    TimeoutError,
)

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
    """
    Print a formatted header for the example.

    Args:
        title: The title to display
    """
    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


def print_success(message: str) -> None:
    """
    Print a success message.

    Args:
        message: The message to display
    """
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """
    Print an error message.

    Args:
        message: The message to display
    """
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message: str) -> None:
    """
    Print a warning message.

    Args:
        message: The message to display
    """
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """
    Print an information message.

    Args:
        message: The message to display
    """
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def print_json(data: Any) -> None:
    """
    Print formatted JSON data.

    Args:
        data: The data to display as JSON
    """
    print(json.dumps(data, indent=2))


def make_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    timeout: int = 300,  # Changed from 60 to 300 seconds
) -> Optional[requests.Response]:
    """
    Make an API request to the Ollama Toolkit with enhanced anti-hanging protection.

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        data: Optional request data
        base_url: Base URL for the API
        timeout: Request timeout in seconds

    Returns:
        Response object or None if request failed
    """
    url = f"{base_url.rstrip('/')}{endpoint}"

    try:
        logger.debug(f"Making {method} request to {url}")
        if data:
            logger.debug(f"Request data: {json.dumps(data)}")

        # Use a session for better timeout control
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(
            max_retries=1  # Minimal retries
        ))
        
        # Use separate connect and read timeouts
        connect_timeout = min(30, timeout/10)  # Connect timeout (max 30s, was 5s)
        read_timeout = timeout - connect_timeout  # Remaining time for reading
        
        response = session.request(
            method=method, 
            url=url, 
            json=data, 
            timeout=(connect_timeout, read_timeout)
        )
        response.raise_for_status()
        return response

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        print_error(f"Connection error: Could not connect to Ollama Toolkit at {base_url}")
        print_info("Make sure Ollama is running and accessible.")
        raise ConnectionError(f"Failed to connect to {base_url}: {str(e)}")

    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error: {str(e)}")
        print_error(
            f"Timeout error: Request to {url} timed out after {timeout} seconds"
        )
        raise TimeoutError(f"Request timed out: {str(e)}")

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        logger.error(f"HTTP error {status_code}: {str(e)}")

        try:
            error_data = e.response.json()
            error_message = error_data.get("error", str(e))
        except json.JSONDecodeError:
            error_message = e.response.text or str(e)

        if status_code == 404 and "model not found" in error_message.lower():
            print_error(f"Model not found: {error_message}")
            raise ModelNotFoundError(error_message)
        elif 400 <= status_code < 500:
            print_error(f"Invalid request: {error_message}")
            raise InvalidRequestError(error_message)
        elif 500 <= status_code < 600:
            print_error(f"Server error: {error_message}")
            raise ServerError(error_message)
        else:
            print_error(f"HTTP error {status_code}: {error_message}")
            raise OllamaAPIError(f"HTTP error {status_code}: {error_message}")

    except Exception as e:
        logger.error(f"Error making API request: {str(e)}")
        print_error(f"Error: {str(e)}")
        raise OllamaAPIError(f"Failed to make API request: {str(e)}")


async def async_make_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    timeout: int = 300,  # Changed from 60 to 300 seconds
) -> Dict[str, Any]:
    """
    Asynchronously make an API request to the Ollama Toolkit

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        data: Optional request data
        base_url: Base URL for the API
        timeout: Request timeout in seconds

    Returns:
        JSON response data
    """
    url = f"{base_url.rstrip('/')}{endpoint}"

    try:
        logger.debug(f"Making async {method} request to {url}")
        if data:
            logger.debug(f"Request data: {json.dumps(data)}")

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as response:
                if response.status >= 400:
                    try:
                        error_data = await response.json()
                        error_message = error_data.get(
                            "error", f"HTTP error {response.status}"
                        )
                    except (json.JSONDecodeError, aiohttp.ContentTypeError):
                        error_message = await response.text()

                    if (
                        response.status == 404
                        and "model not found" in error_message.lower()
                    ):
                        raise ModelNotFoundError(error_message)
                    elif 400 <= response.status < 500:
                        raise InvalidRequestError(error_message)
                    elif 500 <= response.status < 600:
                        raise ServerError(error_message)
                    else:
                        raise OllamaAPIError(
                            f"HTTP error {response.status}: {error_message}"
                        )

                result = await response.json()
                return cast(Dict[str, Any], result)

    except aiohttp.ClientConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        raise ConnectionError(f"Failed to connect to {base_url}: {str(e)}")

    except asyncio.TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        raise TimeoutError(f"Request timed out after {timeout} seconds")

    except (aiohttp.ClientError, json.JSONDecodeError) as e:
        logger.error(f"Error in async request: {str(e)}")
        raise OllamaAPIError(f"Failed to make async API request: {str(e)}")


def check_ollama_installed() -> Tuple[bool, str]:
    """
    Check if Ollama is installed on the system.

    Returns:
        Tuple of (is_installed, version_or_error_message)
    """
    try:
        # Check if ollama command exists
        if platform.system() == "Windows":
            result = subprocess.run(
                ["where", "ollama"], capture_output=True, text=True, check=False
            )
            is_installed = result.returncode == 0
        else:
            result = subprocess.run(
                ["which", "ollama"], capture_output=True, text=True, check=False
            )
            is_installed = result.returncode == 0

        if is_installed:
            # Get version
            version_result = subprocess.run(
                ["ollama", "--version"], capture_output=True, text=True, check=False
            )
            if version_result.returncode == 0:
                return True, version_result.stdout.strip()
            else:
                return True, "Unknown version"
        else:
            return False, "Ollama not found in PATH"

    except Exception as e:
        return False, str(e)


def check_ollama_running() -> Tuple[bool, str]:
    """
    Check if the Ollama server is running.
    
    Returns:
        Tuple of (is_running, message)
    """
    try:
        # Try to get the Ollama version
        cmd = ["ollama", "version"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, f"Ollama server is running (version: {version})"
        else:
            return False, "Ollama server is not running"
    except Exception as e:
        return False, f"Failed to check Ollama status: {str(e)}"


def install_ollama() -> Tuple[bool, str]:
    """
    Attempt to install Ollama on the system.

    Returns:
        Tuple of (success, message)
    """
    system = platform.system().lower()

    try:
        if system == "linux":
            # Install on Linux
            print_info("Installing Ollama on Linux...")
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
                shell=True,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, "Ollama installed successfully"
            else:
                return False, f"Installation failed: {result.stderr}"

        elif system == "darwin":  # macOS
            # Install on macOS
            print_info("Installing Ollama on macOS...")
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
                shell=True,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, "Ollama installed successfully"
            else:
                return False, f"Installation failed: {result.stderr}"

        elif system == "windows":
            print_info(
                "For Windows, please download Ollama from https://ollama.com/download/windows"
            )
            return False, "Automatic installation not supported on Windows"

        else:
            return False, f"Unsupported operating system: {system}"

    except Exception as e:
        return False, f"Error during installation: {str(e)}"


def ensure_ollama_running() -> Tuple[bool, str]:
    """
    Ensure Ollama is installed and running. Attempts to start if installed but not running.

    Returns:
        Tuple of (is_running, message)
    """
    # First check if it's already running
    is_running, message = check_ollama_running()
    if is_running:
        return True, message

    # Check if it's installed
    is_installed, install_message = check_ollama_installed()
    if not is_installed:
        print_warning("Ollama is not installed. Attempting to install...")
        is_installed, install_message = install_ollama()
        if not is_installed:
            print_error(f"Failed to install Ollama: {install_message}")
            print_info(
                "Please install Ollama manually from https://ollama.com/download"
            )
            return False, "Ollama not installed"

    # Try to start the Ollama service
    try:
        print_info("Attempting to start Ollama service...")
        if platform.system() == "Windows":
            # Start process detached on Windows
            # Define Windows-specific constants
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200

            subprocess.Popen(
                ["ollama", "serve"],
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
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
        max_attempts = 5
        for attempt in range(max_attempts):
            print_info(
                f"Waiting for Ollama to start (attempt {attempt+1}/{max_attempts})..."
            )
            time.sleep(2)  # Wait 2 seconds between checks
            is_running, message = check_ollama_running()
            if is_running:
                print_success(f"Ollama is running: {message}")
                return True, message

        return False, "Ollama failed to start after multiple attempts"

    except Exception as e:
        return False, f"Error starting Ollama: {str(e)}"


def format_traceback(e: Exception) -> str:
    """
    Format an exception traceback for logging or display.
    
    Args:
        e: The exception to format
        
    Returns:
        Formatted traceback string
    """
    import traceback
    from io import StringIO
    
    tb_io = StringIO()
    traceback.print_exception(type(e), e, e.__traceback__, file=tb_io)
    return tb_io.getvalue()
