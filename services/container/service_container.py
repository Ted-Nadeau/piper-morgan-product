"""Service container with singleton pattern."""

import logging
from typing import Any, Optional

from services.container.exceptions import ContainerNotInitializedError, ServiceNotFoundError
from services.container.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class ServiceContainer:
    """
    Singleton container for service lifecycle management.

    Usage:
        # Get container instance
        container = ServiceContainer()

        # Initialize (first time only)
        container.initialize()

        # Get services
        llm_service = container.get_service('llm')
    """

    _instance: Optional["ServiceContainer"] = None
    _initialized: bool = False

    def __new__(cls):
        """Enforce singleton pattern."""
        if cls._instance is None:
            logger.info("Creating ServiceContainer instance")
            cls._instance = super().__new__(cls)
            cls._instance._registry = ServiceRegistry()
        return cls._instance

    def __init__(self):
        """Initialize instance (only once due to singleton)."""
        # Don't reinitialize
        pass

    async def initialize(self) -> None:
        """
        Initialize all services.

        This should be called once at application startup.
        Safe to call multiple times (idempotent).
        """
        if self._initialized:
            logger.info("Container already initialized")
            return

        logger.info("Initializing service container")

        try:
            # Import here to avoid circular imports
            from services.container.initialization import ServiceInitializer

            # Initialize services (async)
            initializer = ServiceInitializer(self._registry)
            await initializer.initialize_all()

            self._initialized = True
            logger.info(
                f"Container initialized successfully. "
                f"Services: {self._registry.list_services()}"
            )

        except Exception as e:
            logger.error(f"Container initialization failed: {e}", exc_info=True)
            raise

    def is_initialized(self) -> bool:
        """Check if container is initialized."""
        return self._initialized

    def get_service(self, name: str) -> Any:
        """
        Get service by name.

        Args:
            name: Service name (e.g., 'llm', 'intent')

        Returns:
            Service instance

        Raises:
            ContainerNotInitializedError: If container not initialized
            ServiceNotFoundError: If service not found
        """
        if not self._initialized:
            raise ContainerNotInitializedError()

        try:
            return self._registry.get(name)
        except KeyError:
            raise ServiceNotFoundError(name, available_services=self._registry.list_services())

    def has_service(self, name: str) -> bool:
        """Check if service exists."""
        if not self._initialized:
            return False
        return self._registry.has(name)

    def list_services(self) -> list:
        """List all registered services."""
        if not self._initialized:
            return []
        return self._registry.list_services()

    def shutdown(self) -> None:
        """
        Shutdown container and clean up services.

        This should be called during application shutdown.
        """
        if not self._initialized:
            return

        logger.info("Shutting down service container")

        # Could add service-specific shutdown logic here
        # For now, just clear registry
        self._registry.clear()

        self._initialized = False
        logger.info("Container shut down successfully")

    @classmethod
    def reset(cls) -> None:
        """
        Reset singleton instance (FOR TESTING ONLY).

        This allows tests to create fresh containers.
        """
        if cls._instance is not None:
            if cls._instance._initialized:
                cls._instance.shutdown()
            cls._instance = None
            cls._initialized = False
            logger.info("Container reset (testing)")
