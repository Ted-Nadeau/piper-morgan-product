"""
Consciousness Context Analysis

Analyzes the context to determine which consciousness patterns to apply.

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ConsciousnessContext:
    """
    Context for consciousness injection decisions.

    This context drives pattern selection - determining which templates
    and language patterns to use based on the user's situation.
    """

    # Temporal context
    time_of_day: str = "morning"  # morning, late_morning, afternoon, evening
    is_first_interaction_today: bool = True
    current_hour: int = 9

    # Situational context
    user_in_meeting: bool = False
    has_focus_time: bool = False
    meeting_load: str = "light"  # light, moderate, heavy
    meeting_count: int = 0
    meeting_hours: float = 0.0

    # Data richness
    has_accomplishments: bool = False
    accomplishment_count: int = 0
    has_github_activity: bool = False
    has_calendar_data: bool = False
    has_blockers: bool = False
    blocker_count: int = 0
    data_sources: List[str] = field(default_factory=list)

    # Priority context
    priority_count: int = 0
    has_clear_priority: bool = False

    @property
    def data_sources_count(self) -> int:
        """Number of data sources available."""
        return len(self.data_sources)

    @property
    def richness_level(self) -> str:
        """Assess overall data richness."""
        if self.data_sources_count >= 3:
            return "rich"
        elif self.data_sources_count >= 1:
            return "moderate"
        return "sparse"

    @property
    def should_use_full_arc(self) -> bool:
        """Whether to use full narrative arc vs abbreviated."""
        return (
            self.time_of_day == "morning"
            and self.is_first_interaction_today
            and self.richness_level in ("rich", "moderate")
            and not self.user_in_meeting
        )

    @property
    def needs_empathy(self) -> bool:
        """Whether context suggests empathetic tone needed."""
        return (
            self.meeting_load == "heavy" or self.blocker_count > 0 or not self.has_accomplishments
        )


def analyze_context(
    data: Dict[str, Any],
    current_time: Optional[datetime] = None,
) -> ConsciousnessContext:
    """
    Analyze data to build consciousness context.

    Args:
        data: Dictionary containing standup or other feature data
        current_time: Current time (defaults to now)

    Returns:
        ConsciousnessContext for pattern selection
    """
    if current_time is None:
        current_time = datetime.now()

    hour = current_time.hour

    # Determine time of day
    if 6 <= hour < 9:
        time_of_day = "morning"
    elif 9 <= hour < 12:
        time_of_day = "late_morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    # Extract accomplishments
    accomplishments = data.get("yesterday_accomplishments", [])
    has_accomplishments = len(accomplishments) > 0

    # Extract GitHub activity
    github_activity = data.get("github_activity", {})
    has_github = bool(github_activity.get("commits") or github_activity.get("prs"))

    # Extract calendar data
    calendar_stats = data.get("performance_metrics", {}).get("calendar_stats", {})
    has_calendar = bool(calendar_stats)
    meeting_count = calendar_stats.get("meetings_today", 0)
    meeting_hours = calendar_stats.get("meeting_hours", 0)

    # Determine meeting load
    if meeting_hours >= 5:
        meeting_load = "heavy"
    elif meeting_hours >= 2:
        meeting_load = "moderate"
    else:
        meeting_load = "light"

    # Extract blockers
    blockers = data.get("blockers", [])
    has_blockers = len(blockers) > 0

    # Extract priorities
    priorities = data.get("today_priorities", [])
    priority_count = len(priorities)

    # Build data sources list
    data_sources = []
    if has_github:
        data_sources.append("github")
    if has_calendar:
        data_sources.append("calendar")
    if data.get("context_source") == "persistent":
        data_sources.append("session")

    return ConsciousnessContext(
        time_of_day=time_of_day,
        current_hour=hour,
        has_accomplishments=has_accomplishments,
        accomplishment_count=len(accomplishments),
        has_github_activity=has_github,
        has_calendar_data=has_calendar,
        meeting_count=meeting_count,
        meeting_hours=meeting_hours,
        meeting_load=meeting_load,
        has_blockers=has_blockers,
        blocker_count=len(blockers),
        priority_count=priority_count,
        has_clear_priority=priority_count == 1,
        data_sources=data_sources,
    )
