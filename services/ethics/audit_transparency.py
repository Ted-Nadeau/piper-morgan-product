"""
PM-087 Audit Transparency System
User-visible audit logs with security redactions for transparency

Leverages existing infrastructure:
- services/infrastructure/monitoring/ethics_metrics.py
- services/infrastructure/logging/config.py
- services/domain/models.py patterns
"""

import hashlib
import json
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.domain.models import BoundaryViolation, EthicalDecision
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import ethics_metrics


class SecurityRedactor:
    """Security redaction for sensitive data in audit logs"""

    def __init__(self):
        # Patterns for sensitive data
        self.sensitive_patterns = [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",  # Credit card
            r"\b\d{10,11}\b",  # Phone numbers
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # URLs
        ]

        # Redaction replacement
        self.redaction_replacement = "[REDACTED]"

    def redact_sensitive_data(self, text: str) -> str:
        """Redact sensitive data from text"""
        redacted_text = text

        for pattern in self.sensitive_patterns:
            redacted_text = re.sub(pattern, self.redaction_replacement, redacted_text)

        return redacted_text

    def redact_content_preview(self, content: str, max_length: int = 100) -> str:
        """Create redacted content preview"""
        if not content:
            return ""

        # Redact sensitive data
        redacted_content = self.redact_sensitive_data(content)

        # Truncate if too long
        if len(redacted_content) > max_length:
            redacted_content = redacted_content[:max_length] + "..."

        return redacted_content


class AuditLogEntry:
    """Individual audit log entry for transparency"""

    def __init__(
        self,
        entry_id: str,
        event_type: str,
        timestamp: datetime,
        session_id: Optional[str] = None,
        user_id: Optional[UUID] = None,
        details: Dict[str, Any] = None,
        redacted: bool = True,
    ):
        self.entry_id = entry_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.session_id = session_id
        self.user_id = user_id
        self.details = details or {}
        self.redacted = redacted

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "entry_id": self.entry_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "user_id": self.user_id,
            "details": self.details,
            "redacted": self.redacted,
        }


