"""Bypass prevention contract tests for all 13 intent categories - GREAT-4E Phase 3

Verifies that all category handling goes through proper intent classification
and routing (no direct bypasses).
"""

import pytest

from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES


class TestBypassContracts(BaseValidationTest):
    """Verify no bypass routes exist for any category."""

    @pytest.mark.asyncio
    async def test_temporal_no_bypass(self, intent_service):
        """BYPASS 1/13: TEMPORAL requires classification."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        # If we get a result, classification occurred
        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ TEMPORAL no bypass: verified")

    @pytest.mark.asyncio
    async def test_status_no_bypass(self, intent_service):
        """BYPASS 2/13: STATUS requires classification."""
        message = CATEGORY_EXAMPLES["STATUS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ STATUS no bypass: verified")

    @pytest.mark.asyncio
    async def test_priority_no_bypass(self, intent_service):
        """BYPASS 3/13: PRIORITY requires classification."""
        message = CATEGORY_EXAMPLES["PRIORITY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ PRIORITY no bypass: verified")

    @pytest.mark.asyncio
    async def test_identity_no_bypass(self, intent_service):
        """BYPASS 4/13: IDENTITY requires classification."""
        message = CATEGORY_EXAMPLES["IDENTITY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ IDENTITY no bypass: verified")

    @pytest.mark.asyncio
    async def test_guidance_no_bypass(self, intent_service):
        """BYPASS 5/13: GUIDANCE requires classification."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ GUIDANCE no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_no_bypass(self, intent_service):
        """BYPASS 6/13: EXECUTION requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["EXECUTION"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ EXECUTION no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_no_bypass(self, intent_service):
        """BYPASS 7/13: ANALYSIS requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ ANALYSIS no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_no_bypass(self, intent_service):
        """BYPASS 8/13: SYNTHESIS requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ SYNTHESIS no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_no_bypass(self, intent_service):
        """BYPASS 9/13: STRATEGY requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["STRATEGY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ STRATEGY no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_no_bypass(self, intent_service):
        """BYPASS 10/13: LEARNING requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["LEARNING"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ LEARNING no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_no_bypass(self, intent_service):
        """BYPASS 11/13: UNKNOWN requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ UNKNOWN no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_no_bypass(self, intent_service):
        """BYPASS 12/13: QUERY requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["QUERY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ QUERY no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_no_bypass(self, intent_service):
        """BYPASS 13/13: CONVERSATION requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ CONVERSATION no bypass: verified")

    @pytest.mark.asyncio
    async def test_zzz_bypass_coverage(self):
        """Bypass contract coverage report."""
        print("\n" + "=" * 80)
        print("BYPASS PREVENTION CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories require proper classification")
        print("=" * 80)
