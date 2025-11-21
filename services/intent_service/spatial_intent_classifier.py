"""
Spatial Intent Classifier
Converts spatial events to intents for enhanced IntentClassifier system.

This module bridges the spatial metaphor system with the intent classification
system, enabling spatial events to flow through the main classification pipeline.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from services.domain.models import Intent, IntentCategory
from services.integrations.slack.spatial_types import (
    AttentionLevel,
    EmotionalValence,
    SpatialCoordinates,
    SpatialEvent,
)

logger = logging.getLogger(__name__)


@dataclass
class SpatialIntentContext:
    """Spatial context for intent classification"""

    room_id: str
    territory_id: str
    attention_level: str
    emotional_valence: str
    navigation_intent: str
    spatial_coordinates: Dict[str, Any]
    user_context: Dict[str, Any]


class SpatialIntentClassifier:
    """Converts spatial events to intents for classification"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_spatial_context_from_event(
        self, spatial_event: SpatialEvent, navigation_intent: str, user_context: Dict[str, Any]
    ) -> SpatialIntentContext:
        """Create spatial context from spatial event"""
        coords = spatial_event.coordinates

        # Determine attention level from event type
        attention_level = self._determine_attention_level(spatial_event)

        # Determine emotional valence from event
        emotional_valence = self._determine_emotional_valence(spatial_event)

        return SpatialIntentContext(
            room_id=coords.room_id,
            territory_id=coords.territory_id,
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            spatial_coordinates={
                "territory_id": coords.territory_id,
                "room_id": coords.room_id,
                "path_id": coords.path_id,
                "object_position": coords.object_position,
            },
            user_context=user_context,
        )

    def create_intent_from_spatial_event(
        self, spatial_event: SpatialEvent, navigation_intent: str, user_context: Dict[str, Any]
    ) -> Intent:
        """Create intent from spatial event for classification"""
        # Create spatial context
        spatial_context = self.create_spatial_context_from_event(
            spatial_event, navigation_intent, user_context
        )

        # Determine action based on event type and navigation intent
        action = self._determine_action_from_spatial_event(spatial_event, navigation_intent)

        # Determine category based on event characteristics
        category = self._determine_category_from_spatial_event(spatial_event, navigation_intent)

        # Build context with spatial information
        context = {
            "original_message": f"Spatial event: {spatial_event.event_type}",
            "spatial_context": {
                "room_id": spatial_context.room_id,
                "territory_id": spatial_context.territory_id,
                "attention_level": spatial_context.attention_level,
                "emotional_valence": spatial_context.emotional_valence,
                "navigation_intent": spatial_context.navigation_intent,
                "spatial_coordinates": spatial_context.spatial_coordinates,
            },
            "user_context": spatial_context.user_context,
            "spatial_event_type": spatial_event.event_type,
            "response_target": {
                "channel_id": spatial_context.room_id,
                "thread_ts": spatial_context.spatial_coordinates.get("path_id"),
                "workspace_id": spatial_context.territory_id,
            },
        }

        # Determine confidence based on event significance
        confidence = self._determine_confidence_from_spatial_event(spatial_event)

        return Intent(
            category=category,
            action=action,
            context=context,
            confidence=confidence,
        )

    def _determine_attention_level(self, spatial_event: SpatialEvent) -> str:
        """Determine attention level from spatial event"""
        if spatial_event.event_type == "attention_attracted":
            return "high"
        elif spatial_event.event_type == "message_placed":
            return "medium"
        elif spatial_event.event_type == "emotional_marker_updated":
            return "medium"
        else:
            return "low"

    def _determine_emotional_valence(self, spatial_event: SpatialEvent) -> str:
        """Determine emotional valence from spatial event"""
        if hasattr(spatial_event, "emotional_marker") and spatial_event.emotional_marker:
            return spatial_event.emotional_marker.valence.value
        elif spatial_event.event_type == "attention_attracted":
            return "positive"  # Mentions are generally positive engagement
        else:
            return "neutral"

    def _determine_action_from_spatial_event(
        self, spatial_event: SpatialEvent, navigation_intent: str
    ) -> str:
        """Determine action from spatial event and navigation intent"""
        if navigation_intent == "respond":
            if spatial_event.event_type == "attention_attracted":
                return "respond_to_mention"
            else:
                return "respond_to_message"
        elif navigation_intent == "investigate":
            return "investigate_spatial_event"
        elif navigation_intent == "monitor":
            return "monitor_spatial_context"
        elif navigation_intent == "explore":
            return "explore_new_room"
        else:
            return "process_spatial_event"

    def _determine_category_from_spatial_event(
        self, spatial_event: SpatialEvent, navigation_intent: str
    ) -> IntentCategory:
        """Determine category from spatial event and navigation intent"""
        if navigation_intent == "respond":
            return IntentCategory.EXECUTION
        elif navigation_intent == "investigate":
            return IntentCategory.ANALYSIS
        elif navigation_intent == "monitor":
            return IntentCategory.QUERY
        elif navigation_intent == "explore":
            return IntentCategory.LEARNING
        else:
            return IntentCategory.CONVERSATION

    def _determine_confidence_from_spatial_event(self, spatial_event: SpatialEvent) -> float:
        """Determine confidence from spatial event significance"""
        significance_map = {
            "routine": 0.6,
            "notable": 0.7,
            "significant": 0.8,
            "critical": 0.9,
        }

        return significance_map.get(spatial_event.significance_level, 0.7)

    def convert_spatial_context_to_dict(
        self, spatial_context: SpatialIntentContext
    ) -> Dict[str, Any]:
        """Convert spatial context to dictionary for IntentClassifier"""
        return {
            "room_id": spatial_context.room_id,
            "territory_id": spatial_context.territory_id,
            "attention_level": spatial_context.attention_level,
            "emotional_valence": spatial_context.emotional_valence,
            "navigation_intent": spatial_context.navigation_intent,
            "spatial_coordinates": spatial_context.spatial_coordinates,
            "user_context": spatial_context.user_context,
        }
