"""
Coordination module for mandatory handoff protocols.

This module implements zero-bypass handoff enforcement between agents,
ensuring systematic verification and evidence-based progress tracking.
"""

from .enforcement import EnforcementLevel, EnforcementPatterns, VerificationRequired
from .exceptions import (
    EvidenceRequirementViolation,
    HandoffBypassError,
    HandoffProtocolViolation,
    HandoffValidationError,
    StrictEnforcementViolation,
)
from .handoff import HandoffContext, HandoffResult, MandatoryHandoffProtocol

__all__ = [
    "MandatoryHandoffProtocol",
    "HandoffContext",
    "HandoffResult",
    "HandoffBypassError",
    "HandoffValidationError",
    "StrictEnforcementViolation",
    "EvidenceRequirementViolation",
    "HandoffProtocolViolation",
    "EnforcementPatterns",
    "EnforcementLevel",
    "VerificationRequired",
]
