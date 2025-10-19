"""
Morning Standup MVP - Test Suite
TDD Implementation following Excellence Flywheel methodology

Created: 2025-08-21 by Morning Standup MVP Mission
Tests first, then implementation
"""

import asyncio
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

# These imports will fail initially (TDD approach)
from services.features.morning_standup import MorningStandupWorkflow, StandupContext, StandupResult


@pytest.mark.asyncio
class TestMorningStandupWorkflow:
    """Test suite for MorningStandupWorkflow core functionality"""

    async def test_standup_workflow_initialization(self):
        """Test MorningStandupWorkflow initializes with required dependencies"""
        # Mock dependencies
        mock_preference_manager = Mock()
        mock_session_manager = Mock()
        mock_github_domain_service = Mock()

        # Initialize workflow
        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Verify initialization
        assert workflow.preference_manager == mock_preference_manager
        assert workflow.session_manager == mock_session_manager
        assert workflow.github_domain_service == mock_github_domain_service
        assert workflow.user_id == "xian"  # Default user

    async def test_generate_standup_for_user(self):
        """Test generating standup for specific user with persistent context"""
        # Setup mocks
        mock_preference_manager = AsyncMock()
        # Configure get_preference to return None (no preferences set)
        mock_preference_manager.get_preference.return_value = None

        mock_session_manager = AsyncMock()
        # Mock session context from yesterday
        mock_session_context = {
            "last_standup_date": "2025-08-20",
            "active_projects": ["piper-morgan"],
            "focus_areas": ["database-connectivity", "persistent-context"],
            "yesterday_work": ["database connectivity", "documentation audit"],
        }
        mock_session_manager.get_session_context.return_value = mock_session_context

        mock_github_domain_service = AsyncMock()
        mock_github_domain_service.get_recent_issues.return_value = []

        # Initialize workflow
        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify result structure
        assert isinstance(result, StandupResult)
        assert result.user_id == "xian"
        assert result.generated_at is not None
        assert result.generation_time_ms < 2000  # <2 seconds requirement
        assert len(result.yesterday_accomplishments) > 0 or len(result.today_priorities) > 0
        assert result.blockers is not None

        # Verify dependencies were called
        mock_session_manager.get_session_context.assert_called_once_with("xian")
        mock_github_domain_service.get_recent_issues.assert_called_once()

    async def test_context_persistence_integration(self):
        """Test integration with persistent context from yesterday's sessions"""
        # Mock preference manager with persistent context
        mock_preference_manager = AsyncMock()

        # Configure get_preference to return values directly (not coroutines)
        async def mock_get_preference(key, user_id=None):
            if key == "yesterday_context":
                return {"database": "resolved", "testing": "infrastructure-complete"}
            elif key == "active_repos":
                return ["piper-morgan-product"]
            elif key == "last_session_time":
                return "2025-08-20T17:30:00"
            return None

        mock_preference_manager.get_preference = mock_get_preference

        mock_session_manager = AsyncMock()
        mock_session_manager.get_session_context.return_value = {}

        mock_github_domain_service = AsyncMock()
        mock_github_domain_service.get_recent_issues.return_value = []

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify persistent context was used
        assert result.context_source == "persistent"
        assert result.generation_time_ms < 2000

    async def test_github_activity_integration(self):
        """Test GitHub activity retrieval and processing"""
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()

        # Configure preference manager mocks to return empty values
        mock_preference_manager.get_preference.side_effect = [
            {},  # yesterday_context
            ["piper-morgan"],  # active_repos
            "2025-08-20T17:30:00",  # last_session_time
        ]

        # Configure session manager to return empty context
        mock_session_manager.get_session_context.return_value = {}

        # Mock GitHub domain service with realistic activity
        mock_github_domain_service = AsyncMock()
        mock_github_issues = [
            {"number": 112, "title": "Weekly documentation audit", "state": "closed"},
            {"number": 116, "title": "Branch management tools", "state": "closed"},
            {"number": 117, "title": "Project hygiene", "state": "closed"},
        ]

        mock_github_domain_service.get_recent_issues.return_value = mock_github_issues

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify GitHub issues are available in activity
        assert result.github_activity is not None
        assert "issues" in result.github_activity

    async def test_performance_requirements(self):
        """Test <2 second generation requirement"""
        # Minimal mocks for performance test
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_domain_service = AsyncMock()

        # Fast return values
        mock_preference_manager.get_preference.return_value = {}
        mock_session_manager.get_session_context.return_value = {}
        mock_github_domain_service.get_recent_issues.return_value = []

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Measure performance
        start_time = time.time()
        result = await workflow.generate_standup("xian")
        end_time = time.time()

        generation_time = (end_time - start_time) * 1000

        # Verify performance requirement
        assert generation_time < 2000  # <2 seconds
        assert result.generation_time_ms < 2000
        assert result.performance_metrics["total_time_ms"] < 2000

    async def test_time_savings_calculation(self):
        """Test 15+ minutes time savings vs manual preparation"""
        mock_preference_manager = AsyncMock()
        # Configure get_preference to return empty dict (no saved preferences)
        mock_preference_manager.get_preference.return_value = {}

        mock_session_manager = AsyncMock()
        mock_github_domain_service = AsyncMock()

        # Rich context that would take time to gather manually
        mock_session_context = {
            "sessions_yesterday": 5,
            "tasks_completed": 8,
            "issues_worked": 6,
            "documentation_updated": 3,
            "meetings": 2,
        }

        mock_github_issues = [
            {"number": i, "title": f"Issue {i}", "state": "closed"} for i in range(10)
        ]

        mock_session_manager.get_session_context.return_value = mock_session_context
        mock_github_domain_service.get_recent_issues.return_value = mock_github_issues

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        result = await workflow.generate_standup("xian")

        # Calculate manual preparation time that was saved
        manual_time_saved = workflow._calculate_time_savings(result)

        # Verify 15+ minutes savings
        assert manual_time_saved >= 15 * 60 * 1000  # 15 minutes in milliseconds
        assert result.time_saved_minutes >= 15


