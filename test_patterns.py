"""Quick test of canonical queries after pattern additions"""

import asyncio

from services.intent_service.classifier import classifier
from services.shared_types import IntentCategory

CANONICAL_QUERIES = [
    # TEMPORAL
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
    ("When was the last time we worked on this?", IntentCategory.TEMPORAL),
    ("How long have we been working on this project?", IntentCategory.TEMPORAL),
    # STATUS
    ("What am I working on?", IntentCategory.STATUS),
    ("Show me current projects", IntentCategory.STATUS),
    ("What projects are we working on?", IntentCategory.STATUS),
    ("Give me a project overview", IntentCategory.STATUS),
    ("What's the status of project X?", IntentCategory.STATUS),
    ("Show me the project landscape", IntentCategory.STATUS),
    ("List all my projects", IntentCategory.STATUS),
    # PRIORITY
    ("What's my top priority?", IntentCategory.PRIORITY),
    ("What should I focus on today?", IntentCategory.PRIORITY),
    ("What's most important today?", IntentCategory.PRIORITY),
    ("What needs my attention?", IntentCategory.PRIORITY),
    ("Which project should I focus on?", IntentCategory.PRIORITY),
    ("What patterns do you see?", IntentCategory.PRIORITY),
]


async def test():
    results = []
    for query, expected in CANONICAL_QUERIES:
        result = await classifier.classify(query)
        passed = result.category == expected
        results.append(passed)
        status = "✅" if passed else "❌"
        print(f"{status} {query[:50]:50} → {result.category.value:12} (expected: {expected.value})")

    total = len(results)
    passed_count = sum(results)
    print(f"\n{'='*80}")
    print(
        f"Total: {total} | Passed: {passed_count} ({passed_count/total*100:.1f}%) | Failed: {total-passed_count}"
    )
    return passed_count / total


if __name__ == "__main__":
    asyncio.run(test())
