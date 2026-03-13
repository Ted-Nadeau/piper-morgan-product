"""Independent validation of Code's autonomous handler implementation"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService


async def validate_new_handlers():
    """Test the 4 handlers Code claims to have implemented."""

    print("=" * 80)
    print("INDEPENDENT VALIDATION - Code's Autonomous Work")
    print("=" * 80)

    # Create mock orchestration engine
    mock_orchestration_engine = Mock()
    mock_orchestration_engine.create_workflow_from_intent = AsyncMock()
    mock_orchestration_engine.handle_synthesis_intent = AsyncMock()
    mock_orchestration_engine.handle_strategy_intent = AsyncMock()
    mock_orchestration_engine.handle_learning_intent = AsyncMock()
    mock_orchestration_engine.handle_unknown_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "validation-workflow-123"
    mock_orchestration_engine.create_workflow_from_intent.return_value = mock_workflow

    # Mock classifier
    mock_classifier = Mock()
    mock_classifier.classify = AsyncMock()

    intent_service = IntentService(
        orchestration_engine=mock_orchestration_engine, intent_classifier=mock_classifier
    )

    test_cases = [
        # SYNTHESIS category
        {
            "category": IntentCategory.SYNTHESIS,
            "action": "generate_content",
            "text": "summarize this document",
            "intent": Intent(
                original_message="summarize this document",
                category=IntentCategory.SYNTHESIS,
                action="generate_content",
                confidence=0.90,
                context={"content_type": "document"},
            ),
        },
        {
            "category": IntentCategory.SYNTHESIS,
            "action": "summarize",
            "text": "give me a summary",
            "intent": Intent(
                original_message="give me a summary",
                category=IntentCategory.SYNTHESIS,
                action="summarize",
                confidence=0.88,
                context={"summary_type": "brief"},
            ),
        },
        # STRATEGY category
        {
            "category": IntentCategory.STRATEGY,
            "action": "strategic_planning",
            "text": "create a strategy",
            "intent": Intent(
                original_message="create a strategy",
                category=IntentCategory.STRATEGY,
                action="strategic_planning",
                confidence=0.92,
                context={"planning_scope": "project"},
            ),
        },
        {
            "category": IntentCategory.STRATEGY,
            "action": "prioritization",
            "text": "what should I prioritize",
            "intent": Intent(
                original_message="what should I prioritize",
                category=IntentCategory.STRATEGY,
                action="prioritization",
                confidence=0.85,
                context={"priority_type": "tasks"},
            ),
        },
        # LEARNING category
        {
            "category": IntentCategory.LEARNING,
            "action": "learn_pattern",
            "text": "learn from this",
            "intent": Intent(
                original_message="learn from this",
                category=IntentCategory.LEARNING,
                action="learn_pattern",
                confidence=0.87,
                context={"learning_type": "pattern"},
            ),
        },
        # UNKNOWN category
        {
            "category": IntentCategory.UNKNOWN,
            "action": "unknown",
            "text": "this is something weird",
            "intent": Intent(
                original_message="this is something weird",
                category=IntentCategory.UNKNOWN,
                action="unknown",
                confidence=0.60,
                context={},
            ),
        },
    ]

    results = []

    for test_case in test_cases:
        category = test_case["category"]
        action = test_case["action"]
        text = test_case["text"]
        intent = test_case["intent"]

        print(f"\nTesting: {category.value} / {action}")

        # Mock classifier to return the test intent
        mock_classifier.classify.return_value = intent

        try:
            result = await intent_service.process_intent(text, session_id="validation_test")

            # Check for placeholder messages
            has_placeholder = (
                "Phase 3" in result.message
                or "full orchestration workflow" in result.message
                or "placeholder" in result.message.lower()
            )

            if has_placeholder:
                print(f"  ❌ FAILED - Still returns placeholder")
                print(f"     Message: {result.message[:100]}")
                results.append(False)
            else:
                print(f"  ✅ PASSED - No placeholder")
                print(f"     Message: {result.message[:100]}")
                results.append(True)

        except Exception as e:
            print(f"  ❌ ERROR - {str(e)}")
            results.append(False)

    # Summary
    print("\n" + "=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if all(results):
        print("✅ ALL HANDLERS VERIFIED - Code's work is correct")
        return True
    else:
        print("❌ VERIFICATION FAILED - Code's claims not validated")
        return False


async def verify_complete_coverage():
    """Verify all 13 intent categories are now handled."""

    print("\n" + "=" * 80)
    print("COMPLETE COVERAGE VERIFICATION")
    print("=" * 80)

    # Create mock orchestration engine
    mock_orchestration_engine = Mock()
    mock_orchestration_engine.create_workflow_from_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "coverage-test-123"
    mock_orchestration_engine.create_workflow_from_intent.return_value = mock_workflow

    # Mock classifier
    mock_classifier = Mock()
    mock_classifier.classify = AsyncMock()

    intent_service = IntentService(
        orchestration_engine=mock_orchestration_engine, intent_classifier=mock_classifier
    )

    # List all 13 categories
    from services.shared_types import IntentCategory

    all_categories = [cat for cat in IntentCategory]
    print(f"\nTotal intent categories: {len(all_categories)}")

    # Check each has a handler (no placeholder)
    coverage = []
    for category in all_categories:
        intent = Intent(
            original_message=f"test {category.value}",
            category=category,
            action="test",
            confidence=0.85,
            context={},
        )

        # Mock classifier to return the test intent
        mock_classifier.classify.return_value = intent

        result = await intent_service.process_intent(
            f"test {category.value}", session_id="coverage_test"
        )
        has_placeholder = "Phase 3" in result.message or "full orchestration" in result.message

        status = "❌ Placeholder" if has_placeholder else "✅ Handler"
        print(f"  {category.value:15} → {status}")
        coverage.append(not has_placeholder)

    # Summary
    handled = sum(coverage)
    print(f"\nCoverage: {handled}/{len(all_categories)} = {handled/len(all_categories)*100:.0f}%")

    if handled == len(all_categories):
        print("✅ 100% COVERAGE CONFIRMED")
        return True
    else:
        print(f"❌ INCOMPLETE - {len(all_categories) - handled} categories still have placeholders")
        return False


if __name__ == "__main__":
    print("Starting independent validation of Code's autonomous work...\n")

    # Run both validations
    handlers_ok = asyncio.run(validate_new_handlers())
    coverage_ok = asyncio.run(verify_complete_coverage())

    if handlers_ok and coverage_ok:
        print("\n" + "=" * 80)
        print("✅ VALIDATION COMPLETE - Code's work verified and accepted")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("❌ VALIDATION FAILED - Do not accept Code's commit")
        print("=" * 80)
        sys.exit(1)
