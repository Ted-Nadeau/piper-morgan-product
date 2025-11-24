"""Central registry for all executable actions"""

from typing import Any, Dict, Type

from .commands.base_command import BaseCommand
from .commands.github_issue_command import GithubIssueCommand


class ActionRegistry:
    """Registry mapping action types to command classes"""

    # Low-risk actions (for alpha, all require user approval)
    _actions: Dict[str, Type[BaseCommand]] = {
        "create_github_issue": GithubIssueCommand,
        # "update_notion": NotionUpdateCommand,  # Add when ready
        # "search_slack": SlackSearchCommand,    # Add when ready
    }

    @classmethod
    async def execute(
        cls, action_type: str, params: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an action via its command

        Args:
            action_type: Type of action (e.g., "create_github_issue")
            params: Action parameters from pattern
            context: Execution context (user_id, session, etc.)

        Returns:
            dict: Execution result

        Raises:
            ValueError: If action type not registered
        """
        command_class = cls._actions.get(action_type)

        if not command_class:
            available = ", ".join(cls._actions.keys())
            raise ValueError(f"Unknown action type: {action_type}. " f"Available: {available}")

        # Create command instance
        command = command_class(params, context)

        # Validate parameters
        command.validate_params()

        # Execute
        result = await command.execute()

        return result

    @classmethod
    def is_registered(cls, action_type: str) -> bool:
        """Check if action type is registered"""
        return action_type in cls._actions

    @classmethod
    def list_actions(cls) -> list[str]:
        """List all registered action types"""
        return list(cls._actions.keys())
