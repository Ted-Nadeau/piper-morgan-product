"""
MCP Metrics Monitoring
Tracks connection pool metrics, request latency, circuit breaker state, and error rates for MCP integration.
"""

import threading
import time
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
