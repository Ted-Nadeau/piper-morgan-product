"""
Validate intent classification performance with caching.
"""

import asyncio
import time

from services.intent_service import classifier


async def validate_performance():
    """Test performance with and without cache."""

    test_query = "What day is it?"

    print("Performance Validation\n" + "=" * 50)

    # Test 1: First query (cache miss)
    print("\n1. First query (expected cache miss):")
    start = time.time()
    result1 = await classifier.classify(test_query)
    duration1 = (time.time() - start) * 1000  # Convert to ms
    print(f"   Duration: {duration1:.2f}ms")
    print(f"   Intent: {result1.category}")
    print(f"   Confidence: {result1.confidence}")

    # Test 2: Same query (cache hit)
    print("\n2. Duplicate query (expected cache hit):")
    start = time.time()
    result2 = await classifier.classify(test_query)
    duration2 = (time.time() - start) * 1000
    print(f"   Duration: {duration2:.2f}ms")
    print(f"   Intent: {result2.category}")
    print(f"   Confidence: {result2.confidence}")

    # Calculate improvement
    if duration2 < duration1:
        improvement = ((duration1 - duration2) / duration1) * 100
        print(f"\n✅ Cache improved performance by {improvement:.1f}%")
        print(f"   ({duration1:.2f}ms → {duration2:.2f}ms)")
    else:
        print(f"\n⚠️  Cache did not improve performance")
        print(f"   ({duration1:.2f}ms → {duration2:.2f}ms)")

    # Test different queries to see cache behavior
    print("\n3. Testing different queries:")
    test_queries = [
        "What's my top priority?",
        "What am I working on?",
        "What day is it?",  # Repeat to test cache hit
    ]

    for i, query in enumerate(test_queries, 1):
        start = time.time()
        result = await classifier.classify(query)
        duration = (time.time() - start) * 1000
        print(f"   Query {i}: {duration:.2f}ms - {result.category}")

    # Show cache metrics if available
    try:
        if hasattr(classifier, "cache") and hasattr(classifier.cache, "get_metrics"):
            metrics = classifier.cache.get_metrics()
            print(f"\nCache Metrics:")
            print(f"  Hit Rate: {metrics.get('hit_rate_percent', 'N/A')}%")
            print(f"  Cache Size: {metrics.get('cache_size', 'N/A')} entries")
            print(f"  Hits: {metrics.get('hits', 'N/A')}")
            print(f"  Misses: {metrics.get('misses', 'N/A')}")
        else:
            print(f"\n⚠️  Cache metrics not available")
    except Exception as e:
        print(f"\n⚠️  Error getting cache metrics: {e}")


if __name__ == "__main__":
    asyncio.run(validate_performance())
