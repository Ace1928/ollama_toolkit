#!/usr/bin/env python3
"""
Ollama Forge Command-Line Interface

A powerful and elegant CLI for interacting with Ollama models.
Built with Eidosian principles to ensure both power and simplicity.
"""

import argparse
import sys
import textwrap
from typing import List, Optional, Any, Dict, Union

from . import __version__, DEFAULT_CHAT_MODEL, DEFAULT_EMBEDDING_MODEL
from .client import OllamaClient


def create_parser() -> argparse.ArgumentParser:
    """
    Create elegant command parser with perfect subcommand structure.
    
    Returns:
        Fully configured argument parser
    """
    # Main parser with common arguments
    parser = argparse.ArgumentParser(
        prog="ollama-forge",
        description=textwrap.dedent(
            """
            Ollama Forge CLI - Elegant interaction with Ollama models
            
            This command-line tool provides seamless access to all Ollama capabilities.
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"Ollama Forge v{__version__}"
    )
    parser.add_argument(
        "--api-url",
        help="Ollama API URL (default: http://localhost:11434)",
        default=None,
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    # Create subparsers for each command
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate text from a prompt")
    generate_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    generate_parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)",
    )
    generate_parser.add_argument(
        "--stream", "-s", action="store_true", help="Stream output tokens"
    )
    generate_parser.add_argument("prompt", help="The prompt to generate from")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with a model")
    chat_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    chat_parser.add_argument(
        "--system",
        default="You are a helpful assistant.",
        help="System message (default: You are a helpful assistant.)",
    )
    chat_parser.add_argument("message", help="User message to send")

    # Interactive chat session
    chat_session_parser = subparsers.add_parser(
        "chat-session", help="Start interactive chat session"
    )
    chat_session_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    chat_session_parser.add_argument(
        "--system",
        default="You are a helpful assistant.",
        help="System message (default: You are a helpful assistant.)",
    )

    # Embedding command
    embed_parser = subparsers.add_parser("embed", help="Generate embeddings for text")
    embed_parser.add_argument(
        "--model", "-m", default=DEFAULT_EMBEDDING_MODEL, help="Model name"
    )
    embed_parser.add_argument("text", help="Text to embed")

    # Model management commands
    subparsers.add_parser("list", help="List available models")
    
    pull_parser = subparsers.add_parser("pull", help="Pull a model")
    pull_parser.add_argument("model", help="Model name to pull")

    # Add more commands as needed...

    return parser


def handle_generate(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle text generation command with precision and grace."""
    if args.stream:
        print(f"Generating with {args.model} (streaming)...")
        for chunk in client.generate(
            model=args.model,
            prompt=args.prompt,
            stream=True,
            options={"temperature": args.temperature},
        ):
            if "response" in chunk:
                print(chunk["response"], end="", flush=True)
        print()  # End with newline
    else:
        print(f"Generating with {args.model}...")
        response = client.generate(
            model=args.model,
            prompt=args.prompt,
            options={"temperature": args.temperature},
        )
        print(response.get("response", ""))
    
    return 0


def handle_chat(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle chat command with elegance and functionality."""
    messages = [
        {"role": "system", "content": args.system},
        {"role": "user", "content": args.message},
    ]
    
    print(f"Assistant: ", end="", flush=True)
    for chunk in client.chat(
        model=args.model,
        messages=messages,
        stream=True,
    ):
        if "message" in chunk and "content" in chunk["message"]:
            print(chunk["message"]["content"], end="", flush=True)
    print()  # End with newline
    
    return 0


def handle_chat_session(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle interactive chat session with fluid conversational flow."""
    from colorama import Fore, Style, init
    init()  # Initialize colorama
    
    messages = [{"role": "system", "content": args.system}]
    
    print(f"{Fore.CYAN}Welcome to Ollama Forge Chat Session{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Model: {args.model}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}System: {args.system}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'exit' or 'quit' to end the session{Style.RESET_ALL}")
    print("─" * 50)
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            if user_input.lower() in ("exit", "quit", "/exit", "/quit"):
                break
                
            messages.append({"role": "user", "content": user_input})
            
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}", end="")
            for chunk in client.chat(model=args.model, messages=messages, stream=True):
                if "message" in chunk and "content" in chunk["message"]:
                    print(chunk["message"]["content"], end="", flush=True)
            
            # Add assistant's full response to messages for context
            response = client.chat(model=args.model, messages=messages, stream=False)
            if "message" in response:
                messages.append(response["message"])
            
            print("\n" + "─" * 50)
            
        except KeyboardInterrupt:
            print("\nExiting chat session...")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    return 0


def handle_embed(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle embedding generation command with mathematical precision."""
    result = client.create_embedding(model=args.model, prompt=args.text)
    print(f"Generated embedding with {args.model} (dimensions: {len(result['embedding'])})")
    if args.verbose:
        print(result["embedding"])
    return 0


def handle_list(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle listing models with impeccable formatting."""
    models = client.list_models().get("models", [])
    if not models:
        print("No models available")
        return 0
        
    print(f"Available models ({len(models)}):")
    for model in models:
        print(f"  • {model['name']} ({model.get('size', 'unknown size')})")
    return 0


def handle_pull(args: argparse.Namespace, client: OllamaClient) -> int:
    """Handle model pulling with progress tracking."""
    from tqdm import tqdm
    
    print(f"Pulling model: {args.model}")
    
    with tqdm(unit="B", unit_scale=True, desc=args.model) as pbar:
        last_total = 0
        for progress in client.pull(args.model, stream=True):
            if "completed" in progress and progress.get("total", 0) > 0:
                progress_bytes = int(progress["completed"])
                total_bytes = int(progress["total"])
                
                # Update progress bar
                pbar.total = total_bytes
                increment = progress_bytes - last_total
                if increment > 0:
                    pbar.update(increment)
                    last_total = progress_bytes
    
    print(f"Model {args.model} pulled successfully!")
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI with perfect flow control.
    
    Args:
        args: Command line arguments (uses sys.argv if None)
        
    Returns:
        Exit code (0 for success)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    try:
        client = OllamaClient(api_base=parsed_args.api_url)
        
        # Command dispatch with elegant pattern
        handlers = {
            "generate": handle_generate,
            "chat": handle_chat,
            "chat-session": handle_chat_session,
            "embed": handle_embed,
            "list": handle_list,
            "pull": handle_pull,
            # Add more handlers as needed...
        }
        
        handler = handlers.get(parsed_args.command)
        if handler:
            return handler(parsed_args, client)
        else:
            print(f"Unknown command: {parsed_args.command}")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
