"""
Test Spatial Adapter Interface
Tests the spatial adapter interface and domain models with integer positions.
"""

from unittest.mock import MagicMock

import pytest

from services.domain.models import SpatialContext as DomainSpatialContext
from services.domain.models import SpatialEvent, SpatialObject
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialAdapter,
    SpatialAdapterRegistry,
    SpatialContext,
    SpatialPosition,
)


class TestSpatialPosition:
    """Test spatial position functionality"""

    def test_spatial_position_creation(self):
        """Test creating spatial position with context"""
        # Arrange
        position = 42
        context = {"external_id": "slack_123", "system": "slack"}

        # Act
        spatial_position = SpatialPosition(position=position, context=context)

        # Assert
        assert spatial_position.position == 42
        assert spatial_position.context["external_id"] == "slack_123"
        assert spatial_position.context["system"] == "slack"

    def test_spatial_position_default_context(self):
        """Test spatial position with default context"""
        # Act
        spatial_position = SpatialPosition(position=1)

        # Assert
        assert spatial_position.position == 1
        assert spatial_position.context == {}


class TestSpatialContext:
    """Test spatial context functionality"""

    def test_spatial_context_creation(self):
        """Test creating spatial context"""
        # Arrange
        territory_id = "T123456"
        room_id = "C789012"
        path_id = "1234567890.123456"

        # Act
        context = SpatialContext(
            territory_id=territory_id,
            room_id=room_id,
            path_id=path_id,
            attention_level="high",
            emotional_valence="positive",
            navigation_intent="respond",
        )

        # Assert
        assert context.territory_id == territory_id
        assert context.room_id == room_id
        assert context.path_id == path_id
        assert context.attention_level == "high"
        assert context.emotional_valence == "positive"
        assert context.navigation_intent == "respond"

    def test_spatial_context_defaults(self):
        """Test spatial context with default values"""
        # Act
        context = SpatialContext(territory_id="T123", room_id="C456")

        # Assert
        assert context.territory_id == "T123"
        assert context.room_id == "C456"
        assert context.path_id is None
        assert context.object_position is None
        assert context.attention_level == "medium"
        assert context.emotional_valence == "neutral"
        assert context.navigation_intent == "monitor"
        assert context.external_system == ""
        assert context.external_id == ""
        assert context.external_context == {}


