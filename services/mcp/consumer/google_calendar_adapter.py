"""
Google Calendar MCP Adapter

Google Calendar-specific MCP adapter implementation following the established
spatial adapter pattern for external system integration and temporal awareness.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.mcp.token_counter import TokenCounter

# Google Calendar dependencies - graceful fallback if not available
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build

    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    # Graceful fallback when Google libraries not installed
    GOOGLE_LIBS_AVAILABLE = False
    Request = None
    Credentials = None
    Flow = None
    build = None

from services.integrations.calendar.config_service import CalendarConfigService
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .consumer_core import MCPConsumerCore

logger = logging.getLogger(__name__)


class GoogleCalendarMCPAdapter(BaseSpatialAdapter):
    """
    Google Calendar MCP adapter implementation.

    Maps calendar events to spatial positions using MCP protocol
    for temporal awareness and standup enhancement.
    """

    def __init__(self, config_service: Optional[CalendarConfigService] = None):
        """
        Initialize Google Calendar MCP adapter with config service.

        Args:
            config_service: Optional CalendarConfigService for dependency injection.
                          If not provided, creates a default instance.
        """
        super().__init__("google_calendar_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()

        # Store config service (service injection pattern)
        self.config_service = config_service or CalendarConfigService()

        # Load configuration from service
        config = self.config_service.get_config()

        # Google Calendar API configuration
        self._credentials: Optional[Credentials] = None
        self._service = None
        self._calendar_id = config.calendar_id

        # OAuth 2.0 configuration (from config service, not direct env access)
        self._client_secrets_file = config.client_secrets_file
        self._token_file = config.token_file
        self._scopes = config.scopes

        # Circuit breaker configuration
        self._last_error_time: Optional[datetime] = None
        self._error_count = 0
        self._circuit_open = False
        self._circuit_timeout = config.circuit_timeout

        # Token counting for MCP operations (Issue #369)
        self.token_counter = TokenCounter()

        logger.info(
            "GoogleCalendarMCPAdapter initialized with %s",
            "service injection" if config_service else "default config",
        )

    async def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth 2.0

        Priority:
        1. Keychain refresh token (web OAuth from setup wizard - Issue #529)
        2. File-based token (legacy)
        3. Interactive OAuth flow (manual setup)

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Check if Google libraries are available
            if not GOOGLE_LIBS_AVAILABLE:
                logger.warning(
                    "Google Calendar libraries not installed. Install with: pip install google-auth google-auth-oauthlib google-api-python-client"
                )
                return False

            # Issue #529: Try keychain first (web OAuth flow)
            if await self._authenticate_from_keychain():
                return True

            # Try to load existing credentials from file (legacy)
            if os.path.exists(self._token_file):
                self._credentials = Credentials.from_authorized_user_file(
                    self._token_file, self._scopes
                )

            # If credentials are invalid or don't exist, perform OAuth flow
            if not self._credentials or not self._credentials.valid:
                if (
                    self._credentials
                    and self._credentials.expired
                    and self._credentials.refresh_token
                ):
                    self._credentials.refresh(Request())
                else:
                    if not os.path.exists(self._client_secrets_file):
                        logger.error(
                            f"Google client secrets file not found: {self._client_secrets_file}"
                        )
                        return False

                    flow = Flow.from_client_secrets_file(
                        self._client_secrets_file,
                        self._scopes,
                        redirect_uri="http://localhost:8084",
                    )

                    # For now, return False to indicate manual OAuth setup needed
                    logger.warning("Google Calendar OAuth setup required. Run setup script first.")
                    return False

                # Save credentials for future use
                with open(self._token_file, "w") as token:
                    token.write(self._credentials.to_json())

            # Initialize Calendar service
            self._service = build("calendar", "v3", credentials=self._credentials)
            logger.info("Google Calendar authentication successful")
            return True

        except Exception as e:
            logger.error(f"Google Calendar authentication failed: {e}")
            self._handle_error()
            return False

    async def _authenticate_from_keychain(self) -> bool:
        """
        Authenticate using refresh token stored in keychain (Issue #529).

        This is the preferred method when user connected via web OAuth flow
        in the setup wizard.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            from services.infrastructure.keychain_service import KeychainService
            from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

            keychain = KeychainService()
            refresh_token = keychain.get_api_key("google_calendar")

            if not refresh_token:
                return False

            # Use OAuth handler to refresh the access token
            handler = GoogleCalendarOAuthHandler()
            tokens = await handler.refresh_access_token(refresh_token)

            if not tokens:
                logger.warning("Failed to refresh calendar access token from keychain")
                return False

            # Create credentials object from the refreshed tokens
            self._credentials = Credentials(
                token=tokens.access_token,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
                client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
                scopes=self._scopes,
            )

            # Initialize Calendar service
            self._service = build("calendar", "v3", credentials=self._credentials)
            logger.info("Google Calendar authenticated via keychain (Issue #529)")
            return True

        except ImportError:
            logger.debug("Keychain service not available, falling back to file-based auth")
            return False
        except Exception as e:
            logger.debug(f"Keychain auth failed, falling back to file-based: {e}")
            return False

    async def _get_user_timezone(self, user_id: Optional[str] = None) -> str:
        """
        Get user's timezone from preferences, with fallback.

        Issue #586: Added for timezone-aware calendar queries.

        Args:
            user_id: Optional user ID to look up timezone preference

        Returns:
            str: User's timezone string (e.g., "America/Los_Angeles")
        """
        if user_id:
            try:
                from uuid import UUID

                from services.domain.user_preference_manager import UserPreferenceManager

                pref_manager = UserPreferenceManager()
                return await pref_manager.get_reminder_timezone(UUID(user_id))
            except Exception as e:
                logger.warning(f"Could not get user timezone: {e}")
        return "America/Los_Angeles"  # Default fallback

    async def get_todays_events(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get today's calendar events from Google Calendar (with token counting).

        Issue #586: Added user_id parameter for timezone-aware queries.

        Args:
            user_id: Optional user ID for timezone-aware day boundaries

        Returns:
            List[Dict[str, Any]]: List of today's calendar events
        """
        if self._circuit_open:
            logger.warning("Google Calendar circuit breaker is open")
            return []

        if not self._service:
            if not await self.authenticate():
                return []

        try:
            # Issue #586: Get user's timezone for day boundary calculation
            user_timezone = await self._get_user_timezone(user_id)

            async def _get_events():
                from datetime import timezone
                from zoneinfo import ZoneInfo

                # Issue #586: Use user's timezone for day boundaries
                user_tz = ZoneInfo(user_timezone)

                # Get current time in user's timezone
                now_local = datetime.now(user_tz)

                # Get start/end of day in user's timezone
                start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)

                # Convert to UTC for Google API (RFC3339 format)
                time_min = start_of_day.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
                time_max = end_of_day.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

                events_result = (
                    self._service.events()
                    .list(
                        calendarId=self._calendar_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )

                events = events_result.get("items", [])
                processed_events = []
                for event in events:
                    processed_event = self._process_event(event)
                    if processed_event:
                        processed_events.append(processed_event)

                return processed_events

            events = await self.token_counter.wrap_mcp_call(
                "calendar_get_todays_events",
                _get_events(),
                input_data="",
            )

            logger.info(f"Retrieved {len(events)} events for today (timezone: {user_timezone})")
            self._reset_circuit_breaker()
            return events

        except Exception as e:
            logger.error(f"Failed to retrieve calendar events: {e}")
            self._handle_error()
            return []

    def _process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a calendar event for temporal awareness

        Issue #586: Fixed to use timezone-aware datetime for status calculation.

        Args:
            event: Raw Google Calendar event

        Returns:
            Dict[str, Any]: Processed event data or None if invalid
        """
        try:
            from datetime import timezone

            # Extract essential event information
            event_id = event.get("id", "")
            summary = event.get("summary", "No Title")

            # Handle different start time formats
            start = event.get("start", {})
            if "dateTime" in start:
                start_time = datetime.fromisoformat(start["dateTime"].replace("Z", "+00:00"))
            elif "date" in start:
                # All-day event
                start_time = datetime.fromisoformat(start["date"])
            else:
                logger.warning(f"Event {event_id} has no valid start time")
                return None

            # Extract end time
            end = event.get("end", {})
            if "dateTime" in end:
                end_time = datetime.fromisoformat(end["dateTime"].replace("Z", "+00:00"))
            elif "date" in end:
                end_time = datetime.fromisoformat(end["date"])
            else:
                end_time = start_time + timedelta(hours=1)  # Default 1-hour duration

            # Calculate event status
            # Issue #586: Use timezone-aware now() for consistent comparison
            now = datetime.now(timezone.utc)

            # Ensure start_time and end_time are timezone-aware for comparison
            if start_time.tzinfo is None:
                # All-day events have naive datetimes, treat as UTC for comparison
                start_time_aware = start_time.replace(tzinfo=timezone.utc)
                end_time_aware = (
                    end_time.replace(tzinfo=timezone.utc) if end_time.tzinfo is None else end_time
                )
            else:
                start_time_aware = start_time
                end_time_aware = end_time

            if now < start_time_aware:
                status = "upcoming"
            elif now > end_time_aware:
                status = "completed"
            else:
                status = "current"

            # Create processed event
            processed = {
                "id": event_id,
                "summary": summary,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "status": status,
                "location": event.get("location", ""),
                "description": event.get("description", ""),
                "attendees": len(event.get("attendees", [])),
                "is_all_day": "date" in start,
                "duration_minutes": int((end_time - start_time).total_seconds() / 60),
            }

            return processed

        except Exception as e:
            logger.error(f"Failed to process event: {e}")
            return None

    async def get_current_meeting(self) -> Optional[Dict[str, Any]]:
        """Get currently active meeting if any (with token counting)"""

        async def _get():
            events = await self.get_todays_events()
            for event in events:
                if event["status"] == "current":
                    return event
            return None

        result = await self.token_counter.wrap_mcp_call(
            "calendar_get_current_meeting",
            _get(),
            input_data="",
        )

        return result

    async def get_next_meeting(self) -> Optional[Dict[str, Any]]:
        """Get next upcoming meeting today (with token counting)"""

        async def _get():
            events = await self.get_todays_events()
            for event in events:
                if event["status"] == "upcoming":
                    return event
            return None

        result = await self.token_counter.wrap_mcp_call(
            "calendar_get_next_meeting",
            _get(),
            input_data="",
        )

        return result

    async def get_free_time_blocks(self) -> List[Dict[str, Any]]:
        """Calculate free time blocks between meetings (with token counting)"""

        async def _get():
            from datetime import datetime, timedelta

            events = await self.get_todays_events()
            meetings = [e for e in events if not e["is_all_day"]]

            if not meetings:
                now = datetime.now()
                end_of_day = now.replace(hour=18, minute=0, second=0, microsecond=0)
                return [
                    {
                        "start_time": now.isoformat(),
                        "end_time": end_of_day.isoformat(),
                        "duration_minutes": int((end_of_day - now).total_seconds() / 60),
                        "type": "free_block",
                    }
                ]

            free_blocks = []
            now = datetime.now()
            meetings.sort(key=lambda x: x["start_time"])

            for i, meeting in enumerate(meetings):
                meeting_start = datetime.fromisoformat(meeting["start_time"])

                if i == 0 and now < meeting_start:
                    gap_duration = int((meeting_start - now).total_seconds() / 60)
                    if gap_duration > 15:
                        free_blocks.append(
                            {
                                "start_time": now.isoformat(),
                                "end_time": meeting["start_time"],
                                "duration_minutes": gap_duration,
                                "type": "before_meeting",
                            }
                        )

                if i < len(meetings) - 1:
                    next_meeting = meetings[i + 1]
                    meeting_end = datetime.fromisoformat(meeting["end_time"])
                    next_start = datetime.fromisoformat(next_meeting["start_time"])

                    gap_duration = int((next_start - meeting_end).total_seconds() / 60)
                    if gap_duration > 15:
                        free_blocks.append(
                            {
                                "start_time": meeting["end_time"],
                                "end_time": next_meeting["start_time"],
                                "duration_minutes": gap_duration,
                                "type": "between_meetings",
                            }
                        )

            return free_blocks

        result = await self.token_counter.wrap_mcp_call(
            "calendar_get_free_blocks",
            _get(),
            input_data="",
        )

        logger.info(f"Found {len(result)} free time blocks")
        return result

    async def get_temporal_summary(self) -> Dict[str, Any]:
        """Get comprehensive temporal summary for standup integration (with token counting)"""

        async def _get():
            from datetime import datetime

            try:
                current_meeting = await self.get_current_meeting()
                next_meeting = await self.get_next_meeting()
                free_blocks = await self.get_free_time_blocks()
                all_events = await self.get_todays_events()

                total_meetings = len([e for e in all_events if not e["is_all_day"]])
                total_meeting_time = sum(
                    e["duration_minutes"] for e in all_events if not e["is_all_day"]
                )
                total_free_time = sum(b["duration_minutes"] for b in free_blocks)

                summary = {
                    "current_meeting": current_meeting,
                    "next_meeting": next_meeting,
                    "free_blocks": free_blocks,
                    "stats": {
                        "total_meetings_today": total_meetings,
                        "total_meeting_minutes": total_meeting_time,
                        "total_free_minutes": total_free_time,
                        "calendar_load": "heavy" if total_meeting_time > 240 else "light",
                    },
                    "recommendations": self._generate_recommendations(
                        current_meeting, next_meeting, free_blocks
                    ),
                    "timestamp": datetime.now().isoformat(),
                }

                return summary

            except Exception as e:
                logger.error(f"Failed to generate temporal summary: {e}")
                return {
                    "error": "Calendar unavailable",
                    "fallback": "Static calendar patterns from configuration",
                    "timestamp": datetime.now().isoformat(),
                }

        result = await self.token_counter.wrap_mcp_call(
            "calendar_get_temporal_summary",
            _get(),
            input_data="",
        )

        logger.info("Generated temporal summary")
        return result

    async def get_events_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get calendar events within a date range.

        Issue #518: Added for Query #61 (week calendar) to support router pattern.

        Args:
            start_date: Start of date range (datetime)
            end_date: End of date range (datetime)

        Returns:
            List[Dict[str, Any]]: List of processed calendar events
        """
        if self._circuit_open:
            logger.warning("Google Calendar circuit breaker is open")
            return []

        if not self._service:
            if not await self.authenticate():
                return []

        try:

            async def _get_events():
                # Issue #588: Convert local time to UTC for Google Calendar API
                # If datetime is naive (no timezone), assume it's local time and convert to UTC
                from datetime import timezone as tz

                if start_date.tzinfo is None:
                    # Naive datetime - treat as local, convert to UTC
                    local_tz = datetime.now().astimezone().tzinfo
                    start_utc = start_date.replace(tzinfo=local_tz).astimezone(tz.utc)
                    end_utc = end_date.replace(tzinfo=local_tz).astimezone(tz.utc)
                else:
                    # Already timezone-aware
                    start_utc = start_date.astimezone(tz.utc)
                    end_utc = end_date.astimezone(tz.utc)

                # Format as ISO with Z suffix (UTC)
                time_min = start_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
                time_max = end_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

                events_result = (
                    self._service.events()
                    .list(
                        calendarId=self._calendar_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )

                events = events_result.get("items", [])
                processed_events = []
                for event in events:
                    processed_event = self._process_event(event)
                    if processed_event:
                        processed_events.append(processed_event)

                return processed_events

            events = await self.token_counter.wrap_mcp_call(
                "calendar_get_events_in_range",
                _get_events(),
                input_data="",
            )

            logger.info(f"Retrieved {len(events)} events in range")
            self._reset_circuit_breaker()
            return events

        except Exception as e:
            logger.error(f"Failed to retrieve calendar events in range: {e}")
            self._handle_error()
            return []

    async def get_recurring_events(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Get recurring calendar events.

        Issue #518: Added for Query #35 (recurring meetings) to support router pattern.

        Args:
            days_ahead: Number of days to look ahead (default 30)

        Returns:
            List[Dict[str, Any]]: List of recurring events with frequency info
        """
        if self._circuit_open:
            logger.warning("Google Calendar circuit breaker is open")
            return []

        if not self._service:
            if not await self.authenticate():
                return []

        try:

            async def _get_recurring():
                now = datetime.now(timezone.utc)
                time_min = now.isoformat().replace("+00:00", "Z")
                time_max = (now + timedelta(days=days_ahead)).isoformat().replace("+00:00", "Z")

                # Get events without expanding recurring (singleEvents=False)
                events_result = (
                    self._service.events()
                    .list(
                        calendarId=self._calendar_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=False,  # Don't expand recurring events
                    )
                    .execute()
                )

                raw_events = events_result.get("items", [])
                recurring_events = []

                for event in raw_events:
                    if "recurrence" in event:
                        summary = event.get("summary", "Untitled")
                        recurrence_rules = event.get("recurrence", [])

                        # Parse RRULE to get frequency
                        frequency = "Unknown"
                        for rule in recurrence_rules:
                            if "FREQ=" in rule:
                                freq_part = rule.split("FREQ=")[1].split(";")[0]
                                frequency = freq_part.capitalize()

                        # Estimate duration from start/end
                        start = event.get("start", {})
                        end = event.get("end", {})
                        duration_minutes = 0

                        if "dateTime" in start and "dateTime" in end:
                            start_time = datetime.fromisoformat(
                                start["dateTime"].replace("Z", "+00:00")
                            )
                            end_time = datetime.fromisoformat(
                                end["dateTime"].replace("Z", "+00:00")
                            )
                            duration_minutes = int((end_time - start_time).total_seconds() / 60)

                        recurring_events.append(
                            {
                                "summary": summary,
                                "frequency": frequency,
                                "duration_minutes": duration_minutes,
                                "recurrence_rules": recurrence_rules,
                            }
                        )

                return recurring_events

            events = await self.token_counter.wrap_mcp_call(
                "calendar_get_recurring_events",
                _get_recurring(),
                input_data="",
            )

            logger.info(f"Retrieved {len(events)} recurring events")
            self._reset_circuit_breaker()
            return events

        except Exception as e:
            logger.error(f"Failed to retrieve recurring events: {e}")
            self._handle_error()
            return []

    def _generate_recommendations(
        self, current_meeting: Optional[Dict], next_meeting: Optional[Dict], free_blocks: List[Dict]
    ) -> List[str]:
        """Generate temporal awareness recommendations for standup"""
        recommendations = []

        if current_meeting:
            recommendations.append(f"Currently in: {current_meeting['summary']}")

        if next_meeting:
            next_start = datetime.fromisoformat(next_meeting["start_time"])
            time_until = next_start - datetime.now()
            minutes_until = int(time_until.total_seconds() / 60)

            if minutes_until <= 15:
                recommendations.append(
                    f"⚠️ Next meeting in {minutes_until} minutes: {next_meeting['summary']}"
                )
            else:
                recommendations.append(
                    f"Next meeting: {next_meeting['summary']} in {minutes_until} minutes"
                )

        # Find longest free block
        if free_blocks:
            longest_block = max(free_blocks, key=lambda x: x["duration_minutes"])
            if longest_block["duration_minutes"] >= 60:
                recommendations.append(
                    f"🕐 {longest_block['duration_minutes']} min focus block available"
                )

        if not current_meeting and not next_meeting:
            recommendations.append("📅 Calendar is clear for deep work")

        return recommendations

    def _handle_error(self):
        """Handle API errors with circuit breaker logic"""
        self._error_count += 1
        self._last_error_time = datetime.now()

        if self._error_count >= 3:
            self._circuit_open = True
            logger.warning("Google Calendar circuit breaker opened due to repeated errors")

    def _reset_circuit_breaker(self):
        """Reset circuit breaker on successful operation"""
        if self._circuit_open and self._last_error_time:
            time_since_error = datetime.now() - self._last_error_time
            if time_since_error.total_seconds() > self._circuit_timeout:
                self._circuit_open = False
                self._error_count = 0
                logger.info("Google Calendar circuit breaker reset")

    # Override spatial context creation for calendar-specific mapping
    def _extract_spatial_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract spatial context from calendar event context."""
        spatial_context = super()._extract_spatial_context(context)

        # Calendar-specific spatial mappings
        if "meeting_type" in context:
            spatial_context["meeting_type"] = context["meeting_type"]
        if "duration_minutes" in context:
            spatial_context["duration_minutes"] = context["duration_minutes"]
        if "attendee_count" in context:
            spatial_context["attendee_count"] = context["attendee_count"]
        if "location" in context:
            spatial_context["location"] = context["location"]

        # Default calendar spatial attributes
        spatial_context.setdefault("territory_id", "calendar")
        spatial_context.setdefault("room_id", "events")
        spatial_context.setdefault("path_id", context.get("calendar_id", "primary"))
        spatial_context.setdefault("attention_level", "medium")
        spatial_context.setdefault("emotional_valence", "neutral")
        spatial_context.setdefault("navigation_intent", "monitor")

        return spatial_context

    async def health_check(self) -> Dict[str, Any]:
        """Health check for Google Calendar integration"""
        return {
            "adapter": "google_calendar_mcp",
            "dependencies_available": GOOGLE_LIBS_AVAILABLE,
            "authenticated": (
                self._credentials is not None and self._credentials.valid
                if GOOGLE_LIBS_AVAILABLE
                else False
            ),
            "circuit_open": self._circuit_open,
            "error_count": self._error_count,
            "last_error": self._last_error_time.isoformat() if self._last_error_time else None,
            "service_available": self._service is not None if GOOGLE_LIBS_AVAILABLE else False,
            "required_packages": (
                ["google-auth", "google-auth-oauthlib", "google-api-python-client"]
                if not GOOGLE_LIBS_AVAILABLE
                else []
            ),
        }
