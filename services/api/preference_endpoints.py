"""
Preference API Endpoints - REST API for Persistent Context Foundation
Phase 3: Integration & API Implementation

Created: 2025-08-20 by Enhanced Autonomy Mission
Provides REST API endpoints for user preference management and session context
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from services.domain.user_preference_manager import UserPreferenceManager
from services.orchestration.session_persistence import SessionContextManager


class PreferenceAPI:
    """
    REST API endpoints for preference and session context management.

    Provides HTTP-compatible interface for:
    - User preference CRUD operations
    - Session context management
    - Preference validation and error handling
    - Performance monitoring and rate limiting
    """

    def __init__(
        self,
        preference_manager: UserPreferenceManager,
        session_manager: Optional[SessionContextManager] = None,
    ):
        """
        Initialize preference API with dependencies.

        Args:
            preference_manager: UserPreferenceManager for core functionality
            session_manager: Optional SessionContextManager for persistence
        """
        self.preference_manager = preference_manager
        self.session_manager = session_manager

        # API configuration
        self.max_preferences_per_request = 100
        self.max_preference_value_size = 10240  # 10KB max per preference value

        # Rate limiting simulation (would be Redis-based in production)
        self._rate_limit_cache: Dict[str, List[datetime]] = {}
        self._rate_limit_window_minutes = 1
        self._rate_limit_max_requests = 60

    async def get_user_preferences(
        self,
        user_id: UUID,
        session_id: Optional[str] = None,
        requesting_user_id: Optional[UUID] = None,
    ) -> Dict[str, Any]:
        """
        GET /api/preferences/{user_id}

        Retrieve user preferences with optional session context.

        Args:
            user_id: Target user ID
            session_id: Optional session context
            requesting_user_id: ID of user making request (for auth)

        Returns:
            API response with preferences or error
        """
        try:
            # Validate inputs
            validation_error = self._validate_get_preferences_request(
                user_id, session_id, requesting_user_id
            )
            if validation_error:
                return validation_error

            # Check rate limiting
            rate_limit_error = await self._check_rate_limit(requesting_user_id or user_id)
            if rate_limit_error:
                return rate_limit_error

            # Check authorization
            auth_error = await self._validate_user_access(user_id, requesting_user_id)
            if auth_error:
                return auth_error

            # Get preferences
            preferences = await self.preference_manager.get_all_preferences(
                user_id=user_id, session_id=session_id
            )

            # Build response
            response = {
                "status": "success",
                "preferences": preferences,
                "metadata": {
                    "user_id": user_id,
                    "session_id": session_id,
                    "preference_count": len(preferences),
                    "retrieved_at": datetime.now().isoformat(),
                    "api_version": "1.0",
                },
            }

            return response

        except Exception as e:
            return self._error_response(
                "internal_error", f"Failed to retrieve preferences: {str(e)}"
            )

    async def update_user_preferences(
        self,
        user_id: UUID,
        preferences: Dict[str, Any],
        requesting_user_id: Optional[str] = None,
        merge_strategy: str = "replace",
    ) -> Dict[str, Any]:
        """
        PUT/PATCH /api/preferences/{user_id}

        Update user preferences with validation and error handling.

        Args:
            user_id: Target user ID
            preferences: Preferences to update
            requesting_user_id: ID of user making request
            merge_strategy: "replace" or "merge" (for PATCH vs PUT)

        Returns:
            API response with update results
        """
        try:
            # Validate inputs
            validation_error = self._validate_update_preferences_request(user_id, preferences)
            if validation_error:
                return validation_error

            # Check rate limiting
            rate_limit_error = await self._check_rate_limit(requesting_user_id or user_id)
            if rate_limit_error:
                return rate_limit_error

            # Check authorization
            auth_error = await self._validate_user_access(user_id, requesting_user_id)
            if auth_error:
                return auth_error

            # Update preferences
            updated_count = 0
            failed_count = 0
            failed_preferences = []
            validation_errors = []

            for key, value in preferences.items():
                try:
                    # Validate individual preference
                    if not self._validate_preference_item(key, value):
                        validation_errors.append(f"Invalid preference: {key}")
                        failed_count += 1
                        failed_preferences.append(key)
                        continue

                    # Set preference
                    success = await self.preference_manager.set_preference(
                        key=key, value=value, user_id=user_id
                    )

                    if success:
                        updated_count += 1
                    else:
                        failed_count += 1
                        failed_preferences.append(key)

                except Exception as e:
                    failed_count += 1
                    failed_preferences.append(key)
                    validation_errors.append(f"Failed to set {key}: {str(e)}")

            # Determine response status
            if failed_count == 0:
                status = "success"
            elif updated_count == 0:
                status = "error"
            else:
                status = "partial_success"

            # Build response
            response = {
                "status": status,
                "updated_count": updated_count,
                "failed_count": failed_count,
                "metadata": {
                    "user_id": user_id,
                    "total_preferences": len(preferences),
                    "updated_at": datetime.now().isoformat(),
                    "merge_strategy": merge_strategy,
                },
            }

            if failed_preferences:
                response["failed_preferences"] = failed_preferences

            if validation_errors:
                response["validation_errors"] = validation_errors

            if status == "error":
                response["error_message"] = (
                    f"Failed to update any preferences. Errors: {'; '.join(validation_errors)}"
                )
                response["error_type"] = "validation_error"

            return response

        except Exception as e:
            return self._error_response("internal_error", f"Failed to update preferences: {str(e)}")

    async def update_session_preferences(
        self, session_id: str, preferences: Dict[str, Any], ttl_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        PUT /api/sessions/{session_id}/preferences

        Update session-specific preferences.

        Args:
            session_id: Target session ID
            preferences: Session preferences to update
            ttl_minutes: Optional TTL for session preferences

        Returns:
            API response with update results
        """
        try:
            # Validate inputs
            if not session_id or not session_id.strip():
                return self._error_response("validation_error", "session_id is required")

            if not isinstance(preferences, dict):
                return self._error_response("validation_error", "preferences must be a dictionary")

            # Update session preferences
            updated_count = 0
            failed_count = 0
            failed_preferences = []

            for key, value in preferences.items():
                try:
                    if not self._validate_preference_item(key, value):
                        failed_count += 1
                        failed_preferences.append(key)
                        continue

                    success = await self.preference_manager.set_preference(
                        key=key, value=value, session_id=session_id, ttl_minutes=ttl_minutes
                    )

                    if success:
                        updated_count += 1
                    else:
                        failed_count += 1
                        failed_preferences.append(key)

                except Exception:
                    failed_count += 1
                    failed_preferences.append(key)

            # Build response
            status = (
                "success"
                if failed_count == 0
                else ("partial_success" if updated_count > 0 else "error")
            )

            response = {
                "status": status,
                "updated_count": updated_count,
                "failed_count": failed_count,
                "metadata": {
                    "session_id": session_id,
                    "ttl_minutes": ttl_minutes,
                    "updated_at": datetime.now().isoformat(),
                },
            }

            if failed_preferences:
                response["failed_preferences"] = failed_preferences

            return response

        except Exception as e:
            return self._error_response(
                "internal_error", f"Failed to update session preferences: {str(e)}"
            )

    async def get_session_context(
        self, session_id: str, user_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        GET /api/sessions/{session_id}/context

        Retrieve complete session context including preferences.

        Args:
            session_id: Target session ID
            user_id: Optional user ID for user preference context

        Returns:
            API response with session context
        """
        try:
            # Validate inputs
            if not session_id or not session_id.strip():
                return self._error_response("validation_error", "session_id is required")

            # Get session context
            context_data = await self.preference_manager.get_context_format(
                user_id=user_id, session_id=session_id
            )

            # Build response
            response = {
                "status": "success",
                "context": context_data,
                "metadata": {
                    "session_id": session_id,
                    "user_id": user_id,
                    "retrieved_at": datetime.now().isoformat(),
                    "context_version": context_data.get("context_version", "1.0"),
                },
            }

            return response

        except Exception as e:
            return self._error_response(
                "internal_error", f"Failed to retrieve session context: {str(e)}"
            )

    async def update_session_context(
        self, session_id: str, user_id: UUID, context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PUT /api/sessions/{session_id}/context

        Update complete session context.

        Args:
            session_id: Target session ID
            user_id: User ID for context
            context_data: Complete context data to update

        Returns:
            API response with update results
        """
        try:
            # Validate inputs
            if not session_id or not session_id.strip():
                return self._error_response("validation_error", "session_id is required")

            if not user_id or not user_id.strip():
                return self._error_response("validation_error", "user_id is required")

            if not isinstance(context_data, dict):
                return self._error_response("validation_error", "context_data must be a dictionary")

            # Update user preferences if provided
            if "user_preferences" in context_data:
                for key, value in context_data["user_preferences"].items():
                    await self.preference_manager.set_preference(key, value, user_id=user_id)

            # Update session preferences if provided
            if "session_preferences" in context_data:
                for key, value in context_data["session_preferences"].items():
                    await self.preference_manager.set_preference(key, value, session_id=session_id)

            # Build response
            response = {
                "status": "success",
                "metadata": {
                    "session_id": session_id,
                    "user_id": user_id,
                    "updated_at": datetime.now().isoformat(),
                    "context_sections_updated": [
                        section
                        for section in ["user_preferences", "session_preferences"]
                        if section in context_data
                    ],
                },
            }

            return response

        except Exception as e:
            return self._error_response(
                "internal_error", f"Failed to update session context: {str(e)}"
            )

    async def clear_session_context(self, session_id: str) -> Dict[str, Any]:
        """
        DELETE /api/sessions/{session_id}/context

        Clear all session-specific context and preferences.

        Args:
            session_id: Target session ID

        Returns:
            API response with clear results
        """
        try:
            # Validate inputs
            if not session_id or not session_id.strip():
                return self._error_response("validation_error", "session_id is required")

            # Clear session preferences
            success = await self.preference_manager.clear_session_preferences(session_id)

            # Build response
            response = {
                "status": "success" if success else "error",
                "metadata": {"session_id": session_id, "cleared_at": datetime.now().isoformat()},
            }

            if not success:
                response["error_message"] = "Failed to clear session context"
                response["error_type"] = "clear_error"

            return response

        except Exception as e:
            return self._error_response(
                "internal_error", f"Failed to clear session context: {str(e)}"
            )

    # Validation and utility methods

    def _validate_get_preferences_request(
        self, user_id: UUID, session_id: Optional[str], requesting_user_id: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Validate GET preferences request parameters"""
        if not user_id or not user_id.strip():
            return self._error_response(
                "validation_error", "user_id is required and cannot be empty"
            )

        if session_id is not None and not session_id.strip():
            return self._error_response(
                "validation_error", "session_id cannot be empty if provided"
            )

        return None

    def _validate_update_preferences_request(
        self, user_id: UUID, preferences: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Validate update preferences request parameters"""
        if not user_id or not user_id.strip():
            return self._error_response(
                "validation_error", "user_id is required and cannot be empty"
            )

        if not isinstance(preferences, dict):
            return self._error_response("validation_error", "preferences must be a dictionary")

        if len(preferences) == 0:
            return self._error_response("validation_error", "preferences cannot be empty")

        if len(preferences) > self.max_preferences_per_request:
            return self._error_response(
                "validation_error",
                f"Too many preferences. Maximum {self.max_preferences_per_request} per request",
            )

        return None

    def _validate_preference_item(self, key: str, value: Any) -> bool:
        """Validate individual preference key-value pair"""
        try:
            # Validate key
            if not isinstance(key, str) or not key.strip():
                return False

            # Validate value is JSON serializable
            json.dumps(value)

            # Check value size
            value_size = len(json.dumps(value))
            if value_size > self.max_preference_value_size:
                return False

            return True

        except (TypeError, ValueError):
            return False

    async def _validate_user_access(
        self, target_user_id: UUID, requesting_user_id: Optional[UUID]
    ) -> Optional[Dict[str, Any]]:
        """Validate user access permissions (mock implementation)"""
        # In production, this would check actual authentication/authorization
        if requesting_user_id and requesting_user_id != target_user_id:
            # Mock: Only allow users to access their own preferences
            return self._error_response(
                "unauthorized", "Access denied: cannot access other user's preferences"
            )

        return None

    async def _check_rate_limit(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """Check rate limiting for user (mock implementation)"""
        # Mock rate limiting implementation
        now = datetime.now()
        cutoff = now.replace(
            minute=(
                now.minute - self._rate_limit_window_minutes
                if now.minute >= self._rate_limit_window_minutes
                else 59
            )
        )

        if user_id not in self._rate_limit_cache:
            self._rate_limit_cache[user_id] = []

        # Clean old requests
        self._rate_limit_cache[user_id] = [
            req_time for req_time in self._rate_limit_cache[user_id] if req_time > cutoff
        ]

        # Check limit
        if len(self._rate_limit_cache[user_id]) >= self._rate_limit_max_requests:
            return self._error_response(
                "rate_limit_exceeded",
                f"Rate limit exceeded: {self._rate_limit_max_requests} requests per {self._rate_limit_window_minutes} minute(s)",
            )

        # Record this request
        self._rate_limit_cache[user_id].append(now)

        return None

    def _error_response(self, error_type: str, error_message: str) -> Dict[str, Any]:
        """Generate standardized error response"""
        return {
            "status": "error",
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat(),
            "api_version": "1.0",
        }

    # Health and monitoring endpoints

    async def health_check(self) -> Dict[str, Any]:
        """
        GET /api/preferences/health

        API health check endpoint.

        Returns:
            Health status and metrics
        """
        try:
            # Test preference manager functionality
            test_start = datetime.now()
            await self.preference_manager.get_preference(
                "health_check_test", user_id="health_check"
            )
            test_duration = (datetime.now() - test_start).total_seconds() * 1000

            # Get session statistics if session manager available
            session_stats = {}
            if self.session_manager:
                session_stats = (
                    await self.session_manager.persistence_manager.get_session_statistics()
                )

            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "performance": {
                    "preference_test_duration_ms": test_duration,
                    "rate_limit_cache_size": len(self._rate_limit_cache),
                },
                "session_statistics": session_stats,
                "configuration": {
                    "max_preferences_per_request": self.max_preferences_per_request,
                    "max_preference_value_size": self.max_preference_value_size,
                    "rate_limit_max_requests": self._rate_limit_max_requests,
                    "rate_limit_window_minutes": self._rate_limit_window_minutes,
                },
            }

        except Exception as e:
            return {"status": "unhealthy", "timestamp": datetime.now().isoformat(), "error": str(e)}
