# Phase 4: Boundary Enforcement - CORE-KNOW-BOUNDARY #230

**Agent**: Claude Code (Programmer)
**Issue**: #230 - CORE-KNOW-BOUNDARY
**Phase**: 4 - Boundary Enforcement
**Date**: October 18, 2025, 4:42 PM
**Duration**: ~1 hour estimated

---

## Mission

Implement safety boundaries for Knowledge Graph operations to prevent infinite traversal, resource exhaustion, and ensure predictable performance. This completes the safety framework for Issue #99 (CORE-KNOW).

## Context

**Phases 1-3 Complete** ✅:
- Database schema operational
- IntentService integration working
- Context enhancement validated
- Feature ACTIVATED (ENABLE_KNOWLEDGE_GRAPH=true)
- All tests passing (9/9 = 100%)

**Issue #230 Scope**: Add boundary checking marked as TODO in knowledge services

**Pattern**: Similar to resource limits in any graph database system

---

## Why Boundaries Matter

**Without Boundaries**:
- Infinite traversal loops (A→B→C→A→...)
- Memory exhaustion (loading millions of nodes)
- Hung queries (complex graph algorithms)
- DoS vulnerabilities

**With Boundaries**:
- Predictable performance
- Resource protection
- Graceful degradation
- User-friendly limits

---

## Implementation Strategy

### Step 1: Define Boundary Limits (10 minutes)

**File**: `services/knowledge/boundaries.py` (new)

```python
"""
Knowledge Graph boundary enforcement.

Prevents resource exhaustion and ensures predictable performance
for all graph operations.
"""

from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class GraphBoundaries:
    """
    Boundary limits for Knowledge Graph operations.

    These limits prevent resource exhaustion and ensure
    predictable query performance.
    """

    # Traversal limits
    max_depth: int = 5              # Maximum traversal depth
    max_nodes_visited: int = 1000   # Maximum nodes to visit

    # Time limits
    max_time_ms: int = 5000         # Maximum execution time (5 seconds)
    query_timeout_ms: int = 100     # Quick query timeout (100ms)

    # Memory limits
    max_result_size: int = 100      # Maximum results to return
    max_memory_mb: int = 100        # Maximum memory usage

    # Complexity limits
    max_edges_per_node: int = 50    # Maximum edges to follow from one node
    max_pattern_matches: int = 100  # Maximum pattern matches


@dataclass
class OperationBoundaries:
    """Operation-specific boundary configurations."""

    # Quick searches (conversation context)
    SEARCH = GraphBoundaries(
        max_depth=3,
        max_nodes_visited=500,
        max_time_ms=2000,
        query_timeout_ms=100,
        max_result_size=50
    )

    # Standard traversal
    TRAVERSAL = GraphBoundaries(
        max_depth=5,
        max_nodes_visited=1000,
        max_time_ms=5000,
        query_timeout_ms=500,
        max_result_size=100
    )

    # Deep analysis (admin use)
    ANALYSIS = GraphBoundaries(
        max_depth=10,
        max_nodes_visited=5000,
        max_time_ms=10000,
        query_timeout_ms=2000,
        max_result_size=500
    )


class BoundaryViolation(Exception):
    """Raised when a boundary limit is exceeded."""

    def __init__(self, message: str, boundary_type: str, limit: int, actual: int):
        super().__init__(message)
        self.boundary_type = boundary_type
        self.limit = limit
        self.actual = actual
```

### Step 2: Create Boundary Enforcer (20 minutes)

**Add to `services/knowledge/boundaries.py`**:

