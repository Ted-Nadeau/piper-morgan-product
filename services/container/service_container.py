"""Service container for DDD service lifecycle management.

Issue #322 (ARCH-FIX-SINGLETON): The singleton pattern has been removed to enable
horizontal scaling with multiple uvicorn workers. Each worker now gets its own
container instance via FastAPI's lifespan/app.state pattern.

Migration:
- In FastAPI routes: Use `get_container()` from `web/api/dependencies.py`
- In services: Accept dependencies via constructor injection
- See ADR-048 for architectural context
"""

import logging
import warnings
from typing import Any, Optional

from services.container.exceptions import ContainerNotInitializedError, ServiceNotFoundError
from services.container.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


# Legacy singleton state for backward compatibility during migration
# This will be removed in a future release after all tests are updated
_legacy_instance: Optional["ServiceContainer"] = None


class ServiceContainer:
    """
    Application-scoped container for service lifecycle management.

    NOT a singleton (Issue #322) - one instance per application via FastAPI lifespan.
    For tests, create fresh instances directly.

    Usage:
        # In FastAPI routes (preferred):
        from web.api.dependencies import get_container
        container = Depends(get_container)

        # In startup (web/startup.py):
        container = ServiceContainer()
        await container.initialize()
        app.state.service_container = container

        # In services (constructor injection):
        def __init__(self, llm_service=None):
            self._llm = llm_service

        # Get services (after initialization):
        llm_service = container.get_service('llm')
    """

    def __init__(self):
        """Initialize container with fresh registry."""
        global _legacy_instance

        logger.info("Creating ServiceContainer instance")
        self._registry = ServiceRegistry()
        self._initialized = False  # Instance variable, not class variable

        # Track for legacy reset() compatibility (will be removed)
        _legacy_instance = self

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
        DEPRECATED: Reset legacy singleton state (FOR TESTING ONLY).

        Issue #322: The singleton pattern has been removed. In new tests,
        create fresh ServiceContainer() instances instead of calling reset().

        This method is maintained for backward compatibility during migration
        and will be removed in a future release.
        """
        global _legacy_instance

        warnings.warn(
            "ServiceContainer.reset() is deprecated. "
            "Create fresh ServiceContainer() instances in tests instead. "
            "(Issue #322 - ARCH-FIX-SINGLETON)",
            DeprecationWarning,
            stacklevel=2,
        )

        if _legacy_instance is not None:
            if _legacy_instance._initialized:
                _legacy_instance.shutdown()
            _legacy_instance = None
            logger.info("Container reset (testing - deprecated)")
