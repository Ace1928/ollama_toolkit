#!/usr/bin/env python3
"""
Script for publishing the package to PyPI.
This script builds the package and uploads it to PyPI.
"""

import os
import subprocess
import sys
from typing import List
# Import after fixing version.py to avoid the syntax error
from ollama_toolkit.version import update_version_universally

def run_command(cmd: List[str]) -> None:
    """Run a command and exit if it fails."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main() -> None:
    """Main entry point."""
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Starting package publishing process...")
    
    # Check if there are changes in the repo:
    changed = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
    if changed.returncode != 0:
        confirm = input("Uncommitted changes detected. Bump version? [y/N]: ").strip().lower()
        if confirm == "y":
            new_version = input("Enter new version (e.g. 0.2.0): ").strip()
            update_version_universally(new_version)

            # Check again if changes were actually made
            changed_after = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
            if changed_after.returncode != 0:
                subprocess.run(["git", "add", "."])
                subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
                subprocess.run(["git", "push"])
            else:
                print("No changes detected after version update, skipping commit.")
    
    # Clean build artifacts
    print("Cleaning previous build artifacts...")
    for directory in ["build", "dist", "ollama_toolkit.egg-info"]:
        if os.path.exists(directory):
            run_command(["rm", "-rf", directory])
    
    # Run tests
    print("Running tests...")
    run_command(["python", "-m", "pytest", "tests"])  # Updated path
    
    # Build the package
    print("Building the package...")
    run_command(["python", "-m", "build"])
    
    # Build package documentation
    print("Building package documentation...")
    subprocess.run(["bash", "build_docs.sh"], check=True)
    
    # Upload to PyPI using config from .pypirc
    print("Uploading to PyPI using credentials from .pypirc...")
    run_command(["python", "-m", "twine", "upload", "--config-file", "~/.pypirc", "dist/*"])
    
    print("Package published successfully!")

if __name__ == "__main__":
    main()
