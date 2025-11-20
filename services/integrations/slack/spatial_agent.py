"""
Slack Spatial Agent - Piper's Spatial Awareness & Navigation
Piper's embodied AI agent for spatial awareness and navigation in Slack environments.

Enables Piper to understand and navigate Slack workspaces as physical spaces,
maintaining spatial awareness and making navigation decisions based on spatial metaphors.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from .config_service import SlackConfigService
from .event_handler import EventProcessingResult, SlackEventHandler
from .spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    EmotionalMarker,
    EmotionalValence,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialObject,
    Territory,
    TerritoryType,
)


class NavigationIntent(Enum):
    """Piper's navigation intentions"""

    EXPLORE = "explore"
    RESPOND = "respond"
    MONITOR = "monitor"
    INVESTIGATE = "investigate"
    RETREAT = "retreat"
    PATROL = "patrol"


class SpatialAwarenessLevel(Enum):
    """Piper's spatial awareness levels"""

    UNKNOWN = "unknown"
    FAMILIAR = "familiar"
    EXPLORED = "explored"
    INTIMATE = "intimate"


@dataclass
class SpatialMemory:
    """Piper's spatial memory of rooms and territories"""

    room_id: str
    room_name: str
    last_visited: datetime
    visit_count: int = 0
    awareness_level: SpatialAwarenessLevel = SpatialAwarenessLevel.UNKNOWN
    emotional_association: EmotionalValence = EmotionalValence.NEUTRAL
    attention_attractors: List[AttentionAttractor] = field(default_factory=list)
    recent_activity: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class NavigationDecision:
    """Piper's navigation decision"""

    intent: NavigationIntent
    target_room: str
    confidence: float
    reasoning: str
    spatial_context: Dict[str, Any] = field(default_factory=dict)
    urgency: float = 0.0


@dataclass
class SpatialAwarenessState:
    """Piper's current spatial awareness state"""

    current_territory: Optional[str] = None
    current_room: Optional[str] = None
    current_path: Optional[str] = None
    spatial_memories: Dict[str, SpatialMemory] = field(default_factory=dict)
    attention_focus: List[AttentionAttractor] = field(default_factory=list)
    emotional_state: EmotionalValence = EmotionalValence.NEUTRAL
    navigation_history: List[NavigationDecision] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)


