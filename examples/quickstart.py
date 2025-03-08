#!/usr/bin/env python3
"""
Quick Start Example for Ollama Toolkit

This script provides a seamless first-time experience for Ollama:
1. Ensures recommended models are available (pulls them if needed)
2. Lists models and lets you select one
3. Provides an interactive chat experience with the selected model

Following EIDOSIAN principles of excellence:
- Contextual Integrity: Every function serves a clear purpose
- Recursive Refinement: Constantly improving interaction
- Structure as Control: Precisely organized workflow
- Flow Like a River: Seamless transitions between stages
"""

import os
import sys
import time
import socket
import requests
import subprocess
from typing import Dict, List, Set, Optional, Tuple
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init()

# Store original path to restore if needed
original_sys_path = sys.path.copy()

# Import strategy with multiple fallbacks to ensure it works in all contexts
import_success = False

# Try approach 1: Direct import (when the package is installed)
try:
    from ollama_toolkit import OllamaClient, print_header, print_error, print_success, print_info, print_warning
    from ollama_toolkit.utils.common import ensure_ollama_running, check_ollama_running, check_ollama_installed
    import_success = True
    print_info("Using installed ollama_toolkit package")
except ImportError:
    sys.path = original_sys_path  # Reset path before trying next approach

    # Try approach 2: Add parent directory to path (for development mode)
    try:
        # Add the parent directory to sys.path
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from ollama_toolkit import OllamaClient, print_header, print_error, print_success, print_info, print_warning
        from ollama_toolkit.utils.common import ensure_ollama_running, check_ollama_running, check_ollama_installed
        import_success = True
        print_info(f"Using ollama_toolkit from: {parent_dir}")
    except ImportError:
        sys.path = original_sys_path  # Reset path before trying next approach
        
        # Try approach 3: Add grandparent directory to path
        try:
            grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            if grandparent_dir not in sys.path:
                sys.path.insert(0, grandparent_dir)
            
            from ollama_toolkit import OllamaClient, print_header, print_error, print_success, print_info, print_warning
            from ollama_toolkit.utils.common import ensure_ollama_running, check_ollama_running, check_ollama_installed
            import_success = True
            print_info(f"Using ollama_toolkit from: {grandparent_dir}")
        except ImportError:
            # All import approaches failed
            print(f"{Fore.RED}Error: ollama_toolkit package not found!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Install the package using one of these commands:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}- From PyPI: pip install ollama-toolkit{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}- For development: pip install -e /path/to/ollama_toolkit{Style.RESET_ALL}")
            sys.exit(1)

# List of recommended models for first-time users
RECOMMENDED_MODELS = [
    {"name": "qwen2.5:0.5b", "description": "Small and fast assistant model"},
    {"name": "deepseek-r1:1.5b", "description": "General purpose reasoning model"},
    {"name": "qwen2.5-coder:0.5b", "description": "Code assistant model"},
    {"name": "qwen2.5-instruct:0.5b", "description": "Instruction-following assistant model"},
    {"name": "deepscaler", "description": "Broad knowledge assistant model"}
]

# Model capability tags for enhanced user experience
MODEL_CAPABILITY_TAGS = {
    "qwen": ["general", "chat", "instruct", "fast"],
    "deepseek": ["reasoning", "logic", "mathematics", "robust"],
    "coder": ["programming", "code", "development", "technical"],
    "instruct": ["directions", "specific-tasks", "detailed-control"],
    "deepscaler": ["knowledge", "comprehensive", "detailed"]
}

# Ollama API endpoint and port
OLLAMA_API_URL = "http://localhost:11434"
OLLAMA_API_PORT = 11434


