"""
Unit tests for canonical_handlers.py

Tests for CanonicalHandlers class, focusing on:
- _get_dynamic_capabilities() method (Issue #493)
- Plugin registry integration
- Error handling for registry failures
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.plugins.plugin_interface import PluginMetadata


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance"""
    return CanonicalHandlers()


@pytest.fixture
def mock_plugin_registry():
    """Fixture to create a mock PluginRegistry"""
    registry = MagicMock()

    # Mock get_status_all to return status for configured plugins
    registry.get_status_all.return_value = {
        "slack": {"configured": True, "active": True, "status": "active"},
        "github": {"configured": True, "active": False, "status": "inactive"},
        "notion": {"configured": False, "active": False, "status": "not_configured"},
    }

    # Mock get_plugin to return plugin instances with metadata
    def get_plugin_side_effect(name):
        if name == "slack":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="slack",
                version="1.0.0",
                description="Slack integration for team communication",
                author="Piper Team",
                capabilities=["channels", "messages", "spatial"],
            )
            return plugin
        elif name == "github":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="github",
                version="1.0.0",
                description="GitHub integration for issue tracking",
                author="Piper Team",
                capabilities=["issues", "pull_requests", "webhooks"],
            )
            return plugin
        else:
            return None

    registry.get_plugin.side_effect = get_plugin_side_effect

    return registry


