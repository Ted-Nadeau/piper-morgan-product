"""Base command for all executable actions"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseCommand(ABC):
    """Abstract base class for action commands"""

    def __init__(self, params: Dict[str, Any], context: Dict[str, Any]):
        """
        Initialize command with parameters and context

        Args:
            params: Action-specific parameters (from pattern_data)
            context: Current execution context (user_id, session, etc.)
        """
        self.params = params
        self.context = context

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the action

        Returns:
            dict: Result with at least {"status": "success"|"error", ...}
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def validate_params(self) -> None:
        """Validate required parameters (override if needed)"""
        pass

    async def rollback(self) -> None:
        """Rollback/undo action (future - not implemented in alpha)"""
        raise NotImplementedError("Rollback not implemented in alpha")
