"""
Test script for canonical queries - GREAT-4A Phase 1

Tests all canonical queries across TEMPORAL, STATUS, and PRIORITY categories
to validate that intent classification works correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent_service.classifier import classifier
from services.shared_types import IntentCategory

# Canonical queries from PM-070 document
# Focused on TEMPORAL, STATUS, and PRIORITY categories for GREAT-4A
CANONICAL_QUERIES = [
    # TEMPORAL category (10 queries from PM-070)
    ("What day is it?", IntentCategory.TEMPORAL),
    ("What's today's date?", IntentCategory.TEMPORAL),
    ("What day of the week is it?", IntentCategory.TEMPORAL),
    ("What's the current date?", IntentCategory.TEMPORAL),
    ("Tell me the date", IntentCategory.TEMPORAL),
    ("What did we accomplish yesterday?", IntentCategory.TEMPORAL),
    ("What did we do yesterday?", IntentCategory.TEMPORAL),
    ("What happened yesterday?", IntentCategory.TEMPORAL),
    ("What's on the agenda for today?", IntentCategory.TEMPORAL),
    ("What should I work on today?", IntentCategory.TEMPORAL),
    # STATUS category (5 queries - spatial queries map to STATUS)
    ("What am I working on?", IntentCategory.STATUS),
    ("Show me current projects", IntentCategory.STATUS),
    ("What projects are we working on?", IntentCategory.STATUS),
    ("Give me a project overview", IntentCategory.STATUS),
    ("What's the status of project X?", IntentCategory.STATUS),
    # PRIORITY category (5 queries - predictive queries map to PRIORITY)
    ("What's my top priority?", IntentCategory.PRIORITY),
    ("What should I focus on today?", IntentCategory.PRIORITY),
    ("What's most important today?", IntentCategory.PRIORITY),
    ("What needs my attention?", IntentCategory.PRIORITY),
    ("Which project should I focus on?", IntentCategory.PRIORITY),
    # Additional TEMPORAL variations
    ("When was the last time we worked on this?", IntentCategory.TEMPORAL),
    ("How long have we been working on this project?", IntentCategory.TEMPORAL),
    # Additional STATUS variations
    ("Show me the project landscape", IntentCategory.STATUS),
    ("List all my projects", IntentCategory.STATUS),
    # Additional PRIORITY variations
    ("What patterns do you see?", IntentCategory.PRIORITY),
]


async def test_canonical_queries():
    """Test all canonical queries and report results."""
    print("=" * 80)
    print("CANONICAL QUERY TESTING - GREAT-4A Phase 1")
    print("=" * 80)
    print(f"\nTesting {len(CANONICAL_QUERIES)} canonical queries...\n")

    results = []

    for query, expected_category in CANONICAL_QUERIES:
        try:
            result = await classifier.classify(query)
            passed = result.category == expected_category
            confidence = result.confidence

            results.append(
                {
                    "query": query,
                    "expected": expected_category.value,
                    "actual": result.category.value,
                    "confidence": confidence,
                    "passed": passed,
                }
            )

            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {query[:45]:45} | {result.category.value:12} | {confidence:.2f}")

        except Exception as e:
            results.append(
                {
                    "query": query,
                    "expected": expected_category.value,
                    "error": str(e),
                    "passed": False,
                }
            )
            print(f"❌ ERROR | {query[:45]:45} | {str(e)[:30]}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.get("passed", False))
    failed = total - passed

    print(f"\n{'='*80}")
    print(f"CANONICAL QUERY TEST RESULTS")
    print(f"{'='*80}")
    print(f"Total:  {total}")
    print(f"Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total*100:.1f}%)")

    # Show failures
    if failed > 0:
        print(f"\nFailed Queries:")
        for r in results:
            if not r.get("passed", False):
                print(f"  - {r['query']}")
                if "error" in r:
                    print(f"    Error: {r['error']}")
                else:
                    print(f"    Expected: {r['expected']}, Got: {r['actual']}")

    # Analyze confidence scores
    analyze_confidence(results)

    return results


def analyze_confidence(results):
    """Analyze confidence score patterns."""
    by_category = {}

    for r in results:
        if "confidence" in r:
            cat = r["expected"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(r["confidence"])

    print(f"\n{'='*80}")
    print(f"CONFIDENCE SCORE ANALYSIS")
    print(f"{'='*80}")

    for category, scores in sorted(by_category.items()):
        if scores:
            avg = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            print(
                f"{category:12} | Avg: {avg:.3f} | Min: {min_score:.3f} | Max: {max_score:.3f} | Count: {len(scores)}"
            )

            # Flag if any below 0.8 threshold
            low_conf = [s for s in scores if s < 0.8]
            if low_conf:
                print(f"  ⚠️  {len(low_conf)} queries below 0.8 confidence threshold")


if __name__ == "__main__":
    results = asyncio.run(test_canonical_queries())

    # Exit with error code if any failures
    failed_count = sum(1 for r in results if not r.get("passed", False))
    sys.exit(0 if failed_count == 0 else 1)
