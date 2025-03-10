#!/usr/bin/env bash
# Development environment setup script

set -e  # Exit on error

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Define paths
VENV_PATH="/home/lloyd/Development/eidos_venv"
PROJECT_PATH="/home/lloyd/Development/eidos/ollama_api"

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}  Ollama API Development Environment  ${NC}"
echo -e "${BLUE}====================================${NC}"

# Ensure virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}Creating central virtual environment at $VENV_PATH...${NC}"
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate the virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate" || { 
    echo -e "${RED}Failed to activate virtual environment. Exiting.${NC}"; 
    exit 1; 
}

# Install the package in development mode
echo -e "${BLUE}Installing package in development mode...${NC}"
pip install -e "$PROJECT_PATH[dev]" || {
    echo -e "${RED}Failed to install package. Check for errors above.${NC}"; 
    exit 1;
}

# Set up pre-commit hooks
if [ -f "$PROJECT_PATH/.pre-commit-config.yaml" ]; then
    echo -e "${BLUE}Setting up pre-commit hooks...${NC}"
    pre-commit install || echo -e "${YELLOW}Failed to set up pre-commit hooks. Continuing...${NC}"
fi

# Show environment info
echo -e "\n${GREEN}Development environment ready!${NC}"
echo -e "Virtual Environment: $VENV_PATH"
echo -e "Python Version: $(python --version)"
echo -e "Installed Packages:"
pip list | grep -E 'ollama|requests|aiohttp|pytest|black|isort|mypy'

echo -e "\n${YELLOW}Important:${NC}"
echo -e "1. This script should be sourced, not executed: source ./development.sh"
echo -e "2. Run tests with: pytest"
echo -e "3. Format code with: black ."
echo -e "4. Use ./init_repo.sh to initialize Git repository"
echo -e "5. Use ./update_parent_gitignore.sh to update .gitignore in parent repos"

# Export useful environment variables
export OLLAMA_API_DEV=1
export PYTHONPATH="$PROJECT_PATH:$PYTHONPATH"

echo -e "\n${GREEN}Happy coding!${NC}"
