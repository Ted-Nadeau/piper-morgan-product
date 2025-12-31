"""
Integration Health Check API Routes
Issue #530: ALPHA-SETUP-VERIFY - Integration Health Check Dashboard

Provides API endpoints for checking and testing integration health status.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.health.integration_health_monitor import ComponentStatus

logger = structlog.get_logger()

# Router for integration health endpoints
router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


class IntegrationStatus(BaseModel):
    """Status information for a single integration"""

    name: str
    display_name: str
    status: str  # healthy, degraded, failed, unknown, not_configured
    status_message: str
    last_check: Optional[str] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None
    configure_url: Optional[str] = None
    can_test: bool = True


class IntegrationHealthResponse(BaseModel):
    """Response model for integration health check"""

    overall_status: str
    timestamp: str
    integrations: List[IntegrationStatus]
    healthy_count: int
    total_count: int


class TestConnectionResponse(BaseModel):
    """Response model for testing a single connection"""

    integration: str
    success: bool
    message: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None


# Integration metadata and error guidance
INTEGRATION_REGISTRY = {
    "notion": {
        "display_name": "Notion",
        "icon": "📝",
        "configure_url": "/settings/integrations/notion",
        "errors": {
            "api_key_invalid": {
                "message": "Invalid Notion API key",
                "fix": "Check your Notion integration token in Settings → Integrations → Notion",
            },
            "connection_failed": {
                "message": "Cannot connect to Notion API",
                "fix": "Check your internet connection and Notion service status",
            },
            "permission_denied": {
                "message": "Integration lacks required permissions",
                "fix": "Ensure the integration has access to the required databases in Notion",
            },
        },
    },
    "slack": {
        "display_name": "Slack",
        "icon": "💬",
        "configure_url": "/settings/integrations/slack",
        "errors": {
            "token_expired": {
                "message": "Slack OAuth token has expired",
                "fix": "Re-authorize Slack in Settings → Integrations → Slack",
            },
            "token_invalid": {
                "message": "Invalid Slack token",
                "fix": "Re-connect your Slack workspace",
            },
            "scope_missing": {
                "message": "Missing required Slack permissions",
                "fix": "Re-authorize with updated permissions",
            },
        },
    },
    "github": {
        "display_name": "GitHub",
        "icon": "🐙",
        "configure_url": "/settings/integrations/github",
        "errors": {
            "token_invalid": {
                "message": "Invalid GitHub token",
                "fix": "Update your GitHub personal access token in Settings",
            },
            "rate_limited": {
                "message": "GitHub API rate limit exceeded",
                "fix": "Wait for rate limit reset or use authenticated requests",
            },
            "repo_not_found": {
                "message": "Repository not found or inaccessible",
                "fix": "Check repository permissions and token scope",
            },
        },
    },
    "calendar": {
        "display_name": "Google Calendar",
        "icon": "📅",
        "configure_url": "/settings/integrations/calendar",
        "errors": {
            "auth_failed": {
                "message": "Calendar authentication failed",
                "fix": "Re-authorize Google Calendar access",
            },
            "mcp_not_running": {
                "message": "Calendar MCP server not running",
                "fix": "Start the Google Calendar MCP server",
            },
        },
    },
}


def _get_error_guidance(integration: str, error_type: str) -> tuple[str, Optional[str]]:
    """Get user-friendly error message and fix suggestion"""
    registry = INTEGRATION_REGISTRY.get(integration, {})
    errors = registry.get("errors", {})
    error_info = errors.get(error_type, {})

    message = error_info.get("message", f"Error: {error_type}")
    fix = error_info.get("fix")

    return message, fix


@router.get("/health", response_model=IntegrationHealthResponse)
async def get_integrations_health():
    """
    Get health status of all configured integrations.

    Returns status information for Notion, Slack, GitHub, Calendar, etc.
    Issue #530: ALPHA-SETUP-VERIFY
    """
    try:
        integrations = []
        healthy_count = 0

        # Check each integration
        for integration_id, metadata in INTEGRATION_REGISTRY.items():
            integration_status = await _check_integration_health(integration_id, metadata)
            integrations.append(integration_status)
            if integration_status.status == "healthy":
                healthy_count += 1

        # Determine overall status
        total = len(integrations)
        if healthy_count == total:
            overall = "healthy"
        elif healthy_count > 0:
            overall = "degraded"
        else:
            overall = "unhealthy"

        return IntegrationHealthResponse(
            overall_status=overall,
            timestamp=datetime.utcnow().isoformat(),
            integrations=integrations,
            healthy_count=healthy_count,
            total_count=total,
        )

    except Exception as e:
        logger.error("Failed to check integrations health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/test/{integration_name}", response_model=TestConnectionResponse)
async def test_integration_connection(integration_name: str):
    """
    Test connection to a specific integration.

    Performs an active health check and returns detailed results.
    Issue #530: ALPHA-SETUP-VERIFY
    """
    if integration_name not in INTEGRATION_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown integration: {integration_name}",
        )

    metadata = INTEGRATION_REGISTRY[integration_name]
    start_time = time.time()

    try:
        result = await _test_integration(integration_name)
        latency_ms = (time.time() - start_time) * 1000

        if result["success"]:
            return TestConnectionResponse(
                integration=integration_name,
                success=True,
                message=f"{metadata['display_name']} connection successful",
                latency_ms=round(latency_ms, 2),
            )
        else:
            message, fix = _get_error_guidance(
                integration_name, result.get("error_type", "unknown")
            )
            return TestConnectionResponse(
                integration=integration_name,
                success=False,
                message=message,
                latency_ms=round(latency_ms, 2),
                error=result.get("error"),
                fix_suggestion=fix,
            )

    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        logger.error(f"Integration test failed: {integration_name}", error=str(e))
        return TestConnectionResponse(
            integration=integration_name,
            success=False,
            message=f"Test failed: {str(e)}",
            latency_ms=round(latency_ms, 2),
            error=str(e),
            fix_suggestion="Check logs for details or contact support",
        )


@router.post("/test-all", response_model=List[TestConnectionResponse])
async def test_all_connections():
    """
    Test all configured integrations.

    Issue #530: ALPHA-SETUP-VERIFY
    """
    results = []
    for integration_name in INTEGRATION_REGISTRY.keys():
        try:
            result = await test_integration_connection(integration_name)
            results.append(result)
        except Exception as e:
            results.append(
                TestConnectionResponse(
                    integration=integration_name,
                    success=False,
                    message=f"Test failed: {str(e)}",
                    error=str(e),
                )
            )
    return results


async def _check_integration_health(
    integration_id: str, metadata: Dict[str, Any]
) -> IntegrationStatus:
    """Check health of a specific integration without active testing"""
    try:
        # Try to get cached health status or check configuration
        config_status = await _get_integration_config_status(integration_id)

        if config_status == "not_configured":
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status="not_configured",
                status_message="Not configured",
                configure_url=metadata.get("configure_url"),
                can_test=False,
            )

        # For configured integrations, return last known status
        # In production, this would check the IntegrationHealthMonitor
        return IntegrationStatus(
            name=integration_id,
            display_name=metadata["display_name"],
            status="unknown",
            status_message="Click 'Test' to check connection",
            configure_url=metadata.get("configure_url"),
            can_test=True,
        )

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} health", error=str(e))
        return IntegrationStatus(
            name=integration_id,
            display_name=metadata["display_name"],
            status="unknown",
            status_message="Status unknown",
            error=str(e),
            configure_url=metadata.get("configure_url"),
            can_test=True,
        )


async def _get_integration_config_status(integration_id: str) -> str:
    """Check if an integration is configured by checking environment variables"""
    import os

    try:
        # Check integration-specific environment variables
        if integration_id == "notion":
            if os.environ.get("NOTION_API_TOKEN") or os.environ.get("NOTION_API_KEY"):
                return "configured"
        elif integration_id == "slack":
            if os.environ.get("SLACK_BOT_TOKEN"):
                return "configured"
        elif integration_id == "github":
            if os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_ACCESS_TOKEN"):
                return "configured"
        elif integration_id == "calendar":
            # Calendar uses MCP or Google Calendar credentials
            if os.environ.get("GOOGLE_CALENDAR_CREDENTIALS") or os.environ.get("MCP_ENABLED"):
                return "configured"

        return "not_configured"

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} config", error=str(e))
        return "unknown"


async def _test_integration(integration_id: str) -> Dict[str, Any]:
    """Perform active connection test for an integration"""
    try:
        if integration_id == "notion":
            return await _test_notion()
        elif integration_id == "slack":
            return await _test_slack()
        elif integration_id == "github":
            return await _test_github()
        elif integration_id == "calendar":
            return await _test_calendar()
        else:
            return {"success": False, "error": f"Unknown integration: {integration_id}"}

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_notion() -> Dict[str, Any]:
    """Test Notion API connection"""
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

        router = NotionIntegrationRouter()
        if await router.test_connection():
            return {"success": True}
        else:
            return {"success": False, "error_type": "api_key_invalid"}
    except ImportError:
        return {"success": False, "error": "Notion integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_slack() -> Dict[str, Any]:
    """Test Slack API connection"""
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        router = SlackIntegrationRouter()
        result = await router.test_auth()
        if result.get("ok"):
            return {"success": True}
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "error_type": "token_invalid",
            }
    except ImportError:
        return {"success": False, "error": "Slack integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_github() -> Dict[str, Any]:
    """Test GitHub API connection"""
    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter

        router = GitHubIntegrationRouter()
        result = router.test_connection()
        if result.get("authenticated"):
            return {"success": True}
        else:
            return {
                "success": False,
                "error": result.get("error", "Not authenticated"),
                "error_type": "token_invalid",
            }
    except ImportError:
        return {"success": False, "error": "GitHub integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_calendar() -> Dict[str, Any]:
    """Test Google Calendar MCP connection"""
    try:
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        router = CalendarIntegrationRouter()
        result = await router.health_check()
        if result.get("status") == "healthy":
            return {"success": True}
        else:
            return {
                "success": False,
                "error": result.get("error", "MCP not healthy"),
                "error_type": "mcp_not_running",
            }
    except ImportError:
        return {"success": False, "error": "Calendar integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
