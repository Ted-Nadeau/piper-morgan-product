"""
Place detection for grammar-conscious intent classification.

The Place in MUX grammar represents WHERE the interaction happens.
Different Places call for different communication styles:
- Slack DM: casual, can be personal
- Slack channel: professional, concise (others watching)
- Web chat: warm, full explanations
- CLI: terse, no fluff

See: #619 GRAMMAR-TRANSFORM: Intent Classification
"""

from typing import Any, Dict, Optional

from services.shared_types import InteractionSpace


class PlaceDetector:
    """
    Detects the Place where a conversation is happening.

    Place awareness lets Piper adjust her communication style
    appropriately - more casual in DMs, more professional in
    public channels, more terse on CLI.
    """

    # Place-specific communication settings
    PLACE_SETTINGS: Dict[InteractionSpace, Dict[str, Any]] = {
        InteractionSpace.SLACK_DM: {
            "formality": "casual",
            "verbosity": "medium",
            "can_use_emoji": True,
            "max_response_lines": 20,
        },
        InteractionSpace.SLACK_CHANNEL: {
            "formality": "professional",
            "verbosity": "concise",
            "can_use_emoji": False,
            "max_response_lines": 10,
        },
        InteractionSpace.WEB_CHAT: {
            "formality": "warm",
            "verbosity": "full",
            "can_use_emoji": True,
            "max_response_lines": 50,
        },
        InteractionSpace.CLI: {
            "formality": "terse",
            "verbosity": "minimal",
            "can_use_emoji": False,
            "max_response_lines": 5,
        },
        InteractionSpace.API: {
            "formality": "neutral",
            "verbosity": "structured",
            "can_use_emoji": False,
            "max_response_lines": 100,
        },
        InteractionSpace.UNKNOWN: {
            "formality": "professional",
            "verbosity": "medium",
            "can_use_emoji": False,
            "max_response_lines": 15,
        },
    }

    def detect(self, spatial_context: Optional[Dict[str, Any]]) -> InteractionSpace:
        """
        Determine InteractionSpace from spatial context.

        Args:
            spatial_context: Dictionary with location hints from the request.
                Common keys: room_id, channel, is_dm, source, workspace_id

        Returns:
            InteractionSpace indicating where this conversation is happening.
        """
        if not spatial_context:
            return InteractionSpace.UNKNOWN

        # Check for explicit source indicator (highest priority)
        source = spatial_context.get("source", "").lower()
        if source == "cli":
            return InteractionSpace.CLI
        if source == "api":
            return InteractionSpace.API
        if source in ("web", "web_chat"):
            return InteractionSpace.WEB_CHAT

        # Check for Slack indicators
        if self._is_slack_context(spatial_context):
            if spatial_context.get("is_dm", False):
                return InteractionSpace.SLACK_DM
            # Any Slack context without is_dm = public channel
            return InteractionSpace.SLACK_CHANNEL

        # Check for web indicators
        if spatial_context.get("browser") or spatial_context.get("web_session"):
            return InteractionSpace.WEB_CHAT

        return InteractionSpace.UNKNOWN

    def _is_slack_context(self, spatial_context: Dict[str, Any]) -> bool:
        """Check if this looks like a Slack context."""
        slack_indicators = [
            "room_id",
            "channel",
            "workspace_id",
            "thread_ts",
            "team_id",
            "slack_user_id",
        ]
        return any(key in spatial_context for key in slack_indicators)

    def get_place_settings(self, place: InteractionSpace) -> Dict[str, Any]:
        """
        Get communication settings appropriate for this Place.

        Args:
            place: The InteractionSpace to get settings for.

        Returns:
            Dictionary with formality, verbosity, emoji, and line limit settings.
        """
        return self.PLACE_SETTINGS.get(place, self.PLACE_SETTINGS[InteractionSpace.UNKNOWN])

    def detect_with_settings(
        self, spatial_context: Optional[Dict[str, Any]]
    ) -> tuple[InteractionSpace, Dict[str, Any]]:
        """
        Convenience method to detect Place and get settings in one call.

        Args:
            spatial_context: Location context dictionary.

        Returns:
            Tuple of (InteractionSpace, settings dictionary).
        """
        place = self.detect(spatial_context)
        settings = self.get_place_settings(place)
        return place, settings
