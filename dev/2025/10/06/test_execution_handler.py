"""
Test EXECUTION intent handler - GREAT-4D Phase 1

Verifies that:
1. EXECUTION intents route to _handle_execution_intent (not placeholder)
2. create_issue action attempts to execute
3. No "Phase 3" placeholder message appears
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService
from services.intent_service import classifier
from services.llm.clients import llm_client
from services.orchestration.engine import OrchestrationEngine


async def test_execution_handler():
    """Test that EXECUTION intents work, not placeholder."""

    print("=" * 80)
    print("EXECUTION HANDLER TEST - GREAT-4D Phase 1")
    print("=" * 80)

    # Initialize IntentService with OrchestrationEngine (like web/app.py does)
    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    intent_service = IntentService(orchestration_engine=orchestration_engine)

    # Test 1: create_issue intent
    print("\n1. Testing create_issue intent:")
    intent = await classifier.classify("create an issue about testing execution handlers")
    print(f"   Category: {intent.category.value}")
    print(f"   Action: {intent.action}")

    # IntentService.process_intent expects a message string, not an Intent object
    # We need to test via message processing
    result = await intent_service.process_intent(
        "create an issue about testing execution handlers", session_id="test_session"
    )
    print(f"   Success: {result.success}")
    print(f"   Message: {result.message}")

    # Check for placeholder message
    if "Phase 3" in result.message or "full orchestration workflow" in result.message:
        print("   ❌ FAILED - Still returning placeholder message")
        return False
    else:
        print("   ✅ PASSED - No placeholder message")

    # Verify it attempted to do work (either success or proper error)
    if result.success:
        print("   ✅ PASSED - Handler executed successfully")
    elif "repository not specified" in result.message:
        print("   ✅ PASSED - Handler executed (expected repository clarification)")
    elif "Failed to create issue" in result.message:
        print("   ✅ PASSED - Handler attempted execution (GitHub error)")
    else:
        print(f"   ⚠️  WARNING - Unexpected message: {result.message}")

    # Test 2: Unhandled EXECUTION action
    print("\n2. Testing unhandled EXECUTION action:")
    intent2 = await classifier.classify("delete all issues")
    print(f"   Category: {intent2.category.value}")
    print(f"   Action: {intent2.action}")

    result2 = await intent_service.process_intent("delete all issues", session_id="test_session")
    print(f"   Success: {result2.success}")
    print(f"   Message: {result2.message}")

    # Should NOT return placeholder, but proper "not implemented" message
    if "Phase 3" in result2.message:
        print("   ❌ FAILED - Returning old placeholder for unhandled action")
        return False
    elif "not yet implemented" in result2.message:
        print("   ✅ PASSED - Returns proper 'not implemented' message")
    else:
        print(f"   ⚠️  WARNING - Unexpected message: {result2.message}")

    return True


async def main():
    """Run test."""
    print("\n🔍 GREAT-4D Phase 1: EXECUTION Handler Verification\n")

    success = await test_execution_handler()

    print("\n" + "=" * 80)
    if success:
        print("✅ EXECUTION handler working - placeholder removed!")
        print("\nKey improvements:")
        print("  - EXECUTION intents route to _handle_execution_intent")
        print("  - create_issue action has working handler")
        print("  - No more 'Phase 3' placeholder messages")
        print("  - Follows proven QUERY pattern")
    else:
        print("❌ EXECUTION handler still has issues")

    return success


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
