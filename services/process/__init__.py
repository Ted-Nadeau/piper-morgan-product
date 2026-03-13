"""
Process Registry for Guided Processes.

ADR-049: Two-Tier Intent Architecture

A Guided Process is a multi-turn conversation where Piper maintains control
until completion or exit. The Process Registry tracks active processes and
checks them BEFORE intent classification.

Usage:
    from services.process import get_process_registry, ProcessType

    # Check for active processes
    registry = get_process_registry()
    result = await registry.check_active_processes(user_id, session_id, message)
    if result.handled:
        return result.response_message
"""

from services.process.adapters import (
    OnboardingProcessAdapter,
    StandupProcessAdapter,
    register_default_processes,
)
from services.process.registry import (
    ESCAPE_COMMANDS,
    GuidedProcess,
    ProcessCheckResult,
    ProcessRegistry,
    ProcessType,
    SuspendedInfo,
    get_process_registry,
)

__all__ = [
    "ESCAPE_COMMANDS",
    "GuidedProcess",
    "ProcessCheckResult",
    "ProcessRegistry",
    "ProcessType",
    "SuspendedInfo",
    "get_process_registry",
    "OnboardingProcessAdapter",
    "StandupProcessAdapter",
    "register_default_processes",
]
