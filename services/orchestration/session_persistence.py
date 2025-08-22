"""
Session Persistence Manager - Context Inheritance & Database Integration
Phase 2: Session Context Persistence Implementation

Created: 2025-08-20 by Enhanced Autonomy Mission
Integrates UserPreferenceManager with session persistence and context inheritance
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.domain.user_preference_manager import UserPreferenceManager
from services.session.session_manager import ConversationSession, SessionManager


class SessionPersistenceManager:
    """
    Manages persistence of session context and preference inheritance.

    Responsibilities:
    - Save/restore session context to/from persistent storage
    - Handle context inheritance between sessions
    - Manage session expiration and cleanup
    - Provide performance-optimized persistence operations
    """

    def __init__(self, preference_manager: UserPreferenceManager):
        """
        Initialize persistence manager with preference manager dependency.

        Args:
            preference_manager: UserPreferenceManager instance for handling preferences
        """
        self.preference_manager = preference_manager
        self._storage = None  # Would be actual database connection in real implementation
        self._in_memory_storage: Dict[str, Dict[str, Any]] = {}  # Temporary storage for MVP

    async def save_session_context(
        self, session: ConversationSession, user_id: Optional[str] = None
    ) -> bool:
        """
        Save session context to persistent storage.

        Args:
            session: ConversationSession to persist
            user_id: User ID for preference context

        Returns:
            True if context was saved successfully
        """
        try:
            # Get current context from preference manager
            context_data = await self.preference_manager.get_context_format(
                user_id=user_id, session_id=session.session_id
            )

            # Add session metadata
            persistence_data = {
                "session_id": session.session_id,
                "user_id": user_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "context_data": context_data,
                "session_context": session.context,
                "saved_at": datetime.now().isoformat(),
            }

            # Save to storage (in-memory for MVP, would be database in production)
            await self._save_to_storage(session.session_id, persistence_data)

            return True

        except Exception as e:
            # Log error in production
            return False

    async def restore_session_context(
        self, session: ConversationSession, user_id: Optional[str] = None
    ) -> bool:
        """
        Restore session context from persistent storage.

        Args:
            session: ConversationSession to restore into
            user_id: User ID for preference context

        Returns:
            True if context was restored successfully
        """
        try:
            # Get persisted data
            persisted_data = await self.get_persisted_context(session.session_id)

            if not persisted_data:
                # No persisted context - create fresh context with user preferences
                if user_id:
                    await self.preference_manager.update_session_context(session, user_id=user_id)
                return True

            # Restore context data to preference manager
            if "context_data" in persisted_data:
                context_data = persisted_data["context_data"]

                # Load global preferences
                if "global_preferences" in context_data:
                    for key, value in context_data["global_preferences"].items():
                        await self.preference_manager.set_preference(key, value, scope="global")

                # Load user preferences
                if "user_preferences" in context_data and user_id:
                    for key, value in context_data["user_preferences"].items():
                        await self.preference_manager.set_preference(key, value, user_id=user_id)

                # Load session preferences
                if "session_preferences" in context_data:
                    for key, value in context_data["session_preferences"].items():
                        await self.preference_manager.set_preference(
                            key, value, session_id=session.session_id
                        )

            # Restore session context
            if "session_context" in persisted_data:
                session.context.update(persisted_data["session_context"])

            # Update session with fresh preference context
            if user_id:
                await self.preference_manager.update_session_context(session, user_id=user_id)

            return True

        except Exception as e:
            # Log error in production
            return False

    async def get_persisted_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get persisted context data for a session.

        Args:
            session_id: Session identifier

        Returns:
            Persisted context data or None if not found
        """
        try:
            return await self._get_from_storage(session_id)
        except Exception:
            return None

    async def cleanup_expired_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up expired session contexts.

        Args:
            max_age_hours: Maximum age of sessions to keep (default 24 hours)

        Returns:
            Number of sessions cleaned up
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned_count = 0

            # Get all persisted sessions
            all_sessions = await self._get_all_sessions()

            for session_id, data in all_sessions.items():
                try:
                    last_activity = datetime.fromisoformat(
                        data.get("last_activity", data.get("saved_at"))
                    )
                    if last_activity < cutoff_time:
                        await self._delete_from_storage(session_id)
                        # Clean up session preferences in preference manager
                        await self.preference_manager.clear_session_preferences(session_id)
                        cleaned_count += 1
                except Exception:
                    # Skip invalid sessions
                    continue

            return cleaned_count

        except Exception:
            return 0

    async def migrate_session_context(
        self, old_session_id: str, new_session_id: str, preserve_session_preferences: bool = False
    ) -> bool:
        """
        Migrate context from one session to another.

        Args:
            old_session_id: Source session ID
            new_session_id: Target session ID
            preserve_session_preferences: Whether to copy session-specific preferences

        Returns:
            True if migration was successful
        """
        try:
            # Get old session context
            old_context = await self.get_persisted_context(old_session_id)
            if not old_context:
                return False

            # Create new session with migrated context
            new_session = ConversationSession(new_session_id)

            # Restore user preferences (always migrated)
            if "context_data" in old_context and "user_preferences" in old_context["context_data"]:
                user_id = old_context.get("user_id")
                if user_id:
                    for key, value in old_context["context_data"]["user_preferences"].items():
                        await self.preference_manager.set_preference(key, value, user_id=user_id)

            # Optionally migrate session preferences
            if preserve_session_preferences and "context_data" in old_context:
                if "session_preferences" in old_context["context_data"]:
                    for key, value in old_context["context_data"]["session_preferences"].items():
                        await self.preference_manager.set_preference(
                            key, value, session_id=new_session_id
                        )

            # Save new session context
            user_id = old_context.get("user_id")
            await self.save_session_context(new_session, user_id=user_id)

            return True

        except Exception:
            return False

    async def get_session_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about persisted sessions.

        Returns:
            Dictionary with session statistics
        """
        try:
            all_sessions = await self._get_all_sessions()

            total_sessions = len(all_sessions)
            active_sessions = 0
            total_preferences = 0

            cutoff_time = datetime.now() - timedelta(hours=1)  # Active within last hour

            for session_id, data in all_sessions.items():
                try:
                    last_activity = datetime.fromisoformat(
                        data.get("last_activity", data.get("saved_at"))
                    )
                    if last_activity > cutoff_time:
                        active_sessions += 1

                    # Count preferences
                    if "context_data" in data:
                        context_data = data["context_data"]
                        total_preferences += len(context_data.get("user_preferences", {}))
                        total_preferences += len(context_data.get("session_preferences", {}))

                except Exception:
                    continue

            return {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "total_preferences": total_preferences,
                "storage_type": "in_memory",  # Would be "database" in production
                "last_updated": datetime.now().isoformat(),
            }

        except Exception:
            return {
                "total_sessions": 0,
                "active_sessions": 0,
                "total_preferences": 0,
                "storage_type": "error",
                "last_updated": datetime.now().isoformat(),
            }

    # Private storage methods (would be replaced with actual database operations)

    async def _save_to_storage(self, session_id: str, data: Dict[str, Any]) -> None:
        """Save data to storage (in-memory for MVP)"""
        # Simulate async database operation
        await asyncio.sleep(0.001)  # Minimal delay to simulate I/O
        self._in_memory_storage[session_id] = data

    async def _get_from_storage(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get data from storage (in-memory for MVP)"""
        # Simulate async database operation
        await asyncio.sleep(0.001)  # Minimal delay to simulate I/O
        return self._in_memory_storage.get(session_id)

    async def _delete_from_storage(self, session_id: str) -> None:
        """Delete data from storage (in-memory for MVP)"""
        # Simulate async database operation
        await asyncio.sleep(0.001)  # Minimal delay to simulate I/O
        if session_id in self._in_memory_storage:
            del self._in_memory_storage[session_id]

    async def _get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all sessions from storage (in-memory for MVP)"""
        # Simulate async database operation
        await asyncio.sleep(0.001)  # Minimal delay to simulate I/O
        return self._in_memory_storage.copy()


class SessionContextManager:
    """
    High-level session context management combining SessionManager and SessionPersistenceManager.

    Provides unified interface for session lifecycle with persistence.
    """

    def __init__(self, ttl_minutes: int = 30):
        """
        Initialize session context manager.

        Args:
            ttl_minutes: Session TTL in minutes
        """
        self.session_manager = SessionManager(ttl_minutes=ttl_minutes)
        self.preference_manager = UserPreferenceManager()
        self.persistence_manager = SessionPersistenceManager(self.preference_manager)

    async def get_or_create_session_with_context(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        restore_context: bool = True,
    ) -> ConversationSession:
        """
        Get or create session with full context restoration.

        Args:
            session_id: Optional session ID
            user_id: User ID for preference context
            restore_context: Whether to restore persisted context

        Returns:
            ConversationSession with context loaded
        """
        # Get or create session
        session = self.session_manager.get_or_create_session(session_id)

        # Restore context if requested
        if restore_context:
            await self.persistence_manager.restore_session_context(session, user_id=user_id)
        elif user_id:
            # Load fresh user preferences
            await self.preference_manager.update_session_context(session, user_id=user_id)

        return session

    async def end_session_with_persistence(
        self, session: ConversationSession, user_id: Optional[str] = None
    ) -> bool:
        """
        End session and persist context.

        Args:
            session: Session to end
            user_id: User ID for context

        Returns:
            True if session was ended and persisted successfully
        """
        try:
            # Save session context
            await self.persistence_manager.save_session_context(session, user_id=user_id)

            # Clean up in-memory session
            if session.session_id in self.session_manager._sessions:
                del self.session_manager._sessions[session.session_id]

            return True

        except Exception:
            return False

    async def cleanup_expired_sessions(self) -> Dict[str, int]:
        """
        Clean up expired sessions from both in-memory and persistent storage.

        Returns:
            Cleanup statistics
        """
        # Clean up in-memory sessions
        self.session_manager.cleanup_expired_sessions()
        in_memory_cleaned = len(
            [
                s
                for s in self.session_manager._sessions.values()
                if (datetime.utcnow() - s.last_activity).total_seconds()
                > self.session_manager.ttl.total_seconds()
            ]
        )

        # Clean up persistent sessions
        persistent_cleaned = await self.persistence_manager.cleanup_expired_sessions()

        return {
            "in_memory_cleaned": in_memory_cleaned,
            "persistent_cleaned": persistent_cleaned,
            "total_cleaned": in_memory_cleaned + persistent_cleaned,
        }
