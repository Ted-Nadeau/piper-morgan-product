"""Performance test fixtures"""

import pytest


@pytest.fixture
def performance_threshold():
    """Performance thresholds for tests"""
    return {"overhead_ms": 0.05, "startup_ms": 2000, "memory_mb": 50, "concurrency_ms": 100}
