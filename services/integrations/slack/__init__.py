"""
Slack Integration Module - Spatial Metaphor Implementation
Provides spatial metaphor-based Slack integration following GitHub pattern.

This module implements Piper Morgan's spatial metaphor approach to Slack workspaces:
- Workspaces as territories/buildings to navigate
- Channels as rooms with specific purposes and inhabitants
- Threads as conversational paths/corridors
- Messages as objects placed in rooms
- @mentions as attention attractors
- Reactions as emotional valence markers

Module exports core components for Slack spatial integration following
the established GitHub integration architecture patterns.
"""

# Configuration and client components (from Cursor's parallel work)
from .config_service import SlackConfigService
from .slack_client import SlackClient

# Core spatial metaphor components (from Code's spatial architecture work)
from .spatial_mapper import SlackSpatialMapper
from .spatial_types import (  # Core spatial domain types; Spatial classification enums
    AttentionAttractor,
    AttentionLevel,
    ConversationalPath,
    EmotionalMarker,
    EmotionalValence,
    ObjectType,
    PathType,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialEvent,
    SpatialObject,
    Territory,
    TerritoryType,
)

# Version information
__version__ = "1.0.0-PM-074"
__author__ = "Piper Morgan Development Team"

# Module metadata
__all__ = [
    # Configuration and client components
    "SlackConfigService",
    "SlackClient",
    # Primary spatial mapper
    "SlackSpatialMapper",
    # Core spatial domain types
    "Territory",
    "Room",
    "ConversationalPath",
    "SpatialObject",
    "AttentionAttractor",
    "EmotionalMarker",
    "SpatialEvent",
    "SpatialCoordinates",
    # Spatial classification enums
    "TerritoryType",
    "RoomPurpose",
    "PathType",
    "ObjectType",
    "AttentionLevel",
    "EmotionalValence",
]

# Module configuration
SPATIAL_METAPHOR_VERSION = "1.0"
SUPPORTED_SLACK_API_VERSION = "2.0"


def get_spatial_mapper() -> SlackSpatialMapper:
    """
    Factory function to create SlackSpatialMapper instance.

    Returns:
        Configured SlackSpatialMapper instance ready for spatial metaphor mapping
    """
    return SlackSpatialMapper()


def get_module_info() -> dict:
    """
    Get module information and capabilities.

    Returns:
        Dictionary containing module metadata and spatial capabilities
    """
    return {
        "module": "slack_spatial_integration",
        "version": __version__,
        "spatial_metaphor_version": SPATIAL_METAPHOR_VERSION,
        "supported_slack_api": SUPPORTED_SLACK_API_VERSION,
        "capabilities": [
            "workspace_territory_mapping",
            "channel_room_mapping",
            "thread_conversational_path_mapping",
            "message_spatial_object_mapping",
            "mention_attention_attractor_mapping",
            "reaction_emotional_marker_mapping",
            "spatial_event_processing",
            "spatial_analytics_tracking",
        ],
        "spatial_types": len(__all__) - 3,  # Exclude config, client, mapper
        "architecture_pattern": "layered_integration_following_github_model",
    }
