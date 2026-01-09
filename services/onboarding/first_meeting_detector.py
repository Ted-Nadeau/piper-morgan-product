"""
First Meeting Detector for Portfolio Onboarding.

Issue #490: FTUX-PORTFOLIO
Phase 1: Detect when user has no projects and should be offered onboarding.

This detector checks if a user should be prompted to set up their project portfolio
based on:
1. Having zero active projects
2. Not having previously declined onboarding
"""

import logging
from typing import Optional

from services.database.repositories import ProjectRepository

logger = logging.getLogger(__name__)


class FirstMeetingDetector:
    """
    Detects when a user should be offered portfolio onboarding.

    A user should be offered onboarding when:
    - They have zero active projects
    - They have not previously declined onboarding

    Usage:
        detector = FirstMeetingDetector(project_repository)
        if await detector.should_trigger(user_id):
            # Start portfolio onboarding flow
    """

    def __init__(
        self,
        project_repository: ProjectRepository,
        user_preferences: Optional[dict] = None,
    ):
        """
        Initialize the detector.

        Args:
            project_repository: Repository for querying user projects
            user_preferences: Optional dict containing user preferences
                              (including 'portfolio_onboarding_declined' flag)
        """
        self.project_repository = project_repository
        self.user_preferences = user_preferences or {}

    async def should_trigger(self, user_id: str) -> bool:
        """
        Check if portfolio onboarding should be triggered for this user.

        Args:
            user_id: The user's ID

        Returns:
            True if onboarding should be triggered, False otherwise
        """
        # Check if user has declined onboarding
        if self._has_declined_onboarding(user_id):
            logger.debug(f"User {user_id} previously declined portfolio onboarding")
            return False

        # Check if user has any active projects
        try:
            project_count = await self._count_user_projects(user_id)
            should_trigger = project_count == 0

            if should_trigger:
                logger.info(f"User {user_id} has no projects - triggering onboarding")
            else:
                logger.debug(f"User {user_id} has {project_count} projects - skipping onboarding")

            return should_trigger

        except Exception as e:
            # On error, fail safe - don't trigger onboarding
            logger.error(f"Error checking projects for user {user_id}: {e}")
            return False

    async def _count_user_projects(self, user_id: str) -> int:
        """
        Count active projects for a user.

        Args:
            user_id: The user's ID

        Returns:
            Number of active projects
        """
        return await self.project_repository.count_active_projects(owner_id=user_id)

    def _has_declined_onboarding(self, user_id: str) -> bool:
        """
        Check if user has previously declined portfolio onboarding.

        Args:
            user_id: The user's ID

        Returns:
            True if user has declined, False otherwise
        """
        # Check user preferences for decline flag
        # This can be stored in user preferences or a dedicated table
        declined = self.user_preferences.get("portfolio_onboarding_declined", False)
        return bool(declined)

    def mark_declined(self, user_id: str) -> None:
        """
        Mark that a user has declined portfolio onboarding.

        Args:
            user_id: The user's ID

        Note:
            In a full implementation, this would persist to database.
            For MVP, we update the in-memory preferences.
        """
        self.user_preferences["portfolio_onboarding_declined"] = True
        logger.info(f"User {user_id} declined portfolio onboarding")
