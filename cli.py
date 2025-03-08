#!/usr/bin/env python3
"""
Command-line interface for the Ollama Toolkit client.
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict, List

from colorama import Fore, Style, init

from ollama_toolkit.client import OllamaClient
from ollama_toolkit.exceptions import ConnectionError, ModelNotFoundError, OllamaAPIError
from ollama_toolkit.utils.common import (
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
)

# Initialize colorama
init()


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def list_models_command(args: argparse.Namespace) -> None:
    """Handle the list-models command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        models = client.list_models()
        print_header("Available Models")

        if "models" in models and models["models"]:
            # Pretty print model information
            for model in models["models"]:
                name = model.get("name", "Unknown")
                modified = model.get("modified_at", "Unknown")
                size = model.get("size", 0) / (1024 * 1024)  # Convert to MB

                print(f"{Fore.GREEN}{name}{Style.RESET_ALL}")
                print(f"  Modified: {modified}")
                print(f"  Size: {size:.2f} MB")
                print()
        else:
            print_info("No models found")

    except OllamaAPIError as e:
        print_error(f"Failed to list models: {e}")
        sys.exit(1)


def model_info_command(args: argparse.Namespace) -> None:
    """Handle the model-info command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        info = client.get_model_info(args.model)
        print_header(f"Model Information: {args.model}")

        if args.json:
            print(json.dumps(info, indent=2))
        else:
            # Display key model information in a readable format
            license_info = info.get("license", "Unknown")
            modelfile = info.get("modelfile", "Not available")
            parameters = info.get("parameters", "Unknown")
            template = info.get("template", "Default")

            print(f"{Fore.BLUE}License:{Style.RESET_ALL} {license_info}")
            print(f"{Fore.BLUE}Parameters:{Style.RESET_ALL} {parameters}")
            print(f"{Fore.BLUE}Template:{Style.RESET_ALL} {template}")
            print(f"\n{Fore.YELLOW}Modelfile:{Style.RESET_ALL}\n{modelfile}")

    except OllamaAPIError as e:
        print_error(f"Failed to get model info: {e}")
        sys.exit(1)


def generate_command(args: argparse.Namespace) -> None:
    """Handle the generate command."""
    client = OllamaClient(base_url=args.api_url)

    # Set up options
    options = {
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
    }

    if args.max_tokens:
        options["num_predict"] = args.max_tokens

    print_header(f"Generating with model: {args.model}")
    print_info(f"Prompt: {args.prompt}")

    try:
        if args.stream:
            # Stream the response
            print("\nResponse:")
            for chunk in client.generate(args.model, args.prompt, options, stream=True):
                if isinstance(chunk, dict):
                    response_text = chunk.get("response", "")
                    if response_text:
                        print(response_text, end="", flush=True)
            print("\n")  # Add a newline at the end
            print_success("Generation completed!")
        else:
            # Get the full response at once
            response = client.generate(args.model, args.prompt, options, stream=False)
            print("\nResponse:")
            if isinstance(response, dict) and "response" in response:
                print(response["response"])
            print_success("Generation completed!")

    except OllamaAPIError as e:
        print_error(f"Generation failed: {e}")
        sys.exit(1)


def chat_command(args: argparse.Namespace) -> None:
    """Handle the chat command."""
    client = OllamaClient(base_url=args.api_url)

    # Set up options
    options = {
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
    }

    if args.max_tokens:
        options["num_predict"] = args.max_tokens

    # Initialize messages
    messages: List[Dict[str, str]] = []

    # Add system message if provided
    if args.system:
        messages.append({"role": "system", "content": args.system})

    # Add user message
    messages.append({"role": "user", "content": args.message})

    print_header(f"Chat with model: {args.model}")

    try:
        if args.stream:
            # Stream the response
            print(f"{Fore.GREEN}You:{Style.RESET_ALL} {args.message}")
            print(f"{Fore.BLUE}Assistant:{Style.RESET_ALL} ", end="", flush=True)

            for chunk in client.chat(args.model, messages, options, stream=True):
                if isinstance(chunk, dict) and "message" in chunk:
                    message_dict: Dict[str, Any] = chunk["message"]
                    if "content" in message_dict:
                        # Use direct access with proper type checking instead of get()
                        content_text = ""
                        if "content" in message_dict:
                            content = message_dict["content"]
                            if content is not None:
                                content_text = str(content)

                        if content_text:
                            print(content_text, end="", flush=True)
            print("\n")  # Add a newline at the end
            print_success("Chat completed!")
        else:
            # Get the full response at once
            response = client.chat(args.model, messages, options, stream=False)

            print(f"{Fore.GREEN}You:{Style.RESET_ALL} {args.message}")
            if isinstance(response, dict) and "message" in response:
                message_dict: Dict[str, Any] = response["message"]
                # Use direct access with proper type checking instead of get()
                content_str = ""
                if "content" in message_dict:
                    content = message_dict["content"]
                    if content is not None:
                        content_str = str(content)

                print(f"{Fore.BLUE}Assistant:{Style.RESET_ALL} {content_str}")
            print_success("Chat completed!")

    except OllamaAPIError as e:
        print_error(f"Chat failed: {e}")
        sys.exit(1)


def embedding_command(args: argparse.Namespace) -> None:
    """Handle the embedding command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        result = client.create_embedding(args.model, args.text)
        print_header(f"Embedding with model: {args.model}")

        embedding = result.get("embedding", [])

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_info(f"Embedding dimension: {len(embedding)}")
            print_info(f"First few values: {embedding[:5]}...")

            # Calculate and print embedding norm
            import numpy as np

            norm = np.linalg.norm(embedding)
            print_info(f"Embedding norm: {norm:.4f}")

        print_success("Embedding created!")

    except OllamaAPIError as e:
        print_error(f"Embedding failed: {e}")
        sys.exit(1)


