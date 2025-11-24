"""
Slack Event Handler - Core Event Processing with Spatial Mapping
Processes Slack events through spatial metaphors to update Piper's spatial awareness.

Transforms incoming Slack events into spatial changes that Piper can understand
and navigate, enabling embodied AI concepts in Slack environments.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from services.intent_service.canonical_handlers import CanonicalHandlers

from .config_service import SlackConfigService
from .spatial_mapper import SlackSpatialMapper
from .spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    EmotionalMarker,
    EmotionalValence,
    ObjectType,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialEvent,
    SpatialObject,
    Territory,
    TerritoryType,
)


class EventType(Enum):
    """Slack event types that can be processed"""

    MESSAGE = "message"
    REACTION_ADDED = "reaction_added"
    REACTION_REMOVED = "reaction_removed"
    CHANNEL_CREATED = "channel_created"
    CHANNEL_DELETED = "channel_deleted"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    MENTION = "app_mention"
    THREAD_CREATED = "thread_created"
    THREAD_REPLY = "thread_reply"


@dataclass
class SlackEvent:
    """Slack event wrapper with spatial processing context"""

    event_type: str
    event_data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    spatial_context: Optional[Dict[str, Any]] = None
    processed: bool = False
    spatial_event: Optional[SpatialEvent] = None


@dataclass
class EventProcessingResult:
    """Result of event processing through spatial metaphors"""

    success: bool
    spatial_event: Optional[SpatialEvent] = None
    spatial_changes: List[Dict[str, Any]] = field(default_factory=list)
    attention_level: AttentionLevel = AttentionLevel.AMBIENT
    emotional_valence: EmotionalValence = EmotionalValence.NEUTRAL
    navigation_suggestions: List[str] = field(default_factory=list)
    error: Optional[str] = None


class SlackEventHandler:
    """Core event processing engine with spatial metaphor integration"""

    def __init__(self, config_service: SlackConfigService):
        self.config_service = config_service
        self.spatial_mapper = SlackSpatialMapper()
        self.logger = logging.getLogger(__name__)
        self._spatial_state: Dict[str, Any] = {}
        self._event_history: List[SlackEvent] = []

    async def process_event(self, event_data: Dict[str, Any]) -> EventProcessingResult:
        """Process Slack event through spatial metaphors"""
        try:
            # Create event wrapper
            slack_event = SlackEvent(
                event_type=event_data.get("type", "unknown"), event_data=event_data
            )

            # Determine event type and process accordingly
            if slack_event.event_type == EventType.MESSAGE.value:
                return await self._process_message_event(slack_event)
            elif slack_event.event_type == EventType.REACTION_ADDED.value:
                return await self._process_reaction_event(slack_event, added=True)
            elif slack_event.event_type == EventType.REACTION_REMOVED.value:
                return await self._process_reaction_event(slack_event, added=False)
            elif slack_event.event_type == EventType.MENTION.value:
                return await self._process_mention_event(slack_event)
            elif slack_event.event_type == EventType.CHANNEL_CREATED.value:
                return await self._process_channel_event(slack_event, created=True)
            elif slack_event.event_type == EventType.CHANNEL_DELETED.value:
                return await self._process_channel_event(slack_event, created=False)
            elif slack_event.event_type == EventType.THREAD_CREATED.value:
                return await self._process_thread_event(slack_event, created=True)
            elif slack_event.event_type == EventType.THREAD_REPLY.value:
                return await self._process_thread_event(slack_event, created=False)
            elif slack_event.event_type == EventType.USER_JOINED.value:
                return await self._process_user_event(slack_event, joined=True)
            elif slack_event.event_type == EventType.USER_LEFT.value:
                return await self._process_user_event(slack_event, joined=False)
            else:
                return EventProcessingResult(
                    success=False, error=f"Unsupported event type: {slack_event.event_type}"
                )

        except Exception as e:
            self.logger.error(f"Error processing Slack event: {e}")
            return EventProcessingResult(success=False, error=f"Event processing error: {str(e)}")

    async def _process_message_event(self, slack_event: SlackEvent) -> EventProcessingResult:
        """Process message event through spatial metaphors"""
        event_data = slack_event.event_data

        # Map message to spatial object
        spatial_object = await self.spatial_mapper.map_message_to_spatial_object(
            message_data=event_data,
            room_id=event_data.get("channel"),
            thread_ts=event_data.get("thread_ts"),
        )

        # Create spatial event using correct API
        message_ts = event_data.get("ts", "")
        room_id = event_data.get("channel", "")

        spatial_event = SpatialEvent(
            event_id=f"{room_id}:{message_ts}",
            event_type="message_placed",
            coordinates=SpatialCoordinates(
                territory_id=event_data.get("team"),
                room_id=room_id,
                path_id=event_data.get("thread_ts"),
                object_position=None,  # Position would be calculated if needed
            ),
            actor_id=event_data.get("user"),
            affected_objects=[spatial_object.id],
            spatial_changes={
                "object_placed": spatial_object.get_spatial_context(),
                "content_preview": event_data.get("text", "")[:100],
            },
            spatial_object=spatial_object,  # Add domain object
            event_time=spatial_object.placement_time,
            significance_level="routine",
        )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": "message_placed",
                    "room_id": room_id,
                    "object_id": message_ts,
                    "content_preview": event_data.get("text", "")[:100],
                }
            ],
            attention_level=AttentionLevel.AMBIENT,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

    async def _process_reaction_event(
        self, slack_event: SlackEvent, added: bool
    ) -> EventProcessingResult:
        """Process reaction event as emotional marker"""
        event_data = slack_event.event_data

        # Map reaction to emotional marker
        emotional_marker = await self.spatial_mapper.map_reaction_to_emotional_marker(
            reaction_data=event_data, added=added
        )

        # Extract identifiers
        item = event_data.get("item", {})
        message_ts = item.get("ts", "")
        channel_id = item.get("channel", "")
        reaction_type = event_data.get("reaction", "")

        # Create spatial event using correct API
        spatial_event = SpatialEvent(
            event_id=f"{channel_id}:{message_ts}:reaction:{reaction_type}",
            event_type="emotional_marker_updated",
            coordinates=SpatialCoordinates(
                territory_id=event_data.get("team"),
                room_id=channel_id,
                path_id=item.get("thread_ts"),
                object_position=None,
            ),
            actor_id=event_data.get("user"),
            affected_objects=[message_ts],
            spatial_changes={
                "emotional_marker": emotional_marker.get_emotional_context(),
                "reaction_added": added,
                "valence": emotional_marker.valence.value,
            },
            emotional_marker=emotional_marker,  # Add domain object
            event_time=emotional_marker.created_at,
            significance_level="routine",
        )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": "reaction_" + ("added" if added else "removed"),
                    "room_id": channel_id,
                    "message_id": message_ts,
                    "reaction": reaction_type,
                }
            ],
            attention_level=AttentionLevel.FOCUSED,
            emotional_valence=(
                emotional_marker.valence if emotional_marker else EmotionalValence.NEUTRAL
            ),
        )

    async def _process_mention_event(self, slack_event: SlackEvent) -> EventProcessingResult:
        """Process mention event as attention attractor"""
        event_data = slack_event.event_data

        # Map mention to attention attractor
        attention_attractor = await self.spatial_mapper.map_mention_to_attention_attractor(
            mention_data=event_data
        )

        # Extract identifiers
        message_ts = event_data.get("ts", "")
        channel_id = event_data.get("channel", "")

        # Create spatial event using correct API
        spatial_event = SpatialEvent(
            event_id=f"{channel_id}:{message_ts}:mention",
            event_type="attention_attracted",
            coordinates=SpatialCoordinates(
                territory_id=event_data.get("team"),
                room_id=channel_id,
                path_id=event_data.get("thread_ts"),
                object_position=None,
            ),
            actor_id=event_data.get("user"),
            affected_objects=[message_ts, attention_attractor.target_id],
            spatial_changes={
                "attention_attractor": attention_attractor.get_attention_context(),
                "target_id": attention_attractor.target_id,
                "attention_level": attention_attractor.attractor_type.value,
            },
            attention_attractor=attention_attractor,  # Add domain object
            event_time=attention_attractor.created_at,
            significance_level="notable" if attention_attractor.urgency_indicators else "routine",
        )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": "mention_detected",
                    "room_id": channel_id,
                    "message_id": message_ts,
                    "target": attention_attractor.target_id,
                }
            ],
            attention_level=attention_attractor.attractor_type,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

    async def _process_channel_event(
        self, slack_event: SlackEvent, created: bool
    ) -> EventProcessingResult:
        """Process channel creation/deletion as room changes"""
        event_data = slack_event.event_data

        if created:
            # Map new channel to room
            room = await self.spatial_mapper.map_channel_to_room(
                channel_data=event_data.get("channel", {})
            )

            channel_id = event_data.get("channel", {}).get("id", "")

            spatial_event = SpatialEvent(
                event_id=f"channel_created:{channel_id}",
                event_type="room_created",
                coordinates=SpatialCoordinates(
                    territory_id=event_data.get("team"),
                    room_id=channel_id,
                    path_id=None,
                    object_position=None,
                ),
                affected_objects=[channel_id],
                spatial_changes={
                    "room_created": room.get_room_atmosphere(),
                    "room_name": room.name,
                    "room_purpose": room.purpose.value,
                },
                room=room,  # Add domain object
                event_time=room.created_at,
                significance_level="notable",
            )
        else:
            channel_id = event_data.get("channel", "")

            spatial_event = SpatialEvent(
                event_id=f"channel_deleted:{channel_id}",
                event_type="room_deleted",
                coordinates=SpatialCoordinates(
                    territory_id=event_data.get("team"),
                    room_id=channel_id,
                    path_id=None,
                    object_position=None,
                ),
                affected_objects=[channel_id],
                spatial_changes={
                    "room_deleted": True,
                },
                event_time=datetime.now() if hasattr(datetime, "now") else None,
                significance_level="notable",
            )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": "room_created" if created else "room_deleted",
                    "room_id": (
                        event_data.get("channel", {}).get("id")
                        if created
                        else event_data.get("channel")
                    ),
                    "room_name": event_data.get("channel", {}).get("name") if created else None,
                }
            ],
            attention_level=AttentionLevel.FOCUSED,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

    async def _process_thread_event(
        self, slack_event: SlackEvent, created: bool
    ) -> EventProcessingResult:
        """Process thread creation/reply as conversational path changes"""
        event_data = slack_event.event_data

        message_ts = event_data.get("ts", "")
        thread_ts = event_data.get("thread_ts", message_ts)
        channel_id = event_data.get("channel", "")

        if created:
            spatial_event = SpatialEvent(
                event_id=f"{channel_id}:{thread_ts}:thread_created",
                event_type="conversational_path_created",
                coordinates=SpatialCoordinates(
                    territory_id=event_data.get("team"),
                    room_id=channel_id,
                    path_id=thread_ts,
                    object_position=None,
                ),
                actor_id=event_data.get("user"),
                affected_objects=[thread_ts],
                spatial_changes={
                    "thread_created": True,
                    "thread_ts": thread_ts,
                },
                event_time=datetime.now() if hasattr(datetime, "now") else None,
                significance_level="routine",
            )
        else:
            spatial_event = SpatialEvent(
                event_id=f"{channel_id}:{thread_ts}:{message_ts}",
                event_type="conversational_path_extended",
                coordinates=SpatialCoordinates(
                    territory_id=event_data.get("team"),
                    room_id=channel_id,
                    path_id=thread_ts,
                    object_position=None,
                ),
                actor_id=event_data.get("user"),
                affected_objects=[thread_ts, message_ts],
                spatial_changes={
                    "thread_extended": True,
                    "new_message_ts": message_ts,
                },
                event_time=datetime.now() if hasattr(datetime, "now") else None,
                significance_level="routine",
            )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": (
                        "conversational_path_created" if created else "conversational_path_extended"
                    ),
                    "room_id": channel_id,
                    "path_id": thread_ts,
                    "object_id": message_ts,
                }
            ],
            attention_level=AttentionLevel.FOCUSED,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

    async def _process_user_event(
        self, slack_event: SlackEvent, joined: bool
    ) -> EventProcessingResult:
        """Process user joined/left events as inhabitant changes"""
        event_data = slack_event.event_data

        user_id = event_data.get("user", "")
        channel_id = event_data.get("channel", "")

        spatial_event = SpatialEvent(
            event_id=f"{channel_id}:{user_id}:{'joined' if joined else 'left'}",
            event_type="inhabitant_joined" if joined else "inhabitant_left",
            coordinates=SpatialCoordinates(
                territory_id=event_data.get("team"),
                room_id=channel_id,
                path_id=None,
                object_position=None,
            ),
            actor_id=user_id,
            affected_objects=[user_id],
            spatial_changes={
                "user_joined" if joined else "user_left": True,
                "user_id": user_id,
            },
            event_time=datetime.now() if hasattr(datetime, "now") else None,
            significance_level="routine",
        )

        # Update spatial state
        await self._update_spatial_state(spatial_event)

        return EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            spatial_changes=[
                {
                    "type": "inhabitant_joined" if joined else "inhabitant_left",
                    "room_id": channel_id,
                    "user_id": user_id,
                }
            ],
            attention_level=AttentionLevel.AMBIENT,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

    async def _update_spatial_state(self, spatial_event: SpatialEvent):
        """Update Piper's spatial awareness state"""
        # Store event in history
        self._event_history.append(
            SlackEvent(
                event_type=spatial_event.event_type,
                event_data={},
                spatial_event=spatial_event,
                processed=True,
            )
        )

        # Update spatial state based on event type
        coords = spatial_event.coordinates

        if spatial_event.event_type == "room_created" and spatial_event.room:
            # Use domain object if available, otherwise use spatial_changes
            self._spatial_state.setdefault("rooms", {})[coords.room_id] = spatial_event.room

        elif spatial_event.event_type == "room_deleted":
            self._spatial_state.get("rooms", {}).pop(coords.room_id, None)

        elif spatial_event.event_type == "message_placed" and spatial_event.spatial_object:
            # Use domain object if available
            object_id = spatial_event.spatial_object.id
            self._spatial_state.setdefault("objects", {}).setdefault(coords.room_id, {})[
                object_id
            ] = spatial_event.spatial_object

        elif (
            spatial_event.event_type == "attention_attracted" and spatial_event.attention_attractor
        ):
            # Use domain object if available
            if spatial_event.affected_objects:
                object_id = spatial_event.affected_objects[0]
                self._spatial_state.setdefault("attention_attractors", {}).setdefault(
                    coords.room_id, {}
                )[object_id] = spatial_event.attention_attractor

        elif (
            spatial_event.event_type == "emotional_marker_updated"
            and spatial_event.emotional_marker
        ):
            # Use domain object if available
            if spatial_event.affected_objects:
                object_id = spatial_event.affected_objects[0]
                self._spatial_state.setdefault("emotional_markers", {}).setdefault(
                    coords.room_id, {}
                ).setdefault(object_id, []).append(spatial_event.emotional_marker)

    def get_spatial_state(self) -> Dict[str, Any]:
        """Get current spatial state"""
        return self._spatial_state.copy()

    def get_recent_events(self, limit: int = 10) -> List[SlackEvent]:
        """Get recent processed events"""
        return self._event_history[-limit:]

    def get_attention_attractors(self) -> List[AttentionAttractor]:
        """Get all current attention attractors"""
        attractors = []
        for room_attractors in self._spatial_state.get("attention_attractors", {}).values():
            attractors.extend(room_attractors.values())
        return attractors
