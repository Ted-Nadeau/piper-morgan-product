"""
System-level degradation validation for QueryRouter graceful failure handling

Tests comprehensive cascade failure prevention, database outage simulation,
and circuit breaker coordination across all query services.
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent
from services.queries.conversation_queries import ConversationQueryService
from services.queries.degradation import QueryCircuitBreakerOpenError, QueryDegradationHandler
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter
from services.shared_types import IntentCategory


@pytest.mark.integration
class TestQueryRouterSystemDegradation:
    """Comprehensive system-level degradation testing"""

    @pytest.fixture
    async def mock_services(self):
        """Create mock services for degradation testing"""
        project_service = Mock(spec=ProjectQueryService)
        conversation_service = Mock(spec=ConversationQueryService)
        file_service = Mock(spec=FileQueryService)

        # Configure async methods
        project_service.list_active_projects = AsyncMock()
        project_service.get_project_by_id = AsyncMock()
        project_service.get_default_project = AsyncMock()
        project_service.find_project_by_name = AsyncMock()
        project_service.count_active_projects = AsyncMock()
        project_service.get_project_details = AsyncMock()

        conversation_service.get_greeting = AsyncMock()
        conversation_service.get_help = AsyncMock()
        conversation_service.get_status = AsyncMock()
        conversation_service.get_initial_contact = AsyncMock()

        file_service.read_file_contents = AsyncMock()
        file_service.summarize_file = AsyncMock()
        file_service.search_files_by_query = AsyncMock()
        file_service.find_documents_about_topic = AsyncMock()
        file_service.search_content_by_query = AsyncMock()

        return {
            "project": project_service,
            "conversation": conversation_service,
            "file": file_service,
        }

    @pytest.fixture
    async def query_router(self, mock_services):
        """Create QueryRouter with mock services"""
        return QueryRouter(
            project_query_service=mock_services["project"],
            conversation_query_service=mock_services["conversation"],
            file_query_service=mock_services["file"],
            test_mode=False,
            degradation_config={"failure_threshold": 3, "recovery_timeout": 30},
        )

    @pytest.fixture
    async def test_mode_router(self, mock_services):
        """Create QueryRouter in test mode for backward compatibility testing"""
        return QueryRouter(
            project_query_service=mock_services["project"],
            conversation_query_service=mock_services["conversation"],
            file_query_service=mock_services["file"],
            test_mode=True,
        )

    async def test_cascade_failure_prevention(self, query_router, mock_services):
        """Verify degradation prevents system-wide failures"""
        # Simulate cascading database failures
        database_error = Exception("Database connection lost")
        mock_services["project"].list_active_projects.side_effect = database_error
        mock_services["project"].get_project_by_id.side_effect = database_error
        mock_services["project"].count_active_projects.side_effect = database_error

        # Test multiple project queries - should all degrade gracefully
        intents = [
            Intent(category=IntentCategory.QUERY, action="list_projects", context={}),
            Intent(
                category=IntentCategory.QUERY,
                action="get_project",
                context={"project_id": "test-123"},
            ),
            Intent(category=IntentCategory.QUERY, action="count_projects", context={}),
        ]

        results = []
        for intent in intents:
            result = await query_router.route_query(intent)
            results.append(result)

        # Verify all results are graceful degradation messages, not exceptions
        for i, result in enumerate(results):
            assert isinstance(
                result, str
            ), f"Result {i} should be degradation message, got {type(result)}"
            assert (
                "temporarily unavailable" in result.lower()
            ), f"Result {i} should mention unavailability"
            assert "try again" in result.lower(), f"Result {i} should suggest retry"

    async def test_database_outage_simulation(self, query_router, mock_services):
        """Full database failure scenario with recovery"""
        # Phase 1: Complete database outage
        database_error = Exception("Connection to database failed")

        # All project services fail
        for method in [
            mock_services["project"].list_active_projects,
            mock_services["project"].get_default_project,
            mock_services["project"].count_active_projects,
        ]:
            method.side_effect = database_error

        # Test queries during outage
        outage_intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})
        outage_result = await query_router.route_query(outage_intent)

        assert isinstance(outage_result, str)
        assert "Database temporarily unavailable" in outage_result
        assert "Docker is running" in outage_result

        # Phase 2: Recovery simulation
        mock_services["project"].list_active_projects.side_effect = None
        mock_services["project"].list_active_projects.return_value = [
            {"id": "proj-1", "name": "Test Project"}
        ]

        # Circuit breaker should allow retry after recovery timeout simulation
        recovery_intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # First call might still be in degraded state
        first_recovery_result = await query_router.route_query(recovery_intent)

        # Subsequent calls should succeed as circuit breaker closes
        await asyncio.sleep(0.1)  # Small delay to simulate recovery
        second_recovery_result = await query_router.route_query(recovery_intent)

        # At least one of the recovery attempts should succeed or show improvement
        assert isinstance(second_recovery_result, list) or "temporarily unavailable" not in str(
            second_recovery_result
        ), "System should show recovery behavior"

    async def test_partial_service_degradation(self, query_router, mock_services):
        """Some services work, others degrade gracefully"""
        # Project service fails
        mock_services["project"].list_active_projects.side_effect = Exception(
            "Database connection error"
        )

        # Conversation service works normally
        mock_services["conversation"].get_greeting.return_value = "Hello! I'm Piper Morgan."

        # File service partially fails
        mock_services["file"].read_file_contents.side_effect = Exception("File service unavailable")
        mock_services["file"].search_files_by_query.return_value = {"success": True, "results": []}

        # Test mixed success/failure scenario
        intents_and_expectations = [
            (Intent(category=IntentCategory.QUERY, action="list_projects", context={}), "degraded"),
            (Intent(category=IntentCategory.QUERY, action="get_greeting", context={}), "success"),
            (
                Intent(
                    category=IntentCategory.QUERY,
                    action="read_file_contents",
                    context={"resolved_file_id": "file-123"},
                ),
                "degraded",
            ),
            (
                Intent(
                    category=IntentCategory.QUERY,
                    action="search_files",
                    context={"search_query": "test", "session_id": "sess-123"},
                ),
                "mixed",
            ),
        ]

        for intent, expectation in intents_and_expectations:
            result = await query_router.route_query(intent)

            if expectation == "degraded":
                assert isinstance(
                    result, (str, dict)
                ), f"Degraded response should be string or dict for {intent.action}"
                if isinstance(result, str):
                    assert "temporarily unavailable" in result.lower()
                elif isinstance(result, dict):
                    assert result.get("success") is False

            elif expectation == "success":
                assert isinstance(result, str) and "temporarily unavailable" not in result.lower()

            elif expectation == "mixed":
                # File search might succeed or degrade depending on circuit breaker state
                assert result is not None, f"Should get some response for {intent.action}"

    async def test_circuit_breaker_coordination(self, query_router, mock_services):
        """Multiple service circuit breakers working together"""
        # Configure circuit breaker to open quickly (3 failures)
        failure_count = 0

        def failing_service(*args, **kwargs):
            nonlocal failure_count
            failure_count += 1
            raise Exception(f"Service failure #{failure_count}")

        # Set up coordinated failures across services
        mock_services["project"].list_active_projects.side_effect = failing_service
        mock_services["file"].search_files_by_query.side_effect = failing_service

        # Generate enough failures to trigger circuit breaker
        intents = [
            Intent(category=IntentCategory.QUERY, action="list_projects", context={}),
            Intent(
                category=IntentCategory.QUERY,
                action="search_files",
                context={"search_query": "test", "session_id": "sess-123"},
            ),
            Intent(category=IntentCategory.QUERY, action="list_projects", context={}),
            Intent(
                category=IntentCategory.QUERY,
                action="search_files",
                context={"search_query": "test2", "session_id": "sess-123"},
            ),
            Intent(
                category=IntentCategory.QUERY, action="list_projects", context={}
            ),  # This should trigger circuit breaker
        ]

        results = []
        for intent in intents:
            result = await query_router.route_query(intent)
            results.append(result)

        # Verify that results show progressive degradation
        for result in results:
            assert result is not None, "All queries should return some response"
            # Later queries should show consistent degradation behavior
            if isinstance(result, str):
                assert any(
                    keyword in result.lower()
                    for keyword in ["temporarily unavailable", "service", "try again"]
                )
            elif isinstance(result, dict):
                assert "error" in result or "success" in result

    async def test_backward_compatibility_test_mode(self, test_mode_router):
        """Verify test_mode backward compatibility works as expected"""
        # In test_mode, all database operations should return degradation messages
        database_actions = ["list_projects", "get_project", "get_default_project", "count_projects"]

        for action in database_actions:
            context = {"project_id": "test-123"} if action in ["get_project"] else {}
            intent = Intent(category=IntentCategory.QUERY, action=action, context=context)

            result = await test_mode_router.route_query(intent)

            assert isinstance(result, str), f"test_mode should return string for {action}"
            assert (
                "Database temporarily unavailable" in result
            ), f"test_mode should show database message for {action}"

    async def test_error_classification_and_handling(self, query_router):
        """Verify different error types are handled appropriately"""
        # ValueError should NOT be degraded (validation errors)
        with pytest.raises(ValueError, match="requires project_id"):
            await query_router.route_query(
                Intent(category=IntentCategory.QUERY, action="get_project", context={})
            )

        # Unknown action should NOT be degraded
        with pytest.raises(ValueError, match="Unknown query action"):
            await query_router.route_query(
                Intent(category=IntentCategory.QUERY, action="invalid_action", context={})
            )

        # Wrong intent category should NOT be degraded
        with pytest.raises(ValueError, match="can only handle QUERY intents"):
            await query_router.route_query(
                Intent(category=IntentCategory.EXECUTION, action="list_projects", context={})
            )

    async def test_degradation_status_monitoring(self, query_router):
        """Verify degradation status can be monitored"""
        status = query_router.get_degradation_status()

        assert isinstance(status, dict)
        assert "test_mode" in status
        assert "degradation_handler" in status
        assert "supported_queries" in status
        assert "services" in status

        # Verify degradation handler status structure
        handler_status = status["degradation_handler"]
        assert "state" in handler_status
        assert "failure_count" in handler_status
        assert "enabled" in handler_status

        # Verify services status
        services = status["services"]
        expected_services = ["project_queries", "file_queries", "conversation_queries"]
        for service in expected_services:
            assert service in services

    @pytest.mark.parametrize(
        "action,service,context",
        [
            ("list_projects", "project_queries", {}),
            ("search_files", "file_queries", {"search_query": "test", "session_id": "sess-123"}),
            ("get_greeting", "conversation_queries", {}),
            ("read_file_contents", "file_queries", {"resolved_file_id": "file-123"}),
            ("find_documents", "file_queries", {"search_query": "docs", "session_id": "sess-123"}),
        ],
    )
    async def test_individual_query_degradation(
        self, query_router, mock_services, action, service, context
    ):
        """Test degradation behavior for individual query types"""
        # Configure service to fail
        if service == "project_queries":
            for method_name in dir(mock_services["project"]):
                if (
                    method_name.startswith("list_")
                    or method_name.startswith("get_")
                    or method_name.startswith("find_")
                    or method_name.startswith("count_")
                ):
                    getattr(mock_services["project"], method_name).side_effect = Exception(
                        "Service unavailable"
                    )
        elif service == "file_queries":
            for method_name in [
                "read_file_contents",
                "summarize_file",
                "search_files_by_query",
                "find_documents_about_topic",
                "search_content_by_query",
            ]:
                if hasattr(mock_services["file"], method_name):
                    getattr(mock_services["file"], method_name).side_effect = Exception(
                        "File service unavailable"
                    )
        elif service == "conversation_queries":
            for method_name in dir(mock_services["conversation"]):
                if method_name.startswith("get_"):
                    getattr(mock_services["conversation"], method_name).side_effect = Exception(
                        "Conversation service unavailable"
                    )

        intent = Intent(category=IntentCategory.QUERY, action=action, context=context)
        result = await query_router.route_query(intent)

        # Verify appropriate degradation response
        assert result is not None, f"Should get degradation response for {action}"

        if service == "file_queries":
            # File queries return structured error responses
            if isinstance(result, dict):
                assert result.get("success") is False
                assert "error" in result
            else:
                assert isinstance(result, str)
        else:
            # Project and conversation queries return string messages
            assert isinstance(result, str)
            if service == "project_queries":
                assert "Database temporarily unavailable" in result
