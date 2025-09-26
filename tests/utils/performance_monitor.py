"""
Performance monitoring utilities for testing
Provides PerformanceMonitor for measuring async operations and tracking performance
"""

import asyncio
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple


class PerformanceMeasurement:
    """Performance measurement result"""

    def __init__(self, operation_name: str, latency_ms: float, success: bool = True, error: Optional[str] = None):
        self.operation_name = operation_name
        self.latency_ms = latency_ms
        self.success = success
        self.error = error


class PerformanceMonitor:
    """Mock performance monitor for testing coordination scenarios"""

    def __init__(self, target_latency_ms: int = 1000):
        self.target_latency_ms = target_latency_ms
        self.measurements: List[PerformanceMeasurement] = []
        self.session_started = False
        self.session_start_time: Optional[float] = None

    def start_session(self) -> None:
        """Start a performance monitoring session"""
        self.session_started = True
        self.session_start_time = time.time()
        self.measurements.clear()

    def end_session(self) -> Dict[str, Any]:
        """End the performance monitoring session and return summary"""
        if not self.session_started:
            return {"error": "No session started"}

        self.session_started = False
        session_duration = time.time() - (self.session_start_time or 0)

        return {
            "session_duration_ms": session_duration * 1000,
            "total_measurements": len(self.measurements),
            "successful_operations": sum(1 for m in self.measurements if m.success),
            "failed_operations": sum(1 for m in self.measurements if not m.success),
            "average_latency_ms": (
                sum(m.latency_ms for m in self.measurements) / len(self.measurements)
                if self.measurements else 0
            ),
            "target_latency_ms": self.target_latency_ms
        }

    async def measure_async_operation(
        self, operation_name: str, operation: Callable[[], Awaitable[Any]]
    ) -> Tuple[Any, PerformanceMeasurement]:
        """Measure an async operation and return both result and measurement

        Args:
            operation_name: Name of the operation being measured
            operation: Async callable to execute and measure

        Returns:
            Tuple of (operation_result, performance_measurement)
        """
        start_time = time.time()
        error = None
        result = None

        try:
            result = await operation()
            success = True
        except Exception as e:
            success = False
            error = str(e)
            # For testing, we'll create a mock result that indicates failure
            result = type('MockResult', (), {'success': False, 'error': error})()

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        measurement = PerformanceMeasurement(
            operation_name=operation_name,
            latency_ms=latency_ms,
            success=success,
            error=error
        )

        self.measurements.append(measurement)

        return result, measurement

    def get_measurements(self) -> List[PerformanceMeasurement]:
        """Get all recorded measurements"""
        return self.measurements.copy()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all measurements"""
        if not self.measurements:
            return {"no_measurements": True}

        latencies = [m.latency_ms for m in self.measurements if m.success]
        if not latencies:
            return {"no_successful_measurements": True}

        return {
            "count": len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "target_latency_ms": self.target_latency_ms,
            "within_target_count": sum(1 for l in latencies if l <= self.target_latency_ms),
            "exceeded_target_count": sum(1 for l in latencies if l > self.target_latency_ms)
        }