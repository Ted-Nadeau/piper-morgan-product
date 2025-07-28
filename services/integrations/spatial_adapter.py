"""
Spatial Adapter Interface
Protocol definition for mapping external system entities to spatial positions.

This interface provides a clean abstraction for converting external system
identifiers (like Slack message IDs, GitHub issue numbers) to integer spatial
positions within Piper Morgan's spatial metaphor system.

The adapter pattern ensures that spatial core domain models remain pure
and independent of external system specifics.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Union


@dataclass
class SpatialPosition:
    """Integer position within spatial metaphor system"""

    position: int
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class SpatialContext:
    """Context information for spatial positioning"""

    territory_id: str
    room_id: str
    path_id: Optional[str] = None
    object_position: Optional[int] = None

    # Spatial characteristics
    attention_level: str = "medium"  # low, medium, high, urgent
    emotional_valence: str = "neutral"  # positive, negative, neutral
    navigation_intent: str = "monitor"  # respond, investigate, monitor, explore

    # External system mapping
    external_system: str = ""
    external_id: str = ""
    external_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.external_context is None:
            self.external_context = {}


class SpatialAdapter(Protocol):
    """
    Protocol for spatial adapters that map external system entities to spatial positions.

    This protocol defines the interface that all spatial adapters must implement,
    ensuring consistent mapping between external systems (Slack, GitHub, etc.)
    and Piper Morgan's spatial metaphor system.
    """

    @abstractmethod
    def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """
        Map external system identifier to spatial position.

        Args:
            external_id: External system identifier (e.g., Slack message timestamp)
            context: Additional context for mapping (e.g., channel, thread info)

        Returns:
            SpatialPosition with integer position and context
        """
        ...

    @abstractmethod
    def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """
        Map spatial position back to external system identifier.

        Args:
            position: Spatial position to reverse map

        Returns:
            External system identifier if mapping exists, None otherwise
        """
        ...

    @abstractmethod
    def store_mapping(self, external_id: str, position: SpatialPosition) -> bool:
        """
        Store mapping between external ID and spatial position.

        Args:
            external_id: External system identifier
            position: Spatial position to map to

        Returns:
            True if mapping stored successfully, False otherwise
        """
        ...

    @abstractmethod
    def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """
        Get spatial context for external system identifier.

        Args:
            external_id: External system identifier

        Returns:
            SpatialContext if mapping exists, None otherwise
        """
        ...


class BaseSpatialAdapter(ABC):
    """
    Base implementation of SpatialAdapter protocol.

    Provides common functionality and enforces the protocol interface.
    Subclasses should implement the abstract methods for specific external systems.
    """

    def __init__(self, system_name: str):
        self.system_name = system_name
        self._position_counter = 0
        self._mappings: Dict[str, SpatialPosition] = {}
        self._contexts: Dict[str, SpatialContext] = {}

    def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """Map external system identifier to spatial position."""
        # Check if mapping already exists
        if external_id in self._mappings:
            return self._mappings[external_id]

        # Create new spatial position
        position = self._create_spatial_position(external_id, context)

        # Store mapping
        self.store_mapping(external_id, position)

        return position

    def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to external system identifier."""
        for external_id, mapped_position in self._mappings.items():
            if mapped_position.position == position.position:
                return external_id
        return None

    def store_mapping(self, external_id: str, position: SpatialPosition) -> bool:
        """Store mapping between external ID and spatial position."""
        try:
            self._mappings[external_id] = position
            return True
        except Exception:
            return False

    def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """Get spatial context for external system identifier."""
        return self._contexts.get(external_id)

    def _create_spatial_position(
        self, external_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Create new spatial position for external identifier."""
        self._position_counter += 1

        # Extract spatial context from external context
        spatial_context = self._extract_spatial_context(context)

        return SpatialPosition(
            position=self._position_counter,
            context={
                "external_id": external_id,
                "external_system": self.system_name,
                "spatial_context": spatial_context,
                **context,
            },
        )

    def _extract_spatial_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract spatial context from external system context."""
        spatial_context = {}

        # Map common spatial concepts
        if "territory_id" in context:
            spatial_context["territory_id"] = context["territory_id"]
        if "room_id" in context:
            spatial_context["room_id"] = context["room_id"]
        if "path_id" in context:
            spatial_context["path_id"] = context["path_id"]
        if "attention_level" in context:
            spatial_context["attention_level"] = context["attention_level"]
        if "emotional_valence" in context:
            spatial_context["emotional_valence"] = context["emotional_valence"]
        if "navigation_intent" in context:
            spatial_context["navigation_intent"] = context["navigation_intent"]

        return spatial_context

    def _store_context(self, external_id: str, context: SpatialContext) -> None:
        """Store spatial context for external identifier."""
        self._contexts[external_id] = context

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings."""
        return {
            "system_name": self.system_name,
            "total_mappings": len(self._mappings),
            "total_contexts": len(self._contexts),
            "next_position": self._position_counter + 1,
        }


class SpatialAdapterRegistry:
    """
    Registry for managing multiple spatial adapters.

    Provides centralized access to adapters for different external systems
    and ensures consistent spatial positioning across the system.
    """

    def __init__(self):
        self._adapters: Dict[str, SpatialAdapter] = {}

    def register_adapter(self, system_name: str, adapter: SpatialAdapter) -> None:
        """Register a spatial adapter for an external system."""
        self._adapters[system_name] = adapter

    def get_adapter(self, system_name: str) -> Optional[SpatialAdapter]:
        """Get spatial adapter for external system."""
        return self._adapters.get(system_name)

    def map_to_position(
        self, system_name: str, external_id: str, context: Dict[str, Any]
    ) -> Optional[SpatialPosition]:
        """Map external ID to spatial position using registered adapter."""
        adapter = self.get_adapter(system_name)
        if adapter:
            return adapter.map_to_position(external_id, context)
        return None

    def map_from_position(self, system_name: str, position: SpatialPosition) -> Optional[str]:
        """Map spatial position to external ID using registered adapter."""
        adapter = self.get_adapter(system_name)
        if adapter:
            return adapter.map_from_position(position)
        return None

    def get_context(self, system_name: str, external_id: str) -> Optional[SpatialContext]:
        """Get spatial context using registered adapter."""
        adapter = self.get_adapter(system_name)
        if adapter:
            return adapter.get_context(external_id)
        return None

    def list_adapters(self) -> List[str]:
        """List all registered adapter system names."""
        return list(self._adapters.keys())

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get statistics about registered adapters."""
        stats = {
            "total_adapters": len(self._adapters),
            "registered_systems": list(self._adapters.keys()),
        }

        # Add individual adapter stats
        for system_name, adapter in self._adapters.items():
            if hasattr(adapter, "get_mapping_stats"):
                stats[f"{system_name}_stats"] = adapter.get_mapping_stats()

        return stats
