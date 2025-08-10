#!/usr/bin/env python3
"""
Lightweight Workflow Factory Reality Test
Fast validation that workflow factory creation works for all workflow types.
Designed for CI/CD integration without database dependencies.

Usage:
    python scripts/workflow_factory_test.py
    PYTHONPATH=. python scripts/workflow_factory_test.py
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.domain.models import Intent
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


async def test_workflow_factory_creation():
    """Test workflow factory creation for all workflow types"""
    print("🚀 Workflow Factory Reality Test - CI/CD Integration")
    print("=" * 55)

    factory = WorkflowFactory()

    # Test cases for all 13 workflow types
    test_cases = [
        (WorkflowType.CREATE_TICKET, {"original_message": "test create ticket"}),
        (WorkflowType.LIST_PROJECTS, {"original_message": "test list projects"}),
        (WorkflowType.ANALYZE_FILE, {"original_message": "test analyze file"}),
        (WorkflowType.GENERATE_REPORT, {"original_message": "test generate report"}),
        (WorkflowType.REVIEW_ITEM, {"original_message": "test review item"}),
        (WorkflowType.PLAN_STRATEGY, {"original_message": "test plan strategy"}),
        (WorkflowType.CREATE_FEATURE, {"original_message": "test create feature"}),
        (WorkflowType.ANALYZE_METRICS, {"original_message": "test analyze metrics"}),
        (WorkflowType.CREATE_TASK, {"original_message": "test create task"}),
        (WorkflowType.LEARN_PATTERN, {"original_message": "test learn pattern"}),
        (WorkflowType.ANALYZE_FEEDBACK, {"original_message": "test analyze feedback"}),
        (WorkflowType.CONFIRM_PROJECT, {"original_message": "test confirm project"}),
        (WorkflowType.SELECT_PROJECT, {"original_message": "test select project"}),
    ]

    passed = 0
    failed = 0
    total_time = 0

    print(f"\n🔍 Testing {len(test_cases)} workflow types...")

    for workflow_type, context in test_cases:
        start_time = time.time()

        try:
            intent = Intent(
                action=workflow_type.value,
                category=IntentCategory.EXECUTION,
                context=context,
                confidence=1.0,
            )

            workflow = await factory.create_from_intent(intent)

            duration_ms = (time.time() - start_time) * 1000
            total_time += duration_ms

            if workflow and workflow.id:
                print(f"✅ {workflow_type.value}: PASS ({duration_ms:.1f}ms)")
                passed += 1
            else:
                print(f"❌ {workflow_type.value}: FAIL - No workflow created")
                failed += 1

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            total_time += duration_ms

            print(f"❌ {workflow_type.value}: ERROR - {str(e)[:60]}...")
            failed += 1

    # Results
    avg_time = total_time / len(test_cases)
    success_rate = (passed / len(test_cases)) * 100

    print("\n" + "=" * 55)
    print("📊 WORKFLOW FACTORY TEST RESULTS")
    print("=" * 55)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"⚡ Average Time: {avg_time:.1f}ms")

    if failed == 0:
        print("\n🎉 ALL WORKFLOW TYPES OPERATIONAL!")
        print("🔧 Critical workflow factory bug FIXED")
        print("✅ Ready for production deployment")
        return True
    else:
        print(f"\n⚠️  {failed} workflow types still have issues")
        print("🔧 Further investigation required")
        return False


async def main():
    """Main entry point"""
    try:
        success = await test_workflow_factory_creation()

        if success:
            print("\n✅ Workflow Factory Test: PASSED")
            sys.exit(0)
        else:
            print("\n❌ Workflow Factory Test: FAILED")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 Test execution error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
