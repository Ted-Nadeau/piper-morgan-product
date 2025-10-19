"""
Knowledge Graph boundary enforcement.

Prevents resource exhaustion and ensures predictable performance
for all graph operations.

Issue #230 - CORE-KNOW-BOUNDARY
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class GraphBoundaries:
    """
    Boundary limits for Knowledge Graph operations.

    These limits prevent resource exhaustion and ensure
    predictable query performance.
    """

    # Traversal limits
    max_depth: int = 5  # Maximum traversal depth
    max_nodes_visited: int = 1000  # Maximum nodes to visit

    # Time limits
    max_time_ms: int = 5000  # Maximum execution time (5 seconds)
    query_timeout_ms: int = 100  # Quick query timeout (100ms)

    # Memory limits
    max_result_size: int = 100  # Maximum results to return
    max_memory_mb: int = 100  # Maximum memory usage

    # Complexity limits
    max_edges_per_node: int = 50  # Maximum edges to follow from one node
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
        max_result_size=50,
    )

    # Standard traversal
    TRAVERSAL = GraphBoundaries(
        max_depth=5,
        max_nodes_visited=1000,
        max_time_ms=5000,
        query_timeout_ms=500,
        max_result_size=100,
    )

    # Deep analysis (admin use)
    ANALYSIS = GraphBoundaries(
        max_depth=10,
        max_nodes_visited=5000,
        max_time_ms=10000,
        query_timeout_ms=2000,
        max_result_size=500,
    )


class BoundaryViolation(Exception):
    """Raised when a boundary limit is exceeded."""

    def __init__(self, message: str, boundary_type: str, limit: int, actual: int):
        super().__init__(message)
        self.boundary_type = boundary_type
        self.limit = limit
        self.actual = actual


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
            logger.warning(f"Depth limit exceeded: {current_depth} >= {self.boundaries.max_depth}")
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

        if len(self.visited_nodes) > self.boundaries.max_nodes_visited:
            logger.warning(
                f"Node count limit exceeded: {len(self.visited_nodes)} > "
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
                f"Time limit exceeded: {elapsed_ms:.1f}ms >= " f"{self.boundaries.max_time_ms}ms"
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
                "max_time_ms": self.boundaries.max_time_ms,
            },
        }
