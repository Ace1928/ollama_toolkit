"""
Test package for the ollama_toolkit package.

This package contains comprehensive tests for all ollama_toolkit functionality.
"""

# Import test modules for direct access
try:
    from .test_client import TestOllamaClient
    from .test_chat import TestChat  
    from .test_embedding import TestEmbeddings
    from .test_utils import TestUtils
    from .test_coverage import TestCodeCoverage
    
    # Make test modules directly importable
    from . import test_client
    from . import test_chat
    from . import test_embedding
    from . import test_utils
    from . import test_coverage
    from . import test_nexus
    from . import conftest
    
    __all__ = [
        # Test classes
        "TestOllamaClient",
        "TestChat",
        "TestEmbeddings",
        "TestUtils",
        "TestCodeCoverage",
        
        # Test modules
        "test_client",
        "test_chat", 
        "test_embedding",
        "test_utils",
        "test_coverage",
        "test_nexus",
        "conftest",
    ]
    
except ImportError as e:
    import logging
    logging.debug(f"Some test modules couldn't be imported: {e}")
    
    __all__ = []
