"""
Test EXECUTION/ANALYSIS Intent Behavior Investigation
Date: October 6, 2025, 11:43 AM

Tests whether EXECUTION and ANALYSIS intents actually work or fail.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.intent_service import classifier
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory


async def test_execution_intent():
    """Test EXECUTION intent flow end-to-end"""
    print("=" * 70)
    print("TEST 1: EXECUTION Intent (create GitHub issue)")
    print("=" * 70)

    # Step 1: Classify intent
    message = "create a github issue about login bug"
    print(f"\n1. Classifying: '{message}'")

    try:
        intent = await classifier.classify(message)
        print(f"   ✅ Classification: category={intent.category}, action={intent.action}")
        print(f"   Confidence: {intent.confidence}")
    except Exception as e:
        print(f"   ❌ Classification failed: {e}")
        return False

    # Step 2: Create workflow
    print(f"\n2. Creating workflow from intent...")
    factory = WorkflowFactory()

    try:
        workflow = await factory.create_from_intent(intent)
        if workflow:
            print(f"   ✅ Workflow created: type={workflow.type}, tasks={len(workflow.tasks)}")
            for i, task in enumerate(workflow.tasks):
                print(f"      Task {i+1}: {task.name} (type={task.type})")
        else:
            print(f"   ❌ No workflow created")
            return False
    except Exception as e:
        print(f"   ❌ Workflow creation failed: {e}")
        return False

    # Step 3: Try to execute workflow
    print(f"\n3. Attempting workflow execution...")
    engine = OrchestrationEngine()

    try:
        result = await engine.execute_workflow(workflow)
        print(f"   ✅ Execution completed: status={result.status}")
        print(f"   Result: {result.output_data}")
        return True
    except ValueError as e:
        if "Unknown task type" in str(e):
            print(f"   ❌ EXECUTION FAILS: {e}")
            print(f"   → Task types not implemented in engine")
            return False
        raise
    except Exception as e:
        print(f"   ❌ Execution failed: {type(e).__name__}: {e}")
        return False


async def test_analysis_intent():
    """Test ANALYSIS intent flow end-to-end"""
    print("\n" + "=" * 70)
    print("TEST 2: ANALYSIS Intent (analyze data)")
    print("=" * 70)

    # Step 1: Classify intent
    message = "analyze the performance metrics from last week"
    print(f"\n1. Classifying: '{message}'")

    try:
        intent = await classifier.classify(message)
        print(f"   ✅ Classification: category={intent.category}, action={intent.action}")
        print(f"   Confidence: {intent.confidence}")
    except Exception as e:
        print(f"   ❌ Classification failed: {e}")
        return False

    # Step 2: Create workflow
    print(f"\n2. Creating workflow from intent...")
    factory = WorkflowFactory()

    try:
        workflow = await factory.create_from_intent(intent)
        if workflow:
            print(f"   ✅ Workflow created: type={workflow.type}, tasks={len(workflow.tasks)}")
            for i, task in enumerate(workflow.tasks):
                print(f"      Task {i+1}: {task.name} (type={task.type})")
        else:
            print(f"   ❌ No workflow created")
            return False
    except Exception as e:
        print(f"   ❌ Workflow creation failed: {e}")
        return False

    # Step 3: Try to execute workflow
    print(f"\n3. Attempting workflow execution...")
    engine = OrchestrationEngine()

    try:
        result = await engine.execute_workflow(workflow)
        print(f"   ✅ Execution completed: status={result.status}")
        print(f"   Result: {result.output_data}")
        return True
    except ValueError as e:
        if "Unknown task type" in str(e):
            print(f"   ❌ ANALYSIS FAILS: {e}")
            print(f"   → Task types not implemented in engine")
            return False
        raise
    except Exception as e:
        print(f"   ❌ Execution failed: {type(e).__name__}: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n🔍 INVESTIGATION: EXECUTION/ANALYSIS Intent Behavior\n")

    execution_works = await test_execution_intent()
    analysis_works = await test_analysis_intent()

    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    print(f"\nEXECUTION intents: {'✅ WORKING' if execution_works else '❌ NOT WORKING'}")
    print(f"ANALYSIS intents: {'✅ WORKING' if analysis_works else '❌ NOT WORKING'}")

    if not execution_works or not analysis_works:
        print("\n🚨 FINDING: These intents classify correctly but fail at execution")
        print(
            "   REASON: Task types created by WorkflowFactory are not implemented in OrchestrationEngine"
        )
        print("   RECOMMENDATION: GREAT-4D IS NEEDED to implement missing task handlers")
    else:
        print("\n✅ Both intent types work correctly - no GREAT-4D needed")

    return execution_works and analysis_works


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