def version_command(args: argparse.Namespace) -> None:
    """Handle the version command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        version = client.get_version()
        print_header("Ollama Version")

        if args.json:
            print(json.dumps(version, indent=2))
        else:
            print(f"Version: {version.get('version', 'Unknown')}")

    except OllamaAPIError as e:
        print_error(f"Failed to get version: {e}")
        sys.exit(1)


def pull_command(args: argparse.Namespace) -> None:
    """Handle the pull command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        print_header(f"Pulling model: {args.model}")

        if args.stream:
            # Stream the progress
            for chunk in client.pull_model(args.model, stream=True):
                if isinstance(chunk, dict):
                    status = chunk.get("status", "")
                    if status == "downloading":
                        digest = chunk.get("digest", "unknown")
                        completed = chunk.get("completed", 0)
                        total = chunk.get("total", 0)

                        if total > 0:
                            percent = (completed / total) * 100
                            print(
                                f"\rDownloading {digest}: {percent:.2f}% ({completed}/{total})",
                                end="",
                                flush=True,
                            )
                    elif status:
                        print(f"\n{status}")

            print_success("Model pulled successfully!")
        else:
            # Pull without streaming
            client.pull_model(args.model, stream=False)
            print_success("Model pulled successfully!")

    except OllamaAPIError as e:
        print_error(f"Failed to pull model: {e}")
        sys.exit(1)


