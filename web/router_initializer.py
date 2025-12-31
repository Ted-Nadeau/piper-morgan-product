"""
Router Initialization Factory for web/app.py

Purpose: Centralize and consolidate router mounting logic to eliminate code duplication.
Previously, each router required 5-10 lines of try/catch boilerplate.
This module provides a clean factory interface.

Status: Phase 1 of web/app.py refactoring (Issue #385 - INFR-MAINT-REFACTOR)
Impact: Eliminates 250+ lines of duplicate router-mounting code
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

import structlog

logger = structlog.get_logger()


class RouterInitializer:
    """Factory for initializing and mounting API routers with consistent error handling."""

    # Router configuration: List of (import_path, router_var_name, description, mount_path)
    ROUTERS: List[Tuple[str, str, str, Optional[str]]] = [
        # Routers previously in lifespan()
        ("web.api.routes.standup", "router", "Standup API", "/api/v1/standup"),
        ("web.api.routes.learning", "router", "Learning API", "/api/v1/learning"),
        ("web.api.routes.health", "router", "Health API", "/api/v1/health"),
        ("web.api.routes.api_keys", "router", "API Keys API", "/api/v1/keys"),
        # Routers previously at module level (lines 592-680)
        ("web.api.routes.auth", "router", "Auth API", "/auth"),
        ("web.api.routes.setup", "router", "Setup Wizard API", "/setup"),  # Issue #390
        ("web.api.routes.files", "router", "Files API", "/api/v1/files"),
        ("web.api.routes.documents", "router", "Documents API", "/api/v1/documents"),
        ("services.api.todo_management", "todo_management_router", "Todos API", "/api/v1/todos"),
        ("web.api.routes.lists", "router", "Lists API", "/api/v1/lists"),
        ("web.api.routes.todos", "router", "Todos SEC-RBAC API", "/api/v1/todos"),
        ("web.api.routes.projects", "router", "Projects API", "/api/v1/projects"),
        ("web.api.routes.feedback", "router", "Feedback API", "/api/v1/feedback"),
        ("web.api.routes.knowledge_graph", "router", "Knowledge Graph API", "/api/v1/knowledge"),
        (
            "web.api.routes.integrations",
            "router",
            "Integrations API",
            "/api/v1/integrations",
        ),  # Issue #530
    ]

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

    @staticmethod
    def mount_all_routers(app) -> int:
        """
        Mount all configured routers.

        Args:
            app: FastAPI application instance

        Returns:
            Number of successfully mounted routers
        """
        print("\n🎯 Mounting API Routers...")

        success_count = 0
        total_count = len(RouterInitializer.ROUTERS)

        for import_path, router_var_name, description, mount_path in RouterInitializer.ROUTERS:
            if RouterInitializer.mount_router(app, import_path, router_var_name, description):
                success_count += 1

        print(f"✅ Mounted {success_count}/{total_count} routers\n")

        return success_count

    @staticmethod
    def get_router_count() -> int:
        """Get total number of configured routers."""
        return len(RouterInitializer.ROUTERS)

    @staticmethod
    def print_router_status():
        """Print a summary of all configured routers."""
        print("\n📋 Configured Routers:")
        for import_path, router_var_name, description, mount_path in RouterInitializer.ROUTERS:
            print(f"  - {description}: {import_path}.{router_var_name}")
        print()
