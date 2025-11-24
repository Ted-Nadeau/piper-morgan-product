"""
API Key Audit Service

Provides comprehensive auditing of API key usage and access, including:
- Usage tracking and analytics
- Access pattern analysis
- Security event monitoring
- Compliance reporting
- Anomaly detection

Issue #253 CORE-KEYS-AUDIT
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4

import structlog

from services.infrastructure.keychain_service import KeychainService
from services.security.audit_logger import Action, audit_logger

logger = structlog.get_logger()


class AuditEventType(Enum):
    """Types of audit events"""

    KEY_ACCESS = "key_access"
    KEY_USAGE = "key_usage"
    KEY_CREATION = "key_creation"
    KEY_DELETION = "key_deletion"
    KEY_ROTATION = "key_rotation"
    KEY_VALIDATION = "key_validation"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    COMPLIANCE_VIOLATION = "compliance_violation"


class RiskLevel(Enum):
    """Risk levels for audit events"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Individual audit event"""

    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    provider: str
    key_hash: str  # SHA256 hash of key for tracking
    user_id: Optional[UUID]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    action: str
    resource: Optional[str]
    risk_level: RiskLevel
    details: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageMetrics:
    """Usage metrics for a key or provider"""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    unique_users: Set[str] = field(default_factory=set)
    unique_sessions: Set[str] = field(default_factory=set)
    unique_ips: Set[str] = field(default_factory=set)
    first_used: Optional[datetime] = None
    last_used: Optional[datetime] = None
    avg_requests_per_hour: float = 0.0
    peak_requests_per_hour: int = 0
    error_rate: float = 0.0


@dataclass
class SecurityAlert:
    """Security alert for suspicious activity"""

    alert_id: str
    alert_type: str
    risk_level: RiskLevel
    timestamp: datetime
    provider: str
    key_hash: str
    description: str
    evidence: List[AuditEvent]
    recommended_actions: List[str]
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


@dataclass
class ComplianceReport:
    """Compliance report for audit requirements"""

    report_id: str
    report_type: str
    period_start: datetime
    period_end: datetime
    generated_at: datetime
    total_events: int
    high_risk_events: int
    compliance_violations: int
    key_rotations: int
    unauthorized_attempts: int
    summary: Dict[str, Any]
    recommendations: List[str]


