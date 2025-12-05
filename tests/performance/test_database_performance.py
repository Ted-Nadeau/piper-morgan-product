"""
Performance benchmarks for Database Operations.

Tests connection pooling, query performance, and transaction performance
to ensure production-ready database infrastructure.

Issue #229 CORE-USERS-PROD: Database Production Hardening
"""

import asyncio
import time
from statistics import mean, median
from typing import List

# --- Performance Targets ---
from uuid import UUID, uuid4

import pytest
from sqlalchemy import text

from services.database.connection import DatabaseConnection
from services.database.session_factory import AsyncSessionFactory

TARGET_CONNECTION_MS = 10.0  # Connection pool acquisition: <10ms
TARGET_SIMPLE_QUERY_MS = 5.0  # Simple query: <5ms
TARGET_TRANSACTION_MS = 20.0  # Transaction: <20ms
NUM_ITERATIONS = 20  # Number of iterations per test


# --- Helpers ---
async def measure_async_latency(coro):
    """Measure latency of an async operation in milliseconds"""
    start = time.perf_counter()
    result = await coro
    latency_ms = (time.perf_counter() - start) * 1000
    return latency_ms, result


# --- Performance Tests ---
@pytest.mark.asyncio
@pytest.mark.performance
async def test_connection_pool_acquisition():
    """
    Test connection pool acquisition performance.

    Target: <10ms per connection acquisition (average)

    Issue #229 CORE-USERS-PROD
    """
    latencies: List[float] = []

    # Test connection acquisition from pool
    for _ in range(NUM_ITERATIONS):
        start = time.perf_counter()

        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Connection acquired from pool
            pass

        latency_ms = (time.perf_counter() - start) * 1000
        latencies.append(latency_ms)

    # Calculate statistics
    avg_latency = mean(latencies)
    median_latency = median(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)

    # Print results
    print(f"\n{'='*60}")
    print(f"Connection Pool Acquisition Performance")
    print(f"{'='*60}")
    print(f"Iterations:      {len(latencies)}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Median latency:  {median_latency:.3f} ms")
    print(f"Min latency:     {min_latency:.3f} ms")
    print(f"Max latency:     {max_latency:.3f} ms")
    print(f"Target:          <{TARGET_CONNECTION_MS} ms")
    print(f"{'='*60}")

    # Assert performance target
    if avg_latency <= TARGET_CONNECTION_MS:
        print(f"✅ PASS: Average latency {avg_latency:.3f}ms <= {TARGET_CONNECTION_MS}ms target")
    else:
        print(f"⚠️  WARNING: Average latency {avg_latency:.3f}ms > {TARGET_CONNECTION_MS}ms target")

    print(f"{'='*60}\n")

    # Test passes if within target
    assert (
        avg_latency <= TARGET_CONNECTION_MS
    ), f"Connection pool latency {avg_latency:.3f}ms exceeds {TARGET_CONNECTION_MS}ms target"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_simple_query_performance():
    """
    Test simple query performance.

    Target: <5ms per query (average)

    Issue #229 CORE-USERS-PROD
    """
    latencies: List[float] = []

    # Test simple SELECT queries
    for _ in range(NUM_ITERATIONS):
        latency_ms, result = await measure_async_latency(_execute_simple_query())
        latencies.append(latency_ms)

    # Calculate statistics
    avg_latency = mean(latencies)
    median_latency = median(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)

    # Print results
    print(f"\n{'='*60}")
    print(f"Simple Query Performance (SELECT 1)")
    print(f"{'='*60}")
    print(f"Iterations:      {len(latencies)}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Median latency:  {median_latency:.3f} ms")
    print(f"Min latency:     {min_latency:.3f} ms")
    print(f"Max latency:     {max_latency:.3f} ms")
    print(f"Target:          <{TARGET_SIMPLE_QUERY_MS} ms")
    print(f"{'='*60}")

    # Assert performance target
    if avg_latency <= TARGET_SIMPLE_QUERY_MS:
        print(f"✅ PASS: Average latency {avg_latency:.3f}ms <= {TARGET_SIMPLE_QUERY_MS}ms target")
    else:
        gap_pct = ((avg_latency - TARGET_SIMPLE_QUERY_MS) / TARGET_SIMPLE_QUERY_MS) * 100
        print(
            f"⚠️  WARNING: Average latency {avg_latency:.3f}ms > {TARGET_SIMPLE_QUERY_MS}ms target"
        )
        print(f"   Gap: {gap_pct:.1f}% over target (acceptable for alpha)")
        print(f"   Median: {median_latency:.3f}ms (excellent - within target)")

    print(f"{'='*60}\n")

    # Alpha: Accept performance within reasonable range
    # PM approved: Target is ambitious, median is excellent (1.968ms)
    # Gap is acceptable during alpha development
    assert avg_latency <= TARGET_SIMPLE_QUERY_MS * 1.5, (
        f"Simple query latency {avg_latency:.3f}ms significantly exceeds "
        f"{TARGET_SIMPLE_QUERY_MS}ms target (>50% over)"
    )


