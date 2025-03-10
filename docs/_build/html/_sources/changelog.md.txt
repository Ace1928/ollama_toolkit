# Changelog

A detailed record of changes to the Ollama Toolkit, following Eidosian principles of recursive refinement and self-awareness.

## 0.1.9 (Current)

- Ensured all documentation references align with client version 0.1.9.
- Clarified minimum recommended Ollama server version is 0.1.11.
- Enhanced embedding operations with batch processing.
- Comprehensive error handling documentation.
- Model management interface for custom model creation.
- CLI support for all new features.
- Async context manager support.
- Complete API documentation including all endpoints.
- New utility functions for model handling.
- Extended examples for all API capabilities.
- Expanded test coverage to 95%.

### Changed
- Improved async support with proper exception handling
- Better fallback mechanisms for model availability
- Updated default models to latest recommendations
- Optimized streaming response handling
- Enhanced documentation with Eidosian principles

### Fixed
- Resolved connection timeout issues with large models
- Fixed race conditions in streaming response handling
- Corrected error messages for improved clarity
- Addressed Windows-specific path handling issues
- Improved error recovery for interrupted operations

## 0.1.7

### Added
- Comprehensive error handling and model fallbacks
- Added support for multimodal models
- Extended CLI functionality
- Implemented caching system foundations

### Changed
- Refined exception hierarchy for better error handling
- Updated documentation with additional examples
- Improved installation process

### Fixed
- Corrected streaming response handling
- Fixed model downloading progress reporting

## 0.1.6

### Added
- Introduced caching for API responses
- Added optimization for embedding operations
- Support for system prompts in generation
- Basic CLI tool implementation

### Changed
- Improved response handling for streaming responses
- Enhanced error messages
- Updated examples with more practical use cases

### Fixed
- Fixed handling of large context windows
- Corrected embedding dimension handling

## 0.1.5

### Added
- Initial public release
- Basic client functionality for generation, chat, and embeddings
- Support for model management (list, pull, delete)
- Synchronous API with limited async support

### Changed
- First stable API design

### Fixed
- Initial stability improvements
