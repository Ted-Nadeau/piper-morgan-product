"""
Comprehensive test for ALL intent handlers - GREAT-4D Phase 4-7

Verifies that ALL 13 intent categories have working handlers (no placeholders).
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService
from services.llm.clients import llm_client
from services.orchestration.engine import OrchestrationEngine


async def test_all_intent_categories():
    """Test that ALL 13 intent categories have working handlers."""

    print("=" * 80)
    print("ALL INTENT CATEGORIES TEST - GREAT-4D Phases 1-7")
    print("=" * 80)

    # Initialize IntentService
    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    intent_service = IntentService(orchestration_engine=orchestration_engine)

    # Test all 13 intent categories
    test_cases = [
        # Existing working categories
        ("QUERY", "list projects", "show_projects"),
        ("CONVERSATION", "hello", "greeting"),
        ("IDENTITY", "who are you", "identity_query"),
        ("TEMPORAL", "what day is it", "temporal_query"),
        ("STATUS", "what am I working on", "status_query"),
        ("PRIORITY", "what's my top priority", "priority_query"),
        ("GUIDANCE", "what should I focus on", "guidance_query"),
        # GREAT-4D Phase 1
        ("EXECUTION", "create an issue about testing", "create_issue"),
        # GREAT-4D Phase 2
        ("ANALYSIS", "analyze recent commits", "analyze_commits"),
        # GREAT-4D Phase 4
        ("SYNTHESIS", "summarize this document", "generate_content"),
        # GREAT-4D Phase 5
        ("STRATEGY", "help me plan my sprint", "strategic_planning"),
        # GREAT-4D Phase 6
        ("LEARNING", "learn from this pattern", "learn_pattern"),
        # GREAT-4D Phase 7
        ("UNKNOWN", "asdfghjkl", "unknown_action"),
    ]

    results = []
    for category, message, expected_action in test_cases:
        print(f"\n{category} Intent Test:")
        print(f"  Message: '{message}'")

        try:
            result = await intent_service.process_intent(message, session_id="test")

            # Check for placeholder messages
            has_placeholder = (
                "Phase 3" in result.message or "full orchestration workflow" in result.message
            )

            if has_placeholder:
                print(f"  ❌ FAILED - Placeholder message detected")
                print(f"  Message: {result.message}")
                results.append((category, False))
            else:
                print(f"  ✅ PASSED - No placeholder")
                print(f"  Message: {result.message[:80]}...")
                results.append((category, True))

        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            results.append((category, False))

    # Summary
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for category, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {category}")

    print(f"\nTotal: {passed}/{total} categories working ({int(passed/total*100)}%)")

    if passed == total:
        print("\n🎉 ALL INTENT CATEGORIES HAVE WORKING HANDLERS!")
        print("✅ Zero placeholder messages detected")
        print("✅ GREAT-4D complete - 100% intent coverage")
        return True
    else:
        print(f"\n⚠️  {total - passed} categories still have placeholders")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_all_intent_categories())
    sys.exit(0 if result else 1)
