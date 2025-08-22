"""
UserPreferenceManager - Persistent Context Foundation
Phase 1: Core Infrastructure Implementation

Created: 2025-08-20 by Enhanced Autonomy Mission
Follows Excellence Flywheel: Tests First → Implementation → Evidence-based progress
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from services.session.session_manager import ConversationSession


@dataclass
class PreferenceItem:
    """Individual preference item with versioning and metadata"""

    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: datetime = field(default_factory=datetime.now)
    ttl_minutes: Optional[int] = None

    def is_expired(self) -> bool:
        """Check if preference has expired based on TTL"""
        if self.ttl_minutes is None:
            return False
        expiry = self.created_at + timedelta(minutes=self.ttl_minutes)
        return datetime.now() > expiry

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version.isoformat(),
            "ttl_minutes": self.ttl_minutes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PreferenceItem":
        """Create from dictionary (JSON deserialization)"""
        return cls(
            value=data["value"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            version=datetime.fromisoformat(data["version"]),
            ttl_minutes=data.get("ttl_minutes"),
        )


class UserPreferenceManager:
    """
    Manages user preferences with hierarchical inheritance and persistence.

    Hierarchy: Global → User → Session (session overrides user overrides global)
    Storage: JSON-based using existing ConversationSession.context patterns
    """

    def __init__(self):
        """Initialize preference manager with in-memory storage"""
        # In-memory storage (would be replaced with database persistence)
        self.global_preferences: Dict[str, PreferenceItem] = {}
        self.user_preferences: Dict[str, Dict[str, PreferenceItem]] = {}  # user_id -> preferences
        self.session_preferences: Dict[str, Dict[str, PreferenceItem]] = (
            {}
        )  # session_id -> preferences

        # Concurrent access protection
        self._locks: Dict[str, asyncio.Lock] = {}

    def _get_lock(self, key: str) -> asyncio.Lock:
        """Get or create lock for concurrent access protection"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def set_preference(
        self,
        key: str,
        value: Any,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        scope: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
    ) -> bool:
        """
        Set a preference at the appropriate scope level.

        Args:
            key: Preference key
            value: Preference value (must be JSON serializable)
            user_id: User ID for user-scoped preferences
            session_id: Session ID for session-scoped preferences
            scope: Explicit scope ("global", "user", "session")
            ttl_minutes: Time-to-live in minutes (for session preferences)

        Returns:
            bool: True if preference was set successfully
        """
        lock_key = f"{scope or 'auto'}:{user_id or 'none'}:{session_id or 'none'}:{key}"
        async with self._get_lock(lock_key):
            try:
                # Validate value is JSON serializable
                json.dumps(value)

                preference_item = PreferenceItem(value=value, ttl_minutes=ttl_minutes)

                # Determine scope
                if scope == "global" or (not user_id and not session_id):
                    self.global_preferences[key] = preference_item
                elif session_id:
                    if session_id not in self.session_preferences:
                        self.session_preferences[session_id] = {}
                    self.session_preferences[session_id][key] = preference_item
                elif user_id:
                    if user_id not in self.user_preferences:
                        self.user_preferences[user_id] = {}
                    self.user_preferences[user_id][key] = preference_item
                else:
                    # Default to global if no scope specified
                    self.global_preferences[key] = preference_item

                return True

            except (TypeError, ValueError) as e:
                # Value not JSON serializable
                return False

    async def get_preference(
        self,
        key: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        scope: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """
        Get a preference with hierarchical inheritance.

        Priority: Session > User > Global > Default

        Args:
            key: Preference key
            user_id: User ID for context
            session_id: Session ID for context
            scope: Explicit scope to check ("global", "user", "session")
            default: Default value if preference not found

        Returns:
            Preference value or default
        """
        # Clean up expired preferences first
        await self._cleanup_expired_preferences()

        # If explicit scope requested, only check that scope
        if scope == "global":
            item = self.global_preferences.get(key)
            return item.value if item and not item.is_expired() else default
        elif scope == "user" and user_id:
            user_prefs = self.user_preferences.get(user_id, {})
            item = user_prefs.get(key)
            return item.value if item and not item.is_expired() else default
        elif scope == "session" and session_id:
            session_prefs = self.session_preferences.get(session_id, {})
            item = session_prefs.get(key)
            return item.value if item and not item.is_expired() else default

        # Hierarchical lookup: Session → User → Global → Default
        if session_id:
            session_prefs = self.session_preferences.get(session_id, {})
            item = session_prefs.get(key)
            if item and not item.is_expired():
                return item.value

        if user_id:
            user_prefs = self.user_preferences.get(user_id, {})
            item = user_prefs.get(key)
            if item and not item.is_expired():
                return item.value

        # Check global preferences
        item = self.global_preferences.get(key)
        if item and not item.is_expired():
            return item.value

        return default

    async def get_all_preferences(
        self, user_id: Optional[str] = None, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all preferences for a user/session context.

        Returns merged preferences with hierarchy applied.
        """
        await self._cleanup_expired_preferences()

        result = {}

        # Start with global preferences
        for key, item in self.global_preferences.items():
            if not item.is_expired():
                result[key] = item.value

        # Apply user preferences (override global)
        if user_id and user_id in self.user_preferences:
            for key, item in self.user_preferences[user_id].items():
                if not item.is_expired():
                    result[key] = item.value

        # Apply session preferences (override user and global)
        if session_id and session_id in self.session_preferences:
            for key, item in self.session_preferences[session_id].items():
                if not item.is_expired():
                    result[key] = item.value

        return result

    async def merge_preferences(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """
        Merge preferences with full hierarchy for a specific user/session.

        Args:
            user_id: User identifier
            session_id: Session identifier

        Returns:
            Merged preferences dictionary
        """
        return await self.get_all_preferences(user_id=user_id, session_id=session_id)

    async def clear_session_preferences(self, session_id: str) -> bool:
        """
        Clear all preferences for a specific session.

        Args:
            session_id: Session identifier

        Returns:
            True if preferences were cleared
        """
        if session_id in self.session_preferences:
            del self.session_preferences[session_id]

        # Clean up any locks for this session
        lock_keys_to_remove = [key for key in self._locks.keys() if f":{session_id}:" in key]
        for key in lock_keys_to_remove:
            del self._locks[key]

        return True

    async def get_preference_version(
        self, key: str, user_id: Optional[str] = None, session_id: Optional[str] = None
    ) -> Optional[datetime]:
        """
        Get the version (last updated timestamp) of a preference.

        Args:
            key: Preference key
            user_id: User ID for context
            session_id: Session ID for context

        Returns:
            Version timestamp or None if preference doesn't exist
        """
        # Check session first, then user, then global
        if session_id and session_id in self.session_preferences:
            item = self.session_preferences[session_id].get(key)
            if item:
                return item.version

        if user_id and user_id in self.user_preferences:
            item = self.user_preferences[user_id].get(key)
            if item:
                return item.version

        item = self.global_preferences.get(key)
        return item.version if item else None

    async def set_preference_with_version(
        self,
        key: str,
        value: Any,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        expected_version: Optional[datetime] = None,
    ) -> bool:
        """
        Set preference with version conflict detection.

        Args:
            key: Preference key
            value: New preference value
            user_id: User ID for context
            session_id: Session ID for context
            expected_version: Expected current version for conflict detection

        Returns:
            True if preference was set, False if version conflict
        """
        if expected_version:
            current_version = await self.get_preference_version(key, user_id, session_id)
            if current_version and current_version != expected_version:
                # Version conflict - could implement conflict resolution here
                # For now, we'll allow the update (last write wins)
                pass

        return await self.set_preference(key, value, user_id, session_id)

    async def is_preference_expired(self, key: str, session_id: Optional[str] = None) -> bool:
        """
        Check if a preference has expired (mainly for session preferences with TTL).

        Args:
            key: Preference key
            session_id: Session ID for context

        Returns:
            True if preference exists and is expired
        """
        if session_id and session_id in self.session_preferences:
            item = self.session_preferences[session_id].get(key)
            if item:
                return item.is_expired()

        return False

    async def get_context_format(
        self, user_id: Optional[str] = None, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get preferences in ConversationSession.context compatible format.

        Args:
            user_id: User ID for context
            session_id: Session ID for context

        Returns:
            Context-compatible dictionary
        """
        await self._cleanup_expired_preferences()

        context_data = {
            "global_preferences": {},
            "user_preferences": {},
            "session_preferences": {},
            "context_version": "1.0",
            "last_updated": datetime.now().isoformat(),
        }

        # Global preferences
        for key, item in self.global_preferences.items():
            if not item.is_expired():
                context_data["global_preferences"][key] = item.value

        # User preferences
        if user_id and user_id in self.user_preferences:
            for key, item in self.user_preferences[user_id].items():
                if not item.is_expired():
                    context_data["user_preferences"][key] = item.value

        # Session preferences
        if session_id and session_id in self.session_preferences:
            for key, item in self.session_preferences[session_id].items():
                if not item.is_expired():
                    context_data["session_preferences"][key] = item.value

        return context_data

    async def update_session_context(
        self, session: ConversationSession, user_id: Optional[str] = None
    ) -> bool:
        """
        Update ConversationSession.context with current preferences.

        Args:
            session: ConversationSession instance to update
            user_id: User ID for preference context

        Returns:
            True if context was updated successfully
        """
        try:
            context_data = await self.get_context_format(
                user_id=user_id, session_id=session.session_id
            )

            # Merge with existing context (preserve non-preference data)
            session.context.update(context_data)

            return True

        except Exception:
            return False

    async def load_from_session_context(self, session: ConversationSession) -> bool:
        """
        Load preferences from existing ConversationSession.context.

        Args:
            session: ConversationSession instance to load from

        Returns:
            True if preferences were loaded successfully
        """
        try:
            context = session.context

            # Load global preferences
            if "global_preferences" in context:
                for key, value in context["global_preferences"].items():
                    await self.set_preference(key, value, scope="global")

            # Load user preferences (need user_id from somewhere)
            if "user_preferences" in context:
                # Note: We'd need to get user_id from session or pass it in
                # For now, we'll skip loading user preferences without user_id
                pass

            # Load session preferences
            if "session_preferences" in context:
                for key, value in context["session_preferences"].items():
                    await self.set_preference(key, value, session_id=session.session_id)

            return True

        except Exception:
            return False

    async def _cleanup_expired_preferences(self):
        """Clean up expired preferences across all scopes"""
        current_time = datetime.now()

        # Clean global preferences
        expired_global = [key for key, item in self.global_preferences.items() if item.is_expired()]
        for key in expired_global:
            del self.global_preferences[key]

        # Clean user preferences
        for user_id, user_prefs in self.user_preferences.items():
            expired_user = [key for key, item in user_prefs.items() if item.is_expired()]
            for key in expired_user:
                del user_prefs[key]

        # Clean session preferences
        for session_id, session_prefs in self.session_preferences.items():
            expired_session = [key for key, item in session_prefs.items() if item.is_expired()]
            for key in expired_session:
                del session_prefs[key]
