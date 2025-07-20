import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

from services.infrastructure.monitoring.mcp_metrics import MCPMetrics, content_extraction_metrics


@dataclass
class HealthStatus:
    healthy: bool
    details: Dict[str, Optional[str]]
    metrics: Dict


class MCPHealthCheck:
    """Health monitoring for MCP subsystem"""

    @staticmethod
    async def check_health() -> HealthStatus:
        # Check connection pool status
        metrics = MCPMetrics().get_metrics()
        pool_ok = (
            metrics["connection_pool_size"] > 0 and metrics["circuit_breaker_state"] == "closed"
        )
        # Check recent extraction success rate
        perf = content_extraction_metrics.get_performance_summary()
        extraction_ok = (
            all(v < 0.05 for v in perf["errors_by_type"].values())
            if perf["errors_by_type"]
            else True
        )
        # Check config validity (placeholder: always valid)
        config_ok = True
        # Check performance (e.g., extraction time < 500ms)
        perf_ok = (
            all(t < 500 for t in perf["avg_extraction_time_ms"].values())
            if perf["avg_extraction_time_ms"]
            else True
        )
        healthy = pool_ok and extraction_ok and config_ok and perf_ok
        details = {
            "connection_pool": "OK" if pool_ok else "Degraded",
            "extraction": "OK" if extraction_ok else "High error rate",
            "config": "OK" if config_ok else "Invalid",
            "performance": "OK" if perf_ok else "Slow",
        }
        return HealthStatus(
            healthy=healthy,
            details=details,
            metrics={
                "connection": metrics,
                "extraction": perf,
            },
        )