```python
import time
from typing import Set, Any, Dict


class BoundaryEnforcer:
    """
    Enforces boundary limits during Knowledge Graph operations.

    Usage:
        enforcer = BoundaryEnforcer(OperationBoundaries.SEARCH)

        # Check before each operation
        if not enforcer.check_depth(current_depth):
            return partial_results

        if not enforcer.check_node_count():
            return partial_results

        if not enforcer.check_timeout():
            return partial_results
    """

    def __init__(self, boundaries: GraphBoundaries):
        """
        Initialize boundary enforcer.

        Args:
            boundaries: Boundary limits to enforce
        """
        self.boundaries = boundaries
        self.visited_nodes: Set[str] = set()
        self.start_time: Optional[float] = None
        self.operation_count: int = 0

    def start_operation(self):
        """Start tracking an operation."""
        self.start_time = time.time()
        self.visited_nodes.clear()
        self.operation_count = 0

    def check_depth(self, current_depth: int) -> bool:
        """
        Check if depth limit exceeded.

        Args:
            current_depth: Current traversal depth

        Returns:
            True if within limit, False if exceeded
        """
        if current_depth >= self.boundaries.max_depth:
            logger.warning(
                f"Depth limit exceeded: {current_depth} >= {self.boundaries.max_depth}"
            )
            return False
        return True

    def visit_node(self, node_id: str) -> bool:
        """
        Record a node visit and check node count limit.

        Args:
            node_id: ID of node being visited

        Returns:
            True if within limit, False if exceeded
        """
        self.visited_nodes.add(node_id)

        if len(self.visited_nodes) >= self.boundaries.max_nodes_visited:
            logger.warning(
                f"Node count limit exceeded: {len(self.visited_nodes)} >= "
                f"{self.boundaries.max_nodes_visited}"
            )
            return False
        return True

    def check_timeout(self) -> bool:
        """
        Check if time limit exceeded.

        Returns:
            True if within limit, False if exceeded
        """
        if self.start_time is None:
            return True

        elapsed_ms = (time.time() - self.start_time) * 1000

        if elapsed_ms >= self.boundaries.max_time_ms:
            logger.warning(
                f"Time limit exceeded: {elapsed_ms:.1f}ms >= "
                f"{self.boundaries.max_time_ms}ms"
            )
            return False
        return True

    def check_result_size(self, result_count: int) -> bool:
        """
        Check if result size limit exceeded.

        Args:
            result_count: Number of results so far

        Returns:
            True if within limit, False if exceeded
        """
        if result_count >= self.boundaries.max_result_size:
            logger.warning(
                f"Result size limit exceeded: {result_count} >= "
                f"{self.boundaries.max_result_size}"
            )
            return False
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get operation statistics."""
        elapsed_ms = 0
        if self.start_time:
            elapsed_ms = (time.time() - self.start_time) * 1000

        return {
            "nodes_visited": len(self.visited_nodes),
            "elapsed_ms": elapsed_ms,
            "operations": self.operation_count,
            "limits": {
                "max_depth": self.boundaries.max_depth,
                "max_nodes": self.boundaries.max_nodes_visited,
                "max_time_ms": self.boundaries.max_time_ms
            }
        }
```

### Step 3: Integrate with KnowledgeGraphService (15 minutes)

**Modify**: `services/knowledge/knowledge_graph_service.py`

```python
# Add at top
from services.knowledge.boundaries import (
    BoundaryEnforcer,
    OperationBoundaries,
    GraphBoundaries
)

class KnowledgeGraphService:
    def __init__(self, repository: KnowledgeGraphRepository):
        self.repository = repository
        # Add boundary enforcer
        self.boundary_enforcer = BoundaryEnforcer(OperationBoundaries.SEARCH)

    async def search_nodes(
        self,
        node_type: Optional[NodeType] = None,
        search_term: Optional[str] = None,
        limit: int = 10
    ) -> List[KnowledgeNode]:
        """
        Search for nodes with boundary enforcement.

        Args:
            node_type: Optional node type filter
            search_term: Optional search term
            limit: Maximum results (subject to boundary limits)

        Returns:
            List of matching nodes (may be partial if limits hit)
        """
        # Start boundary tracking
        self.boundary_enforcer.start_operation()

        try:
            # Check result size limit
            actual_limit = min(
                limit,
                self.boundary_enforcer.boundaries.max_result_size
            )

            # Perform search
            nodes = await self.repository.search_nodes(
                node_type=node_type,
                search_term=search_term,
                limit=actual_limit
            )

            # Record nodes visited
            for node in nodes:
                self.boundary_enforcer.visit_node(str(node.id))

            # Check if we hit limits
            stats = self.boundary_enforcer.get_stats()
            if stats["nodes_visited"] >= stats["limits"]["max_nodes"]:
                logger.info("Search hit node count limit - results may be partial")

            return nodes

        except Exception as e:
            logger.error(f"Search failed with boundaries: {e}")
            raise

    async def traverse_relationships(
        self,
        start_node_id: str,
        max_depth: Optional[int] = None
    ) -> List[Dict]:
        """
        Traverse relationships with boundary enforcement.

        Args:
            start_node_id: Starting node ID
            max_depth: Optional max depth (overrides boundary default)

        Returns:
            List of related nodes (may be partial if limits hit)
        """
        # Start boundary tracking
        self.boundary_enforcer.start_operation()

        # Override max depth if specified
        if max_depth and max_depth < self.boundary_enforcer.boundaries.max_depth:
            self.boundary_enforcer.boundaries.max_depth = max_depth

        results = []
        current_depth = 0
        nodes_to_visit = [start_node_id]
        visited = set()

        while nodes_to_visit and current_depth < self.boundary_enforcer.boundaries.max_depth:
            # Check timeout
            if not self.boundary_enforcer.check_timeout():
                logger.warning("Traversal stopped: timeout reached")
                break

            # Check depth
            if not self.boundary_enforcer.check_depth(current_depth):
                logger.warning("Traversal stopped: max depth reached")
                break

            # Visit nodes at this depth
            next_level = []
            for node_id in nodes_to_visit:
                if node_id in visited:
                    continue

                # Check node count
                if not self.boundary_enforcer.visit_node(node_id):
                    logger.warning("Traversal stopped: max nodes reached")
                    return results

                visited.add(node_id)

                # Get node
                node = await self.repository.get_node(node_id)
                if node:
                    results.append({
                        "node": node,
                        "depth": current_depth
                    })

                    # Get edges (with limit)
                    edges = await self.repository.get_edges_from_node(
                        node_id,
                        limit=self.boundary_enforcer.boundaries.max_edges_per_node
                    )

                    # Add targets to next level
                    for edge in edges:
                        if edge.target_node_id not in visited:
                            next_level.append(str(edge.target_node_id))

            nodes_to_visit = next_level
            current_depth += 1

        # Log stats
        stats = self.boundary_enforcer.get_stats()
        logger.info(f"Traversal complete: {stats}")

        return results
```

