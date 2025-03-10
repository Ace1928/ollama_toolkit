#!/usr/bin/env bash
# Build documentation for ollama_forge
# Following Eidosian principles of precision, structured flow, and self-awareness

set -e  # Exit on error

# Text colors for better feedback
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Documentation directory
DOCS_DIR="docs"
BUILD_DIR="${DOCS_DIR}/_build/html"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Ollama Forge Documentation Builder       ${NC}"
echo -e "${BLUE}============================================${NC}"

# Function to handle errors
error_handler() {
    echo -e "${RED}Error occurred at line $1${NC}"
    echo -e "${RED}Documentation build failed!${NC}"
    exit 1
}

# Set up error handling
trap 'error_handler $LINENO' ERR

# Navigate to script directory
cd "$(dirname "$0")" || {
    echo -e "${RED}Failed to navigate to script directory${NC}"
    exit 1
}

echo -e "${YELLOW}Working directory: $(pwd)${NC}"

# Create docs directory if it doesn't exist
if [ ! -d "$DOCS_DIR" ]; then
    echo -e "${YELLOW}Creating docs directory...${NC}"
    mkdir -p "$DOCS_DIR"
    echo -e "${GREEN}✓ Created docs directory${NC}"
fi

# Check requirements.txt exists
if [ ! -f "${DOCS_DIR}/requirements.txt" ]; then
    echo -e "${YELLOW}Creating docs/requirements.txt...${NC}"
    cat > "${DOCS_DIR}/requirements.txt" << EOF
sphinx>=4.0.0
sphinx-rtd-theme>=1.0.0
myst-parser>=0.15.0
sphinx-autobuild>=0.7.1
sphinx-copybutton>=0.3.1
sphinx-autodoc-typehints>=1.11.1
EOF
    echo -e "${GREEN}✓ Created docs/requirements.txt${NC}"
fi

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}✓ Removed previous build${NC}"
else
    echo -e "${GREEN}✓ No previous build to clean${NC}"
fi

# Install documentation dependencies
echo -e "${BLUE}Checking documentation dependencies...${NC}"
MISSING_DEPS=0
for pkg in sphinx myst-parser sphinx-rtd-theme sphinx-autobuild; do
    if ! pip show $pkg &> /dev/null; then
        MISSING_DEPS=1
        break
    fi
done  # Fixed: Added missing 'done' to close the for loop

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${YELLOW}Installing documentation dependencies...${NC}"
    pip install -r "${DOCS_DIR}/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ All dependencies already installed${NC}"
fi

# Check if conf.py exists
if [ ! -f "${DOCS_DIR}/conf.py" ]; then
    echo -e "${YELLOW}Warning: ${DOCS_DIR}/conf.py not found. Creating minimal configuration...${NC}"
    
    # Create a minimal conf.py
    cat > "${DOCS_DIR}/conf.py" << EOF
# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'Ollama Forge'
copyright = '2025, Lloyd Handyside, Eidos'  # Updated: Fixed to use just 2025
author = 'Lloyd Handyside, Eidos'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
]

# Add any paths that contain templates
templates_path = ['_templates']

# List of patterns to exclude
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Import package to get version
try:
    from version import get_version_string
    version = get_version_string()
    release = version
except ImportError:
    version = 'unknown'
    release = 'unknown'
EOF
    echo -e "${GREEN}✓ Created minimal conf.py${NC}"
fi

# Check if index.rst exists
if [ ! -f "${DOCS_DIR}/index.rst" ] && [ ! -f "${DOCS_DIR}/index.md" ]; then
    echo -e "${YELLOW}Warning: No index document found. Creating index.md...${NC}"
    
    # Create a minimal index.md
    cat > "${DOCS_DIR}/index.md" << EOF
# Ollama Forge Documentation

Welcome to the Ollama Forge documentation!

```{toctree}
:maxdepth: 2
:caption: Contents:

README
```

## Indices and tables

* {ref}\`genindex\`
* {ref}\`modindex\`
* {ref}\`search\`
EOF
    
    # Create a symlink to README.md in docs directory
    if [ ! -f "${DOCS_DIR}/README.md" ] && [ -f "README.md" ]; then
        ln -sf "../README.md" "${DOCS_DIR}/README.md"
        echo -e "${GREEN}✓ Linked README.md to docs directory${NC}"
    fi
    
    echo -e "${GREEN}✓ Created minimal index.md${NC}"
fi

# Build the documentation
echo -e "${BLUE}Building documentation...${NC}"
sphinx-build -b html "$DOCS_DIR" "$BUILD_DIR"
echo -e "${GREEN}✓ Documentation built successfully!${NC}"

# Check if build succeeded
if [ -f "${BUILD_DIR}/index.html" ]; then
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  Documentation built successfully!         ${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo -e "📁 Location: ${BUILD_DIR}/index.html"
    
    # Automatically open the documentation if on GUI system
    if [ -n "$DISPLAY" ]; then
        echo -e "${BLUE}Attempting to open documentation in default browser...${NC}"
        if command -v xdg-open > /dev/null; then
            xdg-open "${BUILD_DIR}/index.html"
            echo -e "${GREEN}✓ Documentation opened in browser${NC}"
        elif command -v open > /dev/null; then
            open "${BUILD_DIR}/index.html"
            echo -e "${GREEN}✓ Documentation opened in browser${NC}"
        else
            echo -e "${YELLOW}Could not open browser automatically.${NC}"
            echo -e "Please manually open: file://$(realpath ${BUILD_DIR}/index.html)"
        fi
    else
        echo -e "${YELLOW}No display detected. To view documentation, open:${NC}"
        echo -e "file://$(realpath ${BUILD_DIR}/index.html)"
    fi
else
    echo -e "${RED}Documentation build seems to have failed. Check errors above.${NC}"
    exit 1
fi

# Suggest additional steps
echo -e "\n${BLUE}Suggested next steps:${NC}"
echo -e "1. Review the generated documentation"
echo -e "2. Run 'python -m http.server --directory ${BUILD_DIR}' to serve docs locally"
echo -e "3. Consider publishing docs to ReadTheDocs"

exit 0