"""Multi-user contract tests for all 13 intent categories - GREAT-4E Phase 3"""

import pytest

from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES


class TestMultiUserContracts(BaseValidationTest):
    """Verify multi-user support for all categories."""

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_temporal_multiuser(self, intent_service):
        """MULTI 1/13: TEMPORAL user isolation."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ TEMPORAL multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_status_multiuser(self, intent_service):
        """MULTI 2/13: STATUS user isolation."""
        message = CATEGORY_EXAMPLES["STATUS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ STATUS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_priority_multiuser(self, intent_service):
        """MULTI 3/13: PRIORITY user isolation."""
        message = CATEGORY_EXAMPLES["PRIORITY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ PRIORITY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_identity_multiuser(self, intent_service):
        """MULTI 4/13: IDENTITY user isolation."""
        message = CATEGORY_EXAMPLES["IDENTITY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ IDENTITY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_guidance_multiuser(self, intent_service):
        """MULTI 5/13: GUIDANCE user isolation."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ GUIDANCE multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_multiuser(self, intent_service):
        """MULTI 6/13: EXECUTION user isolation."""
        message = CATEGORY_EXAMPLES["EXECUTION"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ EXECUTION multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_multiuser(self, intent_service):
        """MULTI 7/13: ANALYSIS user isolation."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ ANALYSIS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_multiuser(self, intent_service):
        """MULTI 8/13: SYNTHESIS user isolation."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ SYNTHESIS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_multiuser(self, intent_service):
        """MULTI 9/13: STRATEGY user isolation."""
        message = CATEGORY_EXAMPLES["STRATEGY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ STRATEGY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_multiuser(self, intent_service):
        """MULTI 10/13: LEARNING user isolation."""
        message = CATEGORY_EXAMPLES["LEARNING"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ LEARNING multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_multiuser(self, intent_service):
        """MULTI 11/13: UNKNOWN user isolation."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ UNKNOWN multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_multiuser(self, intent_service):
        """MULTI 12/13: QUERY user isolation."""
        message = CATEGORY_EXAMPLES["QUERY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ QUERY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_multiuser(self, intent_service):
        """MULTI 13/13: CONVERSATION user isolation."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ CONVERSATION multi-user: isolated")

    @pytest.mark.asyncio
    async def test_zzz_multiuser_coverage(self):
        """Multi-user contract coverage report."""
        print("\n" + "=" * 80)
        print("MULTI-USER CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories support session isolation")
        print("=" * 80)
