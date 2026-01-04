"""
Service Container - DDD service lifecycle management.

Usage:
    from services.container import ServiceContainer

    # Initialize
    container = ServiceContainer()
    await container.initialize()

    # Get services
    llm_service = container.get_service('llm')

DEPRECATION WARNING (Issue #322 - ARCH-FIX-SINGLETON):
Direct ServiceContainer() instantiation is deprecated and will be removed
when horizontal scaling is enabled. Instead:

1. In FastAPI routes: Use `get_container()` from `web/api/dependencies.py`
   ```python
   from web.api.dependencies import get_container

   @router.get("/example")
   async def example(container: ServiceContainer = Depends(get_container)):
       service = container.get_service("llm")
   ```

2. In services: Accept dependencies via constructor injection
   ```python
   def __init__(self, llm_service=None):
       self._llm = llm_service  # Inject via constructor
   ```

See ADR-048 (adr-048-service-container-lifecycle.md) for details.
"""

from services.container.exceptions import (
    CircularDependencyError,
    ContainerError,
    ContainerNotInitializedError,
    ServiceInitializationError,
    ServiceNotFoundError,
)
from services.container.service_container import ServiceContainer

__all__ = [
    "ServiceContainer",
    "ContainerError",
    "ServiceNotFoundError",
    "ContainerNotInitializedError",
    "ServiceInitializationError",
    "CircularDependencyError",
]
