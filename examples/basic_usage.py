#!/usr/bin/env python3
"""
Basic example showing how to use the Ollama Toolkit client.
"""

from ollama_toolkit import OllamaClient

def main():
    """Run a basic example of the Ollama Toolkit client."""
    # Initialize the client
    client = OllamaClient()
    
    # Get the version
    version = client.get_version()
    print(f"Connected to Ollama version: {version['version']}")
    
    # List available models
    models = client.list_models()
    print("\nAvailable models:")
    for model in models.get("models", []):
        print(f"- {model.get('name')}")
    
    # Check if we have any models before continuing
    if not models.get("models"):
        print("No models found. Please pull a model using: ollama pull llama2")
        return
        
    # Use the first available model
    model_name = models["models"][0]["name"]
    
    # Generate a completion
    print(f"\nGenerating completion with {model_name}...")
    response = client.generate(
        model=model_name,
        prompt="Explain what an API is in simple terms.",
        options={"temperature": 0.7},
        stream=False
    )
    
    print("\nResponse:")
    print(response["response"])

if __name__ == "__main__":
    main()
