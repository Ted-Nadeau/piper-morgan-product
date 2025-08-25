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
        mock_github_agent = Mock()

        # Initialize workflow
        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        # Verify initialization
        assert workflow.preference_manager == mock_preference_manager
        assert workflow.session_manager == mock_session_manager
        assert workflow.github_agent == mock_github_agent
        assert workflow.user_id == "xian"  # Default user

    async def test_generate_standup_for_user(self):
        """Test generating standup for specific user with persistent context"""
        # Setup mocks
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()

        # Mock session context from yesterday
        mock_session_context = {
            "last_standup_date": "2025-08-20",
            "active_projects": ["piper-morgan"],
            "focus_areas": ["database-connectivity", "persistent-context"],
        }

        mock_session_manager.get_session_context.return_value = mock_session_context

        # Mock GitHub activity
        mock_github_activity = {
            "commits": [
                {"message": "feat: complete weekly documentation audit", "sha": "5631dbf5"},
                {"message": "feat: add persistent context infrastructure", "sha": "a1b2c3d4"},
            ],
            "prs": [],
            "issues_closed": ["PM-112", "PM-116", "PM-117"],
            "issues_created": ["PM-118", "PM-119", "PM-120"],
        }

        mock_github_agent.get_recent_activity.return_value = mock_github_activity

        # Initialize workflow
        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify result structure
        assert isinstance(result, StandupResult)
        assert result.user_id == "xian"
        assert result.generated_at is not None
        assert result.generation_time_ms < 2000  # <2 seconds requirement
        assert len(result.yesterday_accomplishments) > 0
        assert len(result.today_priorities) > 0
        assert result.blockers is not None

        # Verify dependencies were called
        mock_session_manager.get_session_context.assert_called_once_with("xian")
        mock_github_agent.get_recent_activity.assert_called_once()

    async def test_context_persistence_integration(self):
        """Test integration with persistent context from yesterday's sessions"""
        # Mock preference manager with persistent context
        mock_preference_manager = AsyncMock()
        mock_preference_manager.get_preference.side_effect = [
            {"database": "resolved", "testing": "infrastructure-complete"},  # yesterday_context
            ["piper-morgan-product"],  # active_repos
            "2025-08-20T17:30:00",  # last_session_time
        ]

        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()
        mock_github_agent.get_recent_activity.return_value = {
            "commits": [],
            "prs": [],
            "issues_closed": [],
            "issues_created": [],
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify persistent context was used
        assert mock_preference_manager.get_preference.call_count == 3
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

        # Mock GitHub agent with realistic activity
        mock_github_agent = AsyncMock()
        mock_github_activity = {
            "commits": [
                {
                    "message": "feat: complete weekly documentation audit and project hygiene",
                    "sha": "5631dbf5",
                    "timestamp": "2025-08-21T08:44:00Z",
                },
                {
                    "message": "feat: add branch management discoverability and guidance tools",
                    "sha": "e977138a",
                    "timestamp": "2025-08-21T05:39:00Z",
                },
            ],
            "prs": [],
            "issues_closed": ["PM-112", "PM-116", "PM-117"],
            "issues_created": ["PM-118", "PM-119", "PM-120"],
        }

        mock_github_agent.get_recent_activity.return_value = mock_github_activity

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        # Generate standup
        result = await workflow.generate_standup("xian")

        # Verify GitHub activity processing
        assert len(result.yesterday_accomplishments) >= 2  # At least 2 commits
        assert "documentation audit" in str(result.yesterday_accomplishments).lower()
        assert "branch management" in str(result.yesterday_accomplishments).lower()
        assert len(result.github_activity["issues_closed"]) == 3
        assert len(result.github_activity["issues_created"]) == 3

    async def test_performance_requirements(self):
        """Test <2 second generation requirement"""
        # Minimal mocks for performance test
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()

        # Fast return values
        mock_preference_manager.get_preference.return_value = {}
        mock_session_manager.get_session_context.return_value = {}
        mock_github_agent.get_recent_activity.return_value = {
            "commits": [],
            "prs": [],
            "issues_closed": [],
            "issues_created": [],
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
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
        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()

        # Rich context that would take time to gather manually
        mock_session_context = {
            "sessions_yesterday": 5,
            "tasks_completed": 8,
            "issues_worked": 6,
            "documentation_updated": 3,
            "meetings": 2,
        }

        mock_github_activity = {
            "commits": [{"message": f"commit {i}", "sha": f"sha{i}"} for i in range(10)],
            "prs": [{"title": "PR 1", "number": 111}],
            "issues_closed": ["PM-112", "PM-116", "PM-117"],
            "issues_created": ["PM-118", "PM-119", "PM-120"],
        }

        mock_session_manager.get_session_context.return_value = mock_session_context
        mock_github_agent.get_recent_activity.return_value = mock_github_activity

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
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

    async def test_github_api_failure_graceful_degradation(self):
        """Test graceful degradation when GitHub API fails"""
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()

        # GitHub API failure
        mock_github_agent.get_recent_activity.side_effect = Exception("API rate limit")

        # Should still have session context
        mock_session_manager.get_session_context.return_value = {
            "yesterday_work": ["database connectivity", "documentation audit"]
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        # Should not fail, should gracefully degrade
        result = await workflow.generate_standup("xian")

        assert isinstance(result, StandupResult)
        assert result.github_activity == {}  # Empty due to API failure
        assert len(result.yesterday_accomplishments) > 0  # Still has session context
        assert "github-unavailable" in result.performance_metrics.get("warnings", [])

    async def test_empty_context_handling(self):
        """Test handling when no previous context exists"""
        mock_preference_manager = AsyncMock()
        mock_session_manager = AsyncMock()
        mock_github_agent = AsyncMock()

        # Empty context - new user scenario
        mock_preference_manager.get_preference.return_value = None
        mock_session_manager.get_session_context.return_value = {}
        mock_github_agent.get_recent_activity.return_value = {
            "commits": [],
            "prs": [],
            "issues_closed": [],
            "issues_created": [],
        }

        workflow = MorningStandupWorkflow(
            preference_manager=mock_preference_manager,
            session_manager=mock_session_manager,
            github_agent=mock_github_agent,
        )

        result = await workflow.generate_standup("xian")

        # Should handle gracefully with default content
        assert isinstance(result, StandupResult)
        assert result.context_source == "default"
        assert len(result.yesterday_accomplishments) >= 0  # May be empty but not fail
        assert len(result.today_priorities) > 0  # Should have default priorities
