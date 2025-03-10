#!/usr/bin/env python3
"""
Ollama Forge Module Execution Point

This module serves as the direct execution entry point when the package is run with:
`python -m ollama_forge`

Following Eidosian principles of:
- Contextual Integrity: Every component has a precise purpose
- Flow Like a River: Seamless execution path
- Structure as Control: Clear organization and responsibility delegation
"""

import sys
from typing import List, Optional

from .cli import main


def module_entry(args: Optional[List[str]] = None) -> int:
    """
    Pure entry point function for programmatic control.
    
    Args:
        args: Command line arguments (uses sys.argv if None)
        
    Returns:
        Exit code (0 for success)
    """
    return main(args)


if __name__ == "__main__":
    sys.exit(module_entry())
