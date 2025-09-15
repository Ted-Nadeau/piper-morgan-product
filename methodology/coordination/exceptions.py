"""
Exception system for mandatory handoff protocol.

These exceptions create a no-escape system that prevents bypass of
handoff requirements and verification protocols.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class HandoffBypassError(Exception):
    """
    Critical exception preventing bypass of mandatory handoff protocol.

    This exception CANNOT be caught or bypassed - it enforces zero-bypass paths
    in the coordination system.
    """

    def __init__(
        self,
        message: str,
        handoff_context: Optional[Dict[str, Any]] = None,
        bypass_attempt_details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.handoff_context = handoff_context or {}
        self.bypass_attempt_details = bypass_attempt_details or {}
        self.is_critical = True  # Prevents catch-and-continue patterns


class HandoffValidationError(Exception):
    """
    Exception for handoff validation failures.

    Raised when handoff context or verification requirements are not met.
    """

    def __init__(
        self,
        message: str,
        validation_failures: Optional[Dict[str, Any]] = None,
        required_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.validation_failures = validation_failures or {}
        self.required_context = required_context or {}


class HandoffStateError(Exception):
    """
    Exception for invalid handoff state transitions.

    Prevents invalid state changes in the handoff lifecycle.
    """

    def __init__(
        self,
        message: str,
        current_state: Optional[str] = None,
        attempted_state: Optional[str] = None,
    ):
        super().__init__(message)
        self.current_state = current_state
        self.attempted_state = attempted_state


class HandoffEnforcementError(Exception):
    """Base exception for enforcement violations."""

    def __init__(
        self,
        message: str,
        violations: Optional[List[Dict[str, Any]]] = None,
        required_actions: Optional[List[str]] = None,
    ):
        super().__init__(message)
        self.violations = violations or []
        self.required_actions = required_actions or []
        self.timestamp = datetime.now().isoformat()


class StrictEnforcementViolation(HandoffEnforcementError):
    """STRICT level enforcement violation - blocks all progress."""

    def __init__(
        self,
        message: str,
        violations: Optional[List[Dict[str, Any]]] = None,
        required_actions: Optional[List[str]] = None,
    ):
        super().__init__(message, violations, required_actions)
        self.enforcement_level = "STRICT"
        self.blocks_progress = True


class ProgressiveEnforcementViolation(HandoffEnforcementError):
    """PROGRESSIVE level enforcement violation - escalating consequences."""

    def __init__(
        self,
        message: str,
        violations: Optional[List[Dict[str, Any]]] = None,
        required_actions: Optional[List[str]] = None,
        escalation_level: int = 1,
    ):
        super().__init__(message, violations, required_actions)
        self.escalation_level = escalation_level
        self.enforcement_level = "PROGRESSIVE"
        self.blocks_progress = escalation_level >= 3  # Block after 3 escalations


class VerificationBypassAttempt(StrictEnforcementViolation):
    """Attempt to bypass verification system detected."""

    def __init__(self, message: str, bypass_details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.bypass_details = bypass_details or {}
        self.is_security_violation = True


class EvidenceRequirementViolation(StrictEnforcementViolation):
    """Evidence requirements not met for handoff."""

    def __init__(self, message: str, missing_evidence: Optional[List[str]] = None):
        super().__init__(message)
        self.missing_evidence = missing_evidence or []


class HandoffProtocolViolation(StrictEnforcementViolation):
    """Handoff protocol requirements not followed."""

    def __init__(self, message: str, protocol_failures: Optional[List[str]] = None):
        super().__init__(message)
        self.protocol_failures = protocol_failures or []
