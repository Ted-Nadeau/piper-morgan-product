"""
Performance Monitor - PM-033d Testing Infrastructure
Validates latency targets and performance requirements for multi-agent orchestration
"""

import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List, Tuple


@dataclass
class PerformanceMeasurement:
    """Individual performance measurement result"""

    operation_name: str
    latency_ms: float
    success: bool
    error_message: str = None
    metadata: dict = None


class PerformanceMonitor:
    """Monitor test performance and validate PM-033d targets"""

    def __init__(self, target_latency_ms: int = 200):
        self.target_latency_ms = target_latency_ms
        self.measurements: List[PerformanceMeasurement] = []
        self.start_time = None
        self.end_time = None

    @asynccontextmanager
    async def measure_operation(self, operation_name: str, metadata: dict = None):
        """Context manager for measuring operation performance"""
        start_time = time.time()
        measurement = PerformanceMeasurement(
            operation_name=operation_name, latency_ms=0.0, success=False, metadata=metadata or {}
        )

        try:
            yield measurement
            measurement.success = True
        except Exception as e:
            measurement.error_message = str(e)
            raise
        finally:
            end_time = time.time()
            measurement.latency_ms = (end_time - start_time) * 1000
            self.measurements.append(measurement)

    async def measure_async_operation(
        self, operation_name: str, operation: Callable[[], Awaitable[Any]], metadata: dict = None
    ) -> Tuple[Any, PerformanceMeasurement]:
        """Measure async operation performance and validate targets"""
        async with self.measure_operation(operation_name, metadata) as measurement:
            result = await operation()

            # Validate performance target
            if measurement.latency_ms > self.target_latency_ms:
                raise PerformanceTargetExceededError(
                    f"{operation_name} exceeded {self.target_latency_ms}ms target: {measurement.latency_ms:.2f}ms"
                )

            return result, measurement

    def start_session(self):
        """Start a performance testing session"""
        self.start_time = time.time()
        self.measurements.clear()

    def end_session(self):
        """End a performance testing session"""
        self.end_time = time.time()

    def get_session_summary(self) -> dict:
        """Get comprehensive session performance summary"""
        if not self.measurements:
            return {"error": "No measurements recorded"}

        successful_measurements = [m for m in self.measurements if m.success]
        failed_measurements = [m for m in self.measurements if not m.success]

        if successful_measurements:
            latencies = [m.latency_ms for m in successful_measurements]
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
        else:
            avg_latency = min_latency = max_latency = 0

        return {
            "total_operations": len(self.measurements),
            "successful_operations": len(successful_measurements),
            "failed_operations_count": len(failed_measurements),
            "success_rate": len(successful_measurements) / len(self.measurements) * 100,
            "performance_summary": {
                "average_latency_ms": round(avg_latency, 2),
                "min_latency_ms": round(min_latency, 2),
                "max_latency_ms": round(max_latency, 2),
                "target_latency_ms": self.target_latency_ms,
                "targets_met": all(
                    m.latency_ms <= self.target_latency_ms for m in successful_measurements
                ),
            },
            "session_duration_ms": (self.end_time - self.start_time) * 1000 if self.end_time else 0,
            "failed_operations": [
                {
                    "operation": m.operation_name,
                    "error": m.error_message,
                    "latency_ms": m.latency_ms,
                }
                for m in failed_measurements
            ],
        }

    def validate_pm033d_targets(self) -> dict:
        """Validate PM-033d specific performance targets"""
        summary = self.get_session_summary()

        if "error" in summary:
            return {"valid": False, "error": summary["error"]}

        # PM-033d specific targets
        targets = {
            "agent_coordination": {"target": 50, "description": "Agent-to-agent communication"},
            "workflow_parsing": {"target": 100, "description": "Intent to multi-agent workflow"},
            "task_distribution": {"target": 75, "description": "Workflow to agent task assignment"},
            "progress_updates": {"target": 25, "description": "Agent status synchronization"},
            "overall_workflow": {"target": 200, "description": "Total workflow execution"},
        }

        validation_results = {}
        all_targets_met = True

        for target_name, target_info in targets.items():
            # Find measurements for this target type
            relevant_measurements = [
                m
                for m in self.measurements
                if target_name in m.operation_name.lower() and m.success
            ]

            if relevant_measurements:
                max_latency = max(m.latency_ms for m in relevant_measurements)
                target_met = max_latency <= target_info["target"]
                validation_results[target_name] = {
                    "target_ms": target_info["target"],
                    "actual_max_ms": round(max_latency, 2),
                    "target_met": target_met,
                    "description": target_info["description"],
                }
                if not target_met:
                    all_targets_met = False
            else:
                validation_results[target_name] = {
                    "target_ms": target_info["target"],
                    "actual_max_ms": "No measurements",
                    "target_met": False,
                    "description": target_info["description"],
                }
                all_targets_met = False

        return {"valid": all_targets_met, "targets": validation_results, "overall_summary": summary}


class PerformanceTargetExceededError(Exception):
    """Raised when performance target is exceeded"""

    pass


# Convenience function for quick performance testing
async def quick_performance_test(
    operation_name: str, operation: Callable[[], Awaitable[Any]], target_ms: int = 200
) -> Tuple[Any, float]:
    """Quick performance test for single operations"""
    monitor = PerformanceMonitor(target_ms)
    result, measurement = await monitor.measure_async_operation(operation_name, operation)
    return result, measurement.latency_ms
