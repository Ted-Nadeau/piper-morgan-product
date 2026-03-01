"""
Router Initialization Factory for web/app.py

Purpose: Centralize and consolidate router mounting logic to eliminate code duplication.
Previously, each router required 5-10 lines of try/catch boilerplate.
This module provides a clean factory interface.

Issue #385 - INFR-MAINT-REFACTOR (original), #719 (dead code cleanup)
"""

import structlog

logger = structlog.get_logger()


class RouterInitializer:
    """Factory for mounting API routers with consistent error handling.

    Usage: RouterInitializer.mount_router(app, "web.api.routes.auth", "router", "Auth API")

    Routers are mounted individually in web/app.py and web/startup.py.
    """

    @staticmethod
    def mount_router(app, import_path: str, router_var_name: str, description: str) -> bool:
        """
        Mount a single router with consistent error handling.

        Args:
            app: FastAPI application instance
            import_path: Module path (e.g., "web.api.routes.auth")
            router_var_name: Variable name in module (e.g., "router")
            description: Human-readable description for logging

        Returns:
            True if mounted successfully, False otherwise
        """
        try:
            # Import the module
            module = __import__(import_path, fromlist=[router_var_name])

            # Get the router from the module
            router = getattr(module, router_var_name)

            # Mount the router
            app.include_router(router)

            # Log success
            logger.info(f"✅ {description} router mounted", module=import_path)
            return True

        except Exception as e:
            logger.error(
                f"⚠️ Failed to mount {description} router",
                module=import_path,
                error=str(e),
            )
            return False
