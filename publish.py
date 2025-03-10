#!/usr/bin/env python3
"""
Script for publishing the package to PyPI.
This script builds the package and uploads it to PyPI.

Following Eidosian principles:
- Contextual Integrity: Each function serves a precise purpose
- Self-Awareness as Foundation: Built-in validation and verification
- Exhaustive But Concise: Complete without redundancy
- Flow Like a River: Operations flow seamlessly
"""

import os
import subprocess
import sys
import argparse
import shutil
from datetime import datetime
from typing import List, Optional, Tuple
from version import update_version_universally, get_version_string

def run_command(cmd: List[str], check: bool = True) -> Tuple[bool, str]:
    """Run a command and return success status and output.
    
    Args:
        cmd: Command to run as list of strings
        check: Whether to exit on failure
        
    Returns:
        Tuple of (success, output)
    """
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        success = result.returncode == 0
        output = result.stdout if success else result.stderr
        
        if not success and check:
            print(f"Command failed with exit code {result.returncode}")
            print(f"Error: {output}")
            sys.exit(result.returncode)
        
        return success, output
    except Exception as e:
        if check:
            print(f"Failed to execute command: {e}")
            sys.exit(1)
        return False, str(e)

def clean_previous_builds() -> None:
    """Clean previous build artifacts with proper error handling."""
    print("Cleaning previous build artifacts...")
    directories = ["build", "dist", "ollama_forge.egg-info"]
    for directory in directories:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"✓ Removed {directory}")
            except Exception as e:
                print(f"! Warning: Could not remove {directory}: {e}")

def verify_package_integrity() -> bool:
    """Perform pre-publish verification checks.
    
    Returns:
        bool: True if all checks passed
    """
    print("\n📋 Verifying package integrity...")
    checks_passed = True
    
    # Check for required files
    required_files = ["README.md", "LICENSE", "pyproject.toml", "setup.py", "setup.cfg"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            checks_passed = False
        else:
            print(f"✓ Found required file: {file}")
            
    # Check for package importability
    try:
        sys.path.insert(0, os.path.abspath("."))
        import ollama_forge
        print(f"✓ Package imports correctly (version {ollama_forge.__version__})")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        checks_passed = False
    
    # Check for build config consistency
    try:
        with open("pyproject.toml", "r") as f:
            pyproject = f.read()
        with open("setup.cfg", "r") as f:
            setupcfg = f.read()
            
        # Verify package name is consistent
        if "name = \"ollama-forge\"" in pyproject and "name = ollama_forge" not in setupcfg:
            print("⚠️ Package name inconsistency between pyproject.toml and setup.cfg")
            checks_passed = False
    except Exception as e:
        print(f"❌ Failed to check config consistency: {e}")
        checks_passed = False
    
    return checks_passed

def backup_important_files() -> None:
    """Create backups of important files before making changes."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = f".backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    important_files = ["pyproject.toml", "setup.cfg", "setup.py", "version.py"]
    for file in important_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(backup_dir, file))
    
    print(f"📦 Created backups in {backup_dir}")

def main() -> None:
    """Main entry point with enhanced error handling and validation."""
    parser = argparse.ArgumentParser(description="Publish the package to PyPI.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without publishing.")
    parser.add_argument("--test", action="store_true", help="Publish to TestPyPI instead of PyPI.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests.")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🚀 Starting package publishing process...")
    print(f"📍 Working directory: {os.getcwd()}")
    
    # Create backups
    backup_important_files()
    
    # Check git status
    changed = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
    if changed.returncode != 0:
        confirm = input("📝 Uncommitted changes detected. Bump version? [y/N]: ").strip().lower()
        if confirm == "y":
            current_version = get_version_string()
            print(f"Current version: {current_version}")
            new_version = input("Enter new version (e.g. 0.2.0): ").strip()
            
            if new_version == current_version:
                print("❗ New version is the same as current version. No change needed.")
            else:
                update_version_universally(new_version)
                
                changed_after = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
                if changed_after.returncode != 0:
                    subprocess.run(["git", "add", "."])
                    commit_msg = f"Bump version to {new_version}"
                    subprocess.run(["git", "commit", "-m", commit_msg])
                    print(f"✓ Committed version bump to {new_version}")
                    
                    # Ask about pushing to remote
                    if input("Push changes to remote? [y/N]: ").strip().lower() == "y":
                        subprocess.run(["git", "push"])
                        print("✓ Pushed changes to remote")
                else:
                    print("No changes detected after version update, skipping commit.")
    
    # Verify package integrity
    if not verify_package_integrity():
        if input("❌ Package integrity checks failed. Continue anyway? [y/N]: ").strip().lower() != "y":
            print("Aborting publication process.")
            return
    
    # Clean previous build artifacts
    clean_previous_builds()
    
    # Run tests
    if not args.skip_tests:
        print("\n🧪 Running tests...")
        test_cmd = ["python", "-m", "pytest", "tests"]
        success, output = run_command(test_cmd, check=False)
        
        if not success:
            print("⚠️ Some tests failed!")
            print(output)
            if input("Continue despite test failures? [y/N]: ").strip().lower() != "y":
                print("Aborting publication process.")
                return
    else:
        print("\n⏭️ Skipping tests as requested.")
    
    if args.dry_run:
        print("\n🔍 Dry run completed. Skipping actual build and publishing.")
        return
    
    # Build package
    print("\n🏗️ Building the package...")
    build_cmd = ["python", "-m", "build"]
    run_command(build_cmd)
    
    # Verify built package
    print("\n🔍 Verifying built package...")
    twine_check_cmd = ["twine", "check", "dist/*"]
    success, output = run_command(twine_check_cmd, check=False)
    if not success:
        print(f"⚠️ Twine check reported issues:\n{output}")
        if input("Continue despite twine check issues? [y/N]: ").strip().lower() != "y":
            print("Aborting publication process.")
            return
    else:
        print("✅ Package passed twine check!")
    
    # Build documentation
    print("\n📚 Building package documentation...")
    if os.path.exists("build_docs.sh"):
        run_command(["bash", "build_docs.sh"])
    else:
        print("⚠️ build_docs.sh not found, skipping documentation build.")
    
    # Upload to PyPI/TestPyPI
    if args.test:
        print("\n🧪 Uploading to TestPyPI...")
        pypi_cmd = ["python", "-m", "twine", "upload", "--repository-url", "https://test.pypi.org/legacy/", "dist/*"]
    else:
        print("\n🌐 Uploading to PyPI...")
        pypi_cmd = ["python", "-m", "twine", "upload", "dist/*"]
    
    # Final confirmation
    target = "TestPyPI" if args.test else "PyPI"
    if input(f"Ready to upload to {target}. Proceed? [y/N]: ").strip().lower() != "y":
        print("Aborting upload process.")
        return
        
    run_command(pypi_cmd)
    
    print("\n✨ Package published successfully! ✨")
    print(f"Package: ollama-forge v{get_version_string()}")
    print(f"Repository: {'Test PyPI' if args.test else 'PyPI'}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Publication process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
