#!/usr/bin/env python3
"""
Ollama Toolkit: Generate Example

This script demonstrates how to use the Ollama Generate API to create completions.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Optional, Tuple

import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init()

# Try to import as a package first, then try relative imports
try:
    from ollama_toolkit.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error,
        print_header,
        print_info,
        print_success,
    )
    from ollama_toolkit.utils.model_constants import (
        BACKUP_CHAT_MODEL,
        DEFAULT_CHAT_MODEL,
    )
except ImportError:
    # Add parent directory to path for direct execution
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    )
    try:
        from ollama_toolkit.utils.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error,
            print_header,
            print_info,
            print_success,
        )
        from ollama_toolkit.utils.model_constants import (
            BACKUP_CHAT_MODEL,
            DEFAULT_CHAT_MODEL,
        )
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install the package using: pip install -e /path/to/ollama_toolkit")
        sys.exit(1)


def generate_streaming(
    model: str,
    prompt: str,
    options: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    use_fallback: bool = True,
) -> Tuple[bool, str]:
    """
    Generate a completion with streaming responses

    Args:
        model: The model name
        prompt: The prompt to generate a response for
        options: Additional model parameters
        base_url: The base URL for the Ollama Toolkit
        use_fallback: Whether to try the backup model if primary fails

    Returns:
        A tuple of (success, generated_text)
    """
    print_header(f"Generating completion with {model} (Streaming)")
    print_info(f"Prompt: {prompt}\n")

    data: Dict[str, Any] = {"model": model, "prompt": prompt, "stream": True}

    if options:
        data.update(options)

    start_time = time.time()

    try:
        # Stream the response
        print_info(f"Sending generation request to {base_url}/api/generate")
        response = requests.post(f"{base_url}/api/generate", json=data, stream=True)
        response.raise_for_status()

        full_response = ""

        # Display progress bar
        print(f"{Fore.CYAN}Response: {Style.RESET_ALL}", end="")
        sys.stdout.flush()

        # Process the streaming response
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    print(f"{chunk['response']}", end="")
                    sys.stdout.flush()
                    full_response += chunk["response"]

                if chunk.get("done", False):
                    # Print statistics
                    print("\n")
                    if "total_duration" in chunk:
                        print_info(
                            f"Total duration: {chunk['total_duration'] / 1_000_000_000:.2f} seconds"
                        )
                    if "eval_count" in chunk:
                        print_info(f"Generated tokens: {chunk['eval_count']}")

        elapsed_time = time.time() - start_time
        print("\n")
        print_info(f"Client-side total time: {elapsed_time:.2f} seconds")
        print_success("Generation completed!")
        return True, full_response

    except requests.exceptions.RequestException as e:
        print_error(f"Request error with model {model}: {str(e)}")

        # Try fallback model if enabled and not already using it
        if use_fallback and model != BACKUP_CHAT_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_CHAT_MODEL}")
            return generate_streaming(
                BACKUP_CHAT_MODEL, prompt, options, base_url, use_fallback=False
            )
        return False, ""


def generate_non_streaming(
    model: str,
    prompt: str,
    options: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    use_fallback: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Generate a completion without streaming (single response)

    Args:
        model: The model name
        prompt: The prompt to generate a response for
        options: Additional model parameters
        base_url: The base URL for the Ollama Toolkit
        use_fallback: Whether to try the backup model if primary fails

    Returns:
        The response from the API as a dictionary, or None if the request failed
    """
    print_header(f"Generating completion with {model} (Non-streaming)")
    print_info(f"Prompt: {prompt}\n")

    data: Dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}

    if options:
        data.update(options)

    start_time = time.time()

    try:
        # Send the request
        print_info(f"Sending generation request to {base_url}/api/generate")
        response = requests.post(f"{base_url}/api/generate", json=data)
        response.raise_for_status()

        # Process the response
        result = response.json()

        elapsed_time = time.time() - start_time

        print(f"{Fore.CYAN}Response:{Style.RESET_ALL}\n{result['response']}\n")

        # Print statistics
        if "total_duration" in result:
            print_info(
                f"Total duration: {result['total_duration'] / 1_000_000_000:.2f} seconds"
            )
        if "eval_count" in result:
            print_info(f"Generated tokens: {result['eval_count']}")

        print_info(f"Client-side total time: {elapsed_time:.2f} seconds")
        print_success("Generation completed!")
        return result

    except requests.exceptions.RequestException as e:
        print_error(f"Request error with model {model}: {str(e)}")

        # Try fallback model if enabled and not already using it
        if use_fallback and model != BACKUP_CHAT_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_CHAT_MODEL}")
            return generate_non_streaming(
                BACKUP_CHAT_MODEL, prompt, options, base_url, use_fallback=False
            )
        return None


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ollama Generate API Example")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_CHAT_MODEL,
        help=f"Model name (default: {DEFAULT_CHAT_MODEL}, backup: {BACKUP_CHAT_MODEL})",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Why is the sky blue?",
        help="Prompt for generation",
    )
    parser.add_argument("--stream", action="store_true", help="Use streaming mode")
    parser.add_argument(
        "--temperature", type=float, default=0.7, help="Temperature parameter"
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable automatic fallback to backup model",
    )
    args = parser.parse_args()

    # Set options
    options = {"temperature": args.temperature}

    # Run the example
    if args.stream:
        generate_streaming(
            args.model, args.prompt, options, use_fallback=not args.no_fallback
        )
    else:
        generate_non_streaming(
            args.model, args.prompt, options, use_fallback=not args.no_fallback
        )


if __name__ == "__main__":
    main()
