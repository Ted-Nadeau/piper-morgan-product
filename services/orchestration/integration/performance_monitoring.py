"""
Performance Monitoring for Multi-Agent Coordinator
Purpose: Track coordination performance and health
"""

import time
from datetime import datetime, timezone
from typing import Any, Dict, List

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import CoordinationStatus, MultiAgentCoordinator


class PerformanceMonitor:
    """Monitors Multi-Agent Coordinator performance and health"""

    def __init__(self):
        self.coordinator = MultiAgentCoordinator()
        self.performance_history: List[Dict[str, Any]] = []

    async def check_multi_agent_health(self) -> Dict[str, Any]:
        """Monitor Multi-Agent Coordinator health"""

        try:
            # Test coordination performance
            test_intent = Intent(
                id="health_check",
                category="EXECUTION",
                action="test_coordination",
                original_message="Health check coordination",
            )

            start_time = time.time()
            result = await self.coordinator.coordinate_task(test_intent, {})
            duration_ms = int((time.time() - start_time) * 1000)

            health_status = {
                "status": "healthy" if duration_ms < 1000 else "degraded",
                "response_time_ms": duration_ms,
                "target_met": duration_ms < 1000,
                "coordination_success": result.status == CoordinationStatus.COMPLETED,
                "last_check": datetime.now(timezone.utc).isoformat(),
                "performance_target": "<1000ms",
            }

            # Store in history
            self.performance_history.append(health_status)

            # Keep only last 100 entries
            if len(self.performance_history) > 100:
                self.performance_history = self.performance_history[-100:]

            return health_status

        except Exception as e:
            error_status = {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now(timezone.utc).isoformat(),
            }

            self.performance_history.append(error_status)
            return error_status

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""

        if not self.performance_history:
            return {"total_checks": 0, "average_response_time": 0}

        total_checks = len(self.performance_history)
        healthy_checks = sum(1 for h in self.performance_history if h.get("status") == "healthy")
        response_times = [
            h.get("response_time_ms", 0)
            for h in self.performance_history
            if h.get("response_time_ms")
        ]

        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return {
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "health_rate": healthy_checks / total_checks if total_checks > 0 else 0,
            "average_response_time_ms": int(avg_response_time),
            "performance_target_met_rate": (
                sum(1 for h in self.performance_history if h.get("target_met", False))
                / total_checks
                if total_checks > 0
                else 0
            ),
            "last_check": (
                self.performance_history[-1].get("last_check") if self.performance_history else None
            ),
        }
