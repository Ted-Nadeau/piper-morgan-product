"""Service registry for managing service instances."""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Registry for managing service instances and metadata."""

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}

    def register(self, name: str, service: Any, metadata: Optional[Dict] = None) -> None:
        """
        Register a service.

        Args:
            name: Service name (e.g., 'llm', 'intent')
            service: Service instance
            metadata: Optional metadata (version, dependencies, etc.)
        """
        self._services[name] = service
        self._metadata[name] = metadata or {}

        logger.info(f"Registered service '{name}' (type: {type(service).__name__})")

    def get(self, name: str) -> Any:
        """
        Get service by name.

        Args:
            name: Service name

        Returns:
            Service instance

        Raises:
            KeyError: If service not found
        """
        if name not in self._services:
            raise KeyError(
                f"Service '{name}' not found. " f"Available: {list(self._services.keys())}"
            )

        return self._services[name]

    def has(self, name: str) -> bool:
        """Check if service exists."""
        return name in self._services

    def list_services(self) -> List[str]:
        """List all registered service names."""
        return list(self._services.keys())

    def get_metadata(self, name: str) -> Dict:
        """Get service metadata."""
        return self._metadata.get(name, {})

    def clear(self) -> None:
        """Clear all services (for testing/shutdown)."""
        logger.info("Clearing service registry")
        self._services.clear()
        self._metadata.clear()
