"""Fixtures for lens tests."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import pytest


@dataclass
class MockEntity:
    """Mock Entity for testing lenses."""

    id: str
    name: str = "Test Entity"

    def experiences(self, moment: Any) -> Any:
        """Mock experiences method."""
        return {"experienced": moment}


@dataclass
class MockMoment:
    """Mock Moment for testing lenses."""

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
    """Mock Place for testing lenses."""

    id: str
    atmosphere: str = "warm"

    def contains(self) -> List[Any]:
        """Return contained entities/moments."""
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
