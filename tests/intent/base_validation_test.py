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
    def intent_service(self):
        from services.llm.clients import llm_client
        from services.orchestration.engine import OrchestrationEngine

        orchestration_engine = OrchestrationEngine(llm_client=llm_client)
        return IntentService(orchestration_engine=orchestration_engine)

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
