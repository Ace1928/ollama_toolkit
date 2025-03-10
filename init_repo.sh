#!/usr/bin/env bash
# Initialize ollama_api as a standalone Git repository

set -e  # Exit on error

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}  Ollama API Repository Initializer  ${NC}"
echo -e "${BLUE}====================================${NC}"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Check if the current directory is already a Git repository
if [ -d ".git" ]; then
    echo -e "${YELLOW}This directory is already a Git repository.${NC}"
    read -p "Do you want to reinitialize? This will remove the existing .git directory. (y/N) " CONFIRM
    if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
        echo -e "${YELLOW}Operation canceled.${NC}"
        exit 0
    fi
    
    rm -rf .git
    echo -e "${GREEN}Existing Git repository removed.${NC}"
fi

# Initialize a new Git repository
echo -e "\n${BLUE}Initializing new Git repository...${NC}"
git init
echo -e "${GREEN}Git repository initialized.${NC}"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "\n${BLUE}Creating .gitignore file...${NC}"
    cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# Project specific
.env
wheelhouse/
EOL
    echo -e "${GREEN}.gitignore file created.${NC}"
fi

# Add files to Git
echo -e "\n${BLUE}Adding files to Git...${NC}"
git add .
echo -e "${GREEN}Files added to Git.${NC}"

# Create initial commit with GPG signing
echo -e "\n${BLUE}Creating initial commit...${NC}"
git commit -S -m "Initial commit of ollama_api"
echo -e "${GREEN}Initial commit created.${NC}"

# Ask for remote repository URL
echo -e "\n${BLUE}Setting up remote repository...${NC}"
read -p "Enter your GitHub repository URL (e.g. https://github.com/Ace1928/ollama_api.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo -e "${YELLOW}No repository URL provided. Skipping remote setup.${NC}"
else
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}Remote 'origin' added: $REPO_URL${NC}"
    
    read -p "Do you want to push to this remote repository now? (y/N) " PUSH_CONFIRM
    if [[ "$PUSH_CONFIRM" == "y" || "$PUSH_CONFIRM" == "Y" ]]; then
        echo -e "${BLUE}Pushing to remote repository...${NC}"
        git push -u origin main || git push -u origin master
        echo -e "${GREEN}Push completed.${NC}"
    else
        echo -e "${YELLOW}Push skipped. You can push later with 'git push -u origin main'.${NC}"
    fi
fi

echo -e "\n${GREEN}Repository initialization complete!${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. If you're working within a larger repository, add this directory to the parent's .gitignore"
echo -e "2. Run 'git status' to verify your repository state"
echo -e "3. Run 'git remote -v' to verify your remote repository settings"
echo -e "4. Development workflow: modify code → git add → git commit → git push"
echo -e "\n${GREEN}Happy coding!${NC}"

# Make the script executable
chmod +x init_repo.sh
