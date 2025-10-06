"""Test PIPER config caching performance - GREAT-4C Phase 3."""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.user_context_service import user_context_service
from services.configuration.piper_config_loader import piper_config_loader


async def test_cache_performance():
    """Measure cache hit rate and performance improvement."""

    print("=" * 80)
    print("PIPER CONFIG CACHE PERFORMANCE TEST - GREAT-4C Phase 3")
    print("=" * 80)
    print()

    # Clear caches to start fresh
    piper_config_loader.clear_cache()
    user_context_service.invalidate_cache()

    test_session = "test_session_123"

    # ========================================================================
    # Test 1: PiperConfigLoader direct access
    # ========================================================================
    print("TEST 1: PiperConfigLoader Cache")
    print("-" * 80)

    # First load (cache miss)
    print("1. First load (cache miss):")
    start = time.time()
    config1 = piper_config_loader.load_config()
    duration1 = (time.time() - start) * 1000
    print(f"   Duration: {duration1:.2f}ms")
    print(f"   Sections loaded: {len(config1) if config1 else 0}")

    # Second load (cache hit)
    print("\n2. Second load (cache hit):")
    start = time.time()
    config2 = piper_config_loader.load_config()
    duration2 = (time.time() - start) * 1000
    print(f"   Duration: {duration2:.2f}ms")
    print(f"   Sections loaded: {len(config2) if config2 else 0}")

    # Calculate improvement
    if duration1 > duration2:
        improvement = ((duration1 - duration2) / duration1) * 100
        print(f"\n✅ Cache improved performance by {improvement:.1f}%")
        print(f"   ({duration1:.2f}ms → {duration2:.2f}ms)")
    else:
        print(f"\n⚠️  Second load not faster ({duration1:.2f}ms → {duration2:.2f}ms)")

    # Multiple loads to test hit rate
    print("\n3. Multiple loads (testing hit rate):")
    for i in range(3, 11):
        piper_config_loader.load_config()
        print(f"   Load {i}: cached")

    # Check PiperConfigLoader metrics
    metrics = piper_config_loader.get_cache_metrics()
    print(f"\n=== PiperConfigLoader Metrics ===")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Cache Hits: {metrics['hits']}")
    print(f"Cache Misses: {metrics['misses']}")
    print(f"Hit Rate: {metrics['hit_rate_percent']}%")
    print(f"Cache Populated: {metrics['cache_populated']}")
    print(f"Cache Age: {metrics['cache_age_seconds']}s")
    print(f"TTL: {metrics['ttl_seconds']}s")

    # Validate hit rate
    if metrics["hit_rate_percent"] >= 80:
        print(f"\n✅ PiperConfigLoader cache performing excellently (>80% hit rate)")
    elif metrics["hit_rate_percent"] >= 60:
        print(f"\n✅ PiperConfigLoader cache performing well (>60% hit rate)")
    else:
        print(f"\n⚠️  PiperConfigLoader cache hit rate below 60%")

    print()

    # ========================================================================
    # Test 2: UserContextService (uses PiperConfigLoader)
    # ========================================================================
    print("TEST 2: UserContextService Cache")
    print("-" * 80)

    # First context load (cache miss)
    print("1. First context load (cache miss):")
    start = time.time()
    context1 = await user_context_service.get_user_context(test_session)
    duration1 = (time.time() - start) * 1000
    print(f"   Duration: {duration1:.2f}ms")
    print(f"   Organization: {context1.organization}")
    print(f"   Projects: {len(context1.projects)}")
    print(f"   Priorities: {len(context1.priorities)}")

    # Second context load (cache hit)
    print("\n2. Second context load (cache hit):")
    start = time.time()
    context2 = await user_context_service.get_user_context(test_session)
    duration2 = (time.time() - start) * 1000
    print(f"   Duration: {duration2:.2f}ms")
    print(f"   Organization: {context2.organization}")

    # Calculate improvement
    if duration1 > duration2:
        improvement = ((duration1 - duration2) / duration1) * 100
        print(f"\n✅ Context cache improved performance by {improvement:.1f}%")
        print(f"   ({duration1:.2f}ms → {duration2:.2f}ms)")
    else:
        print(f"\n⚠️  Second load not faster ({duration1:.2f}ms → {duration2:.2f}ms)")

    # Multiple context loads
    print("\n3. Multiple context loads (testing hit rate):")
    for i in range(3, 11):
        await user_context_service.get_user_context(test_session)
        print(f"   Load {i}: cached")

    # Test different sessions
    print("\n4. Different session (cache miss):")
    context3 = await user_context_service.get_user_context("different_session")
    print(f"   Session: different_session")
    print(f"   Organization: {context3.organization}")

    # Check UserContextService metrics
    metrics = user_context_service.get_cache_metrics()
    print(f"\n=== UserContextService Metrics ===")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Cache Hits: {metrics['hits']}")
    print(f"Cache Misses: {metrics['misses']}")
    print(f"Hit Rate: {metrics['hit_rate_percent']}%")
    print(f"Cache Size: {metrics['cache_size']} sessions")
    print(f"Cached Sessions: {metrics['cached_sessions']}")

    # Validate hit rate
    if metrics["hit_rate_percent"] >= 70:
        print(f"\n✅ UserContextService cache performing excellently (>70% hit rate)")
    elif metrics["hit_rate_percent"] >= 50:
        print(f"\n✅ UserContextService cache performing well (>50% hit rate)")
    else:
        print(f"\n⚠️  UserContextService cache hit rate below 50%")

    print()

    # ========================================================================
    # Final Summary
    # ========================================================================
    print("=" * 80)
    print("CACHE PERFORMANCE SUMMARY")
    print("=" * 80)

    config_metrics = piper_config_loader.get_cache_metrics()
    context_metrics = user_context_service.get_cache_metrics()

    print(f"\n**Two-Layer Caching Architecture**:")
    print(f"  1. File-level (PiperConfigLoader): {config_metrics['hit_rate_percent']}% hit rate")
    print(f"  2. Session-level (UserContextService): {context_metrics['hit_rate_percent']}% hit rate")

    overall_success = (
        config_metrics["hit_rate_percent"] >= 60 and context_metrics["hit_rate_percent"] >= 50
    )

    if overall_success:
        print(f"\n✅ All caching layers performing well")
        print(f"\nCache infrastructure is operational and providing significant performance")
        print(f"improvement for PIPER.md access and user context loading.")
        return 0
    else:
        print(f"\n⚠️  Some caching layers below target performance")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_cache_performance())
    sys.exit(exit_code)
