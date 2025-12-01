"""
User Interface Template Routes

Provides endpoints for rendering UI pages with Jinja2 templates.

Routes:
- GET / - Home page
- GET /standup - Standup UI
- GET /personality-preferences - Personality preferences configuration
- GET /learning - Learning dashboard
- GET /settings - Settings index page
- GET /account - Account settings page
- GET /files - Files management page
- GET /settings/integrations - Integrations management page
- GET /lists - Lists management page
- GET /todos - Todos management page
- GET /projects - Projects management page
- GET /settings/privacy - Privacy & data settings page
- GET /settings/advanced - Advanced settings page

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 411-874)
Now: Extracted to separate router module
"""

from pathlib import Path

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

logger = structlog.get_logger()

# Router configuration
router = APIRouter(tags=["ui", "templates"])


def _get_templates(request: Request):
    """
    Get Jinja2Templates from app state.

    Templates are initialized in WebComponentsInitializationPhase during startup
    and stored in app.state for dependency injection (Phase 4 - INFR-MAINT-REFACTOR).

    Args:
        request: FastAPI Request object with templates in app.state

    Returns:
        Jinja2Templates instance from app.state

    Raises:
        RuntimeError: If templates not initialized in app state
    """
    if not hasattr(request.app.state, "templates"):
        raise RuntimeError("Jinja2Templates not initialized in app state")

    templates = request.app.state.templates
    if templates is None:
        raise RuntimeError("Jinja2Templates initialization failed")

    return templates


def _extract_user_context(request: Request) -> dict:
    """
    Extract user context from request state for template injection.

    Retrieves authenticated user information from request.state (set by auth middleware)
    and returns it as a dict for passing to templates. The navigation component uses this
    to populate the user dropdown menu with the actual username instead of the default
    "user" placeholder.

    Args:
        request: FastAPI Request object with user_claims/user_id in state

    Returns:
        dict with 'user_id', 'username', and 'is_admin' keys for template context
    """
    user_id = getattr(request.state, "user_id", "user")

    # Try to get username from user_claims if available
    username = user_id  # Default to user_id
    user_claims = getattr(request.state, "user_claims", None)
    if user_claims and hasattr(user_claims, "username"):
        username = user_claims.username
    elif user_claims and isinstance(user_claims, dict) and "username" in user_claims:
        username = user_claims["username"]

    # Extract is_admin flag from user claims (SEC-RBAC Phase 3)
    is_admin = False
    if user_claims:
        is_admin = getattr(user_claims, "is_admin", False) or (
            isinstance(user_claims, dict) and user_claims.get("is_admin", False)
        )

    return {"user_id": user_id, "username": username, "is_admin": is_admin}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("home.html", {"request": request, "user": user_context})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serve login page.

    If user is already authenticated, redirect to homepage.
    Otherwise, show login form.

    Issue #393: CORE-UX-AUTH - Login UI
    """
    templates = _get_templates(request)

    # Check if user is already authenticated (has valid user_id in state)
    user_id = getattr(request.state, "user_id", None)
    if user_id and user_id != "user":  # "user" is the default placeholder
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/standup", response_class=HTMLResponse)
async def standup_ui(request: Request):
    """Render standup UI"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("standup.html", {"request": request, "user": user_context})


@router.get("/personality-preferences", response_class=HTMLResponse)
async def personality_preferences_ui(request: Request):
    """Serve the personality preferences interface"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "personality-preferences.html", {"request": request, "user": user_context}
    )


@router.get("/learning", response_class=HTMLResponse)
async def learning_dashboard_ui(request: Request):
    """Serve the learning dashboard interface"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "learning-dashboard.html", {"request": request, "user": user_context}
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_index_ui(request: Request):
    """Serve the settings index page (G2: Settings Index Page)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings-index.html", {"request": request, "user": user_context}
    )


@router.get("/account", response_class=HTMLResponse)
async def account_settings_ui(request: Request):
    """Serve the account settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("account.html", {"request": request, "user": user_context})


@router.get("/files", response_class=HTMLResponse)
async def files_ui(request: Request):
    """Serve the files page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("files.html", {"request": request, "user": user_context})


@router.get("/settings/integrations", response_class=HTMLResponse)
async def integrations_page(request: Request):
    """Integrations management page - Coming soon"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "integrations.html", {"request": request, "user": user_context}
    )


@router.get("/lists", response_class=HTMLResponse)
async def lists_ui(request: Request):
    """Lists management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    lists_data = []
    return templates.TemplateResponse(
        "lists.html", {"request": request, "user": user_context, "lists": lists_data}
    )


@router.get("/todos", response_class=HTMLResponse)
async def todos_ui(request: Request):
    """Todos management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    todos_data = []
    return templates.TemplateResponse(
        "todos.html", {"request": request, "user": user_context, "todos": todos_data}
    )


@router.get("/projects", response_class=HTMLResponse)
async def projects_ui(request: Request):
    """Projects management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    projects_data = []
    return templates.TemplateResponse(
        "projects.html", {"request": request, "user": user_context, "projects": projects_data}
    )


@router.get("/settings/privacy", response_class=HTMLResponse)
async def privacy_settings_ui(request: Request):
    """Serve the privacy & data settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "privacy-settings.html", {"request": request, "user": user_context}
    )


@router.get("/settings/advanced", response_class=HTMLResponse)
async def advanced_settings_ui(request: Request):
    """Serve the advanced settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "advanced-settings.html", {"request": request, "user": user_context}
    )
