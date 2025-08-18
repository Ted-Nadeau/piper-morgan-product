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

    def __init__(self):
        super().__init__("google_calendar_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()

        # Google Calendar API configuration
        self._credentials: Optional[Credentials] = None
        self._service = None
        self._calendar_id = "primary"  # User's primary calendar

        # OAuth 2.0 configuration
        self._client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
        self._token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
        self._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

        # Circuit breaker configuration
        self._last_error_time: Optional[datetime] = None
        self._error_count = 0
        self._circuit_open = False
        self._circuit_timeout = 300  # 5 minutes

        logger.info("GoogleCalendarMCPAdapter initialized")

    async def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth 2.0

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
            # Try to load existing credentials
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
                        redirect_uri="http://localhost:8080",
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

    async def get_todays_events(self) -> List[Dict[str, Any]]:
        """
        Get today's calendar events from Google Calendar

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
            # Get start and end of today in UTC
            now = datetime.utcnow()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Format for Google Calendar API
            time_min = start_of_day.isoformat() + "Z"
            time_max = end_of_day.isoformat() + "Z"

            # Call Google Calendar API
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

            # Process events for temporal awareness
            processed_events = []
            for event in events:
                processed_event = self._process_event(event)
                if processed_event:
                    processed_events.append(processed_event)

            logger.info(f"Retrieved {len(processed_events)} events for today")
            self._reset_circuit_breaker()
            return processed_events

        except Exception as e:
            logger.error(f"Failed to retrieve calendar events: {e}")
            self._handle_error()
            return []

    def _process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a calendar event for temporal awareness

        Args:
            event: Raw Google Calendar event

        Returns:
            Dict[str, Any]: Processed event data or None if invalid
        """
        try:
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
            now = datetime.now()
            if now < start_time:
                status = "upcoming"
            elif now > end_time:
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
        """
        Get currently active meeting if any

        Returns:
            Dict[str, Any]: Current meeting details or None
        """
        events = await self.get_todays_events()

        for event in events:
            if event["status"] == "current":
                return event

        return None

    async def get_next_meeting(self) -> Optional[Dict[str, Any]]:
        """
        Get next upcoming meeting today

        Returns:
            Dict[str, Any]: Next meeting details or None
        """
        events = await self.get_todays_events()

        for event in events:
            if event["status"] == "upcoming":
                return event

        return None

    async def get_free_time_blocks(self) -> List[Dict[str, Any]]:
        """
        Calculate free time blocks between meetings

        Returns:
            List[Dict[str, Any]]: Available free time blocks
        """
        events = await self.get_todays_events()

        # Filter only scheduled meetings (not all-day events)
        meetings = [e for e in events if not e["is_all_day"]]

        if not meetings:
            # Entire day is free
            now = datetime.now()
            end_of_day = now.replace(hour=18, minute=0, second=0, microsecond=0)  # 6 PM

            return [
                {
                    "start_time": now.isoformat(),
                    "end_time": end_of_day.isoformat(),
                    "duration_minutes": int((end_of_day - now).total_seconds() / 60),
                    "type": "free_block",
                }
            ]

        # Calculate gaps between meetings
        free_blocks = []
        now = datetime.now()

        # Sort meetings by start time
        meetings.sort(key=lambda x: x["start_time"])

        for i, meeting in enumerate(meetings):
            meeting_start = datetime.fromisoformat(meeting["start_time"])

            # Free time before first meeting
            if i == 0 and now < meeting_start:
                gap_duration = int((meeting_start - now).total_seconds() / 60)
                if gap_duration > 15:  # Only include gaps > 15 minutes
                    free_blocks.append(
                        {
                            "start_time": now.isoformat(),
                            "end_time": meeting["start_time"],
                            "duration_minutes": gap_duration,
                            "type": "before_meeting",
                        }
                    )

            # Free time between meetings
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

    async def get_temporal_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive temporal summary for standup integration

        Returns:
            Dict[str, Any]: Temporal awareness summary
        """
        try:
            current_meeting = await self.get_current_meeting()
            next_meeting = await self.get_next_meeting()
            free_blocks = await self.get_free_time_blocks()
            all_events = await self.get_todays_events()

            # Calculate summary statistics
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
                    "calendar_load": (
                        "heavy" if total_meeting_time > 240 else "light"
                    ),  # 4+ hours = heavy
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
