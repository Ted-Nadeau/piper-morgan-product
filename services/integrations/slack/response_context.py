"""
Grammar-conscious Slack response context.

This module provides rich context for generating grammar-conscious
Slack responses. It captures the Place, Entity, and Situation
needed to make Piper feel *present* in Slack conversations.

Issue #620: GRAMMAR-TRANSFORM: Slack Integration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.integrations.slack.spatial_types import (
    AttentionLevel,
    EmotionalValence,
    SpatialCoordinates,
)
from services.shared_types import PlaceType


@dataclass
class SlackResponseContext:
    """
    Rich context for grammar-conscious Slack responses.

    This captures everything Piper knows when responding in Slack:
    - Where she is (DM, channel, thread)
    - Who she's talking to
    - How she was summoned (mention, direct message)
    - The emotional tenor of the conversation

    In MUX grammar: this is the Situation for Slack responses.
    """

    # Place information
    place: PlaceType
    channel_id: str
    channel_name: Optional[str] = None
    is_thread: bool = False
    thread_ts: Optional[str] = None

    # Entity information
    user_id: str = ""
    user_display_name: Optional[str] = None

    # Attention signals
    attention_level: AttentionLevel = AttentionLevel.AMBIENT
    is_direct_mention: bool = False

    # Emotional context
    recent_reactions: List[str] = field(default_factory=list)
    emotional_valence: EmotionalValence = EmotionalValence.NEUTRAL

    # Conversation continuity
    is_new_conversation: bool = True
    messages_in_thread: int = 0

    # Timestamp
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_spatial_context(
        cls,
        spatial_context: Dict[str, Any],
    ) -> "SlackResponseContext":
        """
        Build response context from Slack spatial context.

        This factory method enables integration with existing Slack
        event handling that passes spatial_context dicts.

        Args:
            spatial_context: Dict with Slack context (channel_id, is_dm, etc.)

        Returns:
            SlackResponseContext with grammar-conscious context
        """
        # Determine Place
        is_dm = spatial_context.get("is_dm", False)
        place = PlaceType.SLACK_DM if is_dm else PlaceType.SLACK_CHANNEL

        # Extract attention level
        attention_level = AttentionLevel.AMBIENT
        if spatial_context.get("is_direct_mention"):
            attention_level = AttentionLevel.DIRECT
        elif spatial_context.get("is_channel_mention"):
            attention_level = AttentionLevel.FOCUSED

        # Check for thread context
        thread_ts = spatial_context.get("thread_ts")
        is_thread = thread_ts is not None

        return cls(
            place=place,
            channel_id=spatial_context.get("channel_id", spatial_context.get("channel", "")),
            channel_name=spatial_context.get("channel_name"),
            is_thread=is_thread,
            thread_ts=thread_ts,
            user_id=spatial_context.get("user_id", spatial_context.get("user", "")),
            user_display_name=spatial_context.get("user_display_name"),
            attention_level=attention_level,
            is_direct_mention=spatial_context.get("is_direct_mention", False),
            recent_reactions=spatial_context.get("recent_reactions", []),
            emotional_valence=_infer_valence(spatial_context.get("recent_reactions", [])),
            is_new_conversation=not is_thread,
            messages_in_thread=spatial_context.get("messages_in_thread", 0),
        )

    @classmethod
    def from_spatial_event(
        cls,
        spatial_event: Any,  # SpatialEvent from domain models
    ) -> "SlackResponseContext":
        """
        Build response context from a SpatialEvent.

        Args:
            spatial_event: SpatialEvent with spatial coordinates and metadata

        Returns:
            SlackResponseContext for response generation
        """
        coords = spatial_event.coordinates if hasattr(spatial_event, "coordinates") else None

        # Determine if DM (DMs typically start with 'D')
        room_id = coords.room_id if coords else ""
        is_dm = room_id.startswith("D") if room_id else False
        place = PlaceType.SLACK_DM if is_dm else PlaceType.SLACK_CHANNEL

        # Extract attention level from spatial event
        attention_level = AttentionLevel.AMBIENT
        if hasattr(spatial_event, "attention_attractor") and spatial_event.attention_attractor:
            attention_level = spatial_event.attention_attractor.attractor_type

        # Check for thread
        path_id = coords.path_id if coords else None
        is_thread = path_id is not None

        # Extract actor
        actor_id = spatial_event.actor_id if hasattr(spatial_event, "actor_id") else ""

        # Extract emotional valence
        valence = EmotionalValence.NEUTRAL
        if hasattr(spatial_event, "emotional_marker") and spatial_event.emotional_marker:
            valence = spatial_event.emotional_marker.valence

        return cls(
            place=place,
            channel_id=room_id,
            is_thread=is_thread,
            thread_ts=path_id,
            user_id=actor_id or "",
            attention_level=attention_level,
            is_direct_mention=attention_level == AttentionLevel.DIRECT,
            emotional_valence=valence,
            is_new_conversation=not is_thread,
        )

    def get_formality(self) -> str:
        """
        Determine appropriate formality level for this context.

        DMs are more casual, public channels more professional.
        """
        if self.place == PlaceType.SLACK_DM:
            return "casual"
        elif self.attention_level == AttentionLevel.DIRECT:
            return "warm"
        else:
            return "professional"

    def should_be_concise(self) -> bool:
        """
        Determine if response should be concise.

        Public channels favor brevity; DMs allow more detail.
        """
        return self.place == PlaceType.SLACK_CHANNEL

    def user_seems_frustrated(self) -> bool:
        """
        Detect if user might be frustrated based on signals.

        Signals: negative reactions, rapid messages, repeated attempts.
        """
        if self.emotional_valence == EmotionalValence.NEGATIVE:
            return True
        if self.messages_in_thread > 3 and not self.is_new_conversation:
            # Multiple messages in thread might indicate confusion
            return True
        return False


def _infer_valence(reactions: List[str]) -> EmotionalValence:
    """Infer emotional valence from reaction emojis."""
    if not reactions:
        return EmotionalValence.NEUTRAL

    positive = {"+1", "thumbsup", "heart", "tada", "clap", "raised_hands", "star"}
    negative = {"-1", "thumbsdown", "x", "warning", "angry", "disappointed"}
    supportive = {"muscle", "pray", "hugging_face", "heart_hands"}

    for reaction in reactions:
        reaction_name = reaction.lower().replace(":", "")
        if reaction_name in negative:
            return EmotionalValence.NEGATIVE
        if reaction_name in supportive:
            return EmotionalValence.SUPPORTIVE
        if reaction_name in positive:
            return EmotionalValence.POSITIVE

    return EmotionalValence.NEUTRAL
