"""
Slack Spatial Domain Types
Implements spatial metaphor domain models for Slack integration following GitHub pattern.

Provides type definitions for spatial concepts:
- Territory: Workspaces as navigable territories/buildings
- Room: Channels as rooms with specific purposes and inhabitants
- ConversationalPath: Threads as conversational paths/corridors
- SpatialObject: Messages as objects placed in rooms
- AttentionAttractor: @mentions as attention attractors
- EmotionalValence: Reactions as emotional valence markers
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class TerritoryType(Enum):
    """Types of Slack workspace territories"""

    CORPORATE = "corporate"
    COMMUNITY = "community"
    PROJECT = "project"
    PERSONAL = "personal"
    EXTERNAL = "external"


class RoomPurpose(Enum):
    """Types of channel room purposes"""

    GENERAL = "general"
    ANNOUNCEMENT = "announcement"
    DISCUSSION = "discussion"
    PROJECT_WORK = "project_work"
    COORDINATION = "coordination"
    SOCIAL = "social"
    SUPPORT = "support"
    PRIVATE_MEETING = "private_meeting"


class PathType(Enum):
    """Types of conversational paths (threads)"""

    LINEAR = "linear"
    BRANCHING = "branching"
    CIRCULAR = "circular"
    CONVERGENT = "convergent"


class ObjectType(Enum):
    """Types of spatial objects (messages)"""

    TEXT_MESSAGE = "text_message"
    FILE_DOCUMENT = "file_document"
    IMAGE_ARTIFACT = "image_artifact"
    CODE_BLOCK = "code_block"
    LINK_REFERENCE = "link_reference"
    SYSTEM_NOTIFICATION = "system_notification"


class AttentionLevel(Enum):
    """Levels of attention attraction"""

    AMBIENT = "ambient"  # General message visibility
    FOCUSED = "focused"  # @channel, @here
    DIRECT = "direct"  # @specific_person
    URGENT = "urgent"  # @channel with keywords
    EMERGENCY = "emergency"  # Critical escalation patterns


class EmotionalValence(Enum):
    """Emotional valence markers from reactions"""

    POSITIVE = "positive"  # :thumbsup:, :heart:, :tada:
    NEGATIVE = "negative"  # :thumbsdown:, :x:, :warning:
    NEUTRAL = "neutral"  # :eyes:, :thinking_face:
    HUMOROUS = "humorous"  # :laughing:, :smile:, :wink:
    SUPPORTIVE = "supportive"  # :raised_hands:, :muscle:, :clap:


@dataclass
class SpatialCoordinates:
    """Position within spatial metaphor system"""

    territory_id: str
    room_id: str
    path_id: Optional[str] = None
    object_position: Optional[int] = None

    def to_slack_reference(self) -> Dict[str, str]:
        """Convert to Slack API reference format"""
        reference = {"workspace": self.territory_id, "channel": self.room_id}

        if self.path_id:
            reference["thread_ts"] = self.path_id

        if self.object_position:
            reference["position"] = str(self.object_position)

        return reference


@dataclass
class Territory:
    """Slack workspace as navigable territory/building"""

    id: str
    name: str
    territory_type: TerritoryType
    domain: Optional[str] = None

    # Spatial properties
    total_rooms: int = 0
    active_inhabitants: int = 0
    primary_language: str = "english"
    timezone_region: Optional[str] = None

    # Navigation features
    room_directory: Dict[str, str] = field(default_factory=dict)
    access_permissions: Set[str] = field(default_factory=set)
    navigation_landmarks: List[str] = field(default_factory=list)

    created_at: Optional[datetime] = None

    def get_navigation_context(self) -> Dict[str, Any]:
        """Get context for spatial navigation within territory"""
        return {
            "territory_type": self.territory_type.value,
            "total_rooms": self.total_rooms,
            "active_inhabitants": self.active_inhabitants,
            "primary_language": self.primary_language,
            "landmarks": self.navigation_landmarks,
            "accessible_rooms": len(self.room_directory),
        }


@dataclass
class Room:
    """Slack channel as room with specific purpose and inhabitants"""

    id: str
    name: str
    territory_id: str
    purpose: RoomPurpose

    # Room characteristics
    is_private: bool = False
    description: Optional[str] = None
    topic: Optional[str] = None

    # Inhabitant tracking
    current_inhabitants: Set[str] = field(default_factory=set)
    regular_inhabitants: Set[str] = field(default_factory=set)
    room_moderators: Set[str] = field(default_factory=set)

    # Spatial atmosphere
    activity_level: str = "moderate"  # quiet, moderate, active, busy
    conversation_style: str = "professional"  # casual, professional, technical
    typical_object_types: List[ObjectType] = field(default_factory=list)

    # Navigation
    entrance_restrictions: List[str] = field(default_factory=list)
    connected_rooms: List[str] = field(default_factory=list)

    created_at: Optional[datetime] = None

    def get_room_atmosphere(self) -> Dict[str, Any]:
        """Get atmospheric context for room interactions"""
        return {
            "purpose": self.purpose.value,
            "activity_level": self.activity_level,
            "conversation_style": self.conversation_style,
            "inhabitant_count": len(self.current_inhabitants),
            "privacy_level": "private" if self.is_private else "public",
            "typical_content": [obj_type.value for obj_type in self.typical_object_types],
        }


@dataclass
class ConversationalPath:
    """Slack thread as conversational path/corridor"""

    id: str  # thread_ts in Slack
    room_id: str
    territory_id: str
    path_type: PathType

    # Path characteristics
    origin_object_id: str  # Original message that started thread
    current_length: int = 0
    active_participants: Set[str] = field(default_factory=set)

    # Path dynamics
    conversation_momentum: str = "building"  # building, maintaining, declining, stalled
    topic_coherence: str = "focused"  # focused, drifting, fragmented
    emotional_temperature: str = "neutral"  # cool, neutral, warm, heated

    # Navigation properties
    major_waypoints: List[str] = field(default_factory=list)  # Significant messages
    branching_points: List[str] = field(default_factory=list)  # Topic shifts

    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None

    def get_path_navigation_context(self) -> Dict[str, Any]:
        """Get context for navigating conversational path"""
        return {
            "path_type": self.path_type.value,
            "length": self.current_length,
            "momentum": self.conversation_momentum,
            "coherence": self.topic_coherence,
            "temperature": self.emotional_temperature,
            "active_voices": len(self.active_participants),
            "waypoints": len(self.major_waypoints),
        }


@dataclass
class SpatialObject:
    """Slack message as object placed in spatial environment"""

    id: str  # Message timestamp
    coordinates: SpatialCoordinates
    object_type: ObjectType

    # Object properties
    content: str
    creator_id: str
    size_category: str = "standard"  # minimal, standard, substantial, extensive

    # Spatial relationships
    attention_attractors: List["AttentionAttractor"] = field(default_factory=list)
    emotional_markers: List["EmotionalValence"] = field(default_factory=list)
    connected_objects: List[str] = field(default_factory=list)  # References, replies

    # Context
    placement_time: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    interaction_count: int = 0

    def get_spatial_context(self) -> Dict[str, Any]:
        """Get spatial context for object interaction"""
        return {
            "object_type": self.object_type.value,
            "size_category": self.size_category,
            "attention_level": len(self.attention_attractors),
            "emotional_resonance": len(self.emotional_markers),
            "connections": len(self.connected_objects),
            "interaction_history": self.interaction_count,
        }


@dataclass
class AttentionAttractor:
    """@mention as attention attractor in spatial environment"""

    target_id: str  # User or group being mentioned
    attractor_type: AttentionLevel
    source_object_id: str  # Message containing the mention

    # Attention dynamics
    urgency_indicators: List[str] = field(default_factory=list)
    context_keywords: List[str] = field(default_factory=list)
    expected_response_time: Optional[str] = None

    # Spatial effect
    attention_radius: str = "focused"  # focused, room-wide, territory-wide
    persistence_level: str = "standard"  # brief, standard, sustained

    created_at: Optional[datetime] = None

    def get_attention_context(self) -> Dict[str, Any]:
        """Get context for attention attraction event"""
        return {
            "level": self.attractor_type.value,
            "urgency": len(self.urgency_indicators),
            "radius": self.attention_radius,
            "persistence": self.persistence_level,
            "context_richness": len(self.context_keywords),
        }


@dataclass
class EmotionalMarker:
    """Slack reaction as emotional valence marker"""

    reaction_type: str  # Emoji name
    valence: EmotionalValence
    source_object_id: str  # Message being reacted to
    reactor_id: str  # User who added reaction

    # Emotional context
    intensity: str = "standard"  # subtle, standard, strong
    social_signal: str = "individual"  # individual, social, collective
    timing_significance: str = "normal"  # immediate, delayed, normal

    # Spatial effect
    emotional_radius: str = "local"  # local, room, territory
    contagion_potential: str = "low"  # low, medium, high

    created_at: Optional[datetime] = None

    def get_emotional_context(self) -> Dict[str, Any]:
        """Get context for emotional marker"""
        return {
            "valence": self.valence.value,
            "intensity": self.intensity,
            "social_level": self.social_signal,
            "timing": self.timing_significance,
            "influence_radius": self.emotional_radius,
        }


@dataclass
class SpatialEvent:
    """Spatial event within Slack environment"""

    event_id: str
    event_type: str  # join, leave, message_posted, thread_started, etc.
    coordinates: SpatialCoordinates

    # Event details
    actor_id: Optional[str] = None
    affected_objects: List[str] = field(default_factory=list)
    spatial_changes: Dict[str, Any] = field(default_factory=dict)

    # Event-specific domain objects (optional)
    spatial_object: Optional["SpatialObject"] = None
    attention_attractor: Optional["AttentionAttractor"] = None
    emotional_marker: Optional["EmotionalMarker"] = None
    room: Optional["Room"] = None
    conversational_path: Optional["ConversationalPath"] = None

    # Context
    event_time: Optional[datetime] = None
    significance_level: str = "routine"  # routine, notable, significant, critical

    def get_event_context(self) -> Dict[str, Any]:
        """Get context for spatial event"""
        return {
            "type": self.event_type,
            "significance": self.significance_level,
            "affected_count": len(self.affected_objects),
            "spatial_impact": bool(self.spatial_changes),
        }
