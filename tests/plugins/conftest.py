"""
Pytest fixtures for plugin interface testing
"""

from typing import Any, Dict, Optional

import pytest
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata


@pytest.fixture
def sample_metadata():
    """Sample plugin metadata for testing"""
    return PluginMetadata(
        name="test_plugin",
        version="1.0.0",
        description="Test plugin for validation",
        author="Test Author",
        capabilities=["routes", "webhooks"],
        dependencies=["other_plugin"],
    )


@pytest.fixture
def minimal_plugin():
    """Minimal valid plugin implementation"""

    class MinimalPlugin(PiperPlugin):
        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="minimal",
                version="1.0.0",
                description="Minimal test plugin",
                author="Test",
                capabilities=[],
                dependencies=[],
            )

        def get_router(self) -> Optional[APIRouter]:
            return None

        def is_configured(self) -> bool:
            return True

        async def initialize(self) -> None:
            pass

        async def shutdown(self) -> None:
            pass

        def get_status(self) -> Dict[str, Any]:
            return {"status": "ok"}

    return MinimalPlugin()


@pytest.fixture
def plugin_with_router():
    """Plugin with router implementation"""

    class RouterPlugin(PiperPlugin):
        def __init__(self):
            self._router = APIRouter(prefix="/api/v1/test")

            @self._router.get("/health")
            async def health():
                return {"status": "healthy"}

        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="router_plugin",
                version="1.0.0",
                description="Plugin with routes",
                author="Test",
                capabilities=["routes"],
                dependencies=[],
            )

        def get_router(self) -> Optional[APIRouter]:
            return self._router

        def is_configured(self) -> bool:
            return True

        async def initialize(self) -> None:
            pass

        async def shutdown(self) -> None:
            pass

        def get_status(self) -> Dict[str, Any]:
            return {"router": "active"}

    return RouterPlugin()
