"""Base class for all MCP Skills

Skills are reusable, composable workflows that handle specific tasks efficiently.
Examples: StandupWorkflowSkill, DocumentAnalysisSkill, NotionGitHubSyncSkill

Design principles:
- Minimal token usage (summarize before processing)
- Composable (can chain multiple skills)
- Clear input/output contracts
- Graceful error handling
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseSkill(ABC):
    """Abstract base class for all MCP Skills

    Subclasses should implement:
    - execute(): Main skill logic
    - validate_params(): Parameter validation
    - estimate_tokens_saved(): Token efficiency metric
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill

        Args:
            params: Skill-specific parameters

        Returns:
            dict with at least:
            {
                "success": bool,
                "message": str,
                "result": Any (skill-specific),
                "tokens_used": int (estimate),
                "tokens_saved": int (estimate)
            }
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        Validate input parameters

        Args:
            params: Parameters to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return True

    def estimate_tokens_saved(self, params: Dict[str, Any]) -> int:
        """
        Estimate tokens saved by using this skill vs full context

        Args:
            params: Parameters used for estimation

        Returns:
            int: Estimated token count saved
        """
        return 0

    async def on_error(self, error: Exception) -> Dict[str, Any]:
        """
        Handle skill execution errors with graceful degradation

        Args:
            error: The exception that occurred

        Returns:
            dict with error response and fallback if available
        """
        return {
            "success": False,
            "message": f"Skill execution failed: {str(error)}",
            "error": type(error).__name__,
        }