@pytest.mark.asyncio
class TestStandupDataStructures:
    """Test data structures used in standup workflow"""

    async def test_standup_context_creation(self):
        """Test StandupContext data structure"""
        context = StandupContext(
            user_id="xian",
            date=datetime.now(),
            session_context={"key": "value"},
            github_repos=["piper-morgan-product"],
        )

        assert context.user_id == "xian"
        assert context.date is not None
        assert context.session_context == {"key": "value"}
        assert context.github_repos == ["piper-morgan-product"]

    async def test_standup_result_structure(self):
        """Test StandupResult data structure"""
        result = StandupResult(
            user_id="xian",
            generated_at=datetime.now(),
            generation_time_ms=1500,
            yesterday_accomplishments=["Task 1", "Task 2"],
            today_priorities=["Priority 1", "Priority 2"],
            blockers=[],
            context_source="persistent",
            github_activity={"commits": []},
            performance_metrics={"total_time_ms": 1500},
            time_saved_minutes=18,
        )

        assert result.user_id == "xian"
        assert result.generation_time_ms == 1500
        assert len(result.yesterday_accomplishments) == 2
        assert len(result.today_priorities) == 2
        assert result.blockers == []
        assert result.context_source == "persistent"
        assert result.time_saved_minutes == 18


@pytest.mark.asyncio
class TestStandupErrorHandling:
    """Test error handling and graceful degradation"""

    async def test_github_api_failure_honest_error_reporting(self):
        """Test honest error reporting when GitHub API fails"""
        from services.features.morning_standup import StandupIntegrationError

        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_domain_service = AsyncMock()

        # GitHub API failure
        mock_github_domain_service.get_recent_issues.side_effect = Exception("API rate limit")

        # Should still have session context
        mock_session_manager.get_session_context.return_value = {
            "yesterday_work": ["database connectivity", "documentation audit"]
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Should fail with clear error instead of graceful degradation
        with pytest.raises(StandupIntegrationError) as exc_info:
            await workflow.generate_standup("xian")

        error = exc_info.value
        assert error.service == "github" or error.service == "standup"
        assert "API rate limit" in str(error) or "GitHub integration failed" in str(error)

    async def test_github_method_missing_error_reporting(self):
        """Test honest error reporting when GitHub agent lacks get_recent_activity method"""
        from services.features.morning_standup import StandupIntegrationError

        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_domain_service = AsyncMock()

        # Remove get_recent_issues method to simulate missing method
        del mock_github_domain_service.get_recent_issues

        # Should still have session context
        mock_session_manager.get_session_context.return_value = {
            "yesterday_work": ["database connectivity", "documentation audit"]
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        # Should fail with clear error about missing method
        with pytest.raises(StandupIntegrationError) as exc_info:
            await workflow.generate_standup("xian")

        error = exc_info.value
        assert error.service == "github" or error.service == "standup"
        # Error should indicate GitHub integration failure
        assert "GitHub" in str(error) or "github" in str(error)

    async def test_empty_context_handling(self):
        """Test handling when no previous context exists"""
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_domain_service = AsyncMock()

        # Empty context - new user scenario
        mock_preference_manager.get_preference.return_value = None
        mock_session_manager.get_session_context.return_value = {}
        mock_github_domain_service.get_recent_issues.return_value = []

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_domain_service=mock_github_domain_service,
        )

        result = await workflow.generate_standup("xian")

        # Should handle gracefully with default content
        assert isinstance(result, StandupResult)
        assert result.context_source == "default"
        assert len(result.yesterday_accomplishments) >= 0  # May be empty but not fail
        assert len(result.today_priorities) > 0  # Should have default priorities
