"""
Test intent cache behavior.

Tests cache hits and misses for duplicate queries.
GREAT-4B Phase 3: Intent Caching
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


async def test_cache():
    """Test cache hits and misses with sample queries."""
    # Import after path setup
    from services.intent_service.classifier import IntentClassifier

    # Initialize classifier (which includes cache)
    classifier = IntentClassifier()

    test_queries = [
        "What day is it?",
        "What's my schedule?",
        "What day is it?",  # Duplicate - should hit cache
        "Create an issue about login bug",
        "What's my schedule?",  # Duplicate - should hit cache
        "What day is it?",  # Duplicate - should hit cache
    ]

    print("Testing Intent Cache Behavior")
    print("=" * 60)
    print()

    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Query: {query}")

        try:
            # Classify with cache enabled (default)
            result = await classifier.classify(query)
            print(f"   Intent: {result.action}")

            # Get cache metrics
            metrics = classifier.cache.get_metrics()
            print(
                f"   Cache: {metrics['hits']} hits, {metrics['misses']} misses, "
                f"{metrics['hit_rate_percent']}% hit rate"
            )
            print()

        except Exception as e:
            print(f"   ERROR: {e}")
            print()

    print()
    print("=" * 60)
    print("Final Cache Metrics")
    print("=" * 60)

    final_metrics = classifier.cache.get_metrics()
    print(f"Total Requests:    {final_metrics['total_requests']}")
    print(f"Cache Hits:        {final_metrics['hits']}")
    print(f"Cache Misses:      {final_metrics['misses']}")
    print(f"Hit Rate:          {final_metrics['hit_rate_percent']}%")
    print(f"Cache Size:        {final_metrics['cache_size']} entries")
    print(f"TTL:               {final_metrics['ttl_seconds']}s")
    print()

    # Verify hit rate
    if final_metrics["hit_rate_percent"] >= 50:
        print("✅ Cache performing well (≥50% hit rate)")
        print()
        return 0
    else:
        print(f"⚠️  Cache hit rate below 50% target")
        print()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_cache())
    sys.exit(exit_code)