def is_port_in_use(port: int = OLLAMA_API_PORT) -> bool:
    """
    Check if a port is in use (more reliable than command status checks).
    
    Args:
        port: Port number to check
        
    Returns:
        True if the port is in use, False otherwise
    """
    try:
        # Try to create a socket and bind to the port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Setting a timeout prevents hanging
            s.settimeout(1)
            # If we can bind to the port, it's not in use
            s.bind(("127.0.0.1", port))
            return False
    except (socket.error, OSError):
        # If we get an error, the port is probably in use
        return True
    
    return False


def is_ollama_api_responding() -> bool:
    """
    Check if the Ollama API is responding by making a direct HTTP request.
    
    Returns:
        True if the API is responding, False otherwise
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/version", timeout=3)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    
    return False


def check_ollama_running_direct() -> Tuple[bool, str]:
    """
    Directly check if Ollama is running using multiple methods.
    More reliable than using command-line tools.
    
    Returns:
        Tuple of (is_running, message)
    """
    # First check using the API
    if is_ollama_api_responding():
        try:
            # Get version info for a nicer message
            response = requests.get(f"{OLLAMA_API_URL}/api/version", timeout=3)
            version = response.json().get("version", "unknown version")
            return True, f"Ollama API is running ({version})"
        except:
            return True, "Ollama API is running"
    
    # Then check if the port is in use
    if is_port_in_use():
        return True, "Ollama port is in use (API not responding but port is bound)"
    
    # If all fails, try command-line methods as fallback
    try:
        # Try 'ollama list' instead of 'ollama version' as it works more reliably
        result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True, 
            check=False,
            timeout=5  # Add timeout to avoid hanging
        )
        
        if result.returncode == 0:
            return True, "Ollama server is running (verified with 'ollama list')"
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    try:
        # Try 'ollama ps' as another fallback
        result = subprocess.run(
            ["ollama", "ps"], 
            capture_output=True, 
            text=True, 
            check=False,
            timeout=5  # Add timeout to avoid hanging
        )
        
        if result.returncode == 0:
            return True, "Ollama server is running (verified with 'ollama ps')"
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return False, "Ollama server is not running"


def ensure_ollama_ready(max_wait_seconds: int = 30) -> bool:
    """
    Make sure Ollama is installed and running.
    
    Args:
        max_wait_seconds: Maximum time to wait for Ollama to start in seconds
    
    Returns:
        Whether Ollama is ready for use
    """
    print_header("CHECKING OLLAMA STATUS")
    
    # First, check if Ollama is already running using the direct method
    is_running, message = check_ollama_running_direct()
    if is_running:
        print_success(f"Ollama is already running: {message}")
        return True
    
    # Not running, so check if it's installed
    is_installed, install_message = check_ollama_installed()
    if not is_installed:
        print_warning(f"Ollama is not installed: {install_message}")
        print_info("Attempting to install Ollama automatically...")
    
    # Try to start Ollama
    print_info("Attempting to start Ollama server...")
    
    try:
        # First try using the toolkit's ensure_ollama_running
        is_running, message = ensure_ollama_running()
        
        if not is_running:
            # If that fails, try direct command
            print_info("Trying direct command to start Ollama...")
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
    except Exception as e:
        print_warning(f"Error while starting Ollama: {str(e)}")
        print_info("Continuing anyway as the server might already be running...")
    
    # Wait up to max_wait_seconds for the server to fully initialize
    print_info(f"Waiting up to {max_wait_seconds} seconds for Ollama to initialize...")
    
    start_time = time.time()
    wait_interval = 3  # Check every 3 seconds
    attempts = 0
    
    while (time.time() - start_time) < max_wait_seconds:
        attempts += 1
        is_ready, status = check_ollama_running_direct()
        
        if is_ready:
            print_success(f"Ollama server is ready: {status}")
            return True
            
        print_info(f"Waiting for Ollama to initialize (attempt {attempts})...")
        time.sleep(wait_interval)
    
    # One final check using all possible methods
    print_info("Performing final check for Ollama server...")
    
    # Try direct API access
    if is_ollama_api_responding():
        print_success("Ollama API is responding!")
        return True
    
    # Check if port is in use
    if is_port_in_use():
        print_warning("Ollama API port is in use but API is not responding.")
        print_info("This might indicate a partial startup or another service using the port.")
        print_info("Proceeding anyway, but you might experience issues...")
        return True
    
    # Try using the client to list models as final test
    try:
        client = OllamaClient()
        models = client.list_models()
        if models:
            print_success("Successfully connected to Ollama API!")
            return True
    except Exception:
        pass
    
    print_warning(f"Could not confirm that Ollama is running after {max_wait_seconds} seconds")
    print_error("Please install and start Ollama manually from https://ollama.com/download")
    print_info("Run 'ollama serve' in a separate terminal, then run this script again.")
    return False


def get_available_models() -> List[Dict[str, any]]:
    """Get list of currently available models."""
    client = OllamaClient()
    try:
        result = client.list_models()
        if "models" in result:
            return result["models"]
    except Exception as e:
        print_error(f"Error getting models: {str(e)}")
    
    return []


def ensure_recommended_models(available_models: List[Dict[str, any]]) -> bool:
    """
    Ensure recommended models are available, pull them if needed.
    Returns True if at least one model is available.
    """
    print_header("CHECKING RECOMMENDED MODELS")
    
    # Extract available model names - consider both exact names and names with :latest suffix
    available_model_set = set()
    for model in available_models:
        name = model['name']
        available_model_set.add(name)
        if name.endswith(':latest'):
            # Also add without the :latest suffix
            available_model_set.add(name[:-7])
        else:
            # Also add with the :latest suffix
            available_model_set.add(f"{name}:latest")
    
    # Check which recommended models need to be pulled
    client = OllamaClient()
    models_pulled = False
    
    for model_info in RECOMMENDED_MODELS:
        model_name = model_info["name"]
        
        # Check if model exists (with or without :latest suffix)
        model_exists = model_name in available_model_set or f"{model_name}:latest" in available_model_set
        
        if model_exists:
            print_info(f"✓ Model '{model_name}' is already available")
            models_pulled = True
            continue
            
        # Model needs to be pulled
        print_info(f"Model '{model_name}' ({model_info['description']}) not found - downloading...")
        
        try:
            # Pull model with progress updates
            print()
            pull_success = False
            pull_error = None
            
            try:
                # Get pull stream - check for None or empty response first to avoid iteration errors
                pull_stream = client.pull_model(model_name, stream=True)
                if pull_stream:
                    for update in pull_stream:
                        if not isinstance(update, dict):
                            continue
                            
                        # Check for error status
                        if update.get("status") == "error" or "error" in update:
                            error_msg = update.get("error", "Unknown error")
                            print_error(f"Error pulling model {model_name}: {error_msg}")
                            pull_error = error_msg
                            break

                        status = update.get("status", "")
                        if status == "downloading":
                            digest = update.get("digest", "unknown")
                            completed = update.get("completed", 0)
                            total = update.get("total", 0)

                            if total > 0:
                                percent = (completed / total) * 100
                                # Use a progress bar for more visual feedback
                                bar_length = 30
                                filled_length = int(bar_length * percent // 100)
                                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                                
                                print(f"\r{Fore.BLUE}Downloading {model_name}: {percent:.1f}% |{bar}| ({completed}/{total}){Style.RESET_ALL}", 
                                    end="", flush=True)
                        elif status == "success":
                            pull_success = True
                        elif status:
                            print(f"\r{Fore.BLUE}{status}{' ' * 50}{Style.RESET_ALL}")
                
                # Check final status
                if pull_error:
                    print_warning(f"Could not pull model '{model_name}': {pull_error}")
                    print_info(f"Continuing with other available models.")
                elif pull_success:
                    print()
                    print_success(f"Successfully downloaded '{model_name}'")
                    models_pulled = True
                else:
                    # If model doesn't exist on registry or other issue
                    print()
                    print_warning(f"Could not pull model '{model_name}'. It may not exist in the registry.")
                    print_info(f"Continuing with other available models.")
                
            except Exception as e:
                import traceback
                print_error(f"\nError while downloading: {str(e)}")
                if os.environ.get('DEBUG'):
                    traceback.print_exc()
        
        except Exception as e:
            print_error(f"Failed to pull model '{model_name}': {str(e)}")
    
    return models_pulled


def get_model_tags(model_name: str) -> List[str]:
    """
    Get capability tags for a given model name.
    
    Args:
        model_name: Name of the model to check
    
    Returns:
        List of capability tags associated with the model
    """
    tags = []
    for key, values in MODEL_CAPABILITY_TAGS.items():
        if key.lower() in model_name.lower():
            tags.extend(values)
    return tags


def display_models(models: List[Dict[str, any]]) -> None:
    """Display available models with details."""
    print_header("AVAILABLE MODELS")
    
    if not models:
        print_warning("No models found!")
        return
        
    print(f"{Fore.CYAN}Found {len(models)} models:{Style.RESET_ALL}")
    
    # Create a list to sort recommended models first
    recommended_names = {model["name"] for model in RECOMMENDED_MODELS}
    sorted_models = sorted(models, key=lambda m: (m["name"] not in recommended_names, m["name"]))
    
    # Display header for the table
    print(f"\n{Fore.CYAN}{'#':3} {'':2} {'MODEL NAME':<28} {'SIZE':>10} {'CAPABILITIES'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*3} {'-'*2} {'-'*28} {'-'*10} {'-'*30}{Style.RESET_ALL}")
    
    for i, model in enumerate(sorted_models):
        is_recommended = model["name"] in recommended_names
        model_marker = "★" if is_recommended else " "
        
        # Format size nicely if available
        size_str = "unknown"
        if "size" in model:
            size_bytes = int(model.get("size", 0))
            if size_bytes > 1_000_000_000:
                size_str = f"{size_bytes / 1_000_000_000:.1f} GB"
            elif size_bytes > 1_000_000:
                size_str = f"{size_bytes / 1_000:.1f} MB"
            else:
                size_str = f"{size_bytes / 1_000:.1f} KB"
        
        # Get description if it's a recommended model
        description = next((m["description"] for m in RECOMMENDED_MODELS if m["name"] == model["name"]), "")
        
        # Get capability tags
        tags = get_model_tags(model["name"])
        tag_str = ", ".join(tags) if tags else ""
        if description and not tag_str:
            tag_str = description
        elif description:
            tag_str = f"{description} ({tag_str})"
            
        color = Fore.GREEN if is_recommended else Fore.WHITE
        print(f"{i+1:3} {color}{model_marker} {model['name']:<28}{Style.RESET_ALL} {size_str:>10} {Fore.YELLOW}{tag_str}{Style.RESET_ALL}")


def format_chat_message(message: Dict[str, str]) -> str:
    """
    Format a chat message for display, applying Eidosian principles of elegance.
    
    Args:
        message: The message to format with 'role' and 'content'
        
    Returns:
        Beautifully formatted message string
    """
    role = message.get("role", "").lower()
    content = message.get("content", "")
    
    if role == "system":
        return f"{Fore.YELLOW}System: {Style.RESET_ALL}{content}"
    elif role == "user":
        return f"{Fore.GREEN}You: {Style.RESET_ALL}{content}"
    elif role == "assistant":
        return f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{content}"
    else:
        return f"{role.capitalize()}: {content}"


def display_help_menu() -> None:
    """Display the help menu with available commands."""
    print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}/help{Style.RESET_ALL}           - Show this help menu")
    print(f"  {Fore.GREEN}/exit{Style.RESET_ALL} or {Fore.GREEN}/quit{Style.RESET_ALL} - End the conversation")
    print(f"  {Fore.GREEN}/clear{Style.RESET_ALL}          - Clear the conversation history")
    print(f"  {Fore.GREEN}/system <msg>{Style.RESET_ALL}   - Set a new system message")
    print(f"  {Fore.GREEN}/model <name>{Style.RESET_ALL}   - Switch to a different model")
    print(f"  {Fore.GREEN}/save <file>{Style.RESET_ALL}    - Save conversation to file")
    print(f"  {Fore.GREEN}/load <file>{Style.RESET_ALL}    - Load conversation from file")
    print(f"  {Fore.GREEN}/retry{Style.RESET_ALL}          - Retry the last user message")
    print()


def chat_with_model(model_name: str, available_models: List[Dict[str, any]]) -> None:
    """
    Start an interactive chat session with the specified model.
    
    Args:
        model_name: Name of the model to chat with
        available_models: List of available models for potential switching
    """
    print_header(f"CHAT SESSION WITH {model_name.upper()}")
    
    client = OllamaClient(timeout=300)  # Increased from 30 to 300 seconds
    
    # Initialize chat with a system message
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides concise and accurate answers."}
    ]
    
    # Get capabilities to help craft system messages
    tags = get_model_tags(model_name)
    if "coder" in model_name.lower() or "code" in tags:
        messages = [{"role": "system", "content": "You are a helpful programming assistant. Provide clear, concise code examples and explanations."}]
    elif any(tag in tags for tag in ["reasoning", "mathematics", "robust"]):
        messages = [{"role": "system", "content": "You are a logical reasoning assistant with excellent problem-solving skills. Provide clear, step-by-step reasoning."}]
    
    print(format_chat_message(messages[0]))
    print(f"{Fore.YELLOW}System: You are now chatting with {model_name}.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}System: Type /help for available commands.{Style.RESET_ALL}")
    print()
    
    try:
        last_user_message = None
        
        while True:
            # Get user input
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting chat session.")
                break
                
            # Check for commands
            if user_input.startswith("/"):
                command_parts = user_input[1:].strip().split(maxsplit=1)
                command = command_parts[0].lower()
                args = command_parts[1] if len(command_parts) > 1 else ""
                
                # Process commands
                if command in ["exit", "quit"]:
                    print_info("Exiting chat session.")
                    break
                elif command == "help":
                    display_help_menu()
                    continue
                # ... other command handling ...
                
                # Continue to next iteration if this was a command
                continue
                
            # Regular message (not a command)
            last_user_message = user_input
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Display assistant response
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}", end="", flush=True)
            
            # Send the chat request with aggressive timeout
            assistant_message = ""
            start_time = time.time()
            
            try:
                # Set a more generous timeout to avoid hanging
                chat_options = {
                    "temperature": 0.7,
                    "timeout": 300,     # Increased from 30 to 300 seconds
                    "top_p": 0.9       # Additional parameters to help with response speed
                }
                
                # Get the response stream
                chat_stream = client.chat(
                    model_name, 
                    messages, 
                    stream=True, 
                    options=chat_options
                )
                
                # Process the stream with timeout protection
                absolute_timeout = time.time() + 360  # Hard cutoff after 6 minutes (was 45 seconds)
                
                for chunk in chat_stream:
                    # Force stop if we exceed absolute timeout
                    if time.time() > absolute_timeout:
                        print_warning("\n[Response taking too long, forced stop]")
                        break
                        
                    # Check for errors
                    if "error" in chunk:
                        print_error(f"\n\nError: {chunk['error']}")
                        break
                    
                    # Process the content
                    if chunk.get("raw", False) and "message" in chunk:
                        content = chunk["message"].get("content", "")
                        if content:
                            print(content, end="", flush=True)
                            assistant_message += content
                    elif "message" in chunk and isinstance(chunk["message"], dict):
                        content = chunk["message"].get("content", "")
                        if content:
                            print(content, end="", flush=True)
                            assistant_message += content
                    
                    # Check for completion
                    if chunk.get("done", False):
                        break
                
                # Add the response to history if we got something
                if assistant_message:
                    elapsed_time = time.time() - start_time
                    messages.append({"role": "assistant", "content": assistant_message})
                    print(f"\n{Fore.CYAN}[Response time: {elapsed_time:.2f}s]{Style.RESET_ALL}\n")
                else:
                    print_warning("\n[No valid response received]")
                    
            except Exception as e:
                print_error(f"\n\nError: {str(e)}")
                print_warning("Try simplifying your query or using a different model.")
    
    except Exception as e:
        import traceback
        print_error(f"\nError during chat: {str(e)}")
        if os.environ.get('DEBUG'):
            traceback.print_exc()


def main():
    """
    Main function to run the example.
    Following Eidosian principles of Contextual Integrity and Flow Like a River.
    """
    print_header("OLLAMA QUICKSTART WIZARD")
    
    print(f"{Fore.CYAN}Welcome to the Ollama Quickstart Wizard!{Style.RESET_ALL}")
    print(f"This tool will help you get started with local AI models using {Fore.CYAN}EIDOSIAN{Style.RESET_ALL} principles.")
    print(f"Every interaction is designed to be {Fore.GREEN}efficient{Style.RESET_ALL}, {Fore.YELLOW}seamless{Style.RESET_ALL}, and {Fore.MAGENTA}powerful{Style.RESET_ALL}.\n")
    
    # Step 1: Make sure Ollama is running with enhanced waiting logic
    if not ensure_ollama_ready(max_wait_seconds=30):
        return
        
    print()
    
    # Step 2: Get currently available models
    print_info("Scanning for available models...")
    available_models = get_available_models()
    
    # Step 3: Ensure we have the recommended models
    if not available_models:
        print_info("No models found. Pulling recommended starter models...")
        ensure_recommended_models([])
        # Refresh the model list after pulling
        available_models = get_available_models()
    else:
        # Check if we need to pull any recommended models
        ensure_recommended_models(available_models)
        # Refresh the model list after potentially pulling new models
        available_models = get_available_models()
    
    if not available_models:
        print_error("No models available. Please try again or pull models manually.")
        print_info("You can pull a model using: ollama pull qwen2.5:0.5b")
        return
    
    print()
    
    # Step 4: Display available models with enhanced formatting
    display_models(available_models)
    
    # Step 5: Select a model with enhanced validation
    print()
    while True:
        try:
            choice = input(f"Select a model (1-{len(available_models)}) or type the model name: ")
            
            # Check if the input is a number
            if choice.isdigit() and 1 <= int(choice) <= len(available_models):
                model_index = int(choice) - 1
                model_name = available_models[model_index]["name"]
                break
            
            # Check if the input matches a model name
            matching_models = [model for model in available_models if model["name"] == choice]
            if matching_models:
                model_name = matching_models[0]["name"]
                break
            
            # Fix: Check if user entered the number in the string format (like "5")
            if choice.strip() in [str(i) for i in range(1, len(available_models) + 1)]:
                model_index = int(choice.strip()) - 1
                model_name = available_models[model_index]["name"]
                break
                
            # Check for partial matches if no exact match
            partial_matches = [model for model in available_models if choice.lower() in model["name"].lower()]
            if partial_matches:
                if len(partial_matches) == 1:
                    model_name = partial_matches[0]["name"]
                    print_info(f"Using closest match: {model_name}")
                    break
                else:
                    print_warning(f"Multiple matches found. Please be more specific or use a number:")
                    for i, model in enumerate(partial_matches):
                        print(f"  {i+1}. {model['name']}")
                    continue
                
            print_warning("Invalid selection. Please try again.")
        except (ValueError, KeyboardInterrupt):
            print("\nExiting...")
            return
    
    # Step 6: Chat with the selected model using enhanced interface
    print()
    print_success(f"Starting enhanced chat experience with {model_name}...")
    chat_with_model(model_name, available_models)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted. Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
