"""Test what happens with unhandled intent actions - GREAT-4C Phase -1"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent_service import classifier


async def test_routing():
    """Test intents that may or may not have handlers."""

    test_cases = [
        # Queries that SHOULD work (have handlers via GREAT-4A)
        ("what day is it", "TEMPORAL - should work"),
        ("what am i working on", "STATUS - should work"),
        ("what's my top priority", "PRIORITY - should work"),
        # Actions that MAY NOT have direct handlers
        ("create an issue about login bug", "EXECUTION? CREATE? - unknown"),
        ("update the status of issue 123", "EXECUTION? UPDATE? - unknown"),
        ("search for architecture docs", "QUERY? SEARCH? - unknown"),
        ("analyze the codebase", "ANALYSIS - unknown"),
    ]

    print("=" * 80)
    print("UNHANDLED INTENT ROUTING TEST - GREAT-4C Phase -1")
    print("=" * 80)
    print()

    results = []

    for text, expected in test_cases:
        print(f"\nTest: {text}")
        print(f"Expected: {expected}")

        try:
            result = await classifier.classify(text)
            print(f"  Category: {result.category.value}")
            print(f"  Action: {result.action}")
            print(f"  Confidence: {result.confidence}")

            results.append(
                {
                    "text": text,
                    "category": result.category.value,
                    "action": result.action,
                    "confidence": result.confidence,
                    "success": True,
                }
            )

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback

            traceback.print_exc()

            results.append({"text": text, "error": str(e), "success": False})

    # Summary
    print("\n" + "=" * 80)
    print("CLASSIFICATION RESULTS SUMMARY")
    print("=" * 80)

    for r in results:
        if r["success"]:
            print(f"\n{r['text'][:50]}")
            print(f"  → {r['category']} / {r['action']} (confidence: {r['confidence']:.2f})")
        else:
            print(f"\n{r['text'][:50]}")
            print(f"  → ERROR: {r['error']}")

    # Group by category
    print("\n" + "=" * 80)
    print("INTENTS BY CATEGORY")
    print("=" * 80)

    by_category = {}
    for r in results:
        if r["success"]:
            cat = r["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(r)

    for cat, items in sorted(by_category.items()):
        print(f"\n{cat}:")
        for item in items:
            print(f"  - {item['action']}: \"{item['text'][:40]}...\"")

    return results


if __name__ == "__main__":
    results = asyncio.run(test_routing())

    print("\n" + "=" * 80)
    print("FINDINGS:")
    print("=" * 80)
    print(
        """
This test shows what categories/actions the classifier assigns to different queries.
The key question: Do these classified intents have handlers?

Next step: Trace how IntentService routes these categories to handlers.
"""
    )
