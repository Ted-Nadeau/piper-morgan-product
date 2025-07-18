"""
Performance benchmarks for MCP connection pooling.
Run BEFORE implementing pool to establish baseline.
"""

import asyncio
import os
import time
import tracemalloc
from statistics import median, quantiles

import pytest

from services.mcp.client import PiperMCPClient

# Try to import connection pool - graceful fallback if not available
try:
    from services.infrastructure.mcp.connection_pool import MCPConnectionPool

    POOL_AVAILABLE = True
except ImportError:
    POOL_AVAILABLE = False

# --- Config ---
CLIENT_CONFIG = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

# Check if pool should be used
USE_POOL = os.getenv("USE_MCP_POOL", "false").lower() == "true" and POOL_AVAILABLE


# --- Helpers ---
def measure_latency(coro):
    start = time.perf_counter()
    result = asyncio.get_event_loop().run_until_complete(coro)
    latency = time.perf_counter() - start
    return latency, result


# --- Benchmarks ---
@pytest.mark.asyncio
async def test_single_request_latency():
    """Measure latency of a single MCP request."""
    if USE_POOL:
        # Use connection pool
        pool = MCPConnectionPool.get_instance()
        async with pool.connection(CLIENT_CONFIG) as client:
            start = time.perf_counter()
            await client.list_resources()
            latency = time.perf_counter() - start
        print(f"Single request latency (pool): {latency*1000:.2f} ms")
    else:
        # Use direct connection (original test)
        client = PiperMCPClient(CLIENT_CONFIG)
        await client.connect()
        start = time.perf_counter()
        await client.list_resources()
        latency = time.perf_counter() - start
        print(f"Single request latency (direct): {latency*1000:.2f} ms")
        await client.disconnect()


@pytest.mark.asyncio
@pytest.mark.parametrize("concurrency", [10, 50, 100])
async def test_concurrent_requests(concurrency):
    """Measure latency under concurrent requests."""
    if USE_POOL:
        # Use connection pool
        pool = MCPConnectionPool.get_instance()

        async def do_request():
            async with pool.connection(CLIENT_CONFIG) as client:
                start = time.perf_counter()
                await client.list_resources()
                return time.perf_counter() - start

        latencies = await asyncio.gather(*(do_request() for _ in range(concurrency)))
        print(
            f"Concurrent ({concurrency}) request latencies (pool): p50={median(latencies)*1000:.2f} ms, "
            f"p95={quantiles(latencies, n=100)[94]*1000:.2f} ms, p99={quantiles(latencies, n=100)[98]*1000:.2f} ms"
        )
    else:
        # Use direct connection (original test)
        client = PiperMCPClient(CLIENT_CONFIG)
        await client.connect()

        async def do_request():
            start = time.perf_counter()
            await client.list_resources()
            return time.perf_counter() - start

        latencies = await asyncio.gather(*(do_request() for _ in range(concurrency)))
        print(
            f"Concurrent ({concurrency}) request latencies (direct): p50={median(latencies)*1000:.2f} ms, "
            f"p95={quantiles(latencies, n=100)[94]*1000:.2f} ms, p99={quantiles(latencies, n=100)[98]*1000:.2f} ms"
        )
        await client.disconnect()


@pytest.mark.asyncio
async def test_connection_creation_overhead():
    """Measure time to create and connect a new client."""
    if USE_POOL:
        # Measure pool initialization and first connection
        start = time.perf_counter()
        pool = MCPConnectionPool.get_instance()
        async with pool.connection(CLIENT_CONFIG) as client:
            latency = time.perf_counter() - start
        print(f"Connection creation time (pool): {latency*1000:.2f} ms")
    else:
        # Use direct connection (original test)
        start = time.perf_counter()
        client = PiperMCPClient(CLIENT_CONFIG)
        await client.connect()
        latency = time.perf_counter() - start
        print(f"Connection creation time (direct): {latency*1000:.2f} ms")
        await client.disconnect()


@pytest.mark.asyncio
async def test_memory_usage_per_connection():
    """Measure memory usage per connection."""
    if USE_POOL:
        # Measure memory usage with pool
        tracemalloc.start()
        pool = MCPConnectionPool.get_instance()
        async with pool.connection(CLIENT_CONFIG) as client:
            await client.list_resources()
        current, peak = tracemalloc.get_traced_memory()
        print(
            f"Memory usage per connection (pool): current={current/1024:.2f} KB, peak={peak/1024:.2f} KB"
        )
        tracemalloc.stop()
    else:
        # Use direct connection (original test)
        tracemalloc.start()
        client = PiperMCPClient(CLIENT_CONFIG)
        await client.connect()
        current, peak = tracemalloc.get_traced_memory()
        print(
            f"Memory usage per connection (direct): current={current/1024:.2f} KB, peak={peak/1024:.2f} KB"
        )
        await client.disconnect()
        tracemalloc.stop()


@pytest.mark.asyncio
async def test_circuit_breaker_activation_time():
    """Measure time to circuit breaker activation on repeated failures."""
    if USE_POOL:
        # Test circuit breaker with pool
        pool = MCPConnectionPool.get_instance()
        start = time.perf_counter()
        for _ in range(10):
            try:
                async with pool.connection({"url": "invalid://server", "timeout": 0.01}) as client:
                    await client.connect()
            except Exception:
                pass
        elapsed = time.perf_counter() - start
        stats = pool.get_stats()
        print(
            f"Circuit breaker activation time (pool, 10 failures): {elapsed*1000:.2f} ms, state={stats.get('circuit_state', 'unknown')}"
        )
    else:
        # Use direct connection (original test)
        client = PiperMCPClient({"url": "invalid://server", "timeout": 0.01})
        start = time.perf_counter()
        for _ in range(10):
            try:
                await client.connect()
            except Exception:
                pass
        elapsed = time.perf_counter() - start
        print(
            f"Circuit breaker activation time (direct, 10 failures): {elapsed*1000:.2f} ms, state={client.circuit_breaker.state}"
        )
        await client.disconnect()


# --- Baseline Measurement Instructions ---
# 1. Run these tests BEFORE pool implementation: pytest -s tests/performance/test_mcp_pool_performance.py -v
# 2. Run these tests AFTER pool implementation: USE_MCP_POOL=true pytest -s tests/performance/test_mcp_pool_performance.py -v
# 3. Document:
#    - Connection creation time
#    - Memory leak rate
#    - Connections created per operation
#    - Latency percentiles (p50, p95, p99)
# 4. Use output to populate docs/performance/mcp-baseline-metrics.md and docs/performance/mcp-pool-comparison.md
