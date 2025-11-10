"""
Audit trail system for intelligent automation.

Logs all automation actions for accountability and review.

Issue: #225 (CORE-LEARN-E)
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID


@dataclass
class AutomationEvent:
    """Record of an automation event."""

    timestamp: datetime
    event_type: str  # "prediction", "execution", "approval_request", etc.
    action_type: str
    confidence: float
    safety_level: str
    auto_executed: bool
    user_id: Optional[UUID]
    result: Optional[str]
    details: Dict

    def to_dict(self) -> Dict:
        """Convert event to dictionary for serialization."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


class AuditTrail:
    """
    Audit trail for automation events.

    Provides comprehensive logging of all automation activities for
    accountability, debugging, and analysis.
    """

    def __init__(self):
        self._events: List[AutomationEvent] = []

    def log_event(
        self,
        event_type: str,
        action_type: str,
        confidence: float,
        safety_level: str,
        auto_executed: bool,
        user_id: Optional[UUID] = None,
        result: Optional[str] = None,
        details: Optional[Dict] = None,
    ) -> AutomationEvent:
        """
        Log an automation event.

        Args:
            event_type: Type of event (prediction, execution, approval_request, etc.)
            action_type: Type of action being automated
            confidence: Confidence score (0-1)
            safety_level: Safety classification (SAFE, REQUIRES_CONFIRMATION, DESTRUCTIVE)
            auto_executed: Whether action was auto-executed
            user_id: Optional user ID
            result: Optional result description
            details: Optional additional details

        Returns:
            The logged AutomationEvent
        """
        event = AutomationEvent(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            action_type=action_type,
            confidence=confidence,
            safety_level=safety_level,
            auto_executed=auto_executed,
            user_id=user_id,
            result=result,
            details=details or {},
        )

        self._events.append(event)

        # Log to console for immediate visibility
        emoji = "🤖" if auto_executed else "👤"
        print(
            f"{emoji} AUTOMATION: {event_type} | {action_type} | "
            f"confidence={confidence:.2f} | safety={safety_level} | "
            f"auto={auto_executed} | result={result}"
        )

        return event

    def get_events(
        self,
        event_type: Optional[str] = None,
        user_id: Optional[UUID] = None,
        auto_executed: Optional[bool] = None,
        limit: int = 100,
    ) -> List[AutomationEvent]:
        """
        Retrieve audit events with optional filtering.

        Args:
            event_type: Filter by event type
            user_id: Filter by user ID
            auto_executed: Filter by auto-execution status
            limit: Maximum number of events to return

        Returns:
            List of matching AutomationEvents (most recent first)
        """
        events = self._events

        # Apply filters
        if event_type is not None:
            events = [e for e in events if e.event_type == event_type]

        if user_id is not None:
            events = [e for e in events if e.user_id == user_id]

        if auto_executed is not None:
            events = [e for e in events if e.auto_executed == auto_executed]

        # Sort by timestamp descending (most recent first)
        events = sorted(events, key=lambda e: e.timestamp, reverse=True)

        # Apply limit
        return events[:limit]

    def get_automation_statistics(self) -> Dict:
        """
        Get statistics about automation events.

        Returns:
            Dictionary with automation statistics
        """
        if not self._events:
            return {
                "total_events": 0,
                "auto_executed_count": 0,
                "manual_count": 0,
                "auto_execution_rate": 0.0,
                "safety_distribution": {},
                "event_type_distribution": {},
            }

        total = len(self._events)
        auto_executed = sum(1 for e in self._events if e.auto_executed)
        manual = total - auto_executed

        # Safety level distribution
        safety_dist = {}
        for event in self._events:
            safety_dist[event.safety_level] = safety_dist.get(event.safety_level, 0) + 1

        # Event type distribution
        event_type_dist = {}
        for event in self._events:
            event_type_dist[event.event_type] = event_type_dist.get(event.event_type, 0) + 1

        return {
            "total_events": total,
            "auto_executed_count": auto_executed,
            "manual_count": manual,
            "auto_execution_rate": auto_executed / total if total > 0 else 0.0,
            "safety_distribution": safety_dist,
            "event_type_distribution": event_type_dist,
        }

    def clear(self):
        """Clear all audit events (for testing only)."""
        self._events.clear()


# Global audit trail instance
_audit_trail = AuditTrail()


def get_audit_trail() -> AuditTrail:
    """Get global audit trail instance."""
    return _audit_trail
