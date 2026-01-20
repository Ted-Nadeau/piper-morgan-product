"""
Tests for MUX Protocol Definitions.

Phase 1 TDD: Test protocols for Entity, Moment, Place substrates.
These must be @runtime_checkable to support role fluidity.
"""

from typing import Protocol, runtime_checkable

import pytest


class TestEntityProtocol:
    """Tests for EntityProtocol - actors with identity and agency."""

    def test_entity_protocol_is_runtime_checkable(self):
        """EntityProtocol can be used with isinstance()."""
        from services.mux.protocols import EntityProtocol

        # Protocol should have the runtime_checkable marker
        assert hasattr(EntityProtocol, "_is_runtime_protocol")
        assert EntityProtocol._is_runtime_protocol is True

    def test_entity_protocol_isinstance_works(self, mock_entity):
        """isinstance() check works for EntityProtocol."""
        from services.mux.protocols import EntityProtocol

        # MockEntity satisfies EntityProtocol
        assert isinstance(mock_entity, EntityProtocol)

    def test_entity_requires_id_attribute(self):
        """EntityProtocol requires id attribute."""
        from services.mux.protocols import EntityProtocol

        # Create object without id - should NOT satisfy protocol
        class NoId:
            def experiences(self, moment):
                return {}

        no_id_obj = NoId()
        # Should not be an Entity (missing id)
        assert not isinstance(no_id_obj, EntityProtocol)

    def test_entity_requires_experiences_method(self):
        """EntityProtocol requires experiences() method."""
        from services.mux.protocols import EntityProtocol

        # Create object without experiences method
        class NoExperiences:
            id: str = "test"

        no_exp_obj = NoExperiences()
        # Should not be an Entity (missing experiences)
        assert not isinstance(no_exp_obj, EntityProtocol)


class TestMomentProtocol:
    """Tests for MomentProtocol - bounded significant occurrences."""

    def test_moment_protocol_is_runtime_checkable(self):
        """MomentProtocol can be used with isinstance()."""
        from services.mux.protocols import MomentProtocol

        assert hasattr(MomentProtocol, "_is_runtime_protocol")
        assert MomentProtocol._is_runtime_protocol is True

    def test_moment_protocol_isinstance_works(self, mock_moment):
        """isinstance() check works for MomentProtocol."""
        from services.mux.protocols import MomentProtocol

        assert isinstance(mock_moment, MomentProtocol)

    def test_moment_requires_id_attribute(self):
        """MomentProtocol requires id attribute."""
        from services.mux.protocols import MomentProtocol

        class NoId:
            timestamp = None

            def captures(self):
                return {}

        no_id_obj = NoId()
        assert not isinstance(no_id_obj, MomentProtocol)

    def test_moment_requires_timestamp_attribute(self):
        """MomentProtocol requires timestamp attribute."""
        from services.mux.protocols import MomentProtocol

        class NoTimestamp:
            id: str = "test"

            def captures(self):
                return {}

        no_ts_obj = NoTimestamp()
        assert not isinstance(no_ts_obj, MomentProtocol)

    def test_moment_requires_captures_method(self):
        """MomentProtocol requires captures() method."""
        from services.mux.protocols import MomentProtocol

        class NoCaptures:
            id: str = "test"
            timestamp = None

        no_cap_obj = NoCaptures()
        assert not isinstance(no_cap_obj, MomentProtocol)


class TestPlaceProtocol:
    """Tests for PlaceProtocol - contexts where action happens."""

    def test_place_protocol_is_runtime_checkable(self):
        """PlaceProtocol can be used with isinstance()."""
        from services.mux.protocols import PlaceProtocol

        assert hasattr(PlaceProtocol, "_is_runtime_protocol")
        assert PlaceProtocol._is_runtime_protocol is True

    def test_place_protocol_isinstance_works(self, mock_place):
        """isinstance() check works for PlaceProtocol."""
        from services.mux.protocols import PlaceProtocol

        assert isinstance(mock_place, PlaceProtocol)

    def test_place_requires_id_attribute(self):
        """PlaceProtocol requires id attribute."""
        from services.mux.protocols import PlaceProtocol

        class NoId:
            atmosphere: str = "warm"

            def contains(self):
                return []

        no_id_obj = NoId()
        assert not isinstance(no_id_obj, PlaceProtocol)

    def test_place_requires_atmosphere_attribute(self):
        """PlaceProtocol requires atmosphere attribute."""
        from services.mux.protocols import PlaceProtocol

        class NoAtmosphere:
            id: str = "test"

            def contains(self):
                return []

        no_atm_obj = NoAtmosphere()
        assert not isinstance(no_atm_obj, PlaceProtocol)

    def test_place_requires_contains_method(self):
        """PlaceProtocol requires contains() method."""
        from services.mux.protocols import PlaceProtocol

        class NoContains:
            id: str = "test"
            atmosphere: str = "warm"

        no_cont_obj = NoContains()
        assert not isinstance(no_cont_obj, PlaceProtocol)


class TestRoleFluidity:
    """Tests for role fluidity - same object satisfying multiple protocols."""

    def test_dual_role_satisfies_entity_protocol(self, mock_dual_role):
        """Dual-role object satisfies EntityProtocol."""
        from services.mux.protocols import EntityProtocol

        assert isinstance(mock_dual_role, EntityProtocol)

    def test_dual_role_satisfies_place_protocol(self, mock_dual_role):
        """Dual-role object satisfies PlaceProtocol."""
        from services.mux.protocols import PlaceProtocol

        assert isinstance(mock_dual_role, PlaceProtocol)

    def test_same_object_multiple_protocols(self, mock_dual_role):
        """Same object can satisfy Entity AND Place protocols simultaneously."""
        from services.mux.protocols import EntityProtocol, PlaceProtocol

        # This is the key test for role fluidity
        is_entity = isinstance(mock_dual_role, EntityProtocol)
        is_place = isinstance(mock_dual_role, PlaceProtocol)

        assert is_entity and is_place, "Object should satisfy both Entity and Place protocols"

    def test_role_fluidity_preserves_behavior(self, mock_dual_role):
        """Dual-role object preserves both behaviors."""
        from services.mux.protocols import EntityProtocol, PlaceProtocol

        # Can act as Entity
        experience_result = mock_dual_role.experiences({"test": "moment"})
        assert "experienced" in experience_result

        # Can also act as Place
        contained = mock_dual_role.contains()
        assert isinstance(contained, list)
