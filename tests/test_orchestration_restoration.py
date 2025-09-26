"""
TDD Test for OrchestrationEngine Restoration
Tests the existence and basic functionality of create_workflow_from_intent method

Following Excellence Flywheel: Test First → Implement → Validate
"""

import pytest

from services.domain.models import Intent, IntentCategory


def test_syntax_import_web_app():
    """Test that web.app can be imported without syntax errors"""
    try:
        import web.app

        assert True, "web.app imported successfully"
    except SyntaxError as e:
        pytest.fail(f"Syntax error in web.app: {e}")
    except Exception as e:
        pytest.fail(f"Import error in web.app: {e}")


def test_orchestration_engine_has_create_workflow_method():
    """Test that OrchestrationEngine has create_workflow_from_intent method"""
    from services.orchestration.engine import OrchestrationEngine

    engine = OrchestrationEngine()

    # Method should exist
    assert hasattr(
        engine, "create_workflow_from_intent"
    ), "OrchestrationEngine missing create_workflow_from_intent method"

    # Method should be callable
    assert callable(
        getattr(engine, "create_workflow_from_intent")
    ), "create_workflow_from_intent is not callable"


def test_orchestration_engine_has_factory_attribute():
    """Test that OrchestrationEngine has factory attribute (PM-039 pattern)"""
    from services.orchestration.engine import OrchestrationEngine
    from services.orchestration.workflow_factory import WorkflowFactory

    engine = OrchestrationEngine()

    # Factory attribute should exist
    assert hasattr(engine, "factory"), "OrchestrationEngine missing factory attribute"

    # Factory should be WorkflowFactory instance
    assert isinstance(
        engine.factory, WorkflowFactory
    ), f"factory should be WorkflowFactory instance, got {type(engine.factory)}"

    # Workflows registry should exist (PM-039 pattern)
    assert hasattr(engine, "workflows"), "OrchestrationEngine missing workflows registry"

    assert isinstance(
        engine.workflows, dict
    ), f"workflows should be dict, got {type(engine.workflows)}"


def test_create_workflow_from_intent_basic_functionality():
    """Test that create_workflow_from_intent can be called and returns workflow"""
    import asyncio

    from services.domain.models import Intent, IntentCategory
    from services.orchestration.engine import OrchestrationEngine

    async def run_test():
        engine = OrchestrationEngine()

        # Create a simple test intent
        intent = Intent(
            category=IntentCategory.QUERY,
            action="show_standup",
            context={"original_message": "show me my standup"},
        )

        # Method should be callable and return a workflow
        workflow = await engine.create_workflow_from_intent(intent)

        # Should return a workflow with an ID
        assert workflow is not None, "create_workflow_from_intent returned None"
        assert hasattr(workflow, "id"), "Workflow missing id attribute"
        assert workflow.id is not None, "Workflow id is None"

        return workflow

    # Run the async test
    workflow = asyncio.run(run_test())
    assert workflow.id is not None, "Failed to create workflow with ID"


if __name__ == "__main__":
    print("🧪 Running TDD tests for OrchestrationEngine restoration...")

    # Test 1: Syntax
    try:
        test_syntax_import_web_app()
        print("✅ Test 1 PASSED: web.app syntax")
    except Exception as e:
        print(f"❌ Test 1 FAILED: web.app syntax - {e}")

    # Test 2: Method exists
    try:
        test_orchestration_engine_has_create_workflow_method()
        print("✅ Test 2 PASSED: Method exists")
    except Exception as e:
        print(f"❌ Test 2 FAILED: Method missing - {e}")

    # Test 2B: Factory attributes exist (PM-039 pattern)
    try:
        test_orchestration_engine_has_factory_attribute()
        print("✅ Test 2B PASSED: Factory attributes exist")
    except Exception as e:
        print(f"❌ Test 2B FAILED: Factory missing - {e}")

    # Test 3: Method works
    try:
        test_create_workflow_from_intent_basic_functionality()
        print("✅ Test 3 PASSED: Method functionality")
    except Exception as e:
        print(f"❌ Test 3 FAILED: Method broken - {e}")
