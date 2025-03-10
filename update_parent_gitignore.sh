#!/usr/bin/env bash
# Add ollama_api directory to eidos repository's .gitignore

set -e  # Exit on error

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}  Eidos Repo .gitignore Updater    ${NC}"
echo -e "${BLUE}====================================${NC}"

# Define paths explicitly
OLLAMA_DIR=$(pwd)
EIDOS_DIR="/home/lloyd/Development/eidos"
DEVELOPMENT_DIR="/home/lloyd/Development"

# Ensure we're in the right directory
if [[ "$OLLAMA_DIR" != *"/home/lloyd/Development/eidos/ollama_api"* ]]; then
    echo -e "${YELLOW}Warning: This script should be run from the ollama_api directory.${NC}"
    echo -e "${YELLOW}Current directory: $OLLAMA_DIR${NC}"
    read -p "Continue anyway? (y/N) " CONTINUE
    if [[ "$CONTINUE" != "y" && "$CONTINUE" != "Y" ]]; then
        echo -e "${RED}Operation canceled.${NC}"
        exit 1
    fi
fi

# Check if eidos directory exists
if [ ! -d "$EIDOS_DIR" ]; then
    echo -e "${RED}Eidos directory not found at $EIDOS_DIR${NC}"
    exit 1
fi

# Check if .gitignore exists in eidos directory
EIDOS_GITIGNORE="$EIDOS_DIR/.gitignore"

if [ ! -f "$EIDOS_GITIGNORE" ]; then
    echo -e "${YELLOW}No .gitignore file found in eidos repository.${NC}"
    echo -e "${BLUE}Creating new .gitignore file...${NC}"
    touch "$EIDOS_GITIGNORE"
    echo -e "${GREEN}.gitignore file created in eidos repository.${NC}"
fi

# Path to ignore (relative to eidos directory)
RELATIVE_PATH="ollama_api/"

# Check if the directory is already in .gitignore
if grep -q "^$RELATIVE_PATH" "$EIDOS_GITIGNORE"; then
    echo -e "${GREEN}Directory 'ollama_api/' is already ignored in eidos repository.${NC}"
else
    # Add the directory to .gitignore
    echo -e "\n# Ignore the ollama_api directory (managed as a separate Git repository)" >> "$EIDOS_GITIGNORE"
    echo "$RELATIVE_PATH" >> "$EIDOS_GITIGNORE"
    echo -e "${GREEN}Successfully added 'ollama_api/' to eidos repository's .gitignore.${NC}"
fi

# Also check if Development directory has a gitignore
DEVELOPMENT_GITIGNORE="$DEVELOPMENT_DIR/.gitignore"

if [ -f "$DEVELOPMENT_GITIGNORE" ]; then
    # Check if eidos/ollama_api is already in the Development .gitignore
    DEVELOPMENT_PATH="eidos/ollama_api/"
    if grep -q "^$DEVELOPMENT_PATH" "$DEVELOPMENT_GITIGNORE"; then
        echo -e "${GREEN}Directory 'eidos/ollama_api/' is already ignored in Development repository.${NC}"
    else
        echo -e "${BLUE}Adding 'eidos/ollama_api/' to Development .gitignore...${NC}"
        echo -e "\n# Ignore the ollama_api directory (managed as a separate Git repository)" >> "$DEVELOPMENT_GITIGNORE"
        echo "$DEVELOPMENT_PATH" >> "$DEVELOPMENT_GITIGNORE"
        echo -e "${GREEN}Successfully added to Development repository's .gitignore.${NC}"
    fi
fi

echo -e "${BLUE}Now the ollama_api directory will not be tracked by parent repositories.${NC}"
