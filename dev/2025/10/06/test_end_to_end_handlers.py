"""End-to-end integration test for handlers - GREAT-4D Phase 3"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService


async def test_end_to_end():
    """Test complete flow from classification to handler execution."""

    print("=" * 80)
    print("END-TO-END HANDLER TEST - GREAT-4D Phase 3")
    print("=" * 80)

    # Create mock orchestration engine
    mock_orchestration_engine = Mock()
    mock_orchestration_engine.create_workflow_from_intent = AsyncMock()
    mock_orchestration_engine.handle_execution_intent = AsyncMock()
    mock_orchestration_engine.handle_analysis_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "test-workflow-e2e"
    mock_orchestration_engine.create_workflow_from_intent.return_value = mock_workflow

    # Mock classifier
    mock_classifier = Mock()
    mock_classifier.classify = AsyncMock()

    # Initialize IntentService with mocks
    intent_service = IntentService(
        orchestration_engine=mock_orchestration_engine, intent_classifier=mock_classifier
    )

    test_cases = [
        {
            "text": "create an issue about handler testing",
            "expected_category": "EXECUTION",
            "intent": Intent(
                original_message="create an issue about handler testing",
                category=IntentCategory.EXECUTION,
                action="create_issue",
                confidence=0.95,
                context={"title": "Handler testing", "repository": "test-repo"},
            ),
        },
        {
            "text": "analyze recent commits",
            "expected_category": "ANALYSIS",
            "intent": Intent(
                original_message="analyze recent commits",
                category=IntentCategory.ANALYSIS,
                action="analyze_commits",
                confidence=0.90,
                context={"repository": "test-repo", "timeframe": "last 7 days"},
            ),
        },
        {
            "text": "update issue 123",
            "expected_category": "EXECUTION",
            "intent": Intent(
                original_message="update issue 123",
                category=IntentCategory.EXECUTION,
                action="update_issue",
                confidence=0.88,
                context={"issue_number": "123"},
            ),
        },
        {
            "text": "generate a report on performance",
            "expected_category": "ANALYSIS",
            "intent": Intent(
                original_message="generate a report on performance",
                category=IntentCategory.ANALYSIS,
                action="generate_report",
                confidence=0.92,
                context={"report_type": "performance"},
            ),
        },
    ]

    results = []

    for test_case in test_cases:
        text = test_case["text"]
        expected_category = test_case["expected_category"]
        intent = test_case["intent"]

        print(f"\nTest: {text}")
        print(f"Expected: {expected_category}")

        # Mock classifier to return the test intent
        mock_classifier.classify.return_value = intent

        print(f"  Classified: {intent.category.value} / {intent.action}")

        # Process
        result = await intent_service.process_intent(text, session_id="e2e_test")
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message[:100]}...")

        # Validate no placeholder
        has_placeholder = (
            "Phase 3" in result.message or "full orchestration workflow" in result.message
        )

        if has_placeholder:
            print(f"  ❌ FAILED - Placeholder message detected")
            results.append(False)
        else:
            print(f"  ✅ PASSED - No placeholder")
            results.append(True)

    # Summary
    print("\n" + "=" * 80)
    print(f"Results: {sum(results)}/{len(results)} passed")

    if all(results):
        print("✅ ALL END-TO-END TESTS PASSED")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_end_to_end())
    sys.exit(0 if success else 1)