class AuditTransparency:
    """Audit transparency system for user-visible audit logs"""

    def __init__(self):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics
        self.redactor = SecurityRedactor()

        # Audit log storage (in-memory for demo, would be database in production)
        self.audit_logs: List[AuditLogEntry] = []
        self.max_log_entries = 10000
        self.log_retention_days = 90

        # Transparency metrics
        self.transparency_requests = 0
        self.audit_log_entries_total = 0
        self.redaction_operations = 0

    async def log_ethics_decision(self, decision: EthicalDecision) -> None:
        """Log ethics decision for transparency"""
        try:
            # Create audit log entry
            entry = AuditLogEntry(
                entry_id=f"audit_{int(datetime.utcnow().timestamp())}",
                event_type="ethics_decision",
                timestamp=decision.timestamp,
                session_id=decision.session_id,
                details={
                    "boundary_type": decision.boundary_type,
                    "violation_detected": decision.violation_detected,
                    "explanation": decision.explanation,
                    "audit_data": self._redact_audit_data(decision.audit_data),
                },
            )

            # Add to audit log
            self._add_audit_entry(entry)

            # Record metrics
            self.audit_log_entries_total += 1
            self.metrics.record_audit_trail_entry(success=True)

            # Log transparency event
            self.ethics_logger.log_behavior_pattern(
                "audit_log_entry",
                {
                    "entry_id": entry.entry_id,
                    "event_type": entry.event_type,
                    "session_id": entry.session_id,
                },
            )

        except Exception as e:
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_log_error", {"error": str(e), "decision_id": decision.decision_id}
            )

    async def log_boundary_violation(self, violation: BoundaryViolation) -> None:
        """Log boundary violation for transparency"""
        try:
            # Create audit log entry
            entry = AuditLogEntry(
                entry_id=f"audit_{int(datetime.utcnow().timestamp())}",
                event_type="boundary_violation",
                timestamp=violation.timestamp,
                session_id=violation.session_id,
                details={
                    "violation_type": violation.violation_type,
                    "severity": violation.severity,
                    "context_preview": self.redactor.redact_content_preview(violation.context),
                    "audit_data": self._redact_audit_data(violation.audit_data),
                },
            )

            # Add to audit log
            self._add_audit_entry(entry)

            # Record metrics
            self.audit_log_entries_total += 1
            self.metrics.record_audit_trail_entry(success=True)

            # Log transparency event
            self.ethics_logger.log_behavior_pattern(
                "audit_log_entry",
                {
                    "entry_id": entry.entry_id,
                    "event_type": entry.event_type,
                    "session_id": entry.session_id,
                },
            )

        except Exception as e:
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_log_error", {"error": str(e), "violation_id": violation.violation_id}
            )

    async def get_user_audit_log(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's audit log entries"""
        try:
            self.transparency_requests += 1

            # Filter entries for this session
            user_entries = [entry for entry in self.audit_logs if entry.session_id == session_id]

            # Sort by timestamp (newest first)
            user_entries.sort(key=lambda x: x.timestamp, reverse=True)

            # Limit results
            user_entries = user_entries[:limit]

            # Convert to dictionary format
            audit_log = [entry.to_dict() for entry in user_entries]

            # Log transparency request
            self.ethics_logger.log_behavior_pattern(
                "transparency_request",
                {
                    "session_id": session_id,
                    "entries_returned": len(audit_log),
                    "request_limit": limit,
                },
            )

            return audit_log

        except Exception as e:
            # Log error
            self.ethics_logger.log_boundary_violation(
                "transparency_request_error", {"error": str(e), "session_id": session_id}
            )

            return []

    async def get_system_audit_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get system-wide audit summary (admin only)"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            # Filter recent entries
            recent_entries = [entry for entry in self.audit_logs if entry.timestamp >= cutoff_date]

            # Calculate summary statistics
            event_types = {}
            session_count = set()

            for entry in recent_entries:
                event_types[entry.event_type] = event_types.get(entry.event_type, 0) + 1
                if entry.session_id:
                    session_count.add(entry.session_id)

            summary = {
                "total_entries": len(recent_entries),
                "unique_sessions": len(session_count),
                "event_type_breakdown": event_types,
                "date_range": {
                    "start": cutoff_date.isoformat(),
                    "end": datetime.utcnow().isoformat(),
                },
            }

            return summary

        except Exception as e:
            # Log error
            self.ethics_logger.log_boundary_violation("audit_summary_error", {"error": str(e)})

            return {"error": "Failed to generate audit summary"}

    async def cleanup_old_entries(self) -> None:
        """Clean up old audit log entries"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.log_retention_days)

        original_count = len(self.audit_logs)
        self.audit_logs = [entry for entry in self.audit_logs if entry.timestamp >= cutoff_date]

        cleaned_count = original_count - len(self.audit_logs)

        if cleaned_count > 0:
            # Log cleanup
            self.ethics_logger.log_behavior_pattern(
                "audit_log_cleanup",
                {
                    "entries_removed": cleaned_count,
                    "entries_remaining": len(self.audit_logs),
                    "retention_days": self.log_retention_days,
                },
            )

    def _add_audit_entry(self, entry: AuditLogEntry) -> None:
        """Add audit entry with size management"""
        self.audit_logs.append(entry)

        # Maintain log size limit
        if len(self.audit_logs) > self.max_log_entries:
            # Remove oldest entries
            self.audit_logs.sort(key=lambda x: x.timestamp)
            self.audit_logs = self.audit_logs[-self.max_log_entries :]

    def _redact_audit_data(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive data from audit data"""
        if not audit_data:
            return {}

        redacted_data = {}

        for key, value in audit_data.items():
            if isinstance(value, str):
                # Redact sensitive strings
                redacted_data[key] = self.redactor.redact_sensitive_data(value)
            elif isinstance(value, dict):
                # Recursively redact nested dictionaries
                redacted_data[key] = self._redact_audit_data(value)
            else:
                # Keep non-string values as-is
                redacted_data[key] = value

        self.redaction_operations += 1
        return redacted_data

    def get_transparency_stats(self) -> Dict[str, Any]:
        """Get transparency system statistics"""
        return {
            "total_audit_entries": len(self.audit_logs),
            "transparency_requests": self.transparency_requests,
            "audit_log_entries_total": self.audit_log_entries_total,
            "redaction_operations": self.redaction_operations,
            "max_log_entries": self.max_log_entries,
            "log_retention_days": self.log_retention_days,
            "recent_entries_24h": len(
                [
                    entry
                    for entry in self.audit_logs
                    if entry.timestamp >= datetime.utcnow() - timedelta(days=1)
                ]
            ),
        }


# Singleton instance
audit_transparency = AuditTransparency()
