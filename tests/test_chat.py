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

    @pytest.mark.xfail(reason="Known issue with mock setup")
    @patch("requests.post")
    def test_chat_with_fallback(self, mock_post: Any) -> None:
        """Test chat fallback mechanism."""

        # Setup mock responses for primary and backup model calls
        def mock_side_effect(*args, **kwargs):
            url = args[0] if args else kwargs.get("url", "")
            if kwargs.get("json", {}).get("model") == DEFAULT_CHAT_MODEL:
                # Primary model request - make raise_for_status throw an exception
                # instead of having iter_lines throw it
                mock_resp = Mock()
                mock_resp.raise_for_status.side_effect = Exception(
                    "Model not available"
                )
                return mock_resp
            else:
                # Backup model request - return successful response
                mock_resp = Mock()
                mock_resp.iter_lines.return_value = [
                    json.dumps(
                        {
                            "message": {
                                "role": "assistant",
                                "content": "Backup model response",
                            },
                            "done": True,
                        }
                    ).encode(),
                ]
                mock_resp.raise_for_status = Mock()  # No exception for backup model
                return mock_resp

        # Configure the mock post function
        mock_post.side_effect = mock_side_effect

        # Call function with fallback enabled
        result = chat(DEFAULT_CHAT_MODEL, self.test_messages.copy(), use_fallback=True)

        # Assert results - should get backup model result
        self.assertIsNotNone(result)
        self.assertEqual(result["message"]["content"], "Backup model response")
        self.assertEqual(
            mock_post.call_count, 2
        )  # Called twice: once for primary, once for backup

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
