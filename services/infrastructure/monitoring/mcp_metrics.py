"""
MCP Metrics Monitoring
Tracks connection pool metrics, request latency, circuit breaker state, and error rates for MCP integration.
"""

import asyncio
import threading
import time
import tracemalloc
from collections import defaultdict
from typing import Dict, List, Optional


class MCPMetrics:
    """Singleton for tracking MCP connection and request metrics."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_metrics()
            return cls._instance

    def _init_metrics(self):
        self.connection_pool_size = 0
        self.active_connections = 0
        self.request_latencies: List[float] = []
        self.circuit_breaker_state = "closed"
        self.error_count = 0
        self.total_requests = 0
        self.last_error: Optional[str] = None
        self.last_metrics_snapshot: Dict = {}
        self.search_latency_breakdown = []  # [(conn_ms, extract_ms, score_ms, total_ms)]
        self.memory_usage_during_extraction = []  # [(timestamp, mem_bytes)]
        self.concurrent_extraction_counts = []  # [(timestamp, count)]

    def record_connection_pool(self, pool_size: int, active: int):
        self.connection_pool_size = pool_size
        self.active_connections = active

    def record_request_latency(self, latency: float):
        self.request_latencies.append(latency)
        if len(self.request_latencies) > 1000:
            self.request_latencies = self.request_latencies[-1000:]

    def record_circuit_breaker(self, state: str):
        self.circuit_breaker_state = state

    def record_error(self, error: str):
        self.error_count += 1
        self.last_error = error

    def record_request(self):
        self.total_requests += 1

    def record_search_latency_breakdown(self, conn_ms, extract_ms, score_ms, total_ms):
        self.search_latency_breakdown.append((conn_ms, extract_ms, score_ms, total_ms))
        if len(self.search_latency_breakdown) > 1000:
            self.search_latency_breakdown = self.search_latency_breakdown[-1000:]

    def record_memory_usage(self, mem_bytes):
        self.memory_usage_during_extraction.append((time.time(), mem_bytes))
        if len(self.memory_usage_during_extraction) > 1000:
            self.memory_usage_during_extraction = self.memory_usage_during_extraction[-1000:]

    def record_concurrent_extraction(self, count):
        self.concurrent_extraction_counts.append((time.time(), count))
        if len(self.concurrent_extraction_counts) > 1000:
            self.concurrent_extraction_counts = self.concurrent_extraction_counts[-1000:]

    def get_metrics(self) -> Dict:
        avg_latency = (
            sum(self.request_latencies) / len(self.request_latencies)
            if self.request_latencies
            else 0.0
        )
        error_rate = self.error_count / self.total_requests if self.total_requests else 0.0
        snapshot = {
            "connection_pool_size": self.connection_pool_size,
            "active_connections": self.active_connections,
            "avg_request_latency_ms": avg_latency * 1000,
            "circuit_breaker_state": self.circuit_breaker_state,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "total_requests": self.total_requests,
            "last_error": self.last_error,
        }
        self.last_metrics_snapshot = snapshot
        return snapshot


# Example usage (to be replaced with integration hooks):
# metrics = MCPMetrics()
# metrics.record_connection_pool(pool_size=10, active=3)
# metrics.record_request_latency(0.045)
# metrics.record_circuit_breaker("closed")
# metrics.record_error("TimeoutError")
# print(metrics.get_metrics())


class ContentExtractionMetrics:
    """Track performance of content extraction operations"""

    def __init__(self):
        self.extraction_times = defaultdict(list)  # file_type -> [ms]
        self.extraction_sizes = defaultdict(list)  # file_type -> [(size_bytes, ms)]
        self.errors_by_type = defaultdict(int)
        self.cache_hits = 0
        self.cache_misses = 0
        self.memory_spikes = defaultdict(list)  # file_type -> [peak_mem_bytes]
        self.concurrent_extractions = []  # [(timestamp, count)]

    async def record_extraction(
        self,
        file_type: str,
        size_bytes: int,
        duration_ms: float,
        peak_mem_bytes: Optional[int] = None,
    ):
        """Record successful extraction metrics"""
        self.extraction_times[file_type].append(duration_ms)
        self.extraction_sizes[file_type].append((size_bytes, duration_ms))
        if peak_mem_bytes is not None:
            self.memory_spikes[file_type].append(peak_mem_bytes)
        # Track concurrency (for test harness)
        self.concurrent_extractions.append((time.time(), self.get_current_concurrency()))

    async def record_extraction_error(self, file_type: str, error_type: str):
        """Record extraction failures"""
        self.errors_by_type[(file_type, error_type)] += 1

    def record_cache_hit(self):
        self.cache_hits += 1

    def record_cache_miss(self):
        self.cache_misses += 1

    def get_performance_summary(self) -> dict:
        """Get current performance statistics"""
        summary = {
            "avg_extraction_time_ms": {
                ft: (sum(times) / len(times) if times else 0)
                for ft, times in self.extraction_times.items()
            },
            "max_extraction_time_ms": {
                ft: (max(times) if times else 0) for ft, times in self.extraction_times.items()
            },
            "memory_spikes_bytes": {
                ft: (max(mem) if mem else 0) for ft, mem in self.memory_spikes.items()
            },
            "errors_by_type": dict(self.errors_by_type),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "concurrent_extractions": self.concurrent_extractions[-10:],
        }
        return summary

    def get_current_concurrency(self) -> int:
        # For async test harness: count running tasks
        return len([t for t in asyncio.all_tasks() if not t.done()])


# Singleton instance for content extraction metrics
content_extraction_metrics = ContentExtractionMetrics()
