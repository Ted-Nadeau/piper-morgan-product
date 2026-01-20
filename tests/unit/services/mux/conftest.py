"""Fixtures for mux module tests."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import pytest


@dataclass
class MockEntity:
    """Mock Entity for testing protocols."""

    id: str
    name: str = "Test Entity"

    def experiences(self, moment: Any) -> Any:
        """Mock experiences method."""
        return {"experienced": moment}


@dataclass
class MockMoment:
    """Mock Moment for testing protocols."""

    id: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def captures(self) -> Dict[str, Any]:
        """Return what this moment captures."""
        return {"policy": [], "process": [], "people": [], "outcomes": []}


@dataclass
class MockPlace:
    """Mock Place for testing protocols."""

    id: str
    atmosphere: str = "warm"

    def contains(self) -> List[Any]:
        """Return contained entities/moments."""
        return []


@dataclass
class MockDualRole:
    """Mock object that satisfies both Entity and Place protocols."""

    id: str
    name: str = "Dual Role Object"
    atmosphere: str = "collaborative"

    def experiences(self, moment: Any) -> Any:
        """Entity behavior: experience a moment."""
        return {"experienced": moment}

    def contains(self) -> List[Any]:
        """Place behavior: contain things."""
        return []


@pytest.fixture
def mock_entity():
    """Provide a mock entity for testing."""
    return MockEntity(id="entity-001")


@pytest.fixture
def mock_moment():
    """Provide a mock moment for testing."""
    return MockMoment(id="moment-001")


@pytest.fixture
def mock_place():
    """Provide a mock place for testing."""
    return MockPlace(id="place-001")


@pytest.fixture
def mock_dual_role():
    """Provide a mock dual-role object for testing role fluidity."""
    return MockDualRole(id="dual-001")
