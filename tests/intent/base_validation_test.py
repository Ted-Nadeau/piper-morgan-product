"""Base test class for GREAT-4E validation"""

from typing import Any, Dict

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES, PERFORMANCE_THRESHOLDS


class BaseValidationTest:
    """Base class for intent validation tests."""

    @pytest.fixture
    async def intent_service(self):
        from services.container import ServiceContainer
        from services.container.service_registry import ServiceRegistry
        from services.domain.llm_domain_service import LLMDomainService
        from services.intent_service import classifier
        from services.llm.clients import llm_client
        from services.orchestration.engine import OrchestrationEngine

        # Initialize and register LLM service (Phase 1.6: Updated to use container pattern)
        llm_domain_service = LLMDomainService()
        await llm_domain_service.initialize()

        # Get container instance and access internal registry for test setup
        container = ServiceContainer()
        container._registry.register("llm", llm_domain_service)
        container._initialized = True  # Mark as initialized for tests

        orchestration_engine = OrchestrationEngine(llm_client=llm_client)
        service = IntentService(orchestration_engine=orchestration_engine)

        yield service

        # Cleanup: Reset classifier's cached LLM and ServiceContainer (Phase 1.6)
        classifier._llm = None
        ServiceContainer.reset()

    async def validate_category(
        self, category: str, interface: str, intent_service: IntentService
    ) -> Dict[str, Any]:
        """
        Validate a category through a specific interface.

        Returns validation results.
        """
        example_query = CATEGORY_EXAMPLES[category]

        # Track coverage
        coverage.categories_tested.add(category)
        coverage.interfaces_tested.add(interface)

        # Test will be implemented by subclass
        return {
            "category": category,
            "interface": interface,
            "example": example_query,
            "tested": True,
        }

    def assert_no_placeholder(self, message: str):
        """Verify no placeholder messages."""
        assert "Phase 3" not in message
        assert "full orchestration workflow" not in message
        assert "placeholder" not in message.lower()

    def assert_performance(self, duration_ms: float):
        """Verify performance threshold."""
        threshold = PERFORMANCE_THRESHOLDS["max_response_time_ms"]
        assert (
            duration_ms < threshold
        ), f"Response time {duration_ms}ms exceeds threshold {threshold}ms"
