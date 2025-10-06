"""User context service for multi-user support - GREAT-4C Phase 0."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger()


@dataclass
class UserContext:
    """User-specific context data."""

    user_id: str
    organization: Optional[str] = None
    projects: list = field(default_factory=list)
    priorities: list = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)


class UserContextService:
    """Manages user-specific context without hardcoding."""

    def __init__(self):
        self.cache = {}
        logger.info("UserContextService initialized")

    async def get_user_context(self, session_id: str) -> UserContext:
        """
        Get user context from session.

        Args:
            session_id: Session identifier

        Returns:
            UserContext with user-specific data
        """
        # Check cache first
        if session_id in self.cache:
            logger.debug("user_context_cache_hit", session_id=session_id)
            return self.cache[session_id]

        # Load from session/database
        # For now, load from PIPER.md based on session
        context = await self._load_context_from_config(session_id)

        # Cache it
        self.cache[session_id] = context
        logger.debug("user_context_cached", session_id=session_id, org=context.organization)
        return context

    async def _load_context_from_config(self, session_id: str) -> UserContext:
        """Load user context from PIPER.md configuration."""
        from services.configuration.piper_config_loader import piper_config_loader

        try:
            config = piper_config_loader.load_config()

            # Extract user context from config
            # (This is session-specific PIPER.md, not hardcoded)
            context = UserContext(
                user_id=session_id,  # TODO: Get actual user_id from session
                organization=self._extract_organization(config),
                projects=self._extract_projects(config),
                priorities=self._extract_priorities(config),
            )

            logger.info(
                "user_context_loaded",
                session_id=session_id,
                org=context.organization,
                project_count=len(context.projects),
                priority_count=len(context.priorities),
            )

            return context

        except Exception as e:
            logger.warning("user_context_load_failed", session_id=session_id, error=str(e))
            # Return empty context
            return UserContext(user_id=session_id)

    def _extract_organization(self, config: Dict) -> Optional[str]:
        """Extract organization from config."""
        # Look for organization mentions in config
        for key, value in config.items():
            if "organization" in key.lower():
                return str(value)

            # Also check for common org patterns in section content
            if isinstance(value, str):
                # Look for "Working on [Organization]" patterns
                if "working on" in value.lower() or "organization:" in value.lower():
                    # Try to extract org name
                    lines = value.split("\n")
                    for line in lines:
                        if "organization:" in line.lower():
                            org = line.split(":", 1)[1].strip()
                            return org

        return None

    def _extract_projects(self, config: Dict) -> list:
        """Extract projects from config."""
        projects = []
        for key, value in config.items():
            if "project" in key.lower() or "work" in key.lower():
                # Parse project list from config
                if isinstance(value, list):
                    projects.extend(value)
                elif isinstance(value, str):
                    # Parse from text - look for bulleted lists
                    lines = value.split("\n")
                    for line in lines:
                        stripped = line.strip()
                        # Match bullet points: -, *, •, or numbered lists
                        if stripped.startswith(("-", "*", "•")) or (
                            stripped and stripped[0].isdigit() and "." in stripped
                        ):
                            # Extract project name (remove bullet/number)
                            project = stripped.lstrip("-*•0123456789. ").strip()
                            if project:
                                projects.append(project)

        return projects

    def _extract_priorities(self, config: Dict) -> list:
        """Extract priorities from config."""
        priorities = []
        for key, value in config.items():
            if "priorit" in key.lower() or "focus" in key.lower():
                if isinstance(value, list):
                    priorities.extend(value)
                elif isinstance(value, str):
                    lines = value.split("\n")
                    for line in lines:
                        stripped = line.strip()
                        # Match bullet points or numbered lists
                        if stripped.startswith(("-", "*", "•")) or (
                            stripped and stripped[0].isdigit() and "." in stripped
                        ):
                            priority = stripped.lstrip("-*•0123456789. ").strip()
                            if priority:
                                priorities.append(priority)

        return priorities

    def invalidate_cache(self, session_id: Optional[str] = None):
        """
        Invalidate cached context.

        Args:
            session_id: Optional session to invalidate. If None, clears all cache.
        """
        if session_id:
            if session_id in self.cache:
                del self.cache[session_id]
                logger.debug("user_context_cache_invalidated", session_id=session_id)
        else:
            self.cache.clear()
            logger.debug("user_context_cache_cleared")


# Singleton instance
user_context_service = UserContextService()
