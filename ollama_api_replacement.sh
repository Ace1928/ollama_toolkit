#!/bin/bash
# Navigate to the project root
cd /home/lloyd/Development/eidos/ollama_toolkit

# Recursively find and replace in all Python files, configs, and markdown
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.cfg" -o -name "*.toml" -o -name "MANIFEST.in" \) -exec sed -i 's/ollama_api/ollama_toolkit/g' {} \;
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.cfg" -o -name "*.toml" -o -name "MANIFEST.in" \) -exec sed -i 's/Ollama API/Ollama Toolkit/g' {} \;

# Rename any remaining directory structure
if [ -d "ollama_api.egg-info" ]; then
  mv ollama_api.egg-info ollama_toolkit.egg-info
fi

echo "Renaming complete. Please verify the changes."