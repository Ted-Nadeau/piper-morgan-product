"""Test ANALYSIS intent handler - GREAT-4D Phase 2"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService
from services.intent_service import classifier


async def test_analysis_handler():
    """Test that ANALYSIS intents work, not placeholder."""

    print("=" * 80)
    print("ANALYSIS HANDLER TEST - GREAT-4D Phase 2")
    print("=" * 80)

    # Create mock orchestration engine
    mock_orchestration_engine = Mock()
    mock_orchestration_engine.create_workflow_from_intent = AsyncMock()
    mock_orchestration_engine.handle_analysis_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "test-workflow-123"
    mock_orchestration_engine.create_workflow_from_intent.return_value = mock_workflow

    # Mock classifier to return our test intents
    mock_classifier = Mock()
    mock_classifier.classify = AsyncMock()

    # Initialize IntentService with mock engine and classifier
    intent_service = IntentService(
        orchestration_engine=mock_orchestration_engine, intent_classifier=mock_classifier
    )

    # Test 1: analyze_commits intent
    print("\n1. Testing analyze_commits intent:")

    # Create mock intent directly
    intent1 = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_commits",
        confidence=0.9,
        original_message="analyze the recent commits",
        context={"repository": "test-repo", "timeframe": "last 7 days"},
    )

    # Mock classifier to return this intent
    mock_classifier.classify.return_value = intent1

    print(f"   Category: {intent1.category.value}")
    print(f"   Action: {intent1.action}")

    result = await intent_service.process_intent(
        "analyze the recent commits", session_id="test_session"
    )
    print(f"   Success: {result.success}")
    print(f"   Message: {result.message}")

    # Check for placeholder message
    if "Phase 3" in result.message or "full orchestration workflow" in result.message:
        print("   ❌ FAILED - Still returning placeholder message")
        return False
    else:
        print("   ✅ PASSED - No placeholder message")

    # Test 2: generate_report intent
    print("\n2. Testing generate_report intent:")

    intent2 = Intent(
        category=IntentCategory.ANALYSIS,
        action="generate_report",
        confidence=0.9,
        original_message="generate a report",
        context={"report_type": "summary"},
    )

    mock_classifier.classify.return_value = intent2

    result2 = await intent_service.process_intent("generate a report", session_id="test_session")
    print(f"   Message: {result2.message}")

    if "Phase 3" not in result2.message and "full orchestration workflow" not in result2.message:
        print("   ✅ PASSED - Report generation working")
    else:
        print("   ❌ FAILED - Report generation still placeholder")
        return False

    # Test 3: Generic analysis (should route to orchestration)
    print("\n3. Testing generic ANALYSIS action:")

    intent3 = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_performance",
        confidence=0.9,
        original_message="analyze the performance data",
        context={},
    )

    mock_classifier.classify.return_value = intent3

    result3 = await intent_service.process_intent(
        "analyze the performance data", session_id="test_session"
    )
    print(f"   Message: {result3.message}")

    if "Phase 3" not in result3.message and "full orchestration workflow" not in result3.message:
        print("   ✅ PASSED - Generic ANALYSIS working")
    else:
        print("   ❌ FAILED - Generic ANALYSIS still placeholder")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_analysis_handler())
    if success:
        print("\n✅ ANALYSIS handler working - placeholder removed!")
    else:
        print("\n❌ ANALYSIS handler still has issues")
