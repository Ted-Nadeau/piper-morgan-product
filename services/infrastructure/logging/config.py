"""
Centralized Logging Configuration for Piper Morgan
Supports structured logging with correlation IDs for PM-087 ethics tracking
"""

import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog
from structlog.stdlib import LoggerFactory

# Configure structlog for structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),  # JSON structured format
    ],
    context_class=dict,
    logger_factory=LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


class CorrelationContext:
    """Manages correlation IDs for request tracing"""

    def __init__(self):
        self.session_id: Optional[str] = None
        self.request_id: Optional[str] = None
        self.workflow_id: Optional[str] = None
        self.intent_id: Optional[str] = None
        self.timestamp: Optional[str] = None

    def set_session_id(self, session_id: str) -> None:
        """Set session ID for correlation"""
        self.session_id = session_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def set_request_id(self, request_id: str) -> None:
        """Set request ID for correlation"""
        self.request_id = request_id

    def set_workflow_id(self, workflow_id: str) -> None:
        """Set workflow ID for correlation"""
        self.workflow_id = workflow_id

    def set_intent_id(self, intent_id: str) -> None:
        """Set intent ID for correlation"""
        self.intent_id = intent_id

    def get_correlation_data(self) -> Dict[str, Any]:
        """Get correlation data for structured logging"""
        correlation_data = {}

        if self.session_id:
            correlation_data["session_id"] = self.session_id
        if self.request_id:
            correlation_data["request_id"] = self.request_id
        if self.workflow_id:
            correlation_data["workflow_id"] = self.workflow_id
        if self.intent_id:
            correlation_data["intent_id"] = self.intent_id
        if self.timestamp:
            correlation_data["timestamp"] = self.timestamp

        return correlation_data


class LoggerFactory:
    """Factory for creating structured loggers with correlation support"""

    @staticmethod
    def get_logger(
        name: str,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        intent_id: Optional[str] = None,
    ) -> structlog.BoundLogger:
        """
        Create a structured logger with correlation IDs

        Args:
            name: Logger name (usually __name__)
            session_id: Session ID for correlation
            request_id: Request ID for correlation
            workflow_id: Workflow ID for correlation
            intent_id: Intent ID for correlation

        Returns:
            Structured logger with correlation context
        """
        logger = structlog.get_logger(name)

        # Create correlation context
        correlation_context = CorrelationContext()

        if session_id:
            correlation_context.set_session_id(session_id)
        if request_id:
            correlation_context.set_request_id(request_id)
        if workflow_id:
            correlation_context.set_workflow_id(workflow_id)
        if intent_id:
            correlation_context.set_intent_id(intent_id)

        # Bind correlation data to logger
        correlation_data = correlation_context.get_correlation_data()
        if correlation_data:
            logger = logger.bind(**correlation_data)

        return logger


def generate_request_id() -> str:
    """Generate a unique request ID for correlation"""
    return f"req_{uuid.uuid4().hex[:8]}"


def generate_session_id() -> str:
    """Generate a unique session ID for correlation"""
    return f"sess_{uuid.uuid4().hex[:8]}"


def generate_workflow_id() -> str:
    """Generate a unique workflow ID for correlation"""
    return f"wf_{uuid.uuid4().hex[:8]}"


def generate_intent_id() -> str:
    """Generate a unique intent ID for correlation"""
    return f"int_{uuid.uuid4().hex[:8]}"


class EthicsLogger:
    """Specialized logger for PM-087 ethics behavior tracking"""

    def __init__(self, base_logger: structlog.BoundLogger):
        self.logger = base_logger

    def log_decision_point(self, decision_type: str, context: Dict[str, Any]) -> None:
        """
        Log ethics-related decision points

        Args:
            decision_type: Type of decision (e.g., "intent_processing", "boundary_check")
            context: Decision context data
        """
        self.logger.info(
            "ethics_decision_point",
            decision_type=decision_type,
            context=context,
            event_type="ethics_decision",
        )

    def log_behavior_pattern(self, pattern_type: str, metadata: Dict[str, Any]) -> None:
        """
        Log behavior patterns for analysis

        Args:
            pattern_type: Type of behavior pattern
            metadata: Pattern metadata
        """
        self.logger.info(
            "ethics_behavior_pattern",
            pattern_type=pattern_type,
            metadata=metadata,
            event_type="ethics_behavior",
        )

    def log_compliance_check(self, check_type: str, result: bool, details: Dict[str, Any]) -> None:
        """
        Log compliance verification

        Args:
            check_type: Type of compliance check
            result: Compliance result (True/False)
            details: Compliance check details
        """
        self.logger.info(
            "ethics_compliance_check",
            check_type=check_type,
            result=result,
            details=details,
            event_type="ethics_compliance",
        )

    def log_boundary_violation(self, boundary_type: str, violation_details: Dict[str, Any]) -> None:
        """
        Log ethics boundary violations

        Args:
            boundary_type: Type of boundary violated
            violation_details: Violation details
        """
        self.logger.warning(
            "ethics_boundary_violation",
            boundary_type=boundary_type,
            violation_details=violation_details,
            event_type="ethics_violation",
        )


def get_ethics_logger(
    name: str,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
    workflow_id: Optional[str] = None,
    intent_id: Optional[str] = None,
) -> EthicsLogger:
    """
    Get an ethics logger for PM-087 behavior tracking

    Args:
        name: Logger name
        session_id: Session ID for correlation
        request_id: Request ID for correlation
        workflow_id: Workflow ID for correlation
        intent_id: Intent ID for correlation

    Returns:
        Ethics logger with correlation support
    """
    base_logger = LoggerFactory.get_logger(
        name=name,
        session_id=session_id,
        request_id=request_id,
        workflow_id=workflow_id,
        intent_id=intent_id,
    )

    return EthicsLogger(base_logger)


# Convenience function for getting standard logger
def get_logger(
    name: str,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
    workflow_id: Optional[str] = None,
    intent_id: Optional[str] = None,
) -> structlog.BoundLogger:
    """
    Get a structured logger with correlation support

    Args:
        name: Logger name (usually __name__)
        session_id: Session ID for correlation
        request_id: Request ID for correlation
        workflow_id: Workflow ID for correlation
        intent_id: Intent ID for correlation

    Returns:
        Structured logger with correlation context
    """
    return LoggerFactory.get_logger(
        name=name,
        session_id=session_id,
        request_id=request_id,
        workflow_id=workflow_id,
        intent_id=intent_id,
    )
