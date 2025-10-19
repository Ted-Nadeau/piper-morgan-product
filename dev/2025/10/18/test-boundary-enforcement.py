#!/usr/bin/env python3
"""
Test Knowledge Graph boundary enforcement.

Tests:
1. Depth limit enforcement
2. Node count limit enforcement
3. Timeout enforcement
4. Result size limit enforcement
5. Partial results on limit hit

Issue #230 - CORE-KNOW-BOUNDARY
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.knowledge.boundaries import BoundaryEnforcer, GraphBoundaries, OperationBoundaries


async def test_depth_limit():
    """Test that depth limit is enforced."""
    print("\n=== Test 1: Depth Limit ===")

    boundaries = GraphBoundaries(max_depth=3)
    enforcer = BoundaryEnforcer(boundaries)

    enforcer.start_operation()

    # Depths 0, 1, 2 should be allowed
    assert enforcer.check_depth(0) == True
    assert enforcer.check_depth(1) == True
    assert enforcer.check_depth(2) == True

    # Depth 3 and above should be blocked
    assert enforcer.check_depth(3) == False
    assert enforcer.check_depth(4) == False

    print("✅ PASS: Depth limit enforced correctly")
    return True


async def test_node_count_limit():
    """Test that node count limit is enforced."""
    print("\n=== Test 2: Node Count Limit ===")

    boundaries = GraphBoundaries(max_nodes_visited=5)
    enforcer = BoundaryEnforcer(boundaries)

    enforcer.start_operation()

    # Visit nodes up to limit
    for i in range(5):
        assert enforcer.visit_node(f"node-{i}") == True

    # 6th node should be blocked
    assert enforcer.visit_node("node-5") == False

    print(f"✅ PASS: Node count limit enforced (5 nodes allowed)")
    return True


async def test_timeout():
    """Test that timeout is enforced."""
    print("\n=== Test 3: Timeout ===")

    boundaries = GraphBoundaries(max_time_ms=100)  # 100ms timeout
    enforcer = BoundaryEnforcer(boundaries)

    enforcer.start_operation()

    # Check immediately - should pass
    assert enforcer.check_timeout() == True

    # Wait 150ms
    time.sleep(0.15)

    # Check after timeout - should fail
    assert enforcer.check_timeout() == False

    print("✅ PASS: Timeout enforced correctly")
    return True


async def test_result_size_limit():
    """Test that result size limit is enforced."""
    print("\n=== Test 4: Result Size Limit ===")

    boundaries = GraphBoundaries(max_result_size=10)
    enforcer = BoundaryEnforcer(boundaries)

    enforcer.start_operation()

    # Results up to limit should be allowed
    for i in range(10):
        assert enforcer.check_result_size(i) == True

    # 11th result should be blocked
    assert enforcer.check_result_size(10) == False

    print("✅ PASS: Result size limit enforced")
    return True


async def test_operation_boundaries():
    """Test operation-specific boundary configurations."""
    print("\n=== Test 5: Operation Boundaries ===")

    # Search boundaries (restrictive)
    search = OperationBoundaries.SEARCH
    assert search.max_depth == 3
    assert search.max_nodes_visited == 500
    assert search.query_timeout_ms == 100

    # Traversal boundaries (moderate)
    traversal = OperationBoundaries.TRAVERSAL
    assert traversal.max_depth == 5
    assert traversal.max_nodes_visited == 1000

    # Analysis boundaries (permissive)
    analysis = OperationBoundaries.ANALYSIS
    assert analysis.max_depth == 10
    assert analysis.max_nodes_visited == 5000

    print("✅ PASS: Operation-specific boundaries configured correctly")
    return True


async def test_stats_tracking():
    """Test that statistics are tracked correctly."""
    print("\n=== Test 6: Statistics Tracking ===")

    boundaries = GraphBoundaries()
    enforcer = BoundaryEnforcer(boundaries)

    enforcer.start_operation()

    # Visit some nodes
    enforcer.visit_node("node-1")
    enforcer.visit_node("node-2")
    enforcer.visit_node("node-3")

    # Get stats
    stats = enforcer.get_stats()

    assert stats["nodes_visited"] == 3
    assert stats["elapsed_ms"] >= 0
    assert "limits" in stats

    print(f"✅ PASS: Stats tracked correctly: {stats}")
    return True


async def main():
    """Run all boundary enforcement tests."""
    print("=" * 70)
    print("BOUNDARY ENFORCEMENT TESTS - Issue #230")
    print("=" * 70)

    tests = [
        ("Depth Limit", test_depth_limit),
        ("Node Count Limit", test_node_count_limit),
        ("Timeout", test_timeout),
        ("Result Size Limit", test_result_size_limit),
        ("Operation Boundaries", test_operation_boundaries),
        ("Statistics Tracking", test_stats_tracking),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total} ({100*passed//total if total else 0}%)")
    print()

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    if passed == total:
        print("\n🎉 All boundary enforcement tests passed!")
    else:
        print(f"\n⚠️  Some tests failed - {passed}/{total} passed")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
