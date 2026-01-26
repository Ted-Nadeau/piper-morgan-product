"""
Process Registry for Guided Processes.

ADR-049: Two-Tier Intent Architecture

A Guided Process is a multi-turn conversation where Piper maintains control
until completion or exit. Examples: onboarding, standup, planning, feedback.

The Process Registry tracks active guided processes per session and checks
them BEFORE intent classification to prevent derailment.

Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
Issue #687: ADR-049 Implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable

import structlog

logger = structlog.get_logger(__name__)


class ProcessType(str, Enum):
    """
    Types of guided processes.

    Current (MVP):
    - ONBOARDING: Portfolio setup for new users
    - STANDUP: Interactive standup creation

    Future (Advanced Layer):
    - PLANNING: Structured planning sessions
    - FEEDBACK: User feedback collection
    - CLARIFICATION: Pending question resolution
    """

    ONBOARDING = "onboarding"
    STANDUP = "standup"
    # Future types (Advanced Layer - see #698, #699, #700)
    PLANNING = "planning"
    FEEDBACK = "feedback"
    CLARIFICATION = "clarification"


@dataclass
class ProcessCheckResult:
    """
    Result of checking for an active guided process.

    If handled is True, the message was handled by a guided process
    and classification should be bypassed.
    """

    handled: bool
    process_type: Optional[ProcessType] = None
    response_message: Optional[str] = None
    intent_data: Optional[Dict[str, Any]] = None

    @classmethod
    def not_handled(cls) -> "ProcessCheckResult":
        """No active process claimed the message."""
        return cls(handled=False)

    @classmethod
    def handled_by(
        cls,
        process_type: ProcessType,
        response_message: str,
        intent_data: Dict[str, Any],
    ) -> "ProcessCheckResult":
        """Message was handled by a guided process."""
        return cls(
            handled=True,
            process_type=process_type,
            response_message=response_message,
            intent_data=intent_data,
        )


@runtime_checkable
class GuidedProcess(Protocol):
    """
    Protocol for guided process handlers.

    Each guided process type implements this protocol to integrate
    with the process registry.
    """

    @property
    def process_type(self) -> ProcessType:
        """The type of this guided process."""
        ...

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """
        Check if there's an active session for this user/session.

        Returns True if an active (non-terminal) session exists.
        """
        ...

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """
        Handle a message in the context of an active session.

        Only called if check_active returned True.
        Returns ProcessCheckResult with handled=True and response.
        """
        ...


class ProcessRegistry:
    """
    Registry of guided process handlers.

    Maintains the list of registered processes and checks them in
    priority order when processing a message.

    Design principle: Check processes in a defined priority order.
    First match wins. If no process claims the message, proceed
    with normal intent classification.
    """

    # Singleton instance
    _instance: Optional["ProcessRegistry"] = None

    def __init__(self):
        # Process handlers in priority order
        self._handlers: List[GuidedProcess] = []
        # Priority order for checking (lower = higher priority)
        self._priority_order: Dict[ProcessType, int] = {
            ProcessType.ONBOARDING: 10,  # Highest priority
            ProcessType.STANDUP: 20,
            ProcessType.CLARIFICATION: 30,
            ProcessType.PLANNING: 40,
            ProcessType.FEEDBACK: 50,
        }
        logger.info("ProcessRegistry initialized")

    @classmethod
    def get_instance(cls) -> "ProcessRegistry":
        """Get singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None

    def register(self, handler: GuidedProcess) -> None:
        """
        Register a guided process handler.

        Handlers are automatically sorted by priority order.
        """
        if not isinstance(handler, GuidedProcess):
            raise TypeError(f"Handler must implement GuidedProcess protocol: {handler}")

        # Check for duplicate registration
        for existing in self._handlers:
            if existing.process_type == handler.process_type:
                logger.warning(
                    "Replacing existing handler for process type",
                    process_type=handler.process_type.value,
                )
                self._handlers.remove(existing)
                break

        self._handlers.append(handler)

        # Sort by priority
        self._handlers.sort(key=lambda h: self._priority_order.get(h.process_type, 100))

        logger.info(
            "Registered guided process handler",
            process_type=handler.process_type.value,
            priority=self._priority_order.get(handler.process_type, 100),
        )

    def unregister(self, process_type: ProcessType) -> bool:
        """
        Unregister a handler by process type.

        Returns True if a handler was removed.
        """
        for handler in self._handlers:
            if handler.process_type == process_type:
                self._handlers.remove(handler)
                logger.info(
                    "Unregistered guided process handler",
                    process_type=process_type.value,
                )
                return True
        return False

    async def check_active_processes(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """
        Check all registered processes for an active session.

        Checks in priority order. First process that has an active
        session and can handle the message wins.

        Args:
            user_id: Authenticated user ID (may be None)
            session_id: Session identifier
            message: User's message

        Returns:
            ProcessCheckResult - handled=True if a process claimed the message
        """
        for handler in self._handlers:
            try:
                # First check if there's an active session
                is_active = await handler.check_active(user_id, session_id)

                if is_active:
                    logger.debug(
                        "Found active guided process",
                        process_type=handler.process_type.value,
                        user_id=user_id,
                        session_id=session_id,
                    )

                    # Let the handler process the message
                    result = await handler.handle_message(user_id, session_id, message)

                    if result.handled:
                        logger.info(
                            "Message handled by guided process",
                            process_type=handler.process_type.value,
                            user_id=user_id,
                            session_id=session_id,
                        )
                        return result

            except Exception as e:
                logger.warning(
                    "Error checking guided process",
                    process_type=handler.process_type.value,
                    error=str(e),
                )
                # Continue to next handler
                continue

        return ProcessCheckResult.not_handled()

    @property
    def registered_types(self) -> List[ProcessType]:
        """List of currently registered process types."""
        return [h.process_type for h in self._handlers]


# Convenience function for getting the singleton
def get_process_registry() -> ProcessRegistry:
    """Get the singleton process registry instance."""
    return ProcessRegistry.get_instance()