def delete_command(args: argparse.Namespace) -> None:
    """Handle the delete command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        print_header(f"Deleting model: {args.model}")
        client.delete_model(args.model)
        print_success(f"Model {args.model} deleted successfully!")

    except OllamaAPIError as e:
        print_error(f"Failed to delete model: {e}")
        sys.exit(1)


def copy_command(args: argparse.Namespace) -> None:
    """Handle the copy command."""
    client = OllamaClient(base_url=args.api_url)

    try:
        print_header(f"Copying model: {args.source} to {args.destination}")
        client.copy_model(args.source, args.destination)
        print_success(
            f"Model copied from {args.source} to {args.destination} successfully!"
        )

    except OllamaAPIError as e:
        print_error(f"Failed to copy model: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Ollama Toolkit Command Line Interface",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--api-url", default="http://localhost:11434", help="Ollama Toolkit URL"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--version", action="store_true", help="Show ollama-api version"
    )

    # Create subparsers with better help formatting
    subparsers = parser.add_subparsers(
        dest="command", help="Command to run", metavar="COMMAND"
    )

    # List models command
    subparsers.add_parser("list-models", help="List available models")

    # Model info command
    info_parser = subparsers.add_parser(
        "model-info", help="Get information about a model"
    )
    info_parser.add_argument("model", help="Model name")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate text")
    generate_parser.add_argument("model", help="Model name")
    generate_parser.add_argument("prompt", help="Prompt for generation")
    generate_parser.add_argument(
        "--temperature", type=float, default=0.7, help="Temperature parameter"
    )
    generate_parser.add_argument(
        "--top-p", type=float, default=0.9, help="Top-p sampling parameter"
    )
    generate_parser.add_argument(
        "--top-k", type=int, default=40, help="Top-k sampling parameter"
    )
    generate_parser.add_argument(
        "--max-tokens", type=int, help="Maximum tokens to generate"
    )
    generate_parser.add_argument(
        "--stream", action="store_true", help="Stream the response"
    )

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with a model")
    chat_parser.add_argument(
        "model", help="Model name", default="deepseek-r1:1.5b", nargs="?"
    )
    chat_parser.add_argument("message", help="User message")
    chat_parser.add_argument("--system", help="Optional system message")
    chat_parser.add_argument(
        "--temperature", type=float, default=0.7, help="Temperature parameter"
    )
    chat_parser.add_argument(
        "--top-p", type=float, default=0.9, help="Top-p sampling parameter"
    )
    chat_parser.add_argument(
        "--top-k", type=int, default=40, help="Top-k sampling parameter"
    )
    chat_parser.add_argument(
        "--max-tokens", type=int, help="Maximum tokens to generate"
    )
    chat_parser.add_argument(
        "--stream", action="store_true", help="Stream the response"
    )

    # Embedding command
    embedding_parser = subparsers.add_parser("embedding", help="Create an embedding")
    embedding_parser.add_argument(
        "model", help="Model name", default="deepseek-r1:1.5b", nargs="?"
    )
    embedding_parser.add_argument("text", help="Text to embed")
    embedding_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Version command
    version_parser = subparsers.add_parser("version", help="Get Ollama version")
    version_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Pull model command
    pull_parser = subparsers.add_parser("pull", help="Pull a model")
    pull_parser.add_argument("model", help="Model name")
    pull_parser.add_argument(
        "--stream", action="store_true", help="Stream the progress"
    )

    # Delete model command
    delete_parser = subparsers.add_parser("delete", help="Delete a model")
    delete_parser.add_argument("model", help="Model name")

    # Copy model command
    copy_parser = subparsers.add_parser("copy", help="Copy a model")
    copy_parser.add_argument("source", help="Source model name")
    copy_parser.add_argument("destination", help="Destination model name")

    args = parser.parse_args()

    if args.version:
        from ollama_toolkit import __version__

        print(f"ollama-api version {__version__}")
        return

    setup_logging(args.verbose)

    # Handle commands
    try:
        if args.command == "list-models":
            list_models_command(args)
        elif args.command == "model-info":
            model_info_command(args)
        elif args.command == "generate":
            generate_command(args)
        elif args.command == "chat":
            chat_command(args)
        elif args.command == "embedding":
            embedding_command(args)
        elif args.command == "version":
            version_command(args)
        elif args.command == "pull":
            pull_command(args)
        elif args.command == "delete":
            delete_command(args)
        elif args.command == "copy":
            copy_command(args)
        else:
            parser.print_help()
            sys.exit(1)
    except ConnectionError as e:
        print_error(f"Connection error: {e}")
        print_info("Make sure Ollama is running and accessible.")
        sys.exit(2)
    except ModelNotFoundError as e:
        print_error(f"Model error: {e}")
        print_info("Try running 'ollama list-models' to see available models.")
        sys.exit(3)
    except OllamaAPIError as e:
        print_error(f"API error: {e}")
        sys.exit(4)
    except KeyboardInterrupt:
        print("\n")
        print_warning("Operation interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
