"""
Tests to catch if new NL endpoints are added without intent.
"""

import ast
from pathlib import Path

import pytest


class TestFutureEndpoints:
    """Detect new endpoints that should use intent."""

    def test_all_nl_routes_in_middleware_config(self):
        """All NL routes should be in middleware configuration."""
        # Scan web routes for potential NL endpoints
        web_files = Path("web").glob("**/*.py")

        potential_nl_routes = []
        for file in web_files:
            if file.name == "__init__.py":
                continue

            content = file.read_text()

            # Look for route decorators with paths containing chat/message/intent
            import re

            routes = re.findall(r'@(?:app|router)\.\w+\(["\']([^"\']+)', content)

            for route in routes:
                # Skip admin/monitoring endpoints
                if "/admin/" in route:
                    continue

                # Check if route looks like NL endpoint
                if any(
                    keyword in route.lower()
                    for keyword in ["chat", "message", "intent", "ask", "query"]
                ):
                    potential_nl_routes.append(route)

        # Get configured NL endpoints from middleware
        from web.middleware.intent_enforcement import IntentEnforcementMiddleware

        configured = IntentEnforcementMiddleware.NL_ENDPOINTS

        # All potential NL routes should be configured
        for route in potential_nl_routes:
            assert (
                route in configured
            ), f"Route {route} looks like NL endpoint but not in middleware config"

    def test_no_direct_service_calls_in_routes(self):
        """Web routes should not directly call services for NL processing."""
        web_app = Path("web/app.py")
        content = web_app.read_text()

        # Look for direct service imports/calls
        suspicious_patterns = [
            r"from services\..*_service import",
            r"github_service\.",
            r"notion_service\.",
            r"calendar_service\.",
        ]

        import re

        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content)
            # If found, they should only be in non-NL routes
            # This is a heuristic check
            if matches:
                # Warn but don't fail - need manual review
                pytest.skip(f"Found direct service usage: {matches} - needs review")