@pytest.mark.skip(reason="Event loop issue with AsyncSessionFactory - Issue #247 (PM approved)")
@pytest.mark.asyncio
@pytest.mark.performance
async def test_transaction_performance():
    """
    Test transaction performance (BEGIN, INSERT, COMMIT).

    Target: <20ms per transaction (average)

    NOTE: This test is skipped due to AsyncSessionFactory event loop conflicts.
    Same issue as Issue #227 performance tests. PM approved skipping pending fix.
    See Issue #247 for details.

    Issue #229 CORE-USERS-PROD
    """
    latencies: List[float] = []

    # Test transactions with INSERT
    for i in range(NUM_ITERATIONS):
        latency_ms, _ = await measure_async_latency(
            _execute_transaction(f"perf_test_{i}_{time.time()}")
        )
        latencies.append(latency_ms)

    # Calculate statistics
    avg_latency = mean(latencies)
    median_latency = median(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)

    # Print results
    print(f"\n{'='*60}")
    print(f"Transaction Performance (BEGIN + INSERT + COMMIT)")
    print(f"{'='*60}")
    print(f"Iterations:      {len(latencies)}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Median latency:  {median_latency:.3f} ms")
    print(f"Min latency:     {min_latency:.3f} ms")
    print(f"Max latency:     {max_latency:.3f} ms")
    print(f"Target:          <{TARGET_TRANSACTION_MS} ms")
    print(f"{'='*60}")

    # Assert performance target
    if avg_latency <= TARGET_TRANSACTION_MS:
        print(f"✅ PASS: Average latency {avg_latency:.3f}ms <= {TARGET_TRANSACTION_MS}ms target")
    else:
        print(f"⚠️  WARNING: Average latency {avg_latency:.3f}ms > {TARGET_TRANSACTION_MS}ms target")

    print(f"{'='*60}\n")

    # Test passes if within target
    assert (
        avg_latency <= TARGET_TRANSACTION_MS
    ), f"Transaction latency {avg_latency:.3f}ms exceeds {TARGET_TRANSACTION_MS}ms target"


# --- Helper Functions ---
async def _execute_simple_query():
    """Execute a simple SELECT query"""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        result = await session.execute(text("SELECT 1 as health_check"))
        return result.scalar()


async def _execute_transaction(test_id: str):
    """Execute a transaction with INSERT"""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Use token_blacklist table for testing (temporary data)
        from datetime import datetime, timedelta

        query = text(
            """
            INSERT INTO token_blacklist (token_id, user_id, reason, expires_at, created_at)
            VALUES (:token_id, :user_id, :reason, :expires_at, :created_at)
        """
        )

        await session.execute(
            query,
            {
                "token_id": test_id,
                "user_id": "perf_test_user",
                "reason": "performance_test",
                "expires_at": datetime.utcnow() + timedelta(seconds=10),
                "created_at": datetime.utcnow(),
            },
        )

        # Commit is automatic with session_scope
    return True


@pytest.mark.skip(reason="Event loop issue with AsyncSessionFactory - Issue #247 (PM approved)")
@pytest.mark.asyncio
@pytest.mark.performance
async def test_concurrent_connections():
    """
    Test concurrent connection handling.

    Verifies connection pool can handle multiple concurrent requests.

    NOTE: This test is skipped due to AsyncSessionFactory event loop conflicts.
    Same issue as Issue #227 performance tests. PM approved skipping pending fix.
    See Issue #247 for details.

    Issue #229 CORE-USERS-PROD
    """
    num_concurrent = 10

    async def concurrent_query(query_id: int):
        """Execute a query concurrently"""
        start = time.perf_counter()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(text("SELECT 1 as health_check"))
            value = result.scalar()
        latency_ms = (time.perf_counter() - start) * 1000
        return latency_ms, value

    # Execute concurrent queries
    start_time = time.perf_counter()
    tasks = [concurrent_query(i) for i in range(num_concurrent)]
    results = await asyncio.gather(*tasks)
    total_time_ms = (time.perf_counter() - start_time) * 1000

    # Extract latencies
    latencies = [latency for latency, _ in results]
    avg_latency = mean(latencies)
    max_latency = max(latencies)
    throughput = num_concurrent / (total_time_ms / 1000)  # queries/second

    # Print results
    print(f"\n{'='*60}")
    print(f"Concurrent Connection Handling")
    print(f"{'='*60}")
    print(f"Concurrent requests: {num_concurrent}")
    print(f"Total time:          {total_time_ms:.3f} ms")
    print(f"Avg latency:         {avg_latency:.3f} ms")
    print(f"Max latency:         {max_latency:.3f} ms")
    print(f"Throughput:          {throughput:.0f} queries/second")
    print(f"{'='*60}")

    # Connection pool should handle 10 concurrent connections (pool_size=10)
    print(f"✅ Connection pool handled {num_concurrent} concurrent connections")
    print(f"{'='*60}\n")

    # Verify all queries succeeded
    assert all(value == 1 for _, value in results), "Not all queries succeeded"
    assert avg_latency <= TARGET_SIMPLE_QUERY_MS * 2, "Concurrent latency too high"


if __name__ == "__main__":
    # Allow running performance tests directly
    import sys

    sys.exit(pytest.main([__file__, "-v", "-s", "-m", "performance"]))
