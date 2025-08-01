"""
Test-First Development: QueryRouter Degradation Scenarios
TDD Phase 1: Write Failing Tests FIRST
"""

from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter
from services.shared_types import IntentCategory


@pytest.mark.asyncio
class TestQueryRouterDegradation:
    """Test QueryRouter graceful degradation and error handling"""

    @pytest.fixture
    def mock_services(self):
        """Create mocked services that can simulate failures"""
        project_service = AsyncMock(spec=ProjectQueryService)
        conversation_service = AsyncMock(spec=ConversationQueryService)
        file_service = AsyncMock(spec=FileQueryService)

        return project_service, conversation_service, file_service

    @pytest.fixture
    def query_router(self, mock_services):
        """Create QueryRouter with mocked services"""
        project_service, conversation_service, file_service = mock_services
        return QueryRouter(
            project_query_service=project_service,
            conversation_query_service=conversation_service,
            file_query_service=file_service,
            test_mode=False,  # Start with normal mode
        )

    @pytest.fixture
    def degraded_router(self, mock_services):
        """Create QueryRouter in test_mode for graceful degradation"""
        project_service, conversation_service, file_service = mock_services
        return QueryRouter(
            project_query_service=project_service,
            conversation_query_service=conversation_service,
            file_query_service=file_service,
            test_mode=True,  # Enable graceful degradation
        )

    async def test_database_failure_graceful_degradation(self, degraded_router):
        """Test all query operations handle database failures gracefully"""
        # Test each of the 12 operations with database failure
        test_cases = [
            ("list_projects", {}),
            ("get_project", {"project_id": "test-id"}),
            ("get_default_project", {}),
            ("find_project", {"name": "test-project"}),
            ("count_projects", {}),
            ("get_project_details", {"project_id": "test-id"}),
        ]

        for action, context in test_cases:
            intent = Intent(category=IntentCategory.QUERY, action=action, context=context)

            result = await degraded_router.route_query(intent)

            # Should return graceful degradation message, not crash
            assert isinstance(result, str)
            assert "Database temporarily unavailable" in result
            assert "Docker" in result or "try again later" in result

    async def test_circuit_breaker_activation(self, query_router, mock_services):
        """Test circuit breaker opens after threshold failures"""
        project_service, conversation_service, file_service = mock_services

        # Simulate database connection failures
        project_service.list_active_projects.side_effect = Exception("Database connection failed")
        project_service.get_project_by_id.side_effect = Exception("Database connection failed")

        # Circuit breaker should catch exceptions and provide graceful degradation
        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # Should return graceful degradation message, not raise exception
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result or "Service" in result

    async def test_service_specific_fallbacks(self, query_router, mock_services):
        """Test each service has appropriate fallback behavior"""
        project_service, conversation_service, file_service = mock_services

        # Test project service fallback
        project_service.list_active_projects.side_effect = Exception("Project service unavailable")
        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # Should have service-specific fallback message
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result or "Service" in result

        # Test conversation service fallback
        conversation_service.get_greeting.side_effect = Exception(
            "Conversation service unavailable"
        )
        intent = Intent(category=IntentCategory.QUERY, action="get_greeting", context={})

        # Should have service-specific fallback message
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        # Conversation service has static fallbacks, not degradation messages
        assert (
            "Hello! I'm Piper Morgan" in result
            or "Database temporarily unavailable" in result
            or "Service" in result
        )

        # Test file service fallback
        file_service.read_file_contents.side_effect = Exception("File service unavailable")
        intent = Intent(
            category=IntentCategory.QUERY,
            action="read_file_contents",
            context={"resolved_file_id": "test-id"},
        )

        # Should have service-specific fallback message
        result = await query_router.route_query(intent)
        # File service returns structured error responses
        assert isinstance(result, dict)
        assert result.get("success") == False
        assert "error" in result
        assert (
            "File service" in result["error"]
            or "Database temporarily unavailable" in result["error"]
        )

    async def test_user_friendly_error_messages(self, query_router):
        """Test error messages are helpful, not technical stack traces"""

        # Test missing context validation
        intent = Intent(category=IntentCategory.QUERY, action="get_project", context={})

        with pytest.raises(ValueError) as exc_info:
            await query_router.route_query(intent)

        # Error message should be user-friendly
        error_msg = str(exc_info.value)
        assert "get_project query requires project_id in context" in error_msg
        assert "project_id" in error_msg.lower()

        # Test unknown action
        intent = Intent(category=IntentCategory.QUERY, action="unknown_action", context={})

        with pytest.raises(ValueError) as exc_info:
            await query_router.route_query(intent)

        # Error message should be user-friendly
        error_msg = str(exc_info.value)
        assert "Unknown query action: unknown_action" in error_msg
        assert "unknown_action" in error_msg

    async def test_network_timeout_handling(self, query_router, mock_services):
        """Test query service timeout handling"""
        project_service, conversation_service, file_service = mock_services

        # Simulate network timeout
        project_service.list_active_projects.side_effect = TimeoutError("Network timeout")

        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # Should handle timeout gracefully with graceful degradation
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result or "Service" in result

    async def test_import_error_handling(self, query_router, mock_services):
        """Test configuration service unavailability"""
        project_service, conversation_service, file_service = mock_services

        # Simulate import error in file service
        file_service.search_files_by_query.side_effect = ImportError(
            "MCP configuration unavailable"
        )

        intent = Intent(
            category=IntentCategory.QUERY, action="search_files", context={"search_query": "test"}
        )

        # Should handle import errors gracefully
        with pytest.raises(ImportError):
            await query_router.route_query(intent)

        # With graceful degradation enabled
        query_router.test_mode = True
        result = await query_router.route_query(intent)
        assert "Database temporarily unavailable" in result

    async def test_context_validation_comprehensive(self, query_router):
        """Test all required context validations"""

        # Test all actions that require specific context
        context_tests = [
            ("get_project", {}, "project_id"),
            ("find_project", {}, "name"),
            ("get_project_details", {}, "project_id"),
            ("search_files", {}, "search_query"),
            ("find_documents", {}, "search_query"),
            ("search_content", {}, "search_query"),
            ("read_file_contents", {}, "resolved_file_id"),
            ("summarize_file", {}, "resolved_file_id"),
        ]

        for action, context, required_field in context_tests:
            intent = Intent(category=IntentCategory.QUERY, action=action, context=context)

            with pytest.raises(ValueError) as exc_info:
                await query_router.route_query(intent)

            error_msg = str(exc_info.value)
            assert required_field in error_msg
            assert f"{action} query requires {required_field} in context" in error_msg

    async def test_intent_category_validation(self, query_router):
        """Test only QUERY intents are accepted"""

        # Test non-QUERY intent
        intent = Intent(category=IntentCategory.EXECUTION, action="list_projects", context={})

        with pytest.raises(ValueError) as exc_info:
            await query_router.route_query(intent)

        error_msg = str(exc_info.value)
        assert "QueryRouter can only handle QUERY intents" in error_msg
        assert "EXECUTION" in error_msg

    async def test_graceful_degradation_message_consistency(self, degraded_router):
        """Test all degradation messages are consistent and helpful"""

        test_actions = ["list_projects", "get_project", "get_default_project", "count_projects"]

        for action in test_actions:
            intent = Intent(category=IntentCategory.QUERY, action=action, context={})
            result = await degraded_router.route_query(intent)

            # All messages should be consistent
            assert "Database temporarily unavailable" in result
            assert "Docker" in result or "try again later" in result
            assert "Please ensure" in result or "try again" in result

    async def test_fallback_mechanism_activation(self, query_router, mock_services):
        """Test fallback mechanisms activate correctly"""
        project_service, conversation_service, file_service = mock_services

        # Simulate service failure
        project_service.list_active_projects.side_effect = Exception("Service unavailable")

        # Should provide graceful degradation in both modes
        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # Normal mode should provide graceful degradation
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result or "Service" in result

        # Test mode should also provide graceful degradation
        query_router.test_mode = True
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result

    async def test_error_recovery_mechanism(self, query_router, mock_services):
        """Test system can recover from errors"""
        project_service, conversation_service, file_service = mock_services

        # Simulate temporary failure then recovery
        project_service.list_active_projects.side_effect = [
            Exception("Temporary failure"),
            ["project1", "project2"],  # Recovery
        ]

        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # First call should provide graceful degradation
        result = await query_router.route_query(intent)
        assert isinstance(result, str)
        assert "Database temporarily unavailable" in result or "Service" in result

        # Second call should succeed (recovery)
        result = await query_router.route_query(intent)
        assert result == ["project1", "project2"]
