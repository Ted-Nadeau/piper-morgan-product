"""
Unit tests for FirstMeetingDetector.

Issue #490: FTUX-PORTFOLIO
Phase 1: First-Meeting Detection

Tests:
- test_detects_empty_projects_state: Triggers when user has 0 projects
- test_skips_when_projects_exist: Does not trigger when user has projects
- test_handles_database_error_gracefully: Fails safe on database errors
- test_respects_decline_flag: Does not trigger when user has declined
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.onboarding.first_meeting_detector import FirstMeetingDetector


@pytest.fixture
def mock_project_repository():
    """Create a mock ProjectRepository."""
    repo = MagicMock()
    repo.count_active_projects = AsyncMock(return_value=0)
    return repo


@pytest.fixture
def detector(mock_project_repository):
    """Create a FirstMeetingDetector with mocked dependencies."""
    return FirstMeetingDetector(
        project_repository=mock_project_repository,
        user_preferences={},
    )


class TestFirstMeetingDetector:
    """Tests for FirstMeetingDetector."""

    @pytest.mark.asyncio
    async def test_detects_empty_projects_state(self, detector, mock_project_repository):
        """
        When user has 0 projects, should_trigger returns True.

        This is the primary use case - a new user with no projects
        should be offered portfolio onboarding.
        """
        # Arrange
        mock_project_repository.count_active_projects.return_value = 0
        user_id = "user-123"

        # Act
        result = await detector.should_trigger(user_id)

        # Assert
        assert result is True
        mock_project_repository.count_active_projects.assert_called_once_with(owner_id=user_id)

    @pytest.mark.asyncio
    async def test_skips_when_projects_exist(self, detector, mock_project_repository):
        """
        When user has 1+ projects, should_trigger returns False.

        Users who already have projects don't need onboarding.
        """
        # Arrange
        mock_project_repository.count_active_projects.return_value = 3
        user_id = "user-with-projects"

        # Act
        result = await detector.should_trigger(user_id)

        # Assert
        assert result is False
        mock_project_repository.count_active_projects.assert_called_once_with(owner_id=user_id)

    @pytest.mark.asyncio
    async def test_handles_database_error_gracefully(self, detector, mock_project_repository):
        """
        When database error occurs, should_trigger returns False (fail safe).

        We don't want to annoy users with onboarding prompts if we can't
        verify their project count due to a database error.
        """
        # Arrange
        mock_project_repository.count_active_projects.side_effect = Exception(
            "Database connection failed"
        )
        user_id = "user-456"

        # Act
        result = await detector.should_trigger(user_id)

        # Assert
        assert result is False  # Fail safe - don't trigger on error

    @pytest.mark.asyncio
    async def test_respects_decline_flag(self, mock_project_repository):
        """
        When user has previously declined onboarding, should_trigger returns False.

        Users who said "no thanks" should not be prompted again.
        """
        # Arrange
        user_preferences = {"portfolio_onboarding_declined": True}
        detector = FirstMeetingDetector(
            project_repository=mock_project_repository,
            user_preferences=user_preferences,
        )
        user_id = "user-who-declined"

        # Act
        result = await detector.should_trigger(user_id)

        # Assert
        assert result is False
        # Should not even check project count if user declined
        mock_project_repository.count_active_projects.assert_not_called()


class TestFirstMeetingDetectorMarkDeclined:
    """Tests for the mark_declined functionality."""

    def test_mark_declined_updates_preferences(self, detector):
        """
        mark_declined should update user preferences to prevent future triggers.
        """
        # Arrange
        user_id = "user-declining"

        # Act
        detector.mark_declined(user_id)

        # Assert
        assert detector.user_preferences.get("portfolio_onboarding_declined") is True

    @pytest.mark.asyncio
    async def test_declined_user_not_triggered_after_marking(self, mock_project_repository):
        """
        After mark_declined is called, should_trigger should return False.
        """
        # Arrange
        detector = FirstMeetingDetector(
            project_repository=mock_project_repository,
            user_preferences={},
        )
        user_id = "user-declining"
        mock_project_repository.count_active_projects.return_value = 0

        # Verify they would be triggered before declining
        assert await detector.should_trigger(user_id) is True

        # Act - user declines
        detector.mark_declined(user_id)

        # Assert - should not be triggered anymore
        assert await detector.should_trigger(user_id) is False
