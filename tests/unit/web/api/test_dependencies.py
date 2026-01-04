"""Unit tests for web/api/dependencies.py - ServiceContainer dependency injection.

Issue #322: ARCH-FIX-SINGLETON
These tests verify the get_container() dependency injection function works correctly
for horizontal scaling support.

Test Coverage:
1. Container retrieval from app.state (happy path)
2. HTTPException 503 when container not in app.state
3. HTTPException 503 when container is None
4. Container is properly returned for use
"""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from web.api.dependencies import get_container


class TestGetContainer:
    """Tests for get_container() dependency injection function."""

    def test_returns_container_from_app_state(self):
        """Should return container when available in app.state."""
        # Arrange
        mock_container = MagicMock()
        mock_container.is_initialized.return_value = True

        mock_request = MagicMock()
        mock_request.app.state.service_container = mock_container

        # Act
        result = get_container(mock_request)

        # Assert
        assert result is mock_container

    def test_raises_503_when_service_container_not_in_state(self):
        """Should raise HTTPException 503 when service_container not in app.state."""
        # Arrange
        mock_request = MagicMock()
        # Simulate missing service_container attribute
        del mock_request.app.state.service_container

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_container(mock_request)

        assert exc_info.value.status_code == 503
        assert "not initialized" in exc_info.value.detail

    def test_raises_503_when_container_is_none(self):
        """Should raise HTTPException 503 when container is None."""
        # Arrange
        mock_request = MagicMock()
        mock_request.app.state.service_container = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_container(mock_request)

        assert exc_info.value.status_code == 503
        assert "None" in exc_info.value.detail

    def test_container_can_access_services(self):
        """Should return a container that can be used to access services."""
        # Arrange
        mock_service = MagicMock()
        mock_container = MagicMock()
        mock_container.get_service.return_value = mock_service

        mock_request = MagicMock()
        mock_request.app.state.service_container = mock_container

        # Act
        container = get_container(mock_request)
        service = container.get_service("llm")

        # Assert
        mock_container.get_service.assert_called_once_with("llm")
        assert service is mock_service

    def test_does_not_create_new_container(self):
        """Should NOT create a new container, only retrieve from app.state.

        This is critical for horizontal scaling - we must use the application-scoped
        container, not create new ones per request.
        """
        # Arrange
        mock_container = MagicMock()
        mock_request = MagicMock()
        mock_request.app.state.service_container = mock_container

        # Act
        result1 = get_container(mock_request)
        result2 = get_container(mock_request)

        # Assert - both calls should return the same container
        assert result1 is mock_container
        assert result2 is mock_container
        assert result1 is result2


class TestGetContainerIntegrationPattern:
    """Tests verifying the pattern works with FastAPI Depends().

    These tests simulate how get_container will be used in actual routes.
    """

    def test_pattern_matches_existing_standup_route(self):
        """Verify our pattern matches what standup.py already does.

        standup.py uses:
            container = request.app.state.service_container

        Our get_container() should be a drop-in replacement.
        """
        # Arrange - simulate what standup.py does
        mock_container = MagicMock()
        mock_request = MagicMock()
        mock_request.app.state.service_container = mock_container

        # Old pattern (from standup.py)
        old_pattern_result = mock_request.app.state.service_container

        # New pattern (our DI function)
        new_pattern_result = get_container(mock_request)

        # Assert - both patterns should return the same container
        assert old_pattern_result is new_pattern_result