class SlackSpatialAgent:
    """Piper's spatial awareness and navigation agent"""

    def __init__(self, config_service: SlackConfigService, event_handler: SlackEventHandler):
        self.config_service = config_service
        self.event_handler = event_handler
        self.logger = logging.getLogger(__name__)
        self.spatial_state = SpatialAwarenessState()
        self._navigation_cooldown: Dict[str, datetime] = {}
        self._attention_threshold = 0.7
        self._emotional_threshold = 0.5

    async def process_spatial_event(
        self, event_result: EventProcessingResult
    ) -> NavigationDecision:
        """Process spatial event and determine navigation response"""
        if not event_result.success or not event_result.spatial_event:
            return NavigationDecision(
                intent=NavigationIntent.MONITOR,
                target_room=self.spatial_state.current_room or "general",
                confidence=0.0,
                reasoning="No valid spatial event to process",
            )

        spatial_event = event_result.spatial_event
        coords = spatial_event.coordinates

        # Update spatial awareness
        await self._update_spatial_awareness(spatial_event, event_result)

        # Determine navigation intent based on event
        navigation_decision = await self._determine_navigation_intent(spatial_event, event_result)

        # Update navigation history
        self.spatial_state.navigation_history.append(navigation_decision)

        # Update current position if navigating
        if navigation_decision.confidence > 0.5:
            await self._update_current_position(navigation_decision)

        return navigation_decision

    async def _update_spatial_awareness(
        self, spatial_event: Any, event_result: EventProcessingResult
    ):
        """Update Piper's spatial awareness based on event"""
        coords = spatial_event.coordinates

        # Update current territory if needed
        if coords.territory_id and coords.territory_id != self.spatial_state.current_territory:
            self.spatial_state.current_territory = coords.territory_id

        # Update spatial memory for room
        if coords.room_id:
            room_memory = self.spatial_state.spatial_memories.get(coords.room_id)
            if not room_memory:
                room_memory = SpatialMemory(
                    room_id=coords.room_id,
                    room_name=f"Room {coords.room_id}",
                    last_visited=datetime.now(),
                    visit_count=0,
                )
                self.spatial_state.spatial_memories[coords.room_id] = room_memory

            # Update memory based on event type
            if spatial_event.event_type == "attention_attracted":
                room_memory.attention_attractors.append(spatial_event.attention_attractor)
                room_memory.awareness_level = SpatialAwarenessLevel.EXPLORED
                room_memory.last_visited = datetime.now()
                room_memory.visit_count += 1

                # Add to attention focus
                self.spatial_state.attention_focus.append(spatial_event.attention_attractor)

            elif spatial_event.event_type == "emotional_marker_updated":
                if spatial_event.emotional_marker:
                    room_memory.emotional_association = spatial_event.emotional_marker.valence

            elif spatial_event.event_type == "message_placed":
                room_memory.recent_activity.append(
                    {
                        "type": "message",
                        "timestamp": spatial_event.timestamp,
                        "object_id": coords.object_id,
                    }
                )

                # Keep only recent activity
                cutoff_time = datetime.now() - timedelta(hours=1)
                room_memory.recent_activity = [
                    activity
                    for activity in room_memory.recent_activity
                    if activity["timestamp"] > cutoff_time
                ]

        # Update emotional state
        if event_result.emotional_valence != EmotionalValence.NEUTRAL:
            self.spatial_state.emotional_state = event_result.emotional_valence

        # Update last activity
        self.spatial_state.last_activity = datetime.now()

    async def _determine_navigation_intent(
        self, spatial_event: Any, event_result: EventProcessingResult
    ) -> NavigationDecision:
        """Determine navigation intent based on spatial event"""
        coords = spatial_event.coordinates

        # High attention events (mentions) require immediate response
        if event_result.attention_level == AttentionLevel.URGENT:
            return NavigationDecision(
                intent=NavigationIntent.RESPOND,
                target_room=coords.room_id,
                confidence=0.9,
                reasoning=f"High attention event in room {coords.room_id} requires immediate response",
                urgency=0.9,
            )

        # Emotional events may require investigation
        if event_result.emotional_valence in [EmotionalValence.NEGATIVE, EmotionalValence.POSITIVE]:
            return NavigationDecision(
                intent=NavigationIntent.INVESTIGATE,
                target_room=coords.room_id,
                confidence=0.7,
                reasoning=f"Emotional event ({event_result.emotional_valence.value}) in room {coords.room_id} requires investigation",
                urgency=0.6,
            )

        # New room creation invites exploration
        if spatial_event.event_type == "room_created":
            return NavigationDecision(
                intent=NavigationIntent.EXPLORE,
                target_room=coords.room_id,
                confidence=0.8,
                reasoning=f"New room {coords.room_id} created, exploring new territory",
                urgency=0.5,
            )

        # Check if we should patrol based on activity patterns
        if await self._should_patrol():
            return await self._get_patrol_decision()

        # Default to monitoring current room
        return NavigationDecision(
            intent=NavigationIntent.MONITOR,
            target_room=self.spatial_state.current_room or coords.room_id,
            confidence=0.3,
            reasoning="Monitoring current spatial context",
            urgency=0.1,
        )

    async def _should_patrol(self) -> bool:
        """Determine if Piper should patrol based on activity patterns"""
        # Check if it's been a while since last patrol
        last_patrol = max(
            (
                decision.timestamp
                for decision in self.spatial_state.navigation_history
                if decision.intent == NavigationIntent.PATROL
            ),
            default=datetime.min,
        )

        if datetime.now() - last_patrol > timedelta(minutes=30):
            return True

        # Check if there are unattended attention attractors
        unattended_attractors = [
            attractor
            for attractor in self.spatial_state.attention_focus
            if attractor.level == AttentionLevel.FOCUSED
            and datetime.now() - attractor.timestamp > timedelta(minutes=10)
        ]

        return len(unattended_attractors) > 2

    async def _get_patrol_decision(self) -> NavigationDecision:
        """Get patrol navigation decision"""
        # Find rooms with recent activity but no recent visits
        patrol_candidates = []

        for room_id, memory in self.spatial_state.spatial_memories.items():
            if (
                datetime.now() - memory.last_visited > timedelta(minutes=15)
                and memory.recent_activity
            ):
                patrol_candidates.append((room_id, len(memory.recent_activity)))

        if patrol_candidates:
            # Choose room with most recent activity
            target_room = max(patrol_candidates, key=lambda x: x[1])[0]
            return NavigationDecision(
                intent=NavigationIntent.PATROL,
                target_room=target_room,
                confidence=0.6,
                reasoning=f"Patrolling room {target_room} due to recent activity",
                urgency=0.4,
            )

        # Default patrol to general room
        return NavigationDecision(
            intent=NavigationIntent.PATROL,
            target_room="general",
            confidence=0.4,
            reasoning="General patrol of workspace",
            urgency=0.3,
        )

    async def _update_current_position(self, navigation_decision: NavigationDecision):
        """Update Piper's current position based on navigation decision"""
        self.spatial_state.current_room = navigation_decision.target_room

        # Update room memory
        if navigation_decision.target_room in self.spatial_state.spatial_memories:
            memory = self.spatial_state.spatial_memories[navigation_decision.target_room]
            memory.last_visited = datetime.now()
            memory.visit_count += 1

            # Increase awareness level
            if memory.awareness_level == SpatialAwarenessLevel.UNKNOWN:
                memory.awareness_level = SpatialAwarenessLevel.FAMILIAR
            elif memory.awareness_level == SpatialAwarenessLevel.FAMILIAR:
                memory.awareness_level = SpatialAwarenessLevel.EXPLORED

    def get_spatial_summary(self) -> Dict[str, Any]:
        """Get summary of Piper's spatial awareness"""
        return {
            "current_position": {
                "territory": self.spatial_state.current_territory,
                "room": self.spatial_state.current_room,
                "path": self.spatial_state.current_path,
            },
            "spatial_memories": {
                room_id: {
                    "name": memory.room_name,
                    "awareness_level": memory.awareness_level.value,
                    "visit_count": memory.visit_count,
                    "last_visited": memory.last_visited.isoformat(),
                    "emotional_association": memory.emotional_association.value,
                    "attention_attractors": len(memory.attention_attractors),
                    "recent_activity": len(memory.recent_activity),
                }
                for room_id, memory in self.spatial_state.spatial_memories.items()
            },
            "attention_focus": len(self.spatial_state.attention_focus),
            "emotional_state": self.spatial_state.emotional_state.value,
            "navigation_history": len(self.spatial_state.navigation_history),
            "last_activity": self.spatial_state.last_activity.isoformat(),
        }

    def get_navigation_suggestions(self) -> List[str]:
        """Get navigation suggestions based on current spatial state"""
        suggestions = []

        # Check for high-priority attention attractors
        high_priority = [
            attractor
            for attractor in self.spatial_state.attention_focus
            if attractor.level == AttentionLevel.URGENT
        ]

        if high_priority:
            suggestions.append(
                f"Respond to {len(high_priority)} high-priority attention attractors"
            )

        # Check for rooms with recent activity
        active_rooms = [
            room_id
            for room_id, memory in self.spatial_state.spatial_memories.items()
            if memory.recent_activity
            and datetime.now() - memory.last_visited > timedelta(minutes=10)
        ]

        if active_rooms:
            suggestions.append(f"Check {len(active_rooms)} rooms with recent activity")

        # Check for unexplored rooms
        unexplored_rooms = [
            room_id
            for room_id, memory in self.spatial_state.spatial_memories.items()
            if memory.awareness_level == SpatialAwarenessLevel.UNKNOWN
        ]

        if unexplored_rooms:
            suggestions.append(f"Explore {len(unexplored_rooms)} unfamiliar rooms")

        return suggestions

    def clear_attention_focus(self, room_id: Optional[str] = None):
        """Clear attention focus for specific room or all rooms"""
        if room_id:
            self.spatial_state.attention_focus = [
                attractor
                for attractor in self.spatial_state.attention_focus
                if attractor.coordinates.room_id != room_id
            ]
        else:
            self.spatial_state.attention_focus.clear()
