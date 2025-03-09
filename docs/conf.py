# Configuration file for the Sphinx documentation builder

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Add project root to path

# Project information
project = 'Ollama Toolkit'
copyright = '2025, Lloyd Handyside'
author = 'Lloyd Handyside'
release = '0.1.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',  # Automatically generate API documentation
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx.ext.napoleon',  # Support for Google-style docstrings
'sphinx.ext.coverage',  # Check documentation coverage
    'myst_parser',  # Add this line
]

# HTML output settings
html_theme = 'sphinx_rtd_theme'  # Use the default Alabaster theme
html_static_path = ['_static']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Other settings
autodoc_member_order = 'bysource'

# Configure myst-parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "fieldlist",
]

# Enable Markdown files to be included
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Other settings
autodoc_member_order = 'bysource'
