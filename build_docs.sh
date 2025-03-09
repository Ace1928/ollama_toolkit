#!/usr/bin/env bash

set -e  # Exit on error

echo "Building Ollama Toolkit documentation..."

# Clean previous builds
rm -rf docs/_build/html

# Install documentation dependencies if needed
if ! pip show sphinx myst-parser > /dev/null; then
    echo "Installing documentation dependencies..."
    pip install sphinx myst-parser sphinx-autobuild
fi

# Build the documentation
cd "$(dirname "$0")"
sphinx-build -b html docs docs/_build/html

# Report success and next steps
echo ""
echo "Documentation built successfully!"
echo "Open docs/_build/html/index.html in your browser to view it"

# Automatically open the documentation if on GUI system
if [ -n "$DISPLAY" ]; then
    echo "Attempting to open documentation in default browser..."
    if command -v xdg-open > /dev/null; then
        xdg-open docs/_build/html/index.html
    elif command -v open > /dev/null; then
        open docs/_build/html/index.html
    fi
fi