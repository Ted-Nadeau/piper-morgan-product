from typing import Any, Dict

import numpy as np

from services.infrastructure.monitoring.mcp_metrics import MCPMetrics, content_extraction_metrics


class MCPDashboardMetrics:
    """Aggregate metrics for monitoring dashboard"""

    def __init__(self):
        self.metrics = MCPMetrics()
        self.extraction_metrics = content_extraction_metrics
        self._fallback_count = 0
        self._circuit_breaker_trips = 0
        self._recovery_successes = 0
        self._recovery_attempts = 0

    def _calculate_error_rates(self) -> Dict[str, float]:
        perf = self.extraction_metrics.get_performance_summary()
        error_rates = {}
        total = sum(perf["errors_by_type"].values()) if perf["errors_by_type"] else 0
        for (ft, _), count in perf["errors_by_type"].items():
            error_rates[ft] = count / max(total, 1)
        return error_rates

    def _latency_percentiles(self, latencies):
        if not latencies:
            return {"p50": 0, "p95": 0, "p99": 0}
        arr = np.array(latencies)
        return {
            "p50_latency": float(np.percentile(arr, 50)),
            "p95_latency": float(np.percentile(arr, 95)),
            "p99_latency": float(np.percentile(arr, 99)),
        }

    def _health_status(self) -> Dict[str, Any]:
        metrics = self.metrics.get_metrics()
        healthy = metrics["error_rate"] < 0.05 and metrics["avg_request_latency_ms"] < 500
        status = (
            "healthy" if healthy else ("degraded" if metrics["error_rate"] < 0.1 else "unhealthy")
        )
        issues = []
        if metrics["error_rate"] >= 0.05:
            issues.append("High error rate")
        if metrics["avg_request_latency_ms"] >= 500:
            issues.append("High latency")
        return {"status": status, "issues": issues}

    def _recovery_stats(self) -> Dict[str, Any]:
        rate = self._recovery_successes / max(self._recovery_attempts, 1)
        return {
            "fallback_count": self._fallback_count,
            "circuit_breaker_trips": self._circuit_breaker_trips,
            "recovery_success_rate": rate,
        }

    async def get_dashboard_data(self) -> dict:
        latencies = self.metrics.request_latencies
        latency_percentiles = self._latency_percentiles(latencies)
        return {
            "error_rates": self._calculate_error_rates(),
            "performance": latency_percentiles,
            "health": self._health_status(),
            "recovery": self._recovery_stats(),
        }
