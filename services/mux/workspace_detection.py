"""
Workspace detection for context switching.

Part of #658 WORKSPACE-DETECTION (child of #416 MUX-INTERACT-WORKSPACE epic).

This module provides:
- WorkspaceContext: Represents a user's working context
- ContextSwitch: Detected change in user's working context
- detect_context_switch(): Detection logic for context switches

Bridges existing infrastructure (PlaceType enum, spatial_context dicts)
to typed domain models for workspace-aware behavior.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from services.shared_types import PlaceType


@dataclass
class WorkspaceContext:
    """
    Represents a user's working context.

    Built from PlaceDetector output (PlaceType) and spatial_context dict.
    Provides typed access to workspace information that was previously
    scattered across untyped dictionaries.
    """

    workspace_id: str
    workspace_type: str  # "slack", "web", "cli", "api", "unknown"
    friendly_name: str  # Human-readable: "#general", "web chat", "terminal"
    last_active: datetime
    place_type: PlaceType
    metadata: Dict[str, Any]

    @classmethod
    def from_spatial_context(
        cls,
        spatial_context: Dict[str, Any],
        place_type: PlaceType,
        timestamp: Optional[datetime] = None,
    ) -> "WorkspaceContext":
        """
        Build WorkspaceContext from spatial_context dict and PlaceType.

        This factory method bridges the existing dict-based infrastructure
        to the typed domain model.

        Args:
            spatial_context: Dict with location hints (room_id, channel, workspace_id, etc.)
            place_type: PlaceType enum from PlaceDetector
            timestamp: When this context was active (defaults to now)

        Returns:
            WorkspaceContext instance with extracted/derived fields
        """
        workspace_id = cls._extract_workspace_id(spatial_context, place_type)
        workspace_type = cls._derive_workspace_type(place_type)
        friendly_name = cls._generate_friendly_name(workspace_type, spatial_context)
        return cls(
            workspace_id=workspace_id,
            workspace_type=workspace_type,
            friendly_name=friendly_name,
            last_active=timestamp or datetime.now(timezone.utc),
            place_type=place_type,
            metadata=spatial_context.copy(),
        )

    @staticmethod
    def _extract_workspace_id(ctx: Dict[str, Any], place_type: PlaceType) -> str:
        """
        Extract workspace identifier based on place type.

        Different place types store identity in different keys:
        - Slack: workspace_id or team_id
        - Web: session_id
        - CLI: always "cli"
        - API: client_id
        """
        if place_type in (PlaceType.SLACK_DM, PlaceType.SLACK_CHANNEL):
            return ctx.get("workspace_id") or ctx.get("team_id") or "unknown-slack"
        elif place_type == PlaceType.WEB_CHAT:
            return ctx.get("session_id") or "web-chat"
        elif place_type == PlaceType.CLI:
            return "cli"
        elif place_type == PlaceType.API:
            return ctx.get("client_id") or "api"
        return "unknown"

    @staticmethod
    def _derive_workspace_type(place_type: PlaceType) -> str:
        """Map PlaceType enum to workspace type string."""
        mapping = {
            PlaceType.SLACK_DM: "slack",
            PlaceType.SLACK_CHANNEL: "slack",
            PlaceType.WEB_CHAT: "web",
            PlaceType.CLI: "cli",
            PlaceType.API: "api",
            PlaceType.UNKNOWN: "unknown",
        }
        return mapping.get(place_type, "unknown")

    @staticmethod
    def _generate_friendly_name(workspace_type: str, ctx: Dict[str, Any]) -> str:
        """
        Generate human-readable workspace name.

        Used in responses like "switching from #general to the API repo".
        """
        if workspace_type == "slack":
            channel = ctx.get("channel") or ctx.get("room_id")
            if channel:
                # Add # prefix if not already present
                if not channel.startswith("#"):
                    return f"#{channel}"
                return channel
            return "Slack"
        elif workspace_type == "web":
            return "web chat"
        elif workspace_type == "cli":
            return "terminal"
        elif workspace_type == "api":
            return "API"
        return "unknown context"

    def matches(self, other: "WorkspaceContext") -> bool:
        """
        Check if this context matches another (same workspace).

        Two contexts match if they have the same workspace_id,
        regardless of other metadata differences.
        """
        return self.workspace_id == other.workspace_id


@dataclass
class ContextSwitch:
    """
    Detected change in user's working context.

    Represents a transition from one workspace to another, with metadata
    about the type of switch and time away (for returns).
    """

    from_context: WorkspaceContext
    to_context: WorkspaceContext
    switch_type: str  # "explicit" | "implicit" | "return"
    time_away: Optional[timedelta] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def detect_context_switch(
    current_context: WorkspaceContext,
    previous_context: Optional[WorkspaceContext],
    session_history: Optional[List[WorkspaceContext]] = None,
) -> Optional[ContextSwitch]:
    """
    Detect if user has switched contexts.

    Args:
        current_context: User's current workspace context
        previous_context: User's previous workspace context (if any)
        session_history: List of all contexts in this session (oldest first)

    Returns:
        ContextSwitch if a switch was detected, None otherwise

    Switch types:
        - "explicit": User moved to a different workspace
        - "return": User came back to an earlier context from session history
    """
    if not previous_context:
        return None

    # Same workspace - no switch
    if current_context.matches(previous_context):
        return None

    # Check for return to earlier context
    history = session_history or []
    for earlier in reversed(history[:-1]):  # Exclude current
        if current_context.matches(earlier):
            return ContextSwitch(
                from_context=previous_context,
                to_context=current_context,
                switch_type="return",
                time_away=current_context.last_active - earlier.last_active,
            )

    # Explicit switch to new context
    return ContextSwitch(
        from_context=previous_context,
        to_context=current_context,
        switch_type="explicit",
    )
