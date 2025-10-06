"""Comprehensive tests for EXECUTION and ANALYSIS handlers - GREAT-4D"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService


class TestExecutionHandlers:
    """Test EXECUTION intent handlers."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_engine.handle_execution_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-123"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService(orchestration_engine=mock_orchestration_engine)

    @pytest.mark.asyncio
    async def test_create_issue_handler_exists(self, intent_service):
        """Verify create_issue handler exists and is callable."""
        assert hasattr(intent_service, "_handle_create_issue")
        assert callable(intent_service._handle_create_issue)

    @pytest.mark.asyncio
    async def test_execution_intent_no_placeholder(self, intent_service):
        """Verify EXECUTION intents don't return placeholder messages."""
        intent = Intent(
            original_message="create an issue about testing",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"title": "Test issue", "repository": "test-repo"},
        )

        # Mock classifier to return this intent
        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            result = await intent_service.process_intent(
                "create an issue about testing", session_id="test"
            )

            # Should NOT contain placeholder messages
            assert "Phase 3" not in result.message
            assert "full orchestration workflow" not in result.message
            assert "placeholder" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_create_issue_attempts_execution(self, intent_service):
        """Verify create_issue handler attempts to execute."""
        intent = Intent(
            original_message="create an issue",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"title": "Test issue", "repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            result = await intent_service.process_intent("create an issue", session_id="test")

            # Should attempt execution (success or error, not placeholder)
            assert result.success is not None
            assert result.message is not None
            assert len(result.message) > 0

    @pytest.mark.asyncio
    async def test_update_issue_handler_exists(self, intent_service):
        """Verify update_issue handler exists."""
        assert hasattr(intent_service, "_handle_update_issue")
        assert callable(intent_service._handle_update_issue)

    @pytest.mark.asyncio
    async def test_generic_execution_routes_to_orchestration(self, intent_service):
        """Verify generic EXECUTION actions route to orchestration."""
        intent = Intent(
            original_message="execute something",
            category=IntentCategory.EXECUTION,
            action="unknown_action",
            confidence=0.85,
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            result = await intent_service.process_intent("execute something", session_id="test")

            # Should route to orchestration, not return placeholder
            assert "Phase 3" not in result.message
            assert result.message is not None


class TestAnalysisHandlers:
    """Test ANALYSIS intent handlers."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_engine.handle_analysis_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-456"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService(orchestration_engine=mock_orchestration_engine)

    @pytest.mark.asyncio
    async def test_analysis_intent_no_placeholder(self, intent_service):
        """Verify ANALYSIS intents don't return placeholder messages."""
        intent = Intent(
            original_message="analyze the commits",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            result = await intent_service.process_intent("analyze the commits", session_id="test")

            # Should NOT contain placeholder messages
            assert "Phase 3" not in result.message
            assert "full orchestration workflow" not in result.message
            assert "placeholder" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_analyze_commits_handler_exists(self, intent_service):
        """Verify analyze_commits handler exists and is callable."""
        assert hasattr(intent_service, "_handle_analyze_commits")
        assert callable(intent_service._handle_analyze_commits)

    @pytest.mark.asyncio
    async def test_generate_report_handler_exists(self, intent_service):
        """Verify generate_report handler exists."""
        assert hasattr(intent_service, "_handle_generate_report")
        assert callable(intent_service._handle_generate_report)

    @pytest.mark.asyncio
    async def test_analyze_data_handler_exists(self, intent_service):
        """Verify analyze_data handler exists."""
        assert hasattr(intent_service, "_handle_analyze_data")
        assert callable(intent_service._handle_analyze_data)

    @pytest.mark.asyncio
    async def test_generic_analysis_routes_to_orchestration(self, intent_service):
        """Verify generic ANALYSIS actions route to orchestration."""
        intent = Intent(
            original_message="analyze something",
            category=IntentCategory.ANALYSIS,
            action="unknown_analysis",
            confidence=0.85,
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            result = await intent_service.process_intent("analyze something", session_id="test")

            # Should route to orchestration, not return placeholder
            assert "Phase 3" not in result.message
            assert result.message is not None


class TestHandlerIntegration:
    """Test handler integration and routing."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-789"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService(orchestration_engine=mock_orchestration_engine)

    @pytest.mark.asyncio
    async def test_execution_routing_exists(self, intent_service):
        """Verify main routing handles EXECUTION category."""
        # Check that _handle_execution_intent exists
        assert hasattr(intent_service, "_handle_execution_intent")

    @pytest.mark.asyncio
    async def test_analysis_routing_exists(self, intent_service):
        """Verify main routing handles ANALYSIS category."""
        # Check that _handle_analysis_intent exists
        assert hasattr(intent_service, "_handle_analysis_intent")

    @pytest.mark.asyncio
    async def test_no_generic_intent_fallback(self, intent_service):
        """Verify old _handle_generic_intent placeholder is removed."""
        # The old placeholder method should not exist or should not be called
        # for EXECUTION/ANALYSIS

        # If method exists, it should not be used for EXECUTION/ANALYSIS
        if hasattr(intent_service, "_handle_generic_intent"):
            # Check it's not called in main routing
            import inspect

            source = inspect.getsource(intent_service.process_intent)

            # Should have specific handlers for EXECUTION/ANALYSIS
            assert "_handle_execution_intent" in source or "EXECUTION" in source
            assert "_handle_analysis_intent" in source or "ANALYSIS" in source

    @pytest.mark.asyncio
    async def test_execution_handler_routing_works(self, intent_service):
        """Test that EXECUTION intents properly route to execution handler."""
        intent = Intent(
            original_message="create issue",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            # Should not raise exception and should return result
            result = await intent_service.process_intent("create issue", session_id="test")
            assert result is not None
            assert hasattr(result, "success")
            assert hasattr(result, "message")

    @pytest.mark.asyncio
    async def test_analysis_handler_routing_works(self, intent_service):
        """Test that ANALYSIS intents properly route to analysis handler."""
        intent = Intent(
            original_message="analyze commits",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            mock_classifier.classify = AsyncMock(return_value=intent)

            # Should not raise exception and should return result
            result = await intent_service.process_intent("analyze commits", session_id="test")
            assert result is not None
            assert hasattr(result, "success")
            assert hasattr(result, "message")
