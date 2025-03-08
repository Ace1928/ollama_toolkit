#!/usr/bin/env python3
"""
Example of using the Ollama Toolkit client for chat interactions.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Generator, List, Optional, Tuple, cast

import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init()

# Import strategy:
# 1. Try direct package import (works when installed or in PYTHONPATH)
# 2. Try relative import by adjusting path (works when run directly)
# 3. Provide clear error if both fail

# Store original path to restore later if needed
original_sys_path = sys.path.copy()
import_success = False

# Try package import first (when installed via pip or in development with -e)
try:
    from ollama_toolkit.utils.common import (
        DEFAULT_OLLAMA_API_URL,
        print_error,
        print_header,
        print_info,
        print_success,
        print_warning,
    )
    from ollama_toolkit.utils.model_constants import (
        BACKUP_CHAT_MODEL,
        DEFAULT_CHAT_MODEL,
    )
    import_success = True
    print_info("Imported modules from installed package")
except ImportError:
    # Reset path before trying the next approach
    sys.path = original_sys_path
    
    # Add parent directory to path for direct execution
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        from ollama_toolkit.utils.common import (
            DEFAULT_OLLAMA_API_URL,
            print_error,
            print_header,
            print_info,
            print_success,
            print_warning,
        )
        from ollama_toolkit.utils.model_constants import (
            BACKUP_CHAT_MODEL,
            DEFAULT_CHAT_MODEL,
        )
        import_success = True
        print_info(f"Imported modules using path adjustment to {parent_dir}")
    except ImportError as e:
        # Try one more approach - going up two directories
        sys.path = original_sys_path
        grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        if grandparent_dir not in sys.path:
            sys.path.insert(0, grandparent_dir)
        
        try:
            from ollama_toolkit.utils.common import (
                DEFAULT_OLLAMA_API_URL,
                print_error,
                print_header,
                print_info,
                print_success,
                print_warning,
            )
            from ollama_toolkit.utils.model_constants import (
                BACKUP_CHAT_MODEL,
                DEFAULT_CHAT_MODEL,
            )
            import_success = True
            print_info(f"Imported modules using path adjustment to {grandparent_dir}")
        except ImportError as e:
            print(f"Error importing required modules: {e}")
            print(f"Current sys.path: {sys.path}")
            print("Please install the package using: pip install -e /path/to/ollama_toolkit")
            sys.exit(1)

if not import_success:
    print("Failed to import required modules despite multiple attempts")
    sys.exit(1)

# Define message type for better type checking
Message = Dict[str, str]


def initialize_chat(model: str, system_message: Optional[str] = None) -> List[Message]:
    """
    Initialize a chat session with optional system message.
    
    Args:
        model: The model to use for chat
        system_message: Optional system message to set context
        
    Returns:
        List of initial messages
    """
    messages: List[Message] = []
    
    # Add system message if provided
    if system_message:
        messages.append({"role": "system", "content": system_message})
        
    return messages


def parse_json_stream(line: bytes) -> Generator[Dict[str, Any], None, None]:
    """
    Robustly extract valid JSON objects from a byte stream line.
    """
    try:
        text = line.decode("utf-8", errors="replace").strip()
        if not text:
            return
        try:
            yield json.loads(text)
            return
        except json.JSONDecodeError:
            pass

        depth = 0
        start_idx = -1
        for i, char in enumerate(text):
            if char == "{":
                if depth == 0:
                    start_idx = i
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0 and start_idx != -1:
                    try:
                        obj = json.loads(text[start_idx : i + 1])
                        yield obj
                        start_idx = -1
                    except json.JSONDecodeError:
                        pass
    except Exception as e:
        print_error(f"Error parsing JSON stream: {e}")


def chat(
    model: str,
    messages: List[Message],
    options: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    use_fallback: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Send a chat request to the Ollama Toolkit

    Args:
        model: The model name
        messages: List of message dictionaries with 'role' and 'content' keys
        options: Additional model parameters
        base_url: The base URL for the Ollama Toolkit
        use_fallback: Whether to try the backup model if primary fails

    Returns:
        The response from the API as a dictionary, or None if the request failed
    """
    print_header(f"Chat with {model}")

    # Display the conversation
    for msg in messages:
        role: str = msg.get("role", "")
        if role == "user":
            print(f"{Fore.GREEN}User: {Style.RESET_ALL}{msg.get('content', '')}")
        elif role == "assistant":
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{msg.get('content', '')}")
        elif role == "system":
            print(f"{Fore.YELLOW}System: {Style.RESET_ALL}{msg.get('content', '')}")

    # Prepare the request data
    data: Dict[str, Any] = {"model": model, "messages": messages}

    if options:
        # Add any provided options to the request
        data.update(options)

    # Send the request
    try:
        # Stream by default for more robust handling
        data["stream"] = True

        print_info(f"Sending chat request to {base_url}/api/chat")
        response = requests.post(f"{base_url}/api/chat", json=data, stream=True)
        response.raise_for_status()

        full_content = ""
        final_result = None

        print(f"\n{Fore.BLUE}Assistant: {Style.RESET_ALL}", end="", flush=True)

        # Process the streaming response line by line
        for line in response.iter_lines():
            if not line:
                continue

            try:
                # Each line should be a complete JSON object
                chunk = json.loads(line)

                # Extract content from the message if present
                if "message" in chunk and isinstance(chunk["message"], dict):
                    content = chunk["message"].get("content", "")
                    if content:
                        print(content, end="", flush=True)
                        full_content += content

                # Store the final chunk as our result
                if chunk.get("done", False):
                    final_result = chunk

            except json.JSONDecodeError as e:
                print_error(f"\nJSON parsing error in line: {e}")
                print_info(
                    f"Problematic line: {line.decode('utf-8', errors='replace')[:100]}..."
                )

        print()  # End the line after streaming completes

        if final_result is None:
            print_error("No final response received")
            return None

        # Ensure we have a properly constructed message in the result
        if "message" not in final_result or not isinstance(
            final_result["message"], dict
        ):
            final_result["message"] = {"role": "assistant", "content": full_content}
        elif (
            "content" not in final_result["message"]
            or not final_result["message"]["content"]
        ):
            final_result["message"]["content"] = full_content

        # Add the response to the message history
        message = final_result.get("message", {})
        message_to_append: Message = {
            "role": "assistant",
            "content": full_content or message.get("content", ""),
        }
        messages.append(message_to_append)

        print_success("\nChat completed successfully!")
        return final_result

    except requests.exceptions.RequestException as e:
        print_error(f"Request error with model {model}: {str(e)}")

        # Try fallback model if enabled and not already using it
        if use_fallback and model != BACKUP_CHAT_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_CHAT_MODEL}")
            return chat(
                BACKUP_CHAT_MODEL, messages, options, base_url, use_fallback=False
            )
        return None


