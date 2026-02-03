"""
Emergency stop system for intelligent automation.

Provides immediate halt capability for all automation operations.

Issue: #225 (CORE-LEARN-E)
"""

from datetime import datetime, timezone
from typing import Dict, Optional, Set


class EmergencyStop:
    """
    Emergency stop system for automation.

    Provides global emergency stop capability to immediately halt
    all automation operations.
    """

    def __init__(self):
        self._stop_flag = False
        self._stopped_at: Optional[datetime] = None
        self._active_operations: Set[str] = set()

    def trigger_emergency_stop(self, reason: str = "Manual stop"):
        """
        Trigger emergency stop for all automation.

        Args:
            reason: Reason for emergency stop
        """
        self._stop_flag = True
        self._stopped_at = datetime.now(timezone.utc)

        # Log emergency stop
        print(f"🚨 EMERGENCY STOP TRIGGERED: {reason} at {self._stopped_at}")

        # Cancel all active operations
        self._active_operations.clear()

    def is_stopped(self) -> bool:
        """Check if emergency stop is active."""
        return self._stop_flag

    def reset(self):
        """Reset emergency stop (requires explicit action)."""
        self._stop_flag = False
        self._stopped_at = None
        self._active_operations.clear()

    def register_operation(self, operation_id: str):
        """Register an active automation operation."""
        if self._stop_flag:
            raise RuntimeError("Cannot start operation - emergency stop active!")
        self._active_operations.add(operation_id)

    def unregister_operation(self, operation_id: str):
        """Unregister completed automation operation."""
        self._active_operations.discard(operation_id)

    def get_status(self) -> Dict:
        """Get emergency stop status."""
        return {
            "stopped": self._stop_flag,
            "stopped_at": self._stopped_at.isoformat() if self._stopped_at else None,
            "active_operations": len(self._active_operations),
        }


# Global emergency stop instance
_emergency_stop = EmergencyStop()


def get_emergency_stop() -> EmergencyStop:
    """Get global emergency stop instance."""
    return _emergency_stop
