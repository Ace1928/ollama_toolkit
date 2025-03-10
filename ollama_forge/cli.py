#!/usr/bin/env python3
"""
Command-line interface for the Ollama Forge.
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict, List

from colorama import Fore, Style, init

from ollama_forge.client import OllamaClient
from ollama_forge.exceptions import ConnectionError, ModelNotFoundError, OllamaAPIError
from ollama_forge.utils.common import (
    print_error,
    print_header,
    print_info,
    print_json,
    print_success,
    print_warning,
)

// Initialize colorama
init()


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Ollama Forge CLI")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    subparsers = parser.add_subparsers(dest="command")

    # List models
    subparsers.add_parser("list-models", help="List available models")

    # Generate text
    generate_parser = subparsers.add_parser("generate", help="Generate text")
    generate_parser.add_argument("model", help="Model name")
    generate_parser.add_argument("prompt", help="Prompt text")
    generate_parser.add_argument("--options", help="Additional options as JSON string", default="{}")
    generate_parser.add_argument("--stream", action="store_true", help="Stream the response")

    # Chat
    chat_parser = subparsers.add_parser("chat", help="Chat with a model")
    chat_parser.add_argument("model", help="Model name")
    chat_parser.add_argument("prompt", help="Prompt text")
    chat_parser.add_argument("--system", help="System message", default="")
    chat_parser.add_argument("--options", help="Additional options as JSON string", default="{}")
    chat_parser.add_argument("--stream", action="store_true", help="Stream the response")

    # Create embedding
    embedding_parser = subparsers.add_parser("embedding", help="Create an embedding")
    embedding_parser.add_argument("model", help="Model name")
    embedding_parser.add_argument("prompt", help="Prompt text")

    # Model management
    subparsers.add_parser("version", help="Get Ollama version")
    
    # Pull model
    pull_parser = subparsers.add_parser("pull", help="Pull a model")
    pull_parser.add_argument("model", help="Model name to pull")
    
    # Delete model
    delete_parser = subparsers.add_parser("delete", help="Delete a model")
    delete_parser.add_argument("model", help="Model name to delete")
    
    # Copy model
    copy_parser = subparsers.add_parser("copy", help="Copy a model")
    copy_parser.add_argument("source", help="Source model name")
    copy_parser.add_argument("destination", help="Destination model name")
    
    # Model info
    model_info_parser = subparsers.add_parser("model-info", help="Get model information")
    model_info_parser.add_argument("model", help="Model name")

    args = parser.parse_args()
    
    # Set up logging
    if args.verbose:
        setup_logging(True)

    client = OllamaClient()

    if args.command == "list-models":
        models = client.list_models()
        print_json(models)

    elif args.command == "generate":
        options = json.loads(args.options)
        response = client.generate(args.model, args.prompt, options, args.stream)
        if args.stream:
            for chunk in response:
                print_json(chunk)
        else:
            print_json(response)

    elif args.command == "chat":
        options = json.loads(args.options)
        messages = [{"role": "system", "content": args.system}] if args.system else []
        messages.append({"role": "user", "content": args.prompt})
        # Fix parameter order to match client.chat(model, messages, stream, options)
        response = client.chat(args.model, messages, stream=args.stream, options=options)
        if args.stream:
            for chunk in response:
                print_json(chunk)
        else:
            print_json(response)

    elif args.command == "embedding":
        response = client.create_embedding(args.model, args.prompt)
        print_json(response)

    elif args.command == "version":
        version = client.get_version()
        print_json(version)

    elif args.command == "pull":
        response = client.pull_model(args.model)
        print_json(response)

    elif args.command == "delete":
        success = client.delete_model(args.model)
        if success:
            print_success(f"Model '{args.model}' deleted successfully.")
        else:
            print_error(f"Failed to delete model '{args.model}'.")

    elif args.command == "copy":
        response = client.copy_model(args.source, args.destination)
        if response:
            print_success(f"Model '{args.source}' copied to '{args.destination}' successfully.")
        else:
            print_error(f"Failed to copy model '{args.source}' to '{args.destination}'.")
            
    elif args.command == "model-info":
        info = client.get_model_info(args.model)
        print_json(info)
    
    elif not args.command:
        parser.print_help()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