### Step 4: Test Boundary Enforcement (15 minutes)

**File**: `dev/2025/10/18/test-boundary-enforcement.py`

```python
"""
Test Knowledge Graph boundary enforcement.

Tests:
1. Depth limit enforcement
2. Node count limit enforcement
3. Timeout enforcement
4. Result size limit enforcement
5. Partial results on limit hit
"""

import asyncio
import pytest
from services.knowledge.boundaries import (
    BoundaryEnforcer,
    OperationBoundaries,
    GraphBoundaries
)


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

    import time

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
    print("BOUNDARY ENFORCEMENT TESTS")
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

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```

---

## Success Criteria

Phase 4 is complete when:

- [ ] GraphBoundaries dataclass created
- [ ] OperationBoundaries configurations defined
- [ ] BoundaryEnforcer class implemented
- [ ] KnowledgeGraphService integrated with enforcer
- [ ] All boundary tests passing (6/6)
- [ ] Partial results returned when limits hit
- [ ] Statistics tracked correctly
- [ ] Documentation updated

---

## Deliverables

1. **services/knowledge/boundaries.py** (new) - Boundary classes
2. **services/knowledge/knowledge_graph_service.py** (modified) - Integration
3. **dev/2025/10/18/test-boundary-enforcement.py** (new) - Tests
4. **dev/2025/10/18/phase-4-boundary-report.md** - Completion report

---

## Time Estimate

- Step 1 (Define boundaries): 10 minutes
- Step 2 (Create enforcer): 20 minutes
- Step 3 (Integrate): 15 minutes
- Step 4 (Test): 15 minutes
- **Total**: ~1 hour

---

## Important Notes

### Use Serena Efficiently

**Token Management Critical**: We're at 60% of sprint completion with substantial context loaded.

**Before modifying files**:
```python
# Use Serena to check current structure
mcp__serena__get_symbols_overview("services/knowledge/knowledge_graph_service.py")

# Only read specific sections
mcp__serena__view_file(
    path="services/knowledge/knowledge_graph_service.py",
    start_line=50,
    end_line=100
)
```

### Graceful Degradation

When limits hit:
- Log warning (don't raise exception)
- Return partial results
- Include metadata about truncation
- User sees some results, not an error

### Operation-Specific Limits

Different operations need different limits:
- **Search** (conversation): Fast, restrictive (depth=3, 500 nodes)
- **Traversal** (exploration): Moderate (depth=5, 1000 nodes)
- **Analysis** (admin): Permissive (depth=10, 5000 nodes)

### Testing Focus

Test the **boundaries**, not the graph operations:
- Does enforcer block at limits? ✅
- Are partial results returned? ✅
- Are stats tracked? ✅

Don't need to test actual graph traversal (Phase 3 validated that).

---

## Next Phase Preview

**Phase 5** (Final):
- Complete documentation (30 minutes)
- Configuration guide
- Deployment instructions
- Sprint A3 completion report

But first: Add safety boundaries!

---

**Ready to implement Knowledge Graph boundary enforcement!** 🛡️

**This protects resources and ensures predictable performance!**