def chat_streaming(
    model: str,
    messages: List[Message],
    options: Optional[Dict[str, Any]] = None,
    base_url: str = DEFAULT_OLLAMA_API_URL,
    use_fallback: bool = True,
) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Stream a chat response from the Ollama Toolkit.
    
    Args:
        model: The name of the model to use
        messages: List of message objects with role and content
        options: Optional dictionary of model parameters
        base_url: The base URL of the Ollama Toolkit
        use_fallback: Whether to try the backup model if the primary fails
        
    Returns:
        Tuple of (success boolean, response dictionary or None)
    """
    print_header(f"Starting streaming chat with model: {model}")
    
    # Prepare the request data
    data = {
        "model": model,
        "messages": messages,
        "stream": True,
    }
    
    if options:
        data["options"] = options
    
    # Initialize variables to collect streaming response
    full_content = ""
    response: Dict[str, str] = {"role": "assistant", "content": ""}
    
    try:
        # Make the API request
        url = f"{base_url}/api/chat"
        resp = requests.post(url, json=data, stream=True)
        resp.raise_for_status()
        
        # Process the streaming response
        print_info("Receiving streaming response...")
        
        for line in resp.iter_lines():
            if line:
                try:
                    # Parse the JSON chunk
                    chunks = parse_json_stream(line)
                    for chunk in chunks:
                        if chunk.get("message", {}).get("content"):
                            content = chunk["message"]["content"]
                            full_content += content
                            print(content, end="", flush=True)
                        
                        # Update the response with the final content
                        if chunk.get("done", False):
                            response["content"] = full_content
                            print()  # End the line
                            print_success("Chat streaming completed successfully!")
                            return True, response
                
                except json.JSONDecodeError:
                    print_error(f"Failed to parse response: {line.decode('utf-8')}")
        
        # If we get here without returning, the stream ended without a done message
        if full_content:
            response["content"] = full_content
            return True, response
        
        return False, None
        
    except Exception as e:  # Catch all exceptions, not just RequestException
        print_error(f"Error with model {model}: {str(e)}")
        
        # Try fallback model if enabled and not already using it
        if use_fallback and model != BACKUP_CHAT_MODEL:
            print_info(f"Attempting fallback to backup model: {BACKUP_CHAT_MODEL}")
            return chat_streaming(
                BACKUP_CHAT_MODEL, messages, options, base_url, use_fallback=False
            )
        
        return False, None


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ollama Chat API Example")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_CHAT_MODEL,
        help=f"Model name (default: {DEFAULT_CHAT_MODEL}, backup: {BACKUP_CHAT_MODEL})",
    )
    parser.add_argument("--system", type=str, help="System message")
    parser.add_argument(
        "--temperature", type=float, default=0.7, help="Temperature parameter"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable automatic fallback to backup model",
    )
    args = parser.parse_args()

    # Set options
    options: Dict[str, Any] = {"temperature": args.temperature}

    # Initialize the chat
    messages: List[Message] = []

    # Add the system message if provided
    if args.system:
        messages.append({"role": "system", "content": args.system})
        print(f"{Fore.YELLOW}System: {Style.RESET_ALL}{args.system}")

    if args.interactive:
        # Interactive mode
        try:
            while True:
                # Get user input
                user_input = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")

                # Exit if the user types 'exit' or 'quit'
                if user_input.lower() in ["exit", "quit"]:
                    print_info("Exiting chat...")
                    break

                # Add the user message to the history
                messages.append({"role": "user", "content": user_input})

                # Send the chat request
                chat(args.model, messages, options)

        except KeyboardInterrupt:
            print("\n")
            print_info("Chat session interrupted.")
    else:
        # Single exchange mode
        messages.append({"role": "user", "content": "Tell me a short joke."})
        chat(args.model, messages, options)


if __name__ == "__main__":
    main()
