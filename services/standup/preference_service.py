"""
Standup Preference Service - Preference Storage and Management

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Provides CRUD operations for user standup preferences with persistence.
PM Decision (2026-01-08): Option B - Database persistence with DDD compliance.

Currently uses JSON file storage as intermediate step (can be migrated to
PostgreSQL table later without changing the service interface).
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.standup.preference_models import (
    PreferenceChange,
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)

logger = logging.getLogger(__name__)


class UserPreferenceService:
    """
    Service for managing user standup preferences.

    Provides:
    - CRUD operations for preferences
    - Conflict resolution (latest wins with confidence boost)
    - Preference history tracking
    - Cross-session persistence

    Storage: JSON files in data/preferences/ (interim solution)
    Future: PostgreSQL table for production use.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the preference service.

        Args:
            storage_path: Directory for preference JSON files.
                         Defaults to data/preferences/
        """
        self.storage_path = storage_path or Path("data/preferences")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._locks: Dict[str, asyncio.Lock] = {}

    def _get_user_file(self, user_id: str) -> Path:
        """Get the preferences file path for a user."""
        # Sanitize user_id for filename safety
        safe_id = user_id.replace("/", "_").replace("\\", "_")
        return self.storage_path / f"{safe_id}.json"

    def _get_lock(self, user_id: str) -> asyncio.Lock:
        """Get or create a lock for a user's preferences."""
        if user_id not in self._locks:
            self._locks[user_id] = asyncio.Lock()
        return self._locks[user_id]

    async def _load_user_data(self, user_id: str) -> Dict[str, Any]:
        """Load user preference data from storage."""
        file_path = self._get_user_file(user_id)
        if not file_path.exists():
            return {"preferences": [], "history": []}

        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading preferences for {user_id}: {e}")
            return {"preferences": [], "history": []}

    async def _save_user_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """Save user preference data to storage."""
        file_path = self._get_user_file(user_id)
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Error saving preferences for {user_id}: {e}")
            raise

    async def get_preferences(self, user_id: str) -> List[UserStandupPreference]:
        """
        Get all preferences for a user.

        Args:
            user_id: The user's ID

        Returns:
            List of UserStandupPreference objects
        """
        async with self._get_lock(user_id):
            data = await self._load_user_data(user_id)
            preferences = []
            for pref_dict in data.get("preferences", []):
                try:
                    preferences.append(UserStandupPreference.from_dict(pref_dict))
                except (KeyError, ValueError) as e:
                    logger.warning(f"Invalid preference data: {e}")
            return preferences

    async def get_preference(
        self, user_id: str, preference_type: PreferenceType, key: str
    ) -> Optional[UserStandupPreference]:
        """
        Get a specific preference by type and key.

        Args:
            user_id: The user's ID
            preference_type: Type of preference (CONTENT_FILTER, EXCLUSION, etc.)
            key: Preference key (focus, exclude, format, etc.)

        Returns:
            UserStandupPreference if found, None otherwise
        """
        preferences = await self.get_preferences(user_id)
        for pref in preferences:
            if pref.preference_type == preference_type and pref.key == key:
                return pref
        return None

    async def get_preferences_by_type(
        self, user_id: str, preference_type: PreferenceType
    ) -> List[UserStandupPreference]:
        """
        Get all preferences of a specific type.

        Args:
            user_id: The user's ID
            preference_type: Type of preference to filter by

        Returns:
            List of matching preferences
        """
        preferences = await self.get_preferences(user_id)
        return [p for p in preferences if p.preference_type == preference_type]

    async def save_preference(
        self, pref: UserStandupPreference, session_id: Optional[str] = None
    ) -> UserStandupPreference:
        """
        Save a preference, handling conflicts if one exists.

        Conflict resolution:
        - If same type+key exists: update with higher confidence (latest wins tie)
        - If same preference repeated: boost confidence
        - Records change in history

        Args:
            pref: The preference to save
            session_id: Optional session ID for history tracking

        Returns:
            The saved preference (may be updated with new ID)
        """
        async with self._get_lock(pref.user_id):
            data = await self._load_user_data(pref.user_id)
            preferences = data.get("preferences", [])
            history = data.get("history", [])

            # Find existing preference with same type and key
            existing_idx = None
            existing_pref = None
            for i, p_dict in enumerate(preferences):
                if (
                    p_dict.get("preference_type") == pref.preference_type.value
                    and p_dict.get("key") == pref.key
                ):
                    existing_idx = i
                    existing_pref = UserStandupPreference.from_dict(p_dict)
                    break

            if existing_pref:
                # Same value = confirmation, boost confidence
                if existing_pref.value == pref.value:
                    existing_pref.boost_confidence(0.1)
                    pref = existing_pref
                    change_reason = "repetition"
                else:
                    # Different value = update, record change
                    change = PreferenceChange(
                        preference_id=existing_pref.id,
                        user_id=pref.user_id,
                        previous_value=existing_pref.value,
                        new_value=pref.value,
                        previous_confidence=existing_pref.confidence,
                        new_confidence=pref.confidence,
                        change_reason="user_update",
                        session_id=session_id,
                    )
                    history.append(change.to_dict())
                    pref.id = existing_pref.id  # Keep same ID
                    change_reason = "user_update"

                preferences[existing_idx] = pref.to_dict()
            else:
                # New preference
                preferences.append(pref.to_dict())
                change_reason = "new"

            data["preferences"] = preferences
            data["history"] = history
            await self._save_user_data(pref.user_id, data)

            logger.info(
                f"Saved preference for {pref.user_id}: "
                f"{pref.preference_type.value}/{pref.key}={pref.value} ({change_reason})"
            )
            return pref

    async def update_preference(
        self,
        user_id: str,
        preference_id: str,
        value: Any = None,
        confidence: Optional[float] = None,
        source: Optional[PreferenceSource] = None,
        session_id: Optional[str] = None,
    ) -> Optional[UserStandupPreference]:
        """
        Update an existing preference.

        Args:
            user_id: The user's ID
            preference_id: ID of the preference to update
            value: New value (optional)
            confidence: New confidence (optional)
            source: New source (optional)
            session_id: Session ID for history tracking

        Returns:
            Updated preference if found, None otherwise
        """
        async with self._get_lock(user_id):
            data = await self._load_user_data(user_id)
            preferences = data.get("preferences", [])
            history = data.get("history", [])

            for i, p_dict in enumerate(preferences):
                if p_dict.get("id") == preference_id:
                    pref = UserStandupPreference.from_dict(p_dict)

                    # Record change
                    previous_value = pref.value
                    previous_confidence = pref.confidence

                    # Apply updates
                    if value is not None:
                        pref.value = value
                    if confidence is not None:
                        pref.confidence = confidence
                    if source is not None:
                        pref.source = source

                    pref.updated_at = datetime.now()
                    pref.version += 1

                    # Record in history
                    change = PreferenceChange(
                        preference_id=preference_id,
                        user_id=user_id,
                        previous_value=previous_value,
                        new_value=pref.value,
                        previous_confidence=previous_confidence,
                        new_confidence=pref.confidence,
                        change_reason="explicit_update",
                        session_id=session_id,
                    )
                    history.append(change.to_dict())

                    preferences[i] = pref.to_dict()
                    data["preferences"] = preferences
                    data["history"] = history
                    await self._save_user_data(user_id, data)
                    return pref

            return None

    async def delete_preference(self, user_id: str, preference_id: str) -> bool:
        """
        Delete a preference.

        Args:
            user_id: The user's ID
            preference_id: ID of the preference to delete

        Returns:
            True if deleted, False if not found
        """
        async with self._get_lock(user_id):
            data = await self._load_user_data(user_id)
            preferences = data.get("preferences", [])

            initial_count = len(preferences)
            preferences = [p for p in preferences if p.get("id") != preference_id]

            if len(preferences) < initial_count:
                data["preferences"] = preferences
                await self._save_user_data(user_id, data)
                logger.info(f"Deleted preference {preference_id} for {user_id}")
                return True
            return False

    async def get_preference_history(self, user_id: str, limit: int = 50) -> List[PreferenceChange]:
        """
        Get preference change history for a user.

        Args:
            user_id: The user's ID
            limit: Maximum number of history entries to return

        Returns:
            List of PreferenceChange objects, most recent first
        """
        async with self._get_lock(user_id):
            data = await self._load_user_data(user_id)
            history = data.get("history", [])

            # Parse and sort by changed_at (most recent first)
            changes = []
            for h in history:
                try:
                    change = PreferenceChange(
                        id=h.get("id", ""),
                        preference_id=h.get("preference_id", ""),
                        user_id=h.get("user_id", ""),
                        previous_value=h.get("previous_value"),
                        new_value=h.get("new_value"),
                        previous_confidence=h.get("previous_confidence", 0),
                        new_confidence=h.get("new_confidence", 0),
                        change_reason=h.get("change_reason", ""),
                        session_id=h.get("session_id"),
                        changed_at=(
                            datetime.fromisoformat(h["changed_at"])
                            if h.get("changed_at")
                            else datetime.now()
                        ),
                    )
                    changes.append(change)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Invalid history entry: {e}")

            # Sort by changed_at descending and limit
            changes.sort(key=lambda c: c.changed_at, reverse=True)
            return changes[:limit]

    async def clear_preferences(self, user_id: str) -> int:
        """
        Clear all preferences for a user.

        Args:
            user_id: The user's ID

        Returns:
            Number of preferences cleared
        """
        async with self._get_lock(user_id):
            data = await self._load_user_data(user_id)
            count = len(data.get("preferences", []))
            data["preferences"] = []
            await self._save_user_data(user_id, data)
            logger.info(f"Cleared {count} preferences for {user_id}")
            return count

    async def get_high_confidence_preferences(
        self, user_id: str, threshold: float = 0.8
    ) -> List[UserStandupPreference]:
        """
        Get preferences that exceed the confidence threshold.

        These are preferences that should be auto-applied.

        Args:
            user_id: The user's ID
            threshold: Minimum confidence (default 0.8)

        Returns:
            List of high-confidence preferences
        """
        preferences = await self.get_preferences(user_id)
        return [p for p in preferences if p.is_high_confidence(threshold)]

    async def get_preferences_needing_confirmation(
        self, user_id: str, threshold: float = 0.5
    ) -> List[UserStandupPreference]:
        """
        Get preferences with low confidence that need user confirmation.

        Args:
            user_id: The user's ID
            threshold: Maximum confidence to require confirmation

        Returns:
            List of low-confidence preferences
        """
        preferences = await self.get_preferences(user_id)
        return [p for p in preferences if p.needs_confirmation(threshold)]


# Convenience functions


async def get_user_preferences(user_id: str) -> List[UserStandupPreference]:
    """Get all preferences for a user."""
    service = UserPreferenceService()
    return await service.get_preferences(user_id)


async def save_user_preference(pref: UserStandupPreference) -> UserStandupPreference:
    """Save a preference for a user."""
    service = UserPreferenceService()
    return await service.save_preference(pref)
