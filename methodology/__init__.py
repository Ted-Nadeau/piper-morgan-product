"""
Piper Morgan Methodological Architecture

This module implements systematic methodologies for AI agent coordination,
focusing on verification-first approaches and evidence-based validation.

Core Principles:
- Verification before implementation
- Evidence requirements prevent theater
- Pattern discovery before rebuilding
- Integration validation prevents failures

Components:
- verification: Three-tier verification pyramid
- circuit_breakers: Future coordination safety mechanisms
- communication: Future agent communication protocols
- recovery: Future error recovery and learning systems
"""

__version__ = "0.1.0"
__author__ = "Piper Morgan Development Team"

from .verification.pyramid import VerificationLevel, VerificationPyramid, VerificationResult

__all__ = ["VerificationPyramid", "VerificationLevel", "VerificationResult"]
