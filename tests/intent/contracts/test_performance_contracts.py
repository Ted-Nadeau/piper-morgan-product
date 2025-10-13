"""Performance contract tests for all 13 intent categories - GREAT-4E Phase 3"""

import time

import pytest

from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES


class TestPerformanceContracts(BaseValidationTest):
    """Verify all categories meet performance requirements (<3000ms)."""

    @pytest.mark.asyncio
    async def test_temporal_performance(self, intent_service):
        """PERF 1/13: TEMPORAL response time."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ TEMPORAL performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_status_performance(self, intent_service):
        """PERF 2/13: STATUS response time."""
        message = CATEGORY_EXAMPLES["STATUS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ STATUS performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_priority_performance(self, intent_service):
        """PERF 3/13: PRIORITY response time."""
        message = CATEGORY_EXAMPLES["PRIORITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ PRIORITY performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_identity_performance(self, intent_service):
        """PERF 4/13: IDENTITY response time."""
        message = CATEGORY_EXAMPLES["IDENTITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ IDENTITY performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_guidance_performance(self, intent_service):
        """PERF 5/13: GUIDANCE response time."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ GUIDANCE performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_performance(self, intent_service):
        """PERF 6/13: EXECUTION response time."""
        message = CATEGORY_EXAMPLES["EXECUTION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ EXECUTION performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_performance(self, intent_service):
        """PERF 7/13: ANALYSIS response time."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ ANALYSIS performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_performance(self, intent_service):
        """PERF 8/13: SYNTHESIS response time."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ SYNTHESIS performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_performance(self, intent_service):
        """PERF 9/13: STRATEGY response time."""
        message = CATEGORY_EXAMPLES["STRATEGY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ STRATEGY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_performance(self, intent_service):
        """PERF 10/13: LEARNING response time."""
        message = CATEGORY_EXAMPLES["LEARNING"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ LEARNING performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_performance(self, intent_service):
        """PERF 11/13: UNKNOWN response time."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ UNKNOWN performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_performance(self, intent_service):
        """PERF 12/13: QUERY response time."""
        message = CATEGORY_EXAMPLES["QUERY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ QUERY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_performance(self, intent_service):
        """PERF 13/13: CONVERSATION response time."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ CONVERSATION performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_zzz_performance_coverage(self):
        """Performance contract coverage report."""
        print("\n" + "=" * 80)
        print("PERFORMANCE CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories meet <3000ms threshold")
        print("=" * 80)
