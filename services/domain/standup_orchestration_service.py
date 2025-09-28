"""
Standup Orchestration Domain Service
Mediates standup workflow coordination following DDD principles

Created: 2025-09-12 by Code Agent Phase 1 - Layer Separation Refactoring
Addresses architectural violation: Direct integration access from application layer
"""

from datetime import datetime
from typing import Any, Dict, Optional

from services.configuration.piper_config_loader import piper_config_loader
from services.domain.user_preference_manager import UserPreferenceManager
from services.features.morning_standup import (
    MorningStandupWorkflow,
    StandupIntegrationError,
    StandupResult,
)
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.orchestration.session_persistence import SessionPersistenceManager

# Re-export exception for clean domain boundary
__all__ = ["StandupOrchestrationService", "StandupIntegrationError"]


class StandupOrchestrationService:
    """
    Domain service for standup workflow coordination

    Encapsulates integration orchestration following DDD principles:
    - Mediates between application layer and integration layer
    - Manages dependency injection for standup workflow
    - Provides clean interface for standup operations
    """

    def __init__(self):
        """Initialize orchestration service with dependency management"""
        self._preference_manager = None
        self._session_manager = None
        self._github_agent = None
        self._canonical_handlers = None

    def _initialize_dependencies(self) -> None:
        """Initialize dependencies following lazy loading pattern"""
        if self._preference_manager is None:
            self._preference_manager = UserPreferenceManager()

        if self._session_manager is None:
            self._session_manager = SessionPersistenceManager(self._preference_manager)

        if self._github_agent is None:
            self._github_agent = GitHubIntegrationRouter()

        if self._canonical_handlers is None:
            self._canonical_handlers = CanonicalHandlers()

    async def orchestrate_standup_workflow(
        self, user_id: Optional[str] = None, workflow_type: str = "standard"
    ) -> StandupResult:
        """
        Orchestrate complete standup workflow through domain layer

        Args:
            user_id: User identifier (resolved from config if not provided)
            workflow_type: Type of standup workflow to execute

        Returns:
            StandupResult containing all standup data

        Raises:
            StandupIntegrationError: When integration services fail
        """
        # Initialize dependencies
        self._initialize_dependencies()

        # Resolve user_id from configuration if not provided
        if user_id is None:
            config = piper_config_loader.load_standup_config()
            user_id = config.get("user_identity", {}).get("user_id", "default_user")

        # Create standup workflow with injected dependencies
        workflow = MorningStandupWorkflow(
            preference_manager=self._preference_manager,
            session_manager=self._session_manager,
            github_agent=self._github_agent,
            canonical_handlers=self._canonical_handlers,
        )

        # Execute workflow based on type
        if workflow_type == "with_issues":
            return await workflow.generate_with_issues(user_id)
        elif workflow_type == "with_documents":
            return await workflow.generate_with_documents(user_id)
        elif workflow_type == "with_calendar":
            return await workflow.generate_with_calendar(user_id)
        elif workflow_type == "trifecta":
            # Support complex trifecta workflow (issues + documents + calendar)
            return await workflow.generate_with_trifecta(
                user_id, with_issues=True, with_documents=True, with_calendar=True
            )
        else:
            return await workflow.generate_standup(user_id)

    async def get_standup_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get standup context without executing full workflow

        Args:
            user_id: User identifier

        Returns:
            Dictionary containing context information
        """
        self._initialize_dependencies()

        # Get session context
        session_context = await self._session_manager.get_session_context(user_id)

        # Get GitHub activity if available
        github_activity = {}
        try:
            if hasattr(self._github_agent, "get_recent_activity"):
                github_activity = await self._github_agent.get_recent_activity()
        except Exception:
            # Graceful degradation - GitHub not available
            github_activity = {"commits": [], "prs": [], "issues_closed": [], "issues_created": []}

        return {
            "user_id": user_id,
            "session_context": session_context,
            "github_activity": github_activity,
            "timestamp": datetime.now().isoformat(),
        }

    def get_supported_workflow_types(self) -> list[str]:
        """
        Get list of supported workflow types

        Returns:
            List of workflow type identifiers
        """
        return ["standard", "with_issues", "with_documents", "with_calendar", "trifecta"]