class TestGetDynamicCapabilities:
    """Test suite for _get_dynamic_capabilities() method"""

    def test_returns_expected_structure(self, canonical_handlers, mock_plugin_registry):
        """
        Test that _get_dynamic_capabilities() returns the expected dict structure
        with 'core', 'integrations', and 'capabilities_list' keys.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # Verify structure types
        assert isinstance(result["core"], list)
        assert isinstance(result["integrations"], list)
        assert isinstance(result["capabilities_list"], list)

    def test_core_capabilities_always_present(self, canonical_handlers, mock_plugin_registry):
        """
        Test that core PM capabilities are always included regardless of plugin state.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Core capabilities should be present
        core = result["core"]
        assert "development coordination" in core
        assert "issue tracking" in core
        assert "strategic planning" in core
        assert len(core) == 3

    def test_includes_active_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that active and configured plugins are included in integrations list.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should include slack (active) and github (configured)
        integrations = result["integrations"]
        assert len(integrations) == 2

        # Check slack integration
        slack_integration = next((i for i in integrations if i["name"] == "slack"), None)
        assert slack_integration is not None
        assert slack_integration["description"] == "Slack integration for team communication"
        assert "channels" in slack_integration["capabilities"]

        # Check github integration
        github_integration = next((i for i in integrations if i["name"] == "github"), None)
        assert github_integration is not None
        assert github_integration["description"] == "GitHub integration for issue tracking"
        assert "issues" in github_integration["capabilities"]

    def test_excludes_unconfigured_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that unconfigured and inactive plugins are excluded from integrations.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Notion should NOT be included (not configured, not active)
        integrations = result["integrations"]
        notion_names = [i["name"] for i in integrations]
        assert "notion" not in notion_names

    def test_capabilities_list_includes_all(self, canonical_handlers, mock_plugin_registry):
        """
        Test that capabilities_list includes core capabilities plus integration names.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        capabilities_list = result["capabilities_list"]

        # Should contain core capabilities
        assert "development coordination" in capabilities_list
        assert "issue tracking" in capabilities_list
        assert "strategic planning" in capabilities_list

        # Should contain integration summaries
        assert "slack integration" in capabilities_list
        assert "github integration" in capabilities_list

        # Total should be 3 core + 2 integrations = 5
        assert len(capabilities_list) == 5

    def test_handles_registry_unavailable(self, canonical_handlers):
        """
        Test that method gracefully handles PluginRegistry being unavailable.
        Should return core capabilities only without raising exception.
        """
        # Arrange - Mock get_plugin_registry to raise exception
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_get_registry:
            mock_get_registry.side_effect = Exception("Registry not available")

            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should still return valid structure with core capabilities
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # Core capabilities should be present
        assert len(result["core"]) == 3

        # Integrations should be empty list (not None)
        assert result["integrations"] == []

        # Capabilities list should only have core
        assert len(result["capabilities_list"]) == 3

    def test_handles_plugin_metadata_error(self, canonical_handlers, mock_plugin_registry):
        """
        Test that method handles errors when getting plugin metadata.
        Current implementation: entire plugin processing aborts on first error.
        Returns core capabilities only.
        """

        # Arrange - Make slack plugin raise error on get_metadata
        def get_plugin_error_side_effect(name):
            if name == "slack":
                plugin = MagicMock()
                plugin.get_metadata.side_effect = Exception("Metadata error")
                return plugin
            elif name == "github":
                plugin = MagicMock()
                plugin.get_metadata.return_value = PluginMetadata(
                    name="github",
                    version="1.0.0",
                    description="GitHub integration for issue tracking",
                    author="Piper Team",
                    capabilities=["issues", "pull_requests"],
                )
                return plugin
            return None

        mock_plugin_registry.get_plugin.side_effect = get_plugin_error_side_effect

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Current implementation: entire loop aborts on error
        # So no integrations are returned (caught by broad exception handler)
        integrations = result["integrations"]
        assert len(integrations) == 0  # No plugins included due to error

        # Core capabilities should still be present
        assert len(result["core"]) == 3
        assert len(result["capabilities_list"]) == 3

    def test_empty_plugin_registry(self, canonical_handlers):
        """
        Test behavior when plugin registry has no plugins registered.
        Should return only core capabilities.
        """
        # Arrange
        empty_registry = MagicMock()
        empty_registry.get_status_all.return_value = {}

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=empty_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        assert len(result["core"]) == 3
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 3

    def test_plugin_returns_none(self, canonical_handlers):
        """
        Test that method handles when get_plugin returns None for a plugin.
        Should skip that plugin gracefully.
        """
        # Arrange - Create fresh mock with get_plugin returning None
        registry = MagicMock()
        registry.get_status_all.return_value = {
            "slack": {"configured": True, "active": True},
            "github": {"configured": True, "active": False},
        }
        # All get_plugin calls return None
        registry.get_plugin.return_value = None

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry", return_value=registry
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should have core but no integrations (plugins returned None)
        assert len(result["core"]) == 3
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 3


class TestLastActivityDetection:
    """Test suite for _detect_last_activity_request() method (Issue #504)"""

    def test_detects_last_time_worked_on_pattern(self, canonical_handlers):
        """Test detection of 'last time we worked on X' pattern."""
        # Arrange
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last time we worked on project alpha?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result == "project alpha"

    def test_detects_when_did_we_work_on_pattern(self, canonical_handlers):
        """Test detection of 'when did we work on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When did we work on HealthTrack?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert (note: detection returns lowercase from regex)
        assert result == "healthtrack"

    def test_detects_last_worked_on_pattern(self, canonical_handlers):
        """Test detection of 'last worked on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last worked on the backend?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result == "the backend"

    def test_detects_last_touched_pattern(self, canonical_handlers):
        """Test detection of 'last touched X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last time we touched the API?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert (note: detection returns lowercase from regex)
        assert result == "the api"

    def test_returns_none_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What day is it?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_current_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result is None

    def test_returns_none_for_empty_message(self, canonical_handlers):
        """Test that empty messages return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result is None


class TestProjectDurationDetection:
    """Test suite for _detect_duration_request() method (Issue #505)"""

    def test_detects_how_long_working_on_pattern(self, canonical_handlers):
        """Test detection of 'how long have we been working on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been working on project alpha?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "project alpha"

    def test_detects_how_long_been_on_pattern(self, canonical_handlers):
        """Test detection of 'how long have we been on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been on HealthTrack?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "healthtrack"

    def test_detects_when_did_we_start_pattern(self, canonical_handlers):
        """Test detection of 'when did we start X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When did we start the backend project?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "the backend project"

    def test_detects_this_project_pattern(self, canonical_handlers):
        """Test detection of 'how long this project' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been on this project?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "this project"

    def test_returns_none_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What is the project status?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result is None

    def test_returns_none_for_empty_message(self, canonical_handlers):
        """Test that empty messages return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result is None


class TestPriorityRecommendationDetection:
    """Test suite for _detect_priority_recommendation_request() method (Issue #511)"""

    def test_detects_which_project_focus_pattern(self, canonical_handlers):
        """Test detection of 'which project should I focus on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Which project should I focus on?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_what_project_work_pattern(self, canonical_handlers):
        """Test detection of 'what project should I work on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What project should I work on next?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_what_should_prioritize_pattern(self, canonical_handlers):
        """Test detection of 'what should I prioritize' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What should I prioritize this week?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_most_important_pattern(self, canonical_handlers):
        """Test detection of 'what's most important' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's most important to work on?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_focus_on_pattern(self, canonical_handlers):
        """Test detection of 'what should I focus on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What should I focus on right now?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What are my priorities?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is False


class TestPriorityScoreCalculation:
    """Test suite for _calculate_priority_score() method (Issue #511)"""

    def test_calculates_score_with_staleness(self, canonical_handlers):
        """Test priority score calculation with staleness factor."""
        from datetime import datetime, timedelta

        # Arrange - Project inactive for 20 days
        last_update = (datetime.now() - timedelta(days=20)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] >= 20  # Should have staleness points
        assert result["breakdown"]["staleness"] == 20
        assert "days since last activity" in result["top_reason"]

    def test_calculates_score_with_many_issues(self, canonical_handlers):
        """Test priority score calculation with high issue count."""
        from datetime import datetime, timedelta

        # Arrange - Recent activity but many issues
        last_update = (datetime.now() - timedelta(days=5)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 15}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] > 0
        assert result["breakdown"]["issue_count"] > 0
        assert "open issues" in result["top_reason"]

    def test_calculates_score_with_urgency(self, canonical_handlers):
        """Test priority score calculation with high-priority issues."""
        from datetime import datetime, timedelta

        # Arrange - Project with high-priority issues
        last_update = (datetime.now() - timedelta(days=10)).isoformat()
        github_data = {
            "updated_at": last_update,
            "open_issues_count": 8,
            "issues_preview": [
                {
                    "number": 1,
                    "title": "Critical bug",
                    "labels": [{"name": "critical"}],
                },
                {
                    "number": 2,
                    "title": "High priority feature",
                    "labels": [{"name": "high-priority"}],
                },
            ],
        }

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["breakdown"]["urgency"] > 0
        # Top reason will be first reason added (issue count in this case)
        assert "open issues" in result["top_reason"]

    def test_handles_missing_github_data(self, canonical_handlers):
        """Test priority score calculation with no GitHub data."""
        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", None)

        # Assert
        assert result["score"] == 0
        assert result["top_reason"] == "No GitHub data available"

    def test_handles_active_project_low_issues(self, canonical_handlers):
        """Test priority score for active project with few issues."""
        from datetime import datetime, timedelta

        # Arrange - Recent activity, few issues
        last_update = (datetime.now() - timedelta(days=3)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 2}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] < 20  # Should have low score
        # With 2 issues, we get "2 open issues" as reason
        assert "2 open issues" in result["top_reason"]


class TestPriorityRecommendationFormatting:
    """Test suite for priority recommendation formatting methods (Issue #511)"""

    def test_format_embedded_with_projects(self, canonical_handlers):
        """Test EMBEDDED format with ranked projects."""
        # Arrange
        ranked_projects = [
            {
                "name": "HighPriority",
                "score": 80,
                "top_reason": "30 days since last activity",
                "breakdown": {"staleness": 30, "issue_count": 30, "urgency": 20},
            },
            {
                "name": "LowPriority",
                "score": 10,
                "top_reason": "Active and low issue count",
                "breakdown": {"staleness": 0, "issue_count": 10, "urgency": 0},
            },
        ]

        # Act
        result = canonical_handlers._format_priority_embedded(ranked_projects)

        # Assert
        assert result == "Focus on: HighPriority"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        # Act
        result = canonical_handlers._format_priority_embedded([])

        # Assert
        assert result == "No projects to prioritize"

    def test_format_standard_with_projects(self, canonical_handlers):
        """Test STANDARD format with ranked projects."""
        # Arrange
        ranked_projects = [
            {
                "name": "Project1",
                "score": 70,
                "top_reason": "25 days since last activity",
                "breakdown": {"staleness": 25, "issue_count": 30, "urgency": 15},
            },
            {
                "name": "Project2",
                "score": 50,
                "top_reason": "15 open issues",
                "breakdown": {"staleness": 0, "issue_count": 30, "urgency": 20},
            },
            {
                "name": "Project3",
                "score": 30,
                "top_reason": "10 open issues",
                "breakdown": {"staleness": 0, "issue_count": 30, "urgency": 0},
            },
        ]

        # Act
        result = canonical_handlers._format_priority_standard(ranked_projects)

        # Assert
        assert "Priority Recommendation" in result
        assert "1. **Project1**" in result
        assert "2. **Project2**" in result
        assert "3. **Project3**" in result
        assert "(Score: 70)" in result
        assert "25 days since last activity" in result

    def test_format_standard_with_many_projects(self, canonical_handlers):
        """Test STANDARD format shows only top 3 plus count."""
        # Arrange
        ranked_projects = [
            {
                "name": f"Project{i}",
                "score": 100 - i * 10,
                "top_reason": "Test reason",
                "breakdown": {},
            }
            for i in range(5)
        ]

        # Act
        result = canonical_handlers._format_priority_standard(ranked_projects)

        # Assert
        assert "Plus 2 more projects" in result

    def test_format_granular_with_projects(self, canonical_handlers):
        """Test GRANULAR format with full details."""
        # Arrange
        ranked_projects = [
            {
                "name": "DetailedProject",
                "score": 90,
                "top_reason": "35 days since last activity",
                "breakdown": {"staleness": 35, "issue_count": 30, "urgency": 25},
                "github_data": {
                    "open_issues_count": 12,
                    "updated_at": "2025-11-15T10:00:00Z",
                },
            }
        ]

        # Act
        result = canonical_handlers._format_priority_granular(ranked_projects)

        # Assert
        assert "Full Priority Analysis" in result
        assert "DetailedProject" in result
        assert "Priority Score**: 90/100" in result
        assert "Staleness: 35/40 points" in result
        assert "Issue Count: 30/30 points" in result
        assert "Urgency: 25/30 points" in result
        assert "Open Issues: 12" in result


class TestProjectDurationCalculation:
    """Test suite for project duration calculation (Issue #505)"""

    def test_calculate_duration_with_valid_date(self, canonical_handlers):
        """Test duration calculation with a valid ISO date string."""
        from datetime import datetime, timedelta

        # Arrange - 45 days ago
        start_date = datetime.now() - timedelta(days=45)
        created_at = start_date.isoformat()

        # Act
        result = canonical_handlers._calculate_duration(created_at)

        # Assert
        assert result is not None
        assert result["total_days"] == 45
        assert result["months"] == 1  # 45 // 30 = 1
        assert result["weeks"] == 2  # (45 % 30) // 7 = 2
        assert result["days"] == 1  # ((45 % 30) % 7) = 1

    def test_calculate_duration_with_datetime_object(self, canonical_handlers):
        """Test duration calculation with a datetime object."""
        from datetime import datetime, timedelta

        # Arrange - 10 days ago
        start_date = datetime.now() - timedelta(days=10)

        # Act
        result = canonical_handlers._calculate_duration(start_date)

        # Assert
        assert result is not None
        assert result["total_days"] == 10
        assert result["months"] == 0
        assert result["weeks"] == 1
        assert result["days"] == 3

    def test_calculate_duration_with_recent_start(self, canonical_handlers):
        """Test duration calculation with very recent start date."""
        from datetime import datetime, timedelta

        # Arrange - 2 days ago
        start_date = datetime.now() - timedelta(days=2)
        created_at = start_date.isoformat()

        # Act
        result = canonical_handlers._calculate_duration(created_at)

        # Assert
        assert result is not None
        assert result["total_days"] == 2
        assert result["months"] == 0
        assert result["weeks"] == 0
        assert result["days"] == 2

    def test_calculate_duration_handles_invalid_date(self, canonical_handlers):
        """Test that invalid dates return None."""
        # Act
        result = canonical_handlers._calculate_duration("not-a-date")

        # Assert
        assert result is None


class TestProjectDurationFormatting:
    """Test suite for project duration formatting methods (Issue #505)"""

    def test_format_embedded_with_months(self, canonical_handlers):
        """Test EMBEDDED format with duration in months."""
        # Arrange
        duration = {"total_days": 90, "months": 3, "weeks": 0, "days": 0}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 3 months"

    def test_format_embedded_with_single_month(self, canonical_handlers):
        """Test EMBEDDED format with single month (no 's')."""
        # Arrange
        duration = {"total_days": 30, "months": 1, "weeks": 0, "days": 0}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 1 month"

    def test_format_embedded_with_days(self, canonical_handlers):
        """Test EMBEDDED format with duration in days only."""
        # Arrange
        duration = {"total_days": 15, "months": 0, "weeks": 2, "days": 1}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 15 days"

    def test_format_embedded_without_duration(self, canonical_handlers):
        """Test EMBEDDED format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", None)

        # Assert
        assert result == "TestProject: unknown duration"

    def test_format_standard_with_duration(self, canonical_handlers):
        """Test STANDARD format with duration data."""
        from datetime import datetime

        # Arrange
        start_date = datetime(2025, 11, 1)
        duration = {
            "total_days": 51,
            "months": 1,
            "weeks": 3,
            "days": 0,
            "start_date": start_date,
        }

        # Act
        result = canonical_handlers._format_duration_standard("TestProject", duration, None)

        # Assert
        assert "You've been working on **TestProject**" in result
        assert "1 month and 3 weeks" in result
        assert "started November 01, 2025" in result

    def test_format_standard_without_duration(self, canonical_handlers):
        """Test STANDARD format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_standard("TestProject", None, None)

        # Assert
        assert "I don't have start date information for **TestProject**" in result
        assert "Check if the project is configured" in result

    def test_format_granular_with_duration(self, canonical_handlers):
        """Test GRANULAR format with duration data."""
        from datetime import datetime

        # Arrange
        start_date = datetime(2025, 10, 15)
        duration = {
            "total_days": 68,
            "months": 2,
            "weeks": 1,
            "days": 1,
            "start_date": start_date,
        }

        # Act
        result = canonical_handlers._format_duration_granular("TestProject", duration, None)

        # Assert
        assert "**Project Duration: TestProject**" in result
        assert "**Started**: Wednesday, October 15, 2025" in result
        assert "**Total Days**: 68" in result
        assert "**Breakdown**:" in result
        assert "- Months: 2" in result
        assert "- Weeks: 1" in result
        assert "- Days: 1" in result

    def test_format_granular_without_duration(self, canonical_handlers):
        """Test GRANULAR format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_granular("TestProject", None, None)

        # Assert
        assert "**TestProject** duration unknown" in result
        assert "may not be configured with a start date" in result
        assert "Check Settings → Projects" in result


class TestLastActivityFormatting:
    """Test suite for last activity formatting methods (Issue #504)"""

    def test_format_embedded_with_activity_today(self, canonical_handlers):
        """Test EMBEDDED format with activity from today."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "commit",
            "date": datetime.now().isoformat(),
            "title": "Fix bug in handler",
        }

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: today" == result

    def test_format_embedded_with_activity_yesterday(self, canonical_handlers):
        """Test EMBEDDED format with activity from yesterday."""
        from datetime import datetime, timedelta

        # Arrange
        yesterday = datetime.now() - timedelta(days=1)
        activity = {
            "type": "commit",
            "date": yesterday.isoformat(),
            "title": "Update documentation",
        }

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: yesterday" == result

    def test_format_embedded_with_activity_days_ago(self, canonical_handlers):
        """Test EMBEDDED format with activity from several days ago."""
        from datetime import datetime, timedelta

        # Arrange
        five_days_ago = datetime.now() - timedelta(days=5)
        activity = {"type": "commit", "date": five_days_ago.isoformat(), "title": "Refactor code"}

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: 5 days ago" == result

    def test_format_embedded_without_activity(self, canonical_handlers):
        """Test EMBEDDED format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", None)

        # Assert
        assert result == "TestProject: no recent activity"

    def test_format_standard_with_activity(self, canonical_handlers):
        """Test STANDARD format with activity data."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "pull_request",
            "date": "2025-12-21T10:30:00Z",
            "title": "Add new feature for user authentication",
        }

        # Act
        result = canonical_handlers._format_last_activity_standard("TestProject", activity)

        # Assert
        assert "Last activity on **TestProject**" in result
        assert "pull_request" in result
        assert "December 21, 2025" in result
        assert "Add new feature for user authentication" in result

    def test_format_standard_without_activity(self, canonical_handlers):
        """Test STANDARD format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_standard("TestProject", None)

        # Assert
        assert "I don't have recent activity data for TestProject" in result
        assert "GitHub integration may need to be configured" in result

    def test_format_granular_with_activity(self, canonical_handlers):
        """Test GRANULAR format with activity data."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "issue",
            "date": "2025-12-20T15:45:00Z",
            "title": "Bug: Application crashes on startup",
        }

        # Act
        result = canonical_handlers._format_last_activity_granular("TestProject", activity)

        # Assert
        assert "**Last Activity on TestProject**" in result
        assert "**Date**:" in result
        assert "**Time Since**:" in result
        assert "**Type**: issue" in result
        assert "**Description**: Bug: Application crashes on startup" in result

    def test_format_granular_without_activity(self, canonical_handlers):
        """Test GRANULAR format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_granular("TestProject", None)

        # Assert
        assert "No recent activity found for **TestProject**" in result
        assert "No commits, issues, or PRs in the last 30 days" in result
        assert "GitHub integration not configured" in result


class TestSetupRequestDetection:
    """Tests for _detect_setup_request() method - Issue #498."""

    def test_detects_project_setup(self, canonical_handlers):
        """Detects 'set up my projects' as projects setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me set up my projects",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "projects"

    def test_detects_configure_projects(self, canonical_handlers):
        """Detects 'configure my projects' as projects setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="I want to configure my project portfolio",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "projects"

    def test_detects_integration_setup(self, canonical_handlers):
        """Detects 'set up integrations' as integrations setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me set up my integrations",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "integrations"

    def test_detects_connect_github(self, canonical_handlers):
        """Detects 'connect github' as integrations setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="I want to connect my GitHub account",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "integrations"

    def test_detects_general_setup(self, canonical_handlers):
        """Detects 'get started with piper' as general setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get started with Piper?",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "general"

    def test_returns_none_for_non_setup(self, canonical_handlers):
        """Returns None for non-setup queries."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on my agenda today?",
            category=IntentCategoryEnum.QUERY,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result is None

    def test_handles_empty_intent(self, canonical_handlers):
        """Returns None for empty/None intent."""
        result = canonical_handlers._detect_setup_request(None)
        assert result is None

    def test_handles_missing_message(self, canonical_handlers):
        """Returns None for intent without message."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message=None,
            category=IntentCategoryEnum.GUIDANCE,
            action="request_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result is None


class TestSetupGuidanceFormatting:
    """Tests for setup guidance formatting methods - Issue #498."""

    def test_project_setup_no_existing_projects(self, canonical_handlers):
        """Project setup guidance when user has no projects."""
        result = canonical_handlers._format_project_setup_guidance(None)

        assert "message" in result
        assert "set up your projects" in result["message"].lower()
        assert "/settings/projects" in result["message"]
        assert result["intent"]["action"] == "provide_setup_guidance"
        assert result["setup_type"] == "projects"

    def test_project_setup_with_existing_projects(self, canonical_handlers):
        """Project setup guidance when user has projects."""
        user_context = MagicMock()
        user_context.projects = ["Project A", "Project B"]

        result = canonical_handlers._format_project_setup_guidance(user_context)

        assert "message" in result
        assert "2 project(s)" in result["message"]
        assert "Project A" in result["message"]
        assert "/settings/projects" in result["message"]

    def test_integration_setup_guidance(self, canonical_handlers):
        """Integration setup guidance."""
        result = canonical_handlers._format_integration_setup_guidance()

        assert "message" in result
        assert result["setup_type"] == "integrations"

    def test_general_setup_guidance(self, canonical_handlers):
        """General setup guidance."""
        result = canonical_handlers._format_general_setup_guidance()

        assert "message" in result
        assert result["setup_type"] == "general"


class TestHealthCheckDetection:
    """Test suite for _detect_health_check_request() method (Issue #506)"""

    def test_detects_working_properly_pattern(self, canonical_handlers):
        """Test detection of 'are you working properly' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Are you working properly?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_health",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is True

    def test_detects_are_you_ok_pattern(self, canonical_handlers):
        """Test detection of 'are you ok' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Are you ok?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_health",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is True

    def test_detects_health_keyword(self, canonical_handlers):
        """Test detection of 'health' keyword."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's your health status?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_health",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is True

    def test_detects_system_status_pattern(self, canonical_handlers):
        """Test detection of 'system status' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me system status",
            category=IntentCategoryEnum.IDENTITY,
            action="query_health",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_health_query(self, canonical_handlers):
        """Test that non-health queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's your name?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_identity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.IDENTITY,
            action="query",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_health_check_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_none_intent(self, canonical_handlers):
        """Test that None intent returns False."""
        # Act
        result = canonical_handlers._detect_health_check_request(None)

        # Assert
        assert result is False


class TestHealthCheckFormatting:
    """Test suite for health check formatting methods (Issue #506)"""

    def test_format_embedded_healthy(self, canonical_handlers):
        """Test EMBEDDED format with healthy status."""
        # Arrange
        health_data = {"overall_status": "healthy", "components": {}, "integrations": []}

        # Act
        result = canonical_handlers._format_health_embedded(health_data)

        # Assert
        assert result == "All systems operational"

    def test_format_embedded_degraded(self, canonical_handlers):
        """Test EMBEDDED format with degraded status."""
        # Arrange
        health_data = {"overall_status": "degraded", "components": {}, "integrations": []}

        # Act
        result = canonical_handlers._format_health_embedded(health_data)

        # Assert
        assert result == "Some issues detected"

    def test_format_embedded_unknown(self, canonical_handlers):
        """Test EMBEDDED format with unknown status."""
        # Arrange
        health_data = {"overall_status": "unknown", "components": {}, "integrations": []}

        # Act
        result = canonical_handlers._format_health_embedded(health_data)

        # Assert
        assert result == "Status unknown"

    def test_format_standard_healthy(self, canonical_handlers):
        """Test STANDARD format with healthy status."""
        # Arrange
        health_data = {
            "overall_status": "healthy",
            "components": {},
            "integrations": [
                {"name": "github", "status": "active"},
                {"name": "slack", "status": "active"},
            ],
        }

        # Act
        result = canonical_handlers._format_health_standard(health_data)

        # Assert
        assert "Yes, I'm working properly!" in result
        assert "All systems are operational" in result
        assert "Github" in result
        assert "Slack" in result

    def test_format_standard_degraded(self, canonical_handlers):
        """Test STANDARD format with degraded status."""
        # Arrange
        health_data = {
            "overall_status": "degraded",
            "components": {},
            "integrations": [],
        }

        # Act
        result = canonical_handlers._format_health_standard(health_data)

        # Assert
        assert "mostly working" in result
        assert "some components have issues" in result

    def test_format_granular_healthy(self, canonical_handlers):
        """Test GRANULAR format with healthy components."""
        # Arrange
        health_data = {
            "overall_status": "healthy",
            "components": {
                "database": {"status": "healthy"},
                "integrations": {"status": "healthy", "active_count": 2, "total_count": 3},
            },
            "integrations": [
                {"name": "github", "status": "active"},
                {"name": "slack", "status": "active"},
                {"name": "notion", "status": "inactive"},
            ],
        }

        # Act
        result = canonical_handlers._format_health_granular(health_data)

        # Assert
        assert "**System Health Report**" in result
        assert "**Overall Status**: HEALTHY" in result
        assert "**Components**:" in result
        assert "Database: ✅ healthy" in result
        assert "**Integrations**:" in result
        assert "Github: ✅ active" in result
        assert "Slack: ✅ active" in result
        assert "Notion: ⚪ inactive" in result


class TestDifferentiationDetection:
    """Test suite for _detect_differentiation_request() method (Issue #508)"""

    def test_detects_what_makes_you_different(self, canonical_handlers):
        """Test detection of 'what makes you different' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What makes you different from other AI assistants?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is True

    def test_detects_what_is_special(self, canonical_handlers):
        """Test detection of 'what's special about you' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's special about you?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is True

    def test_detects_vs_chatgpt(self, canonical_handlers):
        """Test detection of 'vs chatgpt' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How are you different vs chatgpt?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is True

    def test_detects_why_use_piper(self, canonical_handlers):
        """Test detection of 'why use piper' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Why should I use Piper instead of other tools?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's your name?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_identity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.IDENTITY,
            action="query_identity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_differentiation_request(intent)

        # Assert
        assert result is False


class TestDifferentiationFormatting:
    """Test suite for differentiation formatting methods (Issue #508)"""

    def test_format_embedded(self, canonical_handlers):
        """Test EMBEDDED format is brief."""
        result = canonical_handlers._format_differentiation_embedded()

        assert "PM-specialized" in result
        assert len(result) < 100  # Should be brief

    def test_format_standard_with_integrations(self, canonical_handlers, mock_plugin_registry):
        """Test STANDARD format includes integrations."""
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            capabilities_data = canonical_handlers._get_dynamic_capabilities()

        result = canonical_handlers._format_differentiation_standard(capabilities_data)

        assert "PM-Specialized" in result
        assert "Integrated" in result
        assert "Context-Aware" in result
        assert "Adaptive" in result
        # Should mention at least one integration
        assert any(name in result for name in ["Slack", "Github", "GitHub"])

    def test_format_standard_without_integrations(self, canonical_handlers):
        """Test STANDARD format works without integrations."""
        capabilities_data = {"integrations": [], "core": [], "capabilities_list": []}

        result = canonical_handlers._format_differentiation_standard(capabilities_data)

        assert "PM-Specialized" in result
        assert "product management" in result.lower()

    def test_format_granular_with_integrations(self, canonical_handlers, mock_plugin_registry):
        """Test GRANULAR format includes detailed examples."""
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            capabilities_data = canonical_handlers._get_dynamic_capabilities()

        result = canonical_handlers._format_differentiation_granular(capabilities_data)

        assert "What Makes Piper Different?" in result
        assert "Purpose-Built for Product Management" in result
        assert "Real Tool Integration" in result
        assert "Project Context Awareness" in result
        assert "Spatial Intelligence" in result
        # Should list actual integrations
        assert "Slack" in result or "Github" in result

    def test_format_granular_without_integrations(self, canonical_handlers):
        """Test GRANULAR format works without integrations."""
        capabilities_data = {"integrations": [], "core": [], "capabilities_list": []}

        result = canonical_handlers._format_differentiation_granular(capabilities_data)

        assert "What Makes Piper Different?" in result
        assert "GitHub, Slack, Calendar, Notion (when configured)" in result


class TestDifferentiationHandler:
    """Test suite for _handle_identity_differentiation() method (Issue #508)"""

    @pytest.mark.asyncio
    async def test_handler_returns_correct_structure(
        self, canonical_handlers, mock_plugin_registry
    ):
        """Test handler returns expected response structure."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What makes you different?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            result = await canonical_handlers._handle_identity_differentiation(
                intent, "test_session"
            )

        # Assert structure
        assert "message" in result
        assert "intent" in result
        assert result["intent"]["category"] == "identity"
        assert result["intent"]["action"] == "provide_differentiation"
        assert result["intent"]["confidence"] == 1.0
        assert "differentiators" in result["intent"]["context"]
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_embedded(
        self, canonical_handlers, mock_plugin_registry
    ):
        """Test handler uses EMBEDDED format for embedded spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What makes you different?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "EMBEDDED"}

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            result = await canonical_handlers._handle_identity_differentiation(
                intent, "test_session"
            )

        # Should use brief embedded format
        assert len(result["message"]) < 100
        assert result["spatial_pattern"] == "EMBEDDED"

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_granular(
        self, canonical_handlers, mock_plugin_registry
    ):
        """Test handler uses GRANULAR format for granular spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What makes you different?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_differentiation",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            result = await canonical_handlers._handle_identity_differentiation(
                intent, "test_session"
            )

        # Should use detailed granular format
        assert "What Makes Piper Different?" in result["message"]
        assert result["spatial_pattern"] == "GRANULAR"


class TestHelpRequestDetection:
    """Test suite for _detect_help_request() method (Issue #507)"""

    def test_detects_get_help_pattern(self, canonical_handlers):
        """Test detection of 'get help' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get help?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is True

    def test_detects_how_do_i_pattern(self, canonical_handlers):
        """Test detection of 'how do i' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I use this tool?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is True

    def test_detects_getting_started_pattern(self, canonical_handlers):
        """Test detection of 'getting started' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="I'm getting started with Piper",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is True

    def test_detects_what_can_i_ask_pattern(self, canonical_handlers):
        """Test detection of 'what can i ask' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What can I ask you?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is True

    def test_excludes_setup_requests(self, canonical_handlers):
        """Test that setup requests are excluded from help detection."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me set up my projects",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert - Should be False because it contains "set up"
        assert result is False

    def test_excludes_configure_requests(self, canonical_handlers):
        """Test that configure requests are excluded from help detection."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me configure my integrations",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert - Should be False because it contains "configure"
        assert result is False

    def test_returns_false_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's your name?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_identity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.IDENTITY,
            action="query",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_help_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_none_intent(self, canonical_handlers):
        """Test that None intent returns False."""
        # Act
        result = canonical_handlers._detect_help_request(None)

        # Assert
        assert result is False


class TestHelpFormatting:
    """Test suite for help formatting methods (Issue #507)"""

    def test_format_embedded(self, canonical_handlers):
        """Test EMBEDDED format is brief."""
        result = canonical_handlers._format_help_embedded()

        assert "agenda" in result.lower()
        assert "projects" in result.lower()
        assert len(result) < 150  # Should be brief

    def test_format_standard_includes_key_sections(self, canonical_handlers):
        """Test STANDARD format includes key sections."""
        result = canonical_handlers._format_help_standard()

        assert "Quick Start Queries" in result
        assert "Settings" in result
        assert "What's on my agenda" in result
        assert "What projects are we working on" in result
        assert "/settings" in result

    def test_format_granular_includes_all_sections(self, canonical_handlers):
        """Test GRANULAR format includes all help sections."""
        result = canonical_handlers._format_help_granular()

        assert "Getting Started with Piper" in result
        assert "Identity Queries" in result
        assert "Time & Schedule" in result
        assert "Projects & Status" in result
        assert "Actions" in result
        assert "Settings & Configuration" in result
        assert "Tips" in result
        # Check some example queries
        assert "What's your name?" in result
        assert "What day is it?" in result
        assert "What projects are we working on?" in result
        assert "/settings" in result
        assert "/settings/projects" in result


class TestHelpHandler:
    """Test suite for _handle_identity_help() method (Issue #507)"""

    @pytest.mark.asyncio
    async def test_handler_returns_correct_structure(self, canonical_handlers):
        """Test handler returns expected response structure."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get help?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        result = await canonical_handlers._handle_identity_help(intent, "test_session")

        # Assert structure
        assert "message" in result
        assert "intent" in result
        assert result["intent"]["category"] == "identity"
        assert result["intent"]["action"] == "provide_help"
        assert result["intent"]["confidence"] == 1.0
        assert result["intent"]["context"]["help_type"] == "getting_started"
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_embedded(self, canonical_handlers):
        """Test handler uses EMBEDDED format for embedded spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get help?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "EMBEDDED"}

        result = await canonical_handlers._handle_identity_help(intent, "test_session")

        # Should use brief embedded format
        assert len(result["message"]) < 150
        assert result["spatial_pattern"] == "EMBEDDED"

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_granular(self, canonical_handlers):
        """Test handler uses GRANULAR format for granular spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get help?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        result = await canonical_handlers._handle_identity_help(intent, "test_session")

        # Should use detailed granular format
        assert "Getting Started with Piper" in result["message"]
        assert result["spatial_pattern"] == "GRANULAR"

    @pytest.mark.asyncio
    async def test_handler_uses_standard_format_by_default(self, canonical_handlers):
        """Test handler uses STANDARD format when no spatial pattern is set."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get help?",
            category=IntentCategoryEnum.IDENTITY,
            action="query_help",
            confidence=0.9,
        )

        result = await canonical_handlers._handle_identity_help(intent, "test_session")

        # Should use standard format
        assert "Quick Start Queries" in result["message"]
        assert result["spatial_pattern"] is None


class TestProjectListDetection:
    """Test suite for _detect_project_list_request() method (Issue #509)"""

    def test_detects_what_projects_pattern(self, canonical_handlers):
        """Test detection of 'what projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What projects are we working on?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_detects_list_projects_pattern(self, canonical_handlers):
        """Test detection of 'list projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="List all projects",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_detects_show_projects_pattern(self, canonical_handlers):
        """Test detection of 'show projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me my projects",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_returns_false_for_non_list_query(self, canonical_handlers):
        """Test that non-list queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of HealthTrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is False


class TestProjectListFormatting:
    """Test suite for project list formatting methods (Issue #509)"""

    def test_format_embedded_with_projects(self, canonical_handlers):
        """Test EMBEDDED format with project list."""
        projects = ["HealthTrack", "MediHub", "CarePro"]

        result = canonical_handlers._format_project_list_embedded(projects, {})

        assert result == "You have 3 active projects: HealthTrack, MediHub, CarePro"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        result = canonical_handlers._format_project_list_embedded([], {})

        assert result == "No active projects"

    def test_format_standard_with_github(self, canonical_handlers):
        """Test STANDARD format with GitHub metadata."""
        projects = ["HealthTrack", "MediHub"]
        metadata = {
            "HealthTrack": {
                "has_github": True,
                "open_issues_count": 12,
                "recent_issues": [
                    {"number": 123, "title": "Fix authentication bug"},
                    {"number": 124, "title": "Add user settings page"},
                ],
            },
            "MediHub": {"has_github": False},
        }

        result = canonical_handlers._format_project_list_standard(projects, metadata)

        # Verify key content elements are present
        assert "active projects" in result.lower()
        assert "HealthTrack" in result
        assert "MediHub" in result
        assert "12 open issues" in result

    def test_format_granular_without_github(self, canonical_handlers):
        """Test GRANULAR format without GitHub connection."""
        # Arrange
        projects = ["HealthTrack"]
        metadata = {"HealthTrack": {"has_github": False}}

        # Act
        result = canonical_handlers._format_project_list_granular(projects, metadata)

        # Assert - verify key content is present
        assert "HealthTrack" in result
        assert "active project" in result.lower() or "project" in result.lower()


class TestLandscapeDetection:
    """Test suite for _detect_landscape_request() method (Issue #510)"""

    def test_detects_project_landscape_pattern(self, canonical_handlers):
        """Test detection of 'project landscape' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me the project landscape",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_portfolio_pattern(self, canonical_handlers):
        """Test detection of 'portfolio' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's my portfolio looking like?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_project_overview_pattern(self, canonical_handlers):
        """Test detection of 'project overview' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Give me a project overview",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_portfolio_health_pattern(self, canonical_handlers):
        """Test detection of 'portfolio health' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me portfolio health",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_all_projects_health_pattern(self, canonical_handlers):
        """Test detection of 'all projects health' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How are all projects health?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_landscape_query(self, canonical_handlers):
        """Test that non-landscape queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is False


class TestProjectHealthCalculation:
    """Test suite for _calculate_project_health() method (Issue #510)"""

    def test_calculates_healthy_status(self, canonical_handlers):
        """Test health calculation for recently active project."""
        from datetime import datetime, timedelta

        # Arrange - Project active 7 days ago
        last_update = (datetime.now() - timedelta(days=7)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "healthy"
        assert "7 days" in result["reason"]

    def test_calculates_at_risk_status_by_time(self, canonical_handlers):
        """Test health calculation for project at risk due to time."""
        from datetime import datetime, timedelta

        # Arrange - Project active 20 days ago
        last_update = (datetime.now() - timedelta(days=20)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "at-risk"
        assert "20 days" in result["reason"]

    def test_calculates_at_risk_status_by_issues(self, canonical_handlers):
        """Test health calculation for project at risk due to open issues."""
        from datetime import datetime, timedelta

        # Arrange - Project active recently but many issues
        last_update = (datetime.now() - timedelta(days=5)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 25}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "at-risk"
        assert "25 open issues" in result["reason"]

    def test_calculates_stalled_status(self, canonical_handlers):
        """Test health calculation for stalled project."""
        from datetime import datetime, timedelta

        # Arrange - Project inactive for 45 days
        last_update = (datetime.now() - timedelta(days=45)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 3}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "stalled"
        assert "45 days" in result["reason"]

    def test_handles_missing_github_data(self, canonical_handlers):
        """Test health calculation with no GitHub data."""
        # Act
        result = canonical_handlers._calculate_project_health("TestProject", None)

        # Assert
        assert result["status"] == "unknown"
        assert "No GitHub data" in result["reason"]

    def test_handles_missing_updated_at(self, canonical_handlers):
        """Test health calculation with missing updated_at field."""
        # Arrange
        github_data = {"open_issues_count": 15}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert - Should fall back to issue count
        assert result["status"] == "healthy"


class TestLandscapeFormatting:
    """Test suite for landscape formatting methods (Issue #510)"""

    def test_format_embedded_with_all_statuses(self, canonical_handlers):
        """Test EMBEDDED format with projects in all health categories."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "Project A"}],
            "at-risk": [{"name": "Project B"}, {"name": "Project C"}],
            "stalled": [{"name": "Project D"}],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert "1 healthy" in result
        assert "2 at-risk" in result
        assert "1 stalled" in result

    def test_format_embedded_healthy_only(self, canonical_handlers):
        """Test EMBEDDED format with only healthy projects."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "Project A"}, {"name": "Project B"}],
            "at-risk": [],
            "stalled": [],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert result == "Portfolio: 2 healthy"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        # Arrange
        health_groups = {"healthy": [], "at-risk": [], "stalled": [], "unknown": []}

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert "No projects configured" in result

    def test_format_standard_includes_project_names(self, canonical_handlers):
        """Test STANDARD format includes project names."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "HealthyProject", "reason": "Active within 5 days"}],
            "at-risk": [
                {"name": "RiskyProject", "reason": "20 days since last activity"},
            ],
            "stalled": [
                {"name": "StalledProject", "reason": "45 days since last activity"},
            ],
            "unknown": [{"name": "UnknownProject", "reason": "No GitHub data"}],
        }

        # Act
        result = canonical_handlers._format_landscape_standard(health_groups)

        # Assert
        assert "Portfolio Health Overview" in result
        assert "HealthyProject" in result
        assert "RiskyProject" in result
        assert "StalledProject" in result
        assert "UnknownProject" in result
        assert "20 days since last activity" in result
        assert "45 days since last activity" in result

    def test_format_granular_includes_github_data(self, canonical_handlers):
        """Test GRANULAR format includes GitHub metadata."""
        # Arrange
        health_groups = {
            "healthy": [
                {
                    "name": "HealthyProject",
                    "reason": "Active within 5 days",
                    "github_data": {
                        "open_issues_count": 3,
                        "updated_at": "2025-12-20T10:00:00Z",
                    },
                }
            ],
            "at-risk": [],
            "stalled": [],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_granular(health_groups)

        # Assert
        assert "Full Health Analysis" in result
        assert "HealthyProject" in result
        assert "Open Issues: 3" in result
        assert "Last Updated:" in result
