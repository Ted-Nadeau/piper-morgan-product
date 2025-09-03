"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture
def mock_async_session():
    """Provide a mock async session for tests that need it"""
    return AsyncMock()