class KeyAuditService:
    """Service for comprehensive API key auditing"""

    def __init__(self, keychain_service: Optional[KeychainService] = None):
        self.keychain = keychain_service or KeychainService()

        # Event storage (in production, would use database)
        self.audit_events: List[AuditEvent] = []
        self.security_alerts: List[SecurityAlert] = []
        self.compliance_reports: List[ComplianceReport] = []

        # Usage tracking
        self.usage_metrics: Dict[str, UsageMetrics] = {}  # key_hash -> metrics
        self.provider_metrics: Dict[str, UsageMetrics] = {}  # provider -> metrics

        # Anomaly detection thresholds
        self.anomaly_thresholds = {
            "requests_per_hour_multiplier": 5.0,  # Alert if 5x normal rate
            "error_rate_threshold": 0.2,  # Alert if >20% error rate
            "unique_ips_threshold": 10,  # Alert if >10 unique IPs per hour
            "failed_attempts_threshold": 5,  # Alert after 5 failed attempts
        }

        # Compliance requirements
        self.compliance_rules = {
            "max_key_age_days": 90,  # Keys should be rotated every 90 days
            "min_rotation_frequency_days": 30,  # Minimum rotation frequency
            "required_audit_retention_days": 365,  # Keep audit logs for 1 year
            "max_failed_attempts": 3,  # Max failed attempts before alert
        }

    async def log_key_access(
        self,
        provider: str,
        key_hash: str,
        action: str,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log API key access event"""

        event = AuditEvent(
            event_id=str(uuid4()),
            event_type=AuditEventType.KEY_ACCESS,
            timestamp=datetime.now(),
            provider=provider,
            key_hash=key_hash,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            action=action,
            resource=resource,
            risk_level=RiskLevel.LOW if success else RiskLevel.MEDIUM,
            details=details or {},
            metadata={"success": success},
        )

        self.audit_events.append(event)

        # Update usage metrics
        await self._update_usage_metrics(event)

        # Check for anomalies
        await self._check_for_anomalies(event)

        # Log to audit system
        audit_logger.log_action(
            Action.API_KEY_ACCESS,
            user_id=user_id,
            details={
                "provider": provider,
                "key_hash": key_hash,
                "action": action,
                "success": success,
                "ip_address": ip_address,
            },
        )

        logger.info(
            "key_access_logged",
            event_id=event.event_id,
            provider=provider,
            key_hash=key_hash,
            action=action,
            success=success,
            user_id=user_id,
        )

        return event.event_id

    async def log_key_usage(
        self,
        provider: str,
        key_hash: str,
        operation: str,
        tokens_used: Optional[int] = None,
        cost: Optional[float] = None,
        response_time_ms: Optional[float] = None,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ) -> str:
        """Log API key usage event"""

        event = AuditEvent(
            event_id=str(uuid4()),
            event_type=AuditEventType.KEY_USAGE,
            timestamp=datetime.now(),
            provider=provider,
            key_hash=key_hash,
            user_id=user_id,
            session_id=session_id,
            ip_address=None,
            user_agent=None,
            action=operation,
            resource=None,
            risk_level=RiskLevel.LOW,
            details={
                "tokens_used": tokens_used,
                "cost": cost,
                "response_time_ms": response_time_ms,
                "error_message": error_message,
            },
            metadata={"success": success},
        )

        self.audit_events.append(event)

        # Update usage metrics
        await self._update_usage_metrics(event)

        logger.debug(
            "key_usage_logged",
            event_id=event.event_id,
            provider=provider,
            operation=operation,
            success=success,
            tokens_used=tokens_used,
        )

        return event.event_id

    async def log_security_event(
        self,
        event_type: AuditEventType,
        provider: str,
        key_hash: str,
        description: str,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        user_id: Optional[UUID] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log security-related event"""

        event = AuditEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            timestamp=datetime.now(),
            provider=provider,
            key_hash=key_hash,
            user_id=user_id,
            session_id=None,
            ip_address=ip_address,
            user_agent=None,
            action=description,
            resource=None,
            risk_level=risk_level,
            details=details or {},
        )

        self.audit_events.append(event)

        # Create security alert for high/critical risk events
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            await self._create_security_alert(event)

        logger.warning(
            "security_event_logged",
            event_id=event.event_id,
            event_type=event_type.value,
            provider=provider,
            risk_level=risk_level.value,
            description=description,
        )

        return event.event_id

    async def _update_usage_metrics(self, event: AuditEvent) -> None:
        """Update usage metrics for key and provider"""

        # Update key-specific metrics
        if event.key_hash not in self.usage_metrics:
            self.usage_metrics[event.key_hash] = UsageMetrics()

        key_metrics = self.usage_metrics[event.key_hash]
        key_metrics.total_requests += 1

        if event.metadata.get("success", True):
            key_metrics.successful_requests += 1
        else:
            key_metrics.failed_requests += 1

        if event.user_id:
            key_metrics.unique_users.add(event.user_id)
        if event.session_id:
            key_metrics.unique_sessions.add(event.session_id)
        if event.ip_address:
            key_metrics.unique_ips.add(event.ip_address)

        if key_metrics.first_used is None:
            key_metrics.first_used = event.timestamp
        key_metrics.last_used = event.timestamp

        # Calculate error rate
        if key_metrics.total_requests > 0:
            key_metrics.error_rate = key_metrics.failed_requests / key_metrics.total_requests

        # Update provider-specific metrics
        if event.provider not in self.provider_metrics:
            self.provider_metrics[event.provider] = UsageMetrics()

        provider_metrics = self.provider_metrics[event.provider]
        provider_metrics.total_requests += 1

        if event.metadata.get("success", True):
            provider_metrics.successful_requests += 1
        else:
            provider_metrics.failed_requests += 1

        if event.user_id:
            provider_metrics.unique_users.add(event.user_id)
        if event.session_id:
            provider_metrics.unique_sessions.add(event.session_id)
        if event.ip_address:
            provider_metrics.unique_ips.add(event.ip_address)

        if provider_metrics.first_used is None:
            provider_metrics.first_used = event.timestamp
        provider_metrics.last_used = event.timestamp

        if provider_metrics.total_requests > 0:
            provider_metrics.error_rate = (
                provider_metrics.failed_requests / provider_metrics.total_requests
            )

    async def _check_for_anomalies(self, event: AuditEvent) -> None:
        """Check for anomalous patterns in usage"""

        # Check for high error rate
        key_metrics = self.usage_metrics.get(event.key_hash)
        if key_metrics and key_metrics.error_rate > self.anomaly_thresholds["error_rate_threshold"]:
            await self.log_security_event(
                AuditEventType.SUSPICIOUS_ACTIVITY,
                event.provider,
                event.key_hash,
                f"High error rate detected: {key_metrics.error_rate:.2%}",
                RiskLevel.HIGH,
                event.user_id,
                event.ip_address,
                {
                    "error_rate": key_metrics.error_rate,
                    "total_requests": key_metrics.total_requests,
                },
            )

        # Check for too many unique IPs
        if (
            key_metrics
            and len(key_metrics.unique_ips) > self.anomaly_thresholds["unique_ips_threshold"]
        ):
            await self.log_security_event(
                AuditEventType.SUSPICIOUS_ACTIVITY,
                event.provider,
                event.key_hash,
                f"Unusual number of unique IP addresses: {len(key_metrics.unique_ips)}",
                RiskLevel.MEDIUM,
                event.user_id,
                event.ip_address,
                {"unique_ips": len(key_metrics.unique_ips)},
            )

        # Check for rapid successive failures
        recent_events = [
            e
            for e in self.audit_events
            if e.key_hash == event.key_hash
            and e.timestamp > datetime.now() - timedelta(minutes=5)
            and not e.metadata.get("success", True)
        ]

        if len(recent_events) >= self.anomaly_thresholds["failed_attempts_threshold"]:
            await self.log_security_event(
                AuditEventType.SUSPICIOUS_ACTIVITY,
                event.provider,
                event.key_hash,
                f"Multiple failed attempts: {len(recent_events)} in 5 minutes",
                RiskLevel.HIGH,
                event.user_id,
                event.ip_address,
                {"failed_attempts": len(recent_events)},
            )

    async def _create_security_alert(self, event: AuditEvent) -> None:
        """Create security alert for high-risk events"""

        # Find related events
        related_events = [
            e
            for e in self.audit_events
            if e.key_hash == event.key_hash and e.timestamp > datetime.now() - timedelta(hours=1)
        ]

        # Determine recommended actions
        recommendations = []
        if event.event_type == AuditEventType.SUSPICIOUS_ACTIVITY:
            recommendations.extend(
                [
                    "Review recent API key usage patterns",
                    "Consider rotating the API key",
                    "Investigate source IP addresses",
                    "Check for unauthorized access",
                ]
            )
        elif event.event_type == AuditEventType.UNAUTHORIZED_ACCESS:
            recommendations.extend(
                [
                    "Immediately rotate the API key",
                    "Review access logs",
                    "Check for data breaches",
                    "Update security policies",
                ]
            )

        alert = SecurityAlert(
            alert_id=str(uuid4()),
            alert_type=event.event_type.value,
            risk_level=event.risk_level,
            timestamp=event.timestamp,
            provider=event.provider,
            key_hash=event.key_hash,
            description=event.action,
            evidence=related_events,
            recommended_actions=recommendations,
        )

        self.security_alerts.append(alert)

        logger.warning(
            "security_alert_created",
            alert_id=alert.alert_id,
            alert_type=alert.alert_type,
            risk_level=alert.risk_level.value,
            provider=event.provider,
        )

    async def generate_usage_report(
        self,
        provider: Optional[str] = None,
        key_hash: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Generate usage report for keys or providers"""

        end_date = end_date or datetime.now()
        start_date = start_date or (end_date - timedelta(days=30))

        # Filter events
        filtered_events = [
            event
            for event in self.audit_events
            if start_date <= event.timestamp <= end_date
            and (provider is None or event.provider == provider)
            and (key_hash is None or event.key_hash == key_hash)
        ]

        # Calculate metrics
        total_events = len(filtered_events)
        usage_events = [e for e in filtered_events if e.event_type == AuditEventType.KEY_USAGE]
        access_events = [e for e in filtered_events if e.event_type == AuditEventType.KEY_ACCESS]

        successful_requests = len([e for e in filtered_events if e.metadata.get("success", True)])
        failed_requests = total_events - successful_requests

        unique_users = set(e.user_id for e in filtered_events if e.user_id)
        unique_sessions = set(e.session_id for e in filtered_events if e.session_id)
        unique_ips = set(e.ip_address for e in filtered_events if e.ip_address)

        # Calculate costs and tokens
        total_tokens = sum(
            e.details.get("tokens_used", 0) for e in usage_events if e.details.get("tokens_used")
        )
        total_cost = sum(e.details.get("cost", 0.0) for e in usage_events if e.details.get("cost"))

        # Calculate average response time
        response_times = [
            e.details.get("response_time_ms", 0)
            for e in usage_events
            if e.details.get("response_time_ms")
        ]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        report = {
            "report_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "duration_days": (end_date - start_date).days,
            },
            "filters": {"provider": provider, "key_hash": key_hash},
            "summary": {
                "total_events": total_events,
                "usage_events": len(usage_events),
                "access_events": len(access_events),
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": successful_requests / total_events if total_events > 0 else 0,
                "unique_users": len(unique_users),
                "unique_sessions": len(unique_sessions),
                "unique_ips": len(unique_ips),
            },
            "usage_metrics": {
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "avg_response_time_ms": avg_response_time,
                "requests_per_day": total_events / max((end_date - start_date).days, 1),
            },
            "top_users": self._get_top_users(filtered_events),
            "top_operations": self._get_top_operations(filtered_events),
            "hourly_distribution": self._get_hourly_distribution(filtered_events),
            "error_analysis": self._analyze_errors(filtered_events),
        }

        return report

    def _get_top_users(self, events: List[AuditEvent], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by request count"""
        user_counts = {}
        for event in events:
            if event.user_id:
                user_counts[event.user_id] = user_counts.get(event.user_id, 0) + 1

        return [
            {"user_id": user_id, "request_count": count}
            for user_id, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[
                :limit
            ]
        ]

    def _get_top_operations(
        self, events: List[AuditEvent], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top operations by frequency"""
        operation_counts = {}
        for event in events:
            if event.action:
                operation_counts[event.action] = operation_counts.get(event.action, 0) + 1

        return [
            {"operation": operation, "count": count}
            for operation, count in sorted(
                operation_counts.items(), key=lambda x: x[1], reverse=True
            )[:limit]
        ]

    def _get_hourly_distribution(self, events: List[AuditEvent]) -> Dict[int, int]:
        """Get hourly distribution of requests"""
        hourly_counts = {hour: 0 for hour in range(24)}
        for event in events:
            hour = event.timestamp.hour
            hourly_counts[hour] += 1
        return hourly_counts

    def _analyze_errors(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Analyze error patterns"""
        failed_events = [e for e in events if not e.metadata.get("success", True)]

        error_types = {}
        for event in failed_events:
            error_msg = event.details.get("error_message", "Unknown error")
            error_types[error_msg] = error_types.get(error_msg, 0) + 1

        return {
            "total_errors": len(failed_events),
            "error_rate": len(failed_events) / len(events) if events else 0,
            "error_types": dict(sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:10]),
        }

    async def generate_compliance_report(
        self,
        report_type: str = "monthly",
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
    ) -> ComplianceReport:
        """Generate compliance report"""

        period_end = period_end or datetime.now()
        if period_start is None:
            if report_type == "daily":
                period_start = period_end - timedelta(days=1)
            elif report_type == "weekly":
                period_start = period_end - timedelta(days=7)
            elif report_type == "monthly":
                period_start = period_end - timedelta(days=30)
            else:
                period_start = period_end - timedelta(days=30)

        # Filter events for period
        period_events = [
            event for event in self.audit_events if period_start <= event.timestamp <= period_end
        ]

        # Count different event types
        high_risk_events = len(
            [e for e in period_events if e.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        )
        compliance_violations = len(
            [e for e in period_events if e.event_type == AuditEventType.COMPLIANCE_VIOLATION]
        )
        key_rotations = len(
            [e for e in period_events if e.event_type == AuditEventType.KEY_ROTATION]
        )
        unauthorized_attempts = len(
            [e for e in period_events if e.event_type == AuditEventType.UNAUTHORIZED_ACCESS]
        )

        # Generate recommendations
        recommendations = []
        if high_risk_events > 0:
            recommendations.append(f"Review {high_risk_events} high-risk security events")
        if compliance_violations > 0:
            recommendations.append(f"Address {compliance_violations} compliance violations")
        if key_rotations == 0:
            recommendations.append(
                "No key rotations detected - consider implementing regular rotation"
            )
        if unauthorized_attempts > 0:
            recommendations.append(
                f"Investigate {unauthorized_attempts} unauthorized access attempts"
            )

        report = ComplianceReport(
            report_id=str(uuid4()),
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            generated_at=datetime.now(),
            total_events=len(period_events),
            high_risk_events=high_risk_events,
            compliance_violations=compliance_violations,
            key_rotations=key_rotations,
            unauthorized_attempts=unauthorized_attempts,
            summary={
                "providers_active": len(set(e.provider for e in period_events)),
                "unique_keys": len(set(e.key_hash for e in period_events)),
                "unique_users": len(set(e.user_id for e in period_events if e.user_id)),
                "avg_events_per_day": len(period_events) / max((period_end - period_start).days, 1),
            },
            recommendations=recommendations,
        )

        self.compliance_reports.append(report)

        logger.info(
            "compliance_report_generated",
            report_id=report.report_id,
            report_type=report_type,
            total_events=report.total_events,
            high_risk_events=high_risk_events,
        )

        return report

    def get_security_alerts(
        self, unresolved_only: bool = True, risk_level: Optional[RiskLevel] = None, limit: int = 50
    ) -> List[SecurityAlert]:
        """Get security alerts"""

        alerts = self.security_alerts

        if unresolved_only:
            alerts = [a for a in alerts if not a.is_resolved]

        if risk_level:
            alerts = [a for a in alerts if a.risk_level == risk_level]

        # Sort by timestamp (newest first)
        alerts = sorted(alerts, key=lambda a: a.timestamp, reverse=True)

        return alerts[:limit]

    async def resolve_security_alert(
        self, alert_id: str, resolved_by: str, resolution_notes: Optional[str] = None
    ) -> bool:
        """Resolve a security alert"""

        for alert in self.security_alerts:
            if alert.alert_id == alert_id:
                alert.is_resolved = True
                alert.resolved_at = datetime.now()
                alert.resolved_by = resolved_by

                if resolution_notes:
                    alert.recommended_actions.append(f"Resolution: {resolution_notes}")

                logger.info(
                    "security_alert_resolved",
                    alert_id=alert_id,
                    resolved_by=resolved_by,
                    alert_type=alert.alert_type,
                )

                return True

        return False

    def get_audit_events(
        self,
        provider: Optional[str] = None,
        key_hash: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000,
    ) -> List[AuditEvent]:
        """Get audit events with filtering"""

        events = self.audit_events

        if provider:
            events = [e for e in events if e.provider == provider]

        if key_hash:
            events = [e for e in events if e.key_hash == key_hash]

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        if start_date:
            events = [e for e in events if e.timestamp >= start_date]

        if end_date:
            events = [e for e in events if e.timestamp <= end_date]

        # Sort by timestamp (newest first)
        events = sorted(events, key=lambda e: e.timestamp, reverse=True)

        return events[:limit]

    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get overall audit statistics"""

        now = datetime.now()
        last_24h = now - timedelta(days=1)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)

        events_24h = [e for e in self.audit_events if e.timestamp >= last_24h]
        events_7d = [e for e in self.audit_events if e.timestamp >= last_7d]
        events_30d = [e for e in self.audit_events if e.timestamp >= last_30d]

        return {
            "total_events": len(self.audit_events),
            "events_last_24h": len(events_24h),
            "events_last_7d": len(events_7d),
            "events_last_30d": len(events_30d),
            "active_providers": len(set(e.provider for e in self.audit_events)),
            "tracked_keys": len(self.usage_metrics),
            "security_alerts": {
                "total": len(self.security_alerts),
                "unresolved": len([a for a in self.security_alerts if not a.is_resolved]),
                "critical": len(
                    [a for a in self.security_alerts if a.risk_level == RiskLevel.CRITICAL]
                ),
                "high": len([a for a in self.security_alerts if a.risk_level == RiskLevel.HIGH]),
            },
            "compliance_reports": len(self.compliance_reports),
        }


# Global instance for easy access
key_audit_service = KeyAuditService()


# Convenience functions
async def log_key_access(
    provider: str,
    key_hash: str,
    action: str,
    user_id: Optional[UUID] = None,
    success: bool = True,
    **kwargs,
) -> str:
    """Convenience function to log key access"""
    return await key_audit_service.log_key_access(
        provider, key_hash, action, user_id=user_id, success=success, **kwargs
    )


async def log_key_usage(
    provider: str, key_hash: str, operation: str, success: bool = True, **kwargs
) -> str:
    """Convenience function to log key usage"""
    return await key_audit_service.log_key_usage(
        provider, key_hash, operation, success=success, **kwargs
    )
