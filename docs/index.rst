.. Ollama Toolkit documentation master file

Ollama Toolkit Documentation
===========================

Welcome to the Ollama Toolkit documentation—where precision meets possibility. This Python client provides a comprehensive interface to interact with Ollama, a framework for running large language models locally with **exceptional efficiency**.

Overview
--------

Ollama Toolkit gives you programmatic access to:

- Text generation with surgical precision
- Chat completion engineered for natural flow
- Embedding creation with mathematical elegance
- Model management (listing, pulling, copying, deleting) with controlled recursion
- Async operations for high-velocity performance applications
- Robust error handling with intuitive fallback mechanisms
- Automatic Ollama installation and startup with zero friction

Key Features
------------

- 🚀 **Complete API Coverage**: Support for all Ollama endpoints—nothing missing, nothing extra
- 🔄 **Recursive Async Support**: Both synchronous and asynchronous interfaces that build upon each other
- 🔧 **Structurally Perfect CLI**: Powerful command-line tools with intuitive architecture
- 🔌 **Zero-Friction Auto-Installation**: Install and start Ollama with mathematically minimal steps
- 💪 **Self-Aware Error Handling**: Comprehensive error types that explain precisely what went wrong
- 📊 **Velocity-Optimized Embeddings**: Create and manipulate embeddings with maximum efficiency
- 🧪 **Recursively Refined Testing**: Every function proven robust through iterative improvement

Getting Started
---------------

.. code-block:: python

    # This implementation follows Eidosian principles of contextual integrity and precision
    from ollama_toolkit import OllamaClient
    from ollama_toolkit.utils.common import ensure_ollama_running

    # Ensure Ollama is installed and running - structurally sound foundation
    is_running, message = ensure_ollama_running()
    if not is_running:
        print(f"Error: {message}")
        exit(1)
        
    print(f"Ollama status: {message}")

    # Initialize the client with optimal timeout
    client = OllamaClient(timeout=300)  # 5-minute timeout for larger operations

    # Check version - self-aware system verification
    version = client.get_version()
    print(f"Connected to Ollama version: {version['version']}")

    # List available models - structural awareness
    models = client.list_models()
    model_names = [model["name"] for model in models.get("models", [])]
    print(f"Available models: {model_names}")

    # Generate text with precision and flow
    if model_names:  # Use first available model if any exist
        model_name = model_names[0]
        print(f"\nGenerating text with {model_name}...")
        
        response = client.generate(
            model=model_name,
            prompt="Explain what makes a good API in three sentences.",
            stream=False
        )
        
        print(f"\nResponse: {response.get('response', 'No response generated')}")
    else:
        print("No models available. Use client.pull_model() to download a model.")

Installation Guide
------------------

- Install via PyPI: ``pip install ollama-toolkit``
- Or install locally in editable mode:

  .. code-block:: bash

      pip install -e /path/to/ollama_toolkit

Documentation Contents
---------------------

.. toctree::
   :maxdepth: 2
   :caption: 📚 Getting Started

   README
   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: 🛠️ Core Documentation
   
   api_reference
   examples
   advanced_usage

.. toctree::
   :maxdepth: 2
   :caption: 🔄 Features & Capabilities
   
   chat
   generate
   embed

.. toctree::
   :maxdepth: 2
   :caption: 🧠 Guides & References
   
   conventions
   troubleshooting
   eidosian_integration
   version
   contributing

Examples
--------

Check out these practical examples:

* :doc:`Basic Usage <examples>` — Precision in simplicity
* :doc:`Generate Text <generate>` — Flow like a river
* :doc:`Chat Completion <chat>` — Universal yet personal
* :doc:`Embeddings <embed>` — Mathematical elegance

All examples can be run via:

.. code-block:: bash

    python -m ollama_toolkit.examples.<example_file>

(e.g. ``python -m ollama_toolkit.examples.quickstart``).

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Authors
-------

- Lloyd Handyside (Biological) - ace1928@gmail.com
- Eidos (Digital) - eidos@gmail.com

Project Repository
-----------------

Find the complete source code on GitHub: https://github.com/Ace1928/ollama_toolkit

