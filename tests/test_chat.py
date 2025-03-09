#!/usr/bin/env python3
"""
Tests for the chat functionality.
"""

import json
import os
import sys
import unittest
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest
import requests

# Add the parent directory to the path before any import attempts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Now try imports
try:
    from ollama_toolkit.examples.chat_example import chat, chat_streaming, initialize_chat
    from ollama_toolkit.utils.model_constants import (
        BACKUP_CHAT_MODEL,
        DEFAULT_CHAT_MODEL,
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you've installed the package with: pip install -e .")
    sys.exit(1)


class TestChat(unittest.TestCase):
    """Test cases for chat functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_messages = [{"role": "user", "content": "Hello!"}]

    @patch("requests.post")
    def test_chat_function(self, mock_post: Any) -> None:
        """Test the chat function with non-streaming response."""
        # Setup mock
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            json.dumps(
                {
                    "message": {"role": "assistant", "content": "Hello there!"},
                    "done": True,
                }
            ).encode(),
        ]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Call function with test messages
        result = chat(DEFAULT_CHAT_MODEL, self.test_messages.copy())

        # Assert results
        mock_post.assert_called_once()
        self.assertEqual(result["message"]["content"], "Hello there!")
        self.assertEqual(len(self.test_messages), 1)  # Original list unchanged

    @patch("requests.post")
    def test_chat_with_fallback(self, mock_post: Any) -> None:
        """Test chat fallback mechanism."""
        # Create two different response objects
        primary_response = Mock()
        primary_response.raise_for_status.side_effect = requests.exceptions.RequestException("Model not available")
        
        backup_response = Mock()
        backup_response.raise_for_status = Mock()  # No exception
        backup_response.raise_for_status = Mock()  # No exception
        backup_response.iter_lines.return_value = [
            json.dumps(
                {
                    "message": {
                        "role": "assistant", 
                        "content": "Backup model response"
                    },
                    "done": True
                }
            ).encode()
        ]
        
        # Configure mock to return different responses based on which call it is
        mock_post.side_effect = [primary_response, backup_response]
        
        # Call function with fallback enabled
        result = chat(DEFAULT_CHAT_MODEL, self.test_messages.copy(), use_fallback=True)
        
        # Assert results
        self.assertIsNotNone(result)
        self.assertEqual(result["message"]["content"], "Backup model response")
        self.assertEqual(mock_post.call_count, 2)  # Called twice: primary then backup

    @patch("requests.post")
    def test_chat_streaming(self, mock_post: Any) -> None:
        """Test streaming chat functionality."""
        # Setup mock
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            json.dumps(
                {
                    "message": {"role": "assistant", "content": "Hello"},
                }
            ).encode(),
            json.dumps(
                {
                    "message": {"role": "assistant", "content": " there"},
                }
            ).encode(),
            json.dumps(
                {"message": {"role": "assistant", "content": "!"}, "done": True}
            ).encode(),
        ]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Call function with test messages
        success, response = chat_streaming(
            DEFAULT_CHAT_MODEL, self.test_messages.copy()
        )

        # Assert results
        self.assertTrue(success)
        self.assertEqual(response["content"], "Hello there!")
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_chat_streaming_failure(self, mock_post: Any) -> None:
        """Test streaming chat failure handling."""
        # Setup the exception side effect properly
        mock_post.side_effect = Exception("Connection error")

        # Call function with test messages
        success, response = chat_streaming(
            DEFAULT_CHAT_MODEL, self.test_messages.copy()
        )

        # Assert results - should fail gracefully
        self.assertFalse(success)
        self.assertIsNone(response)
        self.assertEqual(mock_post.call_count, 2)  # Called twice: once for primary, once for fallback

    def test_initialize_chat(self) -> None:
        """Test chat initialization."""
        # Test with system message
        system_msg = "You are a helpful assistant."
        messages = initialize_chat(DEFAULT_CHAT_MODEL, system_msg)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], system_msg)

        # Test without system message
        messages = initialize_chat(DEFAULT_CHAT_MODEL)
        self.assertEqual(len(messages), 0)


if __name__ == "__main__":
    unittest.main()
