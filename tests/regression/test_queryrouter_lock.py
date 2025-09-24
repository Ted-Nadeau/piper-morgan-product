"""
CORE-GREAT-1C: QueryRouter Lock Tests
Regression prevention for GREAT-1A & GREAT-1B achievements

These tests ensure the QueryRouter infrastructure cannot be accidentally disabled again.
Root cause prevention for the 75% pattern that led to QueryRouter being disabled with TODO comments.
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.orchestration.engine import OrchestrationEngine
from services.queries.query_router import QueryRouter
from services.shared_types import IntentCategory


class TestQueryRouterLock:
    """Lock tests to prevent QueryRouter infrastructure regression"""

    @pytest.mark.asyncio
    async def test_queryrouter_must_be_enabled_in_orchestration_engine(self):
        """
        LOCK TEST: OrchestrationEngine MUST have working QueryRouter integration

        This test prevents the scenario that occurred in commit 8ce699eb6:
        - QueryRouter was disabled with TODO comment due to "complex dependency chain"
        - Real issue was session management, not complexity
        - This led to 75% pattern: working code disabled and abandoned
        """
        engine = OrchestrationEngine()

        # CRITICAL: QueryRouter MUST be accessible through OrchestrationEngine
        query_router = await engine.get_query_router()

        # Verify QueryRouter is properly initialized (not None/disabled)
        assert query_router is not None, "QueryRouter MUST NOT be disabled in OrchestrationEngine"
        assert isinstance(query_router, QueryRouter), "QueryRouter must be proper instance"

        # Verify all required services are connected
        assert query_router.project_queries is not None, "Project queries MUST be connected"
        assert (
            query_router.conversation_queries is not None
        ), "Conversation queries MUST be connected"
        assert query_router.file_queries is not None, "File queries MUST be connected"

    @pytest.mark.asyncio
    async def test_sessionaware_wrappers_must_exist_and_function(self):
        """
        LOCK TEST: Session-aware wrappers MUST exist and function correctly

        Prevents regression to the original failure mode where repositories
        required AsyncSession parameters but were instantiated without sessions.
        """
        from services.queries.session_aware_wrappers import (
            SessionAwareFileQueryService,
            SessionAwareProjectQueryService,
        )

        # Verify session-aware wrappers exist
        project_service = SessionAwareProjectQueryService()
        file_service = SessionAwareFileQueryService()

        # Mock the session and repository layers
        with patch("services.queries.session_aware_wrappers.AsyncSessionFactory") as mock_factory:
            mock_session = AsyncMock()
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            with patch(
                "services.queries.session_aware_wrappers.ProjectRepository"
            ) as mock_proj_repo:
                mock_proj_repo.return_value = AsyncMock()

                with patch(
                    "services.queries.session_aware_wrappers.ProjectQueryService"
                ) as mock_proj_service:
                    mock_service_instance = AsyncMock()
                    mock_service_instance.list_active_projects.return_value = []
                    mock_proj_service.return_value = mock_service_instance

                    # CRITICAL: Must not throw session-related errors
                    result = await project_service.list_active_projects()
                    assert isinstance(
                        result, list
                    ), "Session-aware wrapper must handle sessions correctly"

    @pytest.mark.asyncio
    async def test_handle_query_intent_bridge_must_exist(self):
        """
        LOCK TEST: OrchestrationEngine MUST have working handle_query_intent bridge method

        This is the GREAT-1B integration that bridges Intent → QueryRouter.
        Prevents regression where QUERY intents cannot reach QueryRouter.
        """
        engine = OrchestrationEngine()

        # Verify handle_query_intent method exists
        assert hasattr(
            engine, "handle_query_intent"
        ), "handle_query_intent bridge method MUST exist"

        # Test with mock intent
        intent = Intent(category=IntentCategory.QUERY, action="search_projects", context={})

        # Mock the QueryRouter to avoid database dependencies
        with patch.object(engine, "get_query_router") as mock_get_router:
            mock_router = AsyncMock()
            mock_router.project_queries.list_active_projects.return_value = []
            mock_get_router.return_value = mock_router

            # CRITICAL: Must handle QUERY intents without errors
            result = await engine.handle_query_intent(intent)

            assert isinstance(result, dict), "handle_query_intent must return structured response"
            assert "intent_handled" in result, "Response must indicate intent was handled"
            assert result["intent_handled"] is True, "QUERY intent must be successfully handled"

    @pytest.mark.asyncio
    async def test_queryrouter_initialization_cannot_fail_silently(self):
        """
        LOCK TEST: QueryRouter initialization errors MUST be visible, not hidden

        Prevents the original failure pattern where initialization issues
        were hidden behind TODO comments instead of being resolved.
        """
        engine = OrchestrationEngine()

        # This should succeed or fail loudly, never silently disable
        try:
            query_router = await engine.get_query_router()
            # If it succeeds, verify it's functional
            assert query_router is not None
            assert hasattr(query_router, "route_query")
        except Exception as e:
            # If it fails, the error must be specific and actionable
            pytest.fail(
                f"QueryRouter initialization failed: {e}. "
                f"This MUST be fixed, not disabled with TODO comments."
            )

    def test_orchestration_engine_source_has_no_queryrouter_disabling_comments(self):
        """
        LOCK TEST: Verify OrchestrationEngine source has no TODO comments about disabling QueryRouter

        Code inspection test to prevent future developers from disabling QueryRouter
        with TODO comments instead of fixing the underlying issue.
        """
        import os

        # Read the engine.py source file directly
        engine_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "services", "orchestration", "engine.py"
        )
        with open(engine_path, "r") as f:
            source = f.read()

        # Search for dangerous patterns that led to the original disabling
        dangerous_patterns = [
            "QueryRouter initialization temporarily disabled",
            "TODO.*QueryRouter.*disabled",
            "TODO.*complex dependency chain",
            "# QueryRouter disabled",
            "# TODO.*QueryRouter",
        ]

        import re

        for pattern in dangerous_patterns:
            matches = re.search(pattern, source, re.IGNORECASE)
            assert matches is None, (
                f"DANGEROUS PATTERN DETECTED: '{pattern}' found in engine.py. "
                f"QueryRouter disabling is FORBIDDEN. Fix the issue instead."
            )

    @pytest.mark.asyncio
    async def test_query_intent_processing_end_to_end_path_exists(self):
        """
        LOCK TEST: Complete QUERY intent processing path must exist

        Ensures the full pipeline Intent → OrchestrationEngine → QueryRouter → Response
        is connected and functional (even if mocked for testing).
        """
        engine = OrchestrationEngine()

        # Test QUERY intent end-to-end processing
        query_intent = Intent(category=IntentCategory.QUERY, action="get_greeting", context={})

        # Mock the full chain
        with patch.object(engine, "get_query_router") as mock_get_router:
            mock_router = AsyncMock()
            mock_router.conversation_queries.get_greeting.return_value = "Hello! I'm Piper Morgan."
            mock_get_router.return_value = mock_router

            # CRITICAL: Complete processing path must work
            result = await engine.handle_query_intent(query_intent)

            assert result is not None, "QUERY processing must return a result"
            assert result.get("intent_handled") is True, "QUERY must be successfully processed"
            assert "message" in result, "QUERY processing must return user-friendly message"

    def test_session_aware_wrapper_files_must_exist(self):
        """
        LOCK TEST: Session-aware wrapper files must exist and be importable

        Prevents regression where the session management solution is deleted,
        causing QueryRouter to fail initialization again.
        """
        try:
            from services.queries.session_aware_wrappers import (
                SessionAwareFileQueryService,
                SessionAwareProjectQueryService,
            )
        except ImportError as e:
            pytest.fail(f"Session-aware wrappers MUST exist and be importable. Error: {e}")

        # Verify the classes have required methods
        assert hasattr(SessionAwareProjectQueryService, "list_active_projects")
        assert hasattr(SessionAwareFileQueryService, "list_recent_files")

    @pytest.mark.asyncio
    async def test_performance_requirement_queryrouter_initialization_under_500ms(self):
        """
        LOCK TEST: QueryRouter initialization must meet performance requirements

        Ensures QueryRouter initialization is fast enough for production use,
        preventing performance concerns from being used as excuse to disable it.
        """
        engine = OrchestrationEngine()

        import time

        start_time = time.time()

        # Initialize QueryRouter (should be cached after first call)
        query_router = await engine.get_query_router()

        end_time = time.time()
        initialization_time_ms = (end_time - start_time) * 1000

        # Performance requirement from GREAT-1A success criteria
        assert initialization_time_ms < 500, (
            f"QueryRouter initialization took {initialization_time_ms:.2f}ms, "
            f"must be under 500ms. Optimize, don't disable."
        )

        # Verify subsequent calls are fast (cached)
        start_time = time.time()
        query_router_cached = await engine.get_query_router()
        end_time = time.time()
        cached_time_ms = (end_time - start_time) * 1000

        assert (
            cached_time_ms < 50
        ), f"Cached QueryRouter access took {cached_time_ms:.2f}ms, should be <50ms"
        assert query_router is query_router_cached, "QueryRouter should be cached/singleton"


@pytest.mark.integration
class TestQueryRouterIntegrationLock:
    """Integration lock tests requiring actual database/services"""

    @pytest.mark.asyncio
    async def test_queryrouter_works_with_real_session_factory(self):
        """
        INTEGRATION LOCK TEST: QueryRouter must work with real AsyncSessionFactory

        This tests the actual session management that was the root cause
        of the original QueryRouter disabling. Requires database to be running.
        """
        engine = OrchestrationEngine()

        try:
            # This should work with real database session management
            query_router = await engine.get_query_router()

            # Verify we can create a simple intent and process it
            intent = Intent(category=IntentCategory.QUERY, action="count_projects", context={})

            result = await engine.handle_query_intent(intent)

            # Should return structured response, not crash
            assert isinstance(result, dict)
            assert "intent_handled" in result

        except Exception as e:
            pytest.fail(
                f"QueryRouter integration with real session factory failed: {e}. "
                f"This indicates session management regression."
            )
