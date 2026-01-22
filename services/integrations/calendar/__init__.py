"""
Calendar Integration Module

Provides router-based access to calendar integrations with feature flag control.
"""

from .calendar_integration_router import CalendarIntegrationRouter, create_calendar_integration
from .narrative_bridge import CalendarNarrativeBridge
from .narrative_helpers import (
    get_calendar_formality,
    has_time_for_task,
    is_calendar_busy,
    narrate_calendar_summary,
    narrate_day_summary,
    narrate_free_blocks,
    narrate_meeting_load,
    narrate_meeting_status,
    narrate_next_meeting,
    narrate_time_until_next,
)

# Issue #624: Grammar-conscious response components
from .response_context import CalendarResponseContext

__all__ = [
    # Router
    "CalendarIntegrationRouter",
    "create_calendar_integration",
    # Response context
    "CalendarResponseContext",
    "CalendarNarrativeBridge",
    # Narrative helpers
    "narrate_meeting_status",
    "narrate_day_summary",
    "narrate_next_meeting",
    "narrate_free_blocks",
    "narrate_calendar_summary",
    "narrate_meeting_load",
    "narrate_time_until_next",
    "get_calendar_formality",
    "is_calendar_busy",
    "has_time_for_task",
]
