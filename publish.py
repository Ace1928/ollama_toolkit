#!/usr/bin/env python3
"""
Script for publishing the package to PyPI.
This script builds the package and uploads it to PyPI.
"""

import os
import subprocess
import sys
import argparse
from typing import List
from version import update_version_universally

def run_command(cmd: List[str]) -> None:
    """Run a command and exit if it fails."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Publish the package to PyPI.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without publishing.")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Starting package publishing process...")
    
    changed = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
    if changed.returncode != 0:
        confirm = input("Uncommitted changes detected. Bump version? [y/N]: ").strip().lower()
        if confirm == "y":
            new_version = input("Enter new version (e.g. 0.2.0): ").strip()
            update_version_universally(new_version)
            changed_after = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
            if changed_after.returncode != 0:
                subprocess.run(["git", "add", "."])
                subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
                subprocess.run(["git", "push"])
            else:
                print("No changes detected after version update, skipping commit.")
    
    print("Cleaning previous build artifacts...")
    for directory in ["build", "dist", "ollama_forge.egg-info"]:
        if os.path.exists(directory):
            run_command(["rm", "-rf", directory])
    
    print("Running tests...")
    run_command(["python", "-m", "pytest", "tests"])
    
    if args.dry_run:
        print("Dry run completed. Skipping publishing.")
        return
    
    print("Building the package...")
    run_command(["python", "-m", "build"])
    
    print("Building package documentation...")
    subprocess.run(["bash", "build_docs.sh"], check=True)
    
    print("Uploading to PyPI...")
    run_command(["python", "-m", "twine", "upload", "dist/*"])
    
    print("Package published successfully!")

if __name__ == "__main__":
    main()