class TestBaseSpatialAdapter:
    """Test base spatial adapter functionality"""

    def test_base_adapter_creation(self):
        """Test creating base spatial adapter"""
        # Act
        adapter = BaseSpatialAdapter("slack")

        # Assert
        assert adapter.system_name == "slack"
        assert adapter._position_counter == 0
        assert adapter._mappings == {}
        assert adapter._contexts == {}

    def test_map_to_position_new_mapping(self):
        """Test mapping external ID to new spatial position"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        external_id = "slack_123"
        context = {
            "territory_id": "T123456",
            "room_id": "C789012",
            "attention_level": "high",
        }

        # Act
        position = adapter.map_to_position(external_id, context)

        # Assert
        assert isinstance(position, SpatialPosition)
        assert position.position == 1  # First position
        assert position.context["external_id"] == external_id
        assert position.context["external_system"] == "slack"
        assert position.context["spatial_context"]["territory_id"] == "T123456"
        assert position.context["spatial_context"]["room_id"] == "C789012"
        assert position.context["spatial_context"]["attention_level"] == "high"

    def test_map_to_position_existing_mapping(self):
        """Test mapping external ID to existing spatial position"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        external_id = "slack_123"
        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act - First mapping
        position1 = adapter.map_to_position(external_id, context)
        # Act - Second mapping (should return same position)
        position2 = adapter.map_to_position(external_id, context)

        # Assert
        assert position1.position == position2.position
        assert position1.context == position2.context

    def test_map_from_position(self):
        """Test mapping spatial position back to external ID"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        external_id = "slack_123"
        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act
        position = adapter.map_to_position(external_id, context)
        mapped_external_id = adapter.map_from_position(position)

        # Assert
        assert mapped_external_id == external_id

    def test_map_from_position_not_found(self):
        """Test mapping non-existent spatial position"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        position = SpatialPosition(position=999, context={})

        # Act
        mapped_external_id = adapter.map_from_position(position)

        # Assert
        assert mapped_external_id is None

    def test_store_mapping(self):
        """Test storing mapping between external ID and spatial position"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        external_id = "slack_123"
        position = SpatialPosition(position=42, context={"test": "data"})

        # Act
        success = adapter.store_mapping(external_id, position)

        # Assert
        assert success is True
        assert adapter._mappings[external_id] == position

    def test_get_context(self):
        """Test getting spatial context for external ID"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        external_id = "slack_123"
        context = SpatialContext(
            territory_id="T123456",
            room_id="C789012",
            attention_level="high",
        )
        adapter._contexts[external_id] = context

        # Act
        retrieved_context = adapter.get_context(external_id)

        # Assert
        assert retrieved_context == context

    def test_get_context_not_found(self):
        """Test getting context for non-existent external ID"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")

        # Act
        context = adapter.get_context("non_existent")

        # Assert
        assert context is None

    def test_get_mapping_stats(self):
        """Test getting mapping statistics"""
        # Arrange
        adapter = BaseSpatialAdapter("slack")
        adapter._mappings["slack_123"] = SpatialPosition(position=1, context={})
        adapter._contexts["slack_123"] = SpatialContext(territory_id="T123", room_id="C456")

        # Act
        stats = adapter.get_mapping_stats()

        # Assert
        assert stats["system_name"] == "slack"
        assert stats["total_mappings"] == 1
        assert stats["total_contexts"] == 1
        assert stats["next_position"] == 1  # No new positions created


class TestSpatialAdapterRegistry:
    """Test spatial adapter registry functionality"""

    def test_registry_creation(self):
        """Test creating spatial adapter registry"""
        # Act
        registry = SpatialAdapterRegistry()

        # Assert
        assert registry._adapters == {}

    def test_register_adapter(self):
        """Test registering spatial adapter"""
        # Arrange
        registry = SpatialAdapterRegistry()
        adapter = BaseSpatialAdapter("slack")

        # Act
        registry.register_adapter("slack", adapter)

        # Assert
        assert registry._adapters["slack"] == adapter

    def test_get_adapter(self):
        """Test getting registered adapter"""
        # Arrange
        registry = SpatialAdapterRegistry()
        adapter = BaseSpatialAdapter("slack")
        registry.register_adapter("slack", adapter)

        # Act
        retrieved_adapter = registry.get_adapter("slack")

        # Assert
        assert retrieved_adapter == adapter

    def test_get_adapter_not_found(self):
        """Test getting non-existent adapter"""
        # Arrange
        registry = SpatialAdapterRegistry()

        # Act
        adapter = registry.get_adapter("non_existent")

        # Assert
        assert adapter is None

    def test_map_to_position_through_registry(self):
        """Test mapping through registry"""
        # Arrange
        registry = SpatialAdapterRegistry()
        adapter = BaseSpatialAdapter("slack")
        registry.register_adapter("slack", adapter)
        external_id = "slack_123"
        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act
        position = registry.map_to_position("slack", external_id, context)

        # Assert
        assert isinstance(position, SpatialPosition)
        assert position.position == 1

    def test_list_adapters(self):
        """Test listing registered adapters"""
        # Arrange
        registry = SpatialAdapterRegistry()
        registry.register_adapter("slack", BaseSpatialAdapter("slack"))
        registry.register_adapter("github", BaseSpatialAdapter("github"))

        # Act
        adapters = registry.list_adapters()

        # Assert
        assert "slack" in adapters
        assert "github" in adapters
        assert len(adapters) == 2

    def test_get_registry_stats(self):
        """Test getting registry statistics"""
        # Arrange
        registry = SpatialAdapterRegistry()
        slack_adapter = BaseSpatialAdapter("slack")
        github_adapter = BaseSpatialAdapter("github")
        registry.register_adapter("slack", slack_adapter)
        registry.register_adapter("github", github_adapter)

        # Act
        stats = registry.get_registry_stats()

        # Assert
        assert stats["total_adapters"] == 2
        assert "slack" in stats["registered_systems"]
        assert "github" in stats["registered_systems"]
        assert "slack_stats" in stats
        assert "github_stats" in stats


class TestDomainSpatialModels:
    """Test domain spatial models with integer positions"""

    def test_spatial_event_creation(self):
        """Test creating spatial event with integer positions"""
        # Arrange
        event_type = "message_posted"
        territory_position = 1
        room_position = 2
        path_position = 3
        object_position = 4

        # Act
        event = SpatialEvent(
            event_type=event_type,
            territory_position=territory_position,
            room_position=room_position,
            path_position=path_position,
            object_position=object_position,
            actor_id="U123456",
            significance_level="significant",
        )

        # Assert
        assert event.event_type == event_type
        assert event.territory_position == territory_position
        assert event.room_position == room_position
        assert event.path_position == path_position
        assert event.object_position == object_position
        assert event.actor_id == "U123456"
        assert event.significance_level == "significant"

    def test_spatial_event_coordinates(self):
        """Test spatial event coordinate methods"""
        # Arrange
        event = SpatialEvent(
            territory_position=1,
            room_position=2,
            path_position=3,
            object_position=4,
        )

        # Act
        coords = event.get_spatial_coordinates()

        # Assert
        assert coords["territory_position"] == 1
        assert coords["room_position"] == 2
        assert coords["path_position"] == 3
        assert coords["object_position"] == 4

    def test_spatial_object_creation(self):
        """Test creating spatial object with integer positions"""
        # Arrange
        object_type = "text_message"
        territory_position = 1
        room_position = 2
        path_position = 3
        object_position = 4

        # Act
        obj = SpatialObject(
            object_type=object_type,
            territory_position=territory_position,
            room_position=room_position,
            path_position=path_position,
            object_position=object_position,
            content="Hello world",
            creator_id="U123456",
        )

        # Assert
        assert obj.object_type == object_type
        assert obj.territory_position == territory_position
        assert obj.room_position == room_position
        assert obj.path_position == path_position
        assert obj.object_position == object_position
        assert obj.content == "Hello world"
        assert obj.creator_id == "U123456"

    def test_spatial_object_context(self):
        """Test spatial object context methods"""
        # Arrange
        obj = SpatialObject(
            object_type="text_message",
            territory_position=1,
            room_position=2,
            attention_attractors=["@user1", "@user2"],
            emotional_markers=["heart", "thumbsup"],
            connected_objects=["obj1", "obj2"],
            interaction_count=5,
        )

        # Act
        context = obj.get_spatial_context()

        # Assert
        assert context["object_type"] == "text_message"
        assert context["attention_level"] == 2
        assert context["emotional_resonance"] == 2
        assert context["connections"] == 2
        assert context["interaction_history"] == 5
        assert "spatial_coordinates" in context

    def test_domain_spatial_context_creation(self):
        """Test creating domain spatial context with integer positions"""
        # Arrange
        territory_position = 1
        room_position = 2
        path_position = 3
        object_position = 4

        # Act
        context = DomainSpatialContext(
            territory_position=territory_position,
            room_position=room_position,
            path_position=path_position,
            object_position=object_position,
            attention_level="high",
            emotional_valence="positive",
            navigation_intent="respond",
            external_system="slack",
            external_id="slack_123",
        )

        # Assert
        assert context.territory_position == territory_position
        assert context.room_position == room_position
        assert context.path_position == path_position
        assert context.object_position == object_position
        assert context.attention_level == "high"
        assert context.emotional_valence == "positive"
        assert context.navigation_intent == "respond"
        assert context.external_system == "slack"
        assert context.external_id == "slack_123"

    def test_domain_spatial_context_coordinates(self):
        """Test domain spatial context coordinate methods"""
        # Arrange
        context = DomainSpatialContext(
            territory_position=1,
            room_position=2,
            path_position=3,
            object_position=4,
        )

        # Act
        coords = context.get_spatial_coordinates()

        # Assert
        assert coords["territory_position"] == 1
        assert coords["room_position"] == 2
        assert coords["path_position"] == 3
        assert coords["object_position"] == 4
