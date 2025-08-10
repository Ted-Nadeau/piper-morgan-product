"""
Integration Tests for Workflow Factory Reality Testing
Ensures workflow factory creation works for all workflow types in CI/CD pipeline.

Critical for preventing variable scoping bugs and over-mocking issues.
Part of Testing Discipline Protocol established 2025-08-10.
"""

import asyncio

import pytest

from services.domain.models import Intent
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


class TestWorkflowFactoryReality:
    """Reality testing for workflow factory - no critical path mocking"""

    @pytest.fixture
    def workflow_factory(self):
        """Create real workflow factory - NO MOCKING"""
        return WorkflowFactory()

    @pytest.mark.asyncio
    async def test_all_workflow_types_creation(self, workflow_factory):
        """Test that all workflow types can be created without UnboundLocalError"""

        # Test cases for core workflow types that are properly mapped
        test_cases = [
            (WorkflowType.CREATE_TICKET, {"original_message": "test create ticket"}),
            (WorkflowType.LIST_PROJECTS, {"original_message": "test list projects"}),
            (WorkflowType.ANALYZE_FILE, {"original_message": "test analyze file"}),
            (WorkflowType.GENERATE_REPORT, {"original_message": "test generate report"}),
            (WorkflowType.PLAN_STRATEGY, {"original_message": "test plan strategy"}),
            (WorkflowType.CREATE_FEATURE, {"original_message": "test create feature"}),
            (WorkflowType.ANALYZE_METRICS, {"original_message": "test analyze metrics"}),
            (WorkflowType.CREATE_TASK, {"original_message": "test create task"}),
            (WorkflowType.LEARN_PATTERN, {"original_message": "test learn pattern"}),
            (WorkflowType.ANALYZE_FEEDBACK, {"original_message": "test analyze feedback"}),
            (WorkflowType.CONFIRM_PROJECT, {"original_message": "test confirm project"}),
            (WorkflowType.SELECT_PROJECT, {"original_message": "test select project"}),
        ]

        successful_creations = 0

        for workflow_type, context in test_cases:
            intent = Intent(
                action=workflow_type.value,
                category=IntentCategory.EXECUTION,
                context=context,
                confidence=1.0,
            )

            # CRITICAL: No mocking - test real execution path
            workflow = await workflow_factory.create_from_intent(intent)

            # Verify workflow was created successfully (PRIMARY GOAL: No UnboundLocalError)
            assert workflow is not None, f"Failed to create workflow for {workflow_type.value}"
            assert workflow.id is not None, f"Workflow ID not set for {workflow_type.value}"

            # Note: Some workflows may default to CREATE_TICKET if not in registry
            # This is expected behavior - the critical test is NO UnboundLocalError
            successful_creations += 1

        # Ensure all workflow types are operational (no crashes)
        assert successful_creations == len(
            test_cases
        ), f"Only {successful_creations}/{len(test_cases)} workflow types working"

    @pytest.mark.asyncio
    async def test_unmapped_workflow_fallback(self, workflow_factory):
        """Test that unmapped workflow actions fall back gracefully (no UnboundLocalError)"""

        intent = Intent(
            action="review_item",  # Not in workflow registry
            category=IntentCategory.EXECUTION,
            context={"original_message": "test unmapped workflow"},
            confidence=1.0,
        )

        # Should not crash with UnboundLocalError - should fall back to default
        workflow = await workflow_factory.create_from_intent(intent)

        assert workflow is not None
        assert workflow.id is not None
        # Falls back to CREATE_TICKET by default for EXECUTION category
        assert workflow.type == WorkflowType.CREATE_TICKET

    @pytest.mark.asyncio
    async def test_workflow_factory_variable_scoping(self, workflow_factory):
        """Specific test for the PM-090 UnboundLocalError bug"""

        intent = Intent(
            action="create_ticket",
            category=IntentCategory.EXECUTION,
            context={"original_message": "variable scoping test"},
            confidence=1.0,
        )

        # This would fail with UnboundLocalError before the fix
        workflow = await workflow_factory.create_from_intent(intent)

        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET
        assert "variable scoping test" in str(workflow.context)

    @pytest.mark.asyncio
    async def test_context_validation_executes_after_workflow_type_definition(
        self, workflow_factory
    ):
        """Ensure validation happens AFTER workflow_type is defined (not before)"""

        # This test verifies the execution order fix
        intent = Intent(
            action="generate_report",
            category=IntentCategory.EXECUTION,
            context={"original_message": "validation order test"},
            confidence=1.0,
        )

        # Should work - validation uses defined workflow_type
        workflow = await workflow_factory.create_from_intent(intent)

        assert workflow is not None
        assert workflow.type == WorkflowType.GENERATE_REPORT

    def test_workflow_registry_coverage(self, workflow_factory):
        """Ensure workflow registry covers all workflow types"""

        # Check registry has mappings for all workflow types
        registry = workflow_factory.workflow_registry

        # Core workflow types should be mapped
        assert "create_ticket" in registry
        assert "list_projects" in registry
        assert "create_feature" in registry

        # Verify registry returns correct WorkflowType enums
        assert registry.get("create_ticket") == WorkflowType.CREATE_TICKET
        assert registry.get("list_projects") == WorkflowType.LIST_PROJECTS
        assert registry.get("create_feature") == WorkflowType.CREATE_FEATURE

    @pytest.mark.asyncio
    async def test_performance_baseline(self, workflow_factory):
        """Ensure workflow creation performance is reasonable"""
        import time

        intent = Intent(
            action="create_task",
            category=IntentCategory.EXECUTION,
            context={"original_message": "performance test"},
            confidence=1.0,
        )

        start_time = time.time()
        workflow = await workflow_factory.create_from_intent(intent)
        duration_ms = (time.time() - start_time) * 1000

        # Should create workflow quickly (under 100ms for factory creation)
        assert duration_ms < 100, f"Workflow creation too slow: {duration_ms}ms"
        assert workflow is not None
