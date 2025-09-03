"""
Verification Module - Three-Tier Verification Pyramid

Implements systematic verification framework preventing verification theater
in agent coordination and task completion validation.

The three tiers:
1. PATTERN - Archaeological discovery of existing implementations
2. INTEGRATION - Validation of coordination requirements
3. EVIDENCE - Concrete proof requirements, no claims without evidence

This prevents agents from claiming completion without demonstrable results.
"""

from .evidence import EvidenceCollector, EvidenceType
from .patterns import PatternDiscovery
from .pyramid import VerificationLevel, VerificationPyramid, VerificationResult
from .requirements import TaskComplexity, TaskEvidenceRequirements, TaskType, ValidationReport

__all__ = [
    "VerificationPyramid",
    "VerificationLevel",
    "VerificationResult",
    "EvidenceCollector",
    "EvidenceType",
    "PatternDiscovery",
    "TaskEvidenceRequirements",
    "TaskType",
    "TaskComplexity",
    "ValidationReport",
]
