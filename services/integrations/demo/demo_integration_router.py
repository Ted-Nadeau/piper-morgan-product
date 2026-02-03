"""Demo integration router - business logic template

This demonstrates the standard router pattern for integrations.
Routers contain business logic and FastAPI routes.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from .config_service import DemoConfigService


class DemoIntegrationRouter:
    """Demo integration router showing standard patterns

    This is a template showing common integration patterns:
    - Router setup with prefix and tags
    - Config service dependency injection
    - Health check endpoint
    - Example data endpoint
    - Error handling
    """

    def __init__(self, config_service: DemoConfigService):
        """Initialize router with config service

        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.router = APIRouter(prefix="/api/integrations/demo", tags=["demo", "example"])
        self._setup_routes()

    def _setup_routes(self):
        """Define API routes

        This method sets up all the routes for this integration.
        Use @self.router decorators to define routes.
        """

        @self.router.get("/health")
        async def health_check() -> Dict[str, str]:
            """Health check endpoint

            Every integration should have a health check.
            Returns configuration status and basic info.

            Returns:
                Dict with status and service info
            """
            is_configured = self.config.is_configured()
            return {
                "status": "ok" if is_configured else "unconfigured",
                "service": "demo",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        @self.router.get("/echo")
        async def echo(message: str = Query(default="Hello from Demo plugin!")) -> Dict[str, Any]:
            """Echo endpoint - returns the message sent

            Simple endpoint demonstrating:
            - Query parameters
            - JSON response
            - Configuration check

            Args:
                message: Message to echo back

            Returns:
                Dict with echoed message and metadata
            """
            if not self.config.is_configured():
                raise HTTPException(status_code=503, detail="Demo integration not configured")

            return {
                "echo": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "demo",
                "configured": True,
            }

        @self.router.get("/status")
        async def get_status() -> Dict[str, Any]:
            """Status endpoint showing integration details

            Returns:
                Dict with integration configuration and status
            """
            return {
                "integration": "demo",
                "configured": self.config.is_configured(),
                "endpoint": self.config.get_endpoint(),
                "routes": [route.path for route in self.router.routes],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
