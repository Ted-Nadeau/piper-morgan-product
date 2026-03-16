"""
Tests for Issue #902: Reopen issue functionality and close issue fallback fix.

Covers:
- Pre-classifier patterns for close and reopen
- Reopen handler: mock GitHubIntegrationRouter, verify state="open"
- Close handler still works
- Fallback messages are helpful, not misleading
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """Create IntentService instance for testing"""
    with patch("services.intent.intent_service.OrchestrationEngine"):
        with patch("services.intent.intent_service.LearningHandler"):
            with patch(
                "services.intent.intent_service.ConversationKnowledgeGraphIntegration"
            ):
                service = IntentService()
                return service


@pytest.fixture
def fallback_service():
    """Lightweight IntentService for sync fallback testing (no __init__)."""
    return IntentService.__new__(IntentService)


# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestPreClassifierClosePatterns:
    """Verify close issue patterns still classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "close issue #123",
            "close issue 456",
            "close the completed issue",
            "please close issue #789",
        ],
    )
    def test_close_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\bclose issue\s*#?\d+\b",
                r"\bclose.*completed.*issue\b",
                r"\bclose.*issue\b",
            ],
        )
        assert result is True


class TestPreClassifierReopenPatterns:
    """Verify reopen issue patterns classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "reopen issue #456",
            "reopen issue 789",
            "re-open issue #789",
            "reopen the closed issue",
            "re-open that issue",
        ],
    )
    def test_reopen_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\breopen\s+issue\s*#?\d+\b",
                r"\bre-open\s+issue\s*#?\d+\b",
                r"\breopen\s+.*issue\b",
                r"\bre-open\s+.*issue\b",
            ],
        )
        assert result is True


# ---------------------------------------------------------------------------
# Reopen handler tests
# ---------------------------------------------------------------------------


class TestReopenIssueHandler:
    """Test _handle_reopen_issue_query handler."""

    @pytest.mark.asyncio
    async def test_reopens_issue_with_state_open(self, intent_service):
        """Verify the handler passes state='open' to update_issue."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        mock_updated_issue = {
            "number": 42,
            "title": "Add search feature",
            "state": "open",
            "html_url": "https://github.com/org/repo/issues/42",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(return_value=mock_updated_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(
                intent, "workflow-id"
            )

            assert result.success is True
            assert "Successfully reopened issue #42" in result.message
            assert "Add search feature" in result.message
            assert result.intent_data["issue_number"] == 42

            # The critical assertion: state="open"
            mock_router.update_issue.assert_awaited_once_with(
                "piper-morgan-product", 42, state="open"
            )

    @pytest.mark.asyncio
    async def test_reopen_missing_issue_number(self, intent_service):
        """Test handling when no issue number is present."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen that issue"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(
                intent, "workflow-id"
            )

            assert result.success is False
            assert "couldn't find an issue number" in result.message
            assert result.requires_clarification is True

    @pytest.mark.asyncio
    async def test_reopen_github_not_configured(self, intent_service):
        """Test graceful message when GitHub is not configured."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(
                intent, "workflow-id"
            )

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_reopen_handles_github_error(self, intent_service):
        """Test error handling for GitHub API failures."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(
                side_effect=Exception("GitHub API error")
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(
                intent, "workflow-id"
            )

            assert result.success is False
            assert "reopening that issue" in result.message.lower() or "error" in result.message.lower()


# ---------------------------------------------------------------------------
# Close handler still-works test
# ---------------------------------------------------------------------------


class TestCloseIssueHandlerStillWorks:
    """Verify close handler is unbroken by the reopen changes."""

    @pytest.mark.asyncio
    async def test_close_still_passes_state_closed(self, intent_service):
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        mock_updated_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "closed",
            "html_url": "https://github.com/org/repo/issues/123",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(return_value=mock_updated_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(
                intent, "workflow-id"
            )

            assert result.success is True
            assert "Successfully closed issue #123" in result.message
            mock_router.update_issue.assert_awaited_once_with(
                "piper-morgan-product", 123, state="closed"
            )


# ---------------------------------------------------------------------------
# Fallback message tests
# ---------------------------------------------------------------------------


class TestFallbackMessages:
    """Test that fallback messages are helpful, not misleading."""

    def test_close_fallback_says_can_not_cant(self, fallback_service):
        """Close fallback should say 'I can close issues!' not 'I can't'."""
        result = fallback_service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="close that completed issue",
        )
        assert "I can close issues!" in result
        assert "can't close" not in result

    def test_reopen_fallback_says_can(self, fallback_service):
        """Reopen fallback should say 'I can reopen issues!'."""
        result = fallback_service._get_contextual_fallback(
            mapped_action="reopen_issue",
            original_message="reopen the issue we discussed",
        )
        assert "I can reopen issues!" in result
        assert "can't" not in result

    def test_close_fallback_suggests_issue_number(self, fallback_service):
        result = fallback_service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="close the issue",
        )
        assert "#123" in result  # suggests format

    def test_reopen_fallback_suggests_issue_number(self, fallback_service):
        result = fallback_service._get_contextual_fallback(
            mapped_action="reopen_issue",
            original_message="reopen that issue",
        )
        assert "#123" in result  # suggests format
