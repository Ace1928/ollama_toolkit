#!/usr/bin/env bash
# Activate the central eidos virtual environment

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Define the virtual environment path
VENV_PATH="/home/lloyd/Development/eidos_venv"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}Virtual environment not found at $VENV_PATH${NC}"
    echo -e "${BLUE}Creating new virtual environment...${NC}"
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate the virtual environment
echo -e "${BLUE}Activating virtual environment at $VENV_PATH${NC}"
source "$VENV_PATH/bin/activate"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Virtual environment activated successfully.${NC}"
    echo -e "Python path: $(which python)"
    echo -e "Python version: $(python --version)"
else
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install required packages
echo -e "${BLUE}Installing required packages...${NC}"
pip install -e "/home/lloyd/Development/eidos/ollama_api"

echo -e "${GREEN}Environment ready for development.${NC}"
echo -e "${YELLOW}Note: This script should be sourced, not executed:${NC}"
echo -e "  source ./activate_venv.sh"
