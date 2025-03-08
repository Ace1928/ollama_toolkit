#!/usr/bin/env python3
"""
Centralized test runner for the Ollama Toolkit client.

This script discovers and runs all tests in the tests directory.
It can be run directly or through pytest.
"""

import argparse
import os
import sys
import unittest
from typing import List, Optional

import pytest  # Add pytest import

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def run_all_tests(
    verbosity: int = 2,
    pattern: str = "test_*.py",
    ignore: Optional[List[str]] = None,
    use_pytest: bool = False,
) -> bool:
    """
    Discover and run all tests matching the pattern.

    Args:
        verbosity: The verbosity level for test output
        pattern: The file pattern to match for test discovery
        ignore: List of test files to ignore
        use_pytest: Whether to use pytest for running tests

    Returns:
        True if all tests passed, False otherwise
    """
    # Print header
    print("\n" + "=" * 80)
    print(f"OLLAMA API TEST NEXUS".center(80))
    print(f"Discovering tests with pattern: {pattern}".center(80))
    print("=" * 80 + "\n")

    # Get the directory containing this file
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Add option to use pytest directly
    if use_pytest:
        pytest_args = ["-xvs", test_dir]
        if ignore:
            for ign in ignore:
                pytest_args.extend(["-k", f"not {ign}"])
        return pytest.main(pytest_args) == 0
    else:
        # Create a test loader
        loader = unittest.TestLoader()

        # Discover all test modules
        all_tests = loader.discover(test_dir, pattern=pattern)

        # Filter out ignored tests if specified
        if ignore:
            filtered_tests = unittest.TestSuite()
            for test in all_tests:
                for module_tests in test:
                    module_name = module_tests.__class__.__module__
                    if not any(ignored in module_name for ignored in ignore):
                        filtered_tests.addTest(module_tests)
            all_tests = filtered_tests

        # Run the tests
        test_runner = unittest.TextTestRunner(verbosity=verbosity)
        result = test_runner.run(all_tests)

        # Print summary
        print("\n" + "=" * 80)
        test_count = result.testsRun
        fail_count = len(result.failures)
        error_count = len(result.errors)
        success_count = test_count - fail_count - error_count

        print(f"SUMMARY: Ran {test_count} tests".center(80))
        print(
            f"SUCCESS: {success_count} | FAILURES: {fail_count} | ERRORS: {error_count}".center(
                80
            )
        )
        print("=" * 80 + "\n")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0


def main() -> None:
    """Parse command line arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run all Ollama Toolkit tests")
    parser.add_argument(
        "--verbosity", "-v", type=int, default=2, help="Verbosity level (1-3)"
    )
    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        default="test_*.py",
        help="Pattern to match test files",
    )
    parser.add_argument(
        "--ignore",
        "-i",
        type=str,
        nargs="+",
        help="Test files to ignore (e.g., test_nexus.py)",
    )
    parser.add_argument(
        "--exit-code",
        "-e",
        action="store_true",
        help="Return non-zero exit code on test failure",
    )
    parser.add_argument(
        "--use-pytest", "-u", action="store_true", help="Use pytest for running tests"
    )

    args = parser.parse_args()

    # Default to ignoring this file to prevent recursion
    if args.ignore is None:
        args.ignore = ["test_nexus.py"]

    # Run all tests
    success = run_all_tests(args.verbosity, args.pattern, args.ignore, args.use_pytest)

    # Exit with appropriate code
    if args.exit_code and not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
