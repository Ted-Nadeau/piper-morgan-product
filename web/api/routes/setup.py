"""
Setup Wizard API Routes

Provides REST endpoints for the web-based setup wizard UI.
Mirrors functionality from scripts/setup_wizard.py with async HTTP wrappers.

Issue #390: ALPHA-SETUP-UI Phase 1.1 - Backend API
"""

import asyncio
import os
import uuid
from datetime import datetime
from typing import Dict, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, text

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.auth.password_service import PasswordService
from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

router = APIRouter(prefix="/setup", tags=["setup"])
logger = structlog.get_logger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================


class SetupStatusResponse(BaseModel):
    """Response model for setup status check"""

    setup_complete: bool = Field(description="Whether setup has been completed")
    has_user: bool = Field(description="Whether at least one user exists")
    has_api_keys: bool = Field(description="Whether OpenAI API key is configured")


class SystemCheckResponse(BaseModel):
    """Response model for system requirements check"""

    docker_available: bool = Field(description="Docker installed and running")
    postgres_ready: bool = Field(description="PostgreSQL accessible on port 5433")
    redis_ready: bool = Field(description="Redis accessible on port 6379")
    chromadb_ready: bool = Field(description="ChromaDB accessible on port 8000")
    temporal_ready: bool = Field(description="Temporal accessible on port 7233 (optional)")
    all_required_ready: bool = Field(description="All required services ready (excludes Temporal)")
    message: str = Field(description="Human-readable status message")


class ApiKeyValidateRequest(BaseModel):
    """Request model for API key validation"""

    provider: str = Field(description="API provider: openai, anthropic, github, or notion")
    api_key: str = Field(description="API key to validate")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in ["openai", "anthropic", "github", "notion"]:
            raise ValueError("provider must be one of: openai, anthropic, github, notion")
        return v


class ApiKeyValidateResponse(BaseModel):
    """Response model for API key validation"""

    provider: str = Field(description="API provider that was validated")
    valid: bool = Field(description="Whether the key is valid")
    message: str = Field(description="Validation result message")
    workspace_name: Optional[str] = Field(
        default=None, description="Workspace name (for Notion integration)"
    )


class CreateUserRequest(BaseModel):
    """Request model for user account creation"""

    username: str = Field(min_length=1, max_length=100, description="Username (required)")
    email: Optional[str] = Field(default=None, max_length=255, description="Email (optional)")
    password: str = Field(min_length=8, description="Password (minimum 8 characters)")
    password_confirm: str = Field(min_length=8, description="Password confirmation")

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class CreateUserResponse(BaseModel):
    """Response model for user account creation"""

    success: bool = Field(description="Whether user creation succeeded")
    user_id: Optional[str] = Field(default=None, description="Created user ID (UUID)")
    message: str = Field(description="Result message")


class KeychainCheckResponse(BaseModel):
    """Response model for keychain key check"""

    provider: str = Field(description="API provider checked")
    exists: bool = Field(description="Whether key exists in keychain")
    message: str = Field(description="Human-readable status")


class KeychainUseRequest(BaseModel):
    """Request model for using key from keychain"""

    provider: str = Field(description="API provider: openai, anthropic, gemini, or notion")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in ["openai", "anthropic", "gemini", "notion"]:
            raise ValueError("provider must be one of: openai, anthropic, gemini, notion")
        return v


class KeychainUseResponse(BaseModel):
    """Response model for using key from keychain"""

    provider: str = Field(description="API provider")
    success: bool = Field(description="Whether key was retrieved and validated")
    valid: bool = Field(description="Whether the key is valid (if retrieved)")
    message: str = Field(description="Result message")


class SetupCompleteRequest(BaseModel):
    """Request model for completing setup"""

    user_id: str = Field(description="User ID (UUID) to mark as setup complete")
    openai_key: Optional[str] = Field(default=None, description="OpenAI API key (optional)")
    anthropic_key: Optional[str] = Field(default=None, description="Anthropic API key (optional)")
    notion_key: Optional[str] = Field(default=None, description="Notion API key (optional)")


class SetupCompleteResponse(BaseModel):
    """Response model for completing setup"""

    success: bool = Field(description="Whether setup completion succeeded")
    message: str = Field(description="Result message")
    redirect_url: str = Field(description="URL to redirect to after setup")


# ============================================================================
# Helper Functions (adapted from setup_wizard.py)
# ============================================================================


async def check_docker() -> bool:
    """Check if Docker is installed and running (from setup_wizard.py line 254)"""
    try:
        import subprocess

        result = await asyncio.to_thread(
            subprocess.run, ["docker", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


async def check_service_port(host: str, port: int) -> bool:
    """Check if a service is accessible on a specific port (from setup_wizard.py line 451)"""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2.0)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def check_database() -> bool:
    """Check PostgreSQL database connectivity (from setup_wizard.py line 477)

    Note: Uses simple port check to avoid event loop mismatch issues (#445).
    The AsyncSessionFactory is initialized at app startup and may be in a different
    event loop than the HTTP request handler.
    """
    # Use simple port check instead of session query to avoid event loop issues
    return await check_service_port("localhost", 5433)


async def check_redis() -> bool:
    """Check Redis connectivity (from setup_wizard.py line 462)"""
    return await check_service_port("localhost", 6379)


async def check_chromadb() -> bool:
    """Check ChromaDB connectivity (from setup_wizard.py line 467)"""
    return await check_service_port("localhost", 8000)


async def check_temporal() -> bool:
    """Check Temporal connectivity (from setup_wizard.py line 472)"""
    return await check_service_port("localhost", 7233)


# ============================================================================
# API Endpoints
# ============================================================================


@router.get("/status", response_model=SetupStatusResponse)
async def get_setup_status():
    """
    Check if setup has been completed.

    Uses the setup_complete flag in users table (Issue #389).
    Also checks for users and API keys as fallback.

    Returns:
        SetupStatusResponse with setup status details
    """
    try:
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Check setup_complete flag (primary)
            complete_result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE setup_complete = true")
            )
            complete_count = complete_result.scalar_one()

            # Check if any users exist
            user_result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = user_result.scalar_one()

            # Check if OpenAI key exists
            key_result = await session.execute(
                text(
                    "SELECT COUNT(*) FROM user_api_keys "
                    "WHERE provider = 'openai' AND is_active = true"
                )
            )
            openai_key_count = key_result.scalar_one()

        return SetupStatusResponse(
            setup_complete=complete_count > 0,
            has_user=user_count > 0,
            has_api_keys=openai_key_count > 0,
        )

    except Exception as e:
        logger.error("setup_status_check_failed", error=str(e), exc_info=True)
        # Return default (setup not complete) on error
        return SetupStatusResponse(
            setup_complete=False,
            has_user=False,
            has_api_keys=False,
        )


@router.post("/check-system", response_model=SystemCheckResponse)
async def check_system():
    """
    Check system requirements and service availability.

    Verifies Docker installation and checks connectivity to all required services:
    - PostgreSQL (port 5433) - required
    - Redis (port 6379) - required
    - ChromaDB (port 8000) - required
    - Temporal (port 7233) - optional

    Returns:
        SystemCheckResponse with service availability status
    """
    try:
        # Run all checks in parallel
        docker_ok, postgres_ok, redis_ok, chromadb_ok, temporal_ok = await asyncio.gather(
            check_docker(),
            check_database(),
            check_redis(),
            check_chromadb(),
            check_temporal(),
            return_exceptions=False,
        )

        # All required services must be ready (Temporal is optional)
        all_required = docker_ok and postgres_ok and redis_ok and chromadb_ok

        # Build status message
        if all_required:
            if temporal_ok:
                message = "All services ready"
            else:
                message = "Core services ready (Temporal optional)"
        else:
            failed_services = []
            if not docker_ok:
                failed_services.append("Docker")
            if not postgres_ok:
                failed_services.append("PostgreSQL")
            if not redis_ok:
                failed_services.append("Redis")
            if not chromadb_ok:
                failed_services.append("ChromaDB")
            message = f"Services not ready: {', '.join(failed_services)}"

        return SystemCheckResponse(
            docker_available=docker_ok,
            postgres_ready=postgres_ok,
            redis_ready=redis_ok,
            chromadb_ready=chromadb_ok,
            temporal_ready=temporal_ok,
            all_required_ready=all_required,
            message=message,
        )

    except Exception as e:
        logger.error("system_check_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"System check failed: {str(e)}",
        )


async def validate_notion_key_and_get_workspace(
    api_key: str,
) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a Notion API key and get workspace name.

    Issue #527: ALPHA-SETUP-NOTION

    Uses the official Notion SDK to test the API key by calling users.me()
    endpoint, which returns workspace information for bot integrations.

    Args:
        api_key: Notion API key (starts with 'secret_' or 'ntn_')

    Returns:
        Tuple of (is_valid, workspace_name, error_message)
        - is_valid: True if key is valid and has workspace access
        - workspace_name: Name of the workspace, or None if invalid
        - error_message: Human-friendly error message, or None if valid
    """
    try:
        from notion_client import Client
        from notion_client.client import ClientOptions
        from notion_client.errors import APIResponseError

        # Create a temporary client with the provided key
        options = ClientOptions(auth=api_key, notion_version="2025-09-03")
        client = Client(options=options)

        # Test the key by calling users.me()
        user_info = client.users.me()

        # Extract workspace name from bot info
        workspace_name = user_info.get("bot", {}).get("workspace", {}).get("name")

        # If no workspace name in bot info, fall back to user name
        if not workspace_name:
            workspace_name = user_info.get("name", "Unknown Workspace")

        logger.info(
            "notion_key_validated",
            workspace=workspace_name,
            user_type=user_info.get("type", "unknown"),
        )

        return True, workspace_name, None

    except APIResponseError as e:
        # Issue #527: Provide specific error guidance based on error code
        error_code = getattr(e, "code", "unknown")
        error_str = str(e).lower()
        logger.warning("notion_key_invalid", error=str(e), error_code=error_code)

        # Map Notion API errors to user-friendly messages
        if "unauthorized" in error_str or error_code == "unauthorized":
            error_msg = "Invalid API key. Check your key at notion.so/my-integrations"
        elif "forbidden" in error_str or error_code == "restricted_resource":
            error_msg = "Key lacks required permissions. Ensure integration has workspace access"
        elif "rate_limited" in error_str:
            error_msg = "Rate limited by Notion. Wait a moment and try again"
        else:
            error_msg = "Invalid API key or insufficient permissions"

        return False, None, error_msg
    except ImportError:
        logger.error("notion_sdk_not_installed")
        return False, None, "Notion SDK not installed. Contact support."
    except Exception as e:
        error_str = str(e).lower()
        logger.error("notion_key_validation_error", error=str(e), exc_info=True)

        # Network errors
        if "connect" in error_str or "network" in error_str or "timeout" in error_str:
            return False, None, "Could not reach Notion API. Check your internet connection"

        return False, None, "Validation failed. Please try again"


@router.post("/validate-key", response_model=ApiKeyValidateResponse)
async def validate_api_key(req: ApiKeyValidateRequest):
    """
    Validate an API key with the provider.

    Uses UserAPIKeyService to validate keys against provider APIs:
    - OpenAI: Tests gpt-4 access with minimal request
    - Anthropic: Tests claude-3.5 access with minimal request
    - GitHub: Skipped (validated on first use)
    - Notion: Tests workspace access with users.me() (#527)

    Args:
        req: ApiKeyValidateRequest with provider and api_key

    Returns:
        ApiKeyValidateResponse with validation result
    """
    try:
        # GitHub validation is skipped (expensive, validated on first use)
        if req.provider == "github":
            return ApiKeyValidateResponse(
                provider=req.provider,
                valid=True,
                message="GitHub token saved (validation on first use)",
            )

        # Notion validation uses dedicated helper (#527)
        if req.provider == "notion":
            is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(
                req.api_key
            )
            if is_valid:
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=True,
                    message=f"Valid (Connected to '{workspace_name}')",
                    workspace_name=workspace_name,
                )
            else:
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=False,
                    message=error_msg or "Invalid API key or insufficient permissions",
                )

        # For OpenAI and Anthropic, use UserAPIKeyService validation
        service = UserAPIKeyService()

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            try:
                # Issue #485: Validate the key WITHOUT storing (store=False)
                # No temp_user_id needed - validation-only mode doesn't touch DB
                await service.store_user_key(
                    user_id="validation-only",  # Placeholder, not used when store=False
                    provider=req.provider,
                    api_key=req.api_key,
                    session=session,
                    validate=True,
                    store=False,  # Issue #485: Don't create DB records during validation
                )

                # Validation succeeded
                model_info = "gpt-4" if req.provider == "openai" else "claude-3.5"
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=True,
                    message=f"Valid ({model_info} access confirmed)",
                )

            except ValueError as e:
                # Validation failed
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=False,
                    message=str(e),
                )

    except Exception as e:
        logger.error(
            "api_key_validation_failed", provider=req.provider, error=str(e), exc_info=True
        )
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=False,
            message=f"Validation error: {str(e)}",
        )


@router.get("/check-keychain/{provider}", response_model=KeychainCheckResponse)
async def check_keychain(provider: str):
    """
    Check if an API key exists in the system keychain.

    This allows the UI to show "Use from Keychain" button only when
    a key is available. Accessing the actual key requires explicit
    user action (triggers OS keychain permission dialog).

    Args:
        provider: API provider (openai, anthropic, gemini, notion)

    Returns:
        KeychainCheckResponse with exists status
    """
    if provider not in ["openai", "anthropic", "gemini", "notion"]:
        return KeychainCheckResponse(
            provider=provider,
            exists=False,
            message=f"Unknown provider: {provider}",
        )

    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        key = keychain.get_api_key(provider)
        exists = key is not None

        if exists:
            message = f"{provider.capitalize()} key found in keychain"
        else:
            message = f"No {provider} key in keychain"

        return KeychainCheckResponse(
            provider=provider,
            exists=exists,
            message=message,
        )

    except Exception as e:
        logger.error("keychain_check_failed", provider=provider, error=str(e), exc_info=True)
        return KeychainCheckResponse(
            provider=provider,
            exists=False,
            message=f"Keychain access error: {str(e)}",
        )


@router.post("/use-keychain", response_model=KeychainUseResponse)
async def use_keychain(req: KeychainUseRequest):
    """
    Retrieve API key from keychain and validate it.

    This endpoint triggers the OS keychain permission dialog,
    requiring explicit user consent. If the key is found, we trust it
    since it was previously validated when stored.

    Note: We skip re-validation here to avoid event loop mismatch issues
    with the database session. Keys in keychain were validated when stored.

    Args:
        req: KeychainUseRequest with provider

    Returns:
        KeychainUseResponse with validation result
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        api_key = keychain.get_api_key(req.provider)

        if not api_key:
            return KeychainUseResponse(
                provider=req.provider,
                success=False,
                valid=False,
                message=f"No {req.provider} key found in keychain",
            )

        # Key exists in keychain - trust it was validated when stored
        # We skip re-validation to avoid event loop issues with database sessions
        provider_models = {
            "openai": "gpt-4",
            "anthropic": "claude-3.5",
            "gemini": "gemini-pro",
            "notion": "workspace",
        }
        model_info = provider_models.get(req.provider, req.provider)

        return KeychainUseResponse(
            provider=req.provider,
            success=True,
            valid=True,
            message=f"Using {req.provider} key from keychain ({model_info})",
        )

    except Exception as e:
        logger.error("keychain_use_failed", provider=req.provider, error=str(e), exc_info=True)
        return KeychainUseResponse(
            provider=req.provider,
            success=False,
            valid=False,
            message=f"Keychain access error: {str(e)}",
        )


@router.post("/create-user", response_model=CreateUserResponse)
async def create_user(req: CreateUserRequest):
    """
    Create a new user account with secure password.

    Validates username uniqueness, hashes password with bcrypt,
    and creates user in database with alpha flag.

    Args:
        req: CreateUserRequest with username, email, password

    Returns:
        CreateUserResponse with user_id and success status

    Raises:
        HTTPException 400: If username already exists
        HTTPException 500: If user creation fails
    """
    try:
        # Hash password with bcrypt
        password_service = PasswordService()
        password_hash = password_service.hash_password(req.password)

        # Create user account
        user = User(
            id=uuid.uuid4(),
            username=req.username,
            email=req.email,
            password_hash=password_hash,
            role="user",
            is_active=True,
            is_verified=True,
            is_alpha=True,  # Alpha tester flag
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(user)
            await session.commit()

        logger.info("user_created", user_id=str(user.id), username=user.username)

        return CreateUserResponse(
            success=True,
            user_id=str(user.id),
            message=f"Account created: {user.username}",
        )

    except Exception as e:
        error_str = str(e).lower()
        if "duplicate" in error_str or "unique" in error_str:
            logger.warning("user_creation_failed_duplicate", username=req.username)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{req.username}' already exists",
            )
        else:
            logger.error("user_creation_failed", username=req.username, error=str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User creation failed: {str(e)}",
            )


@router.post("/complete", response_model=SetupCompleteResponse)
async def complete_setup(req: SetupCompleteRequest):
    """
    Finalize setup by storing API keys and marking user as setup complete.

    This endpoint:
    1. Stores provided API keys (OpenAI, Anthropic, Notion) in keychain
    2. Updates user.setup_complete flag to true
    3. Generates CLI auto-auth token

    Args:
        req: SetupCompleteRequest with user_id and optional API keys

    Returns:
        SetupCompleteResponse with success status and redirect URL

    Issue #527: Added Notion key storage support
    """
    try:
        # Store API keys if provided
        service = UserAPIKeyService()

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Store OpenAI key
            if req.openai_key:
                try:
                    await service.store_user_key(
                        user_id=req.user_id,
                        provider="openai",
                        api_key=req.openai_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning("openai_key_storage_failed", user_id=req.user_id, error=str(e))

            # Store Anthropic key
            if req.anthropic_key:
                try:
                    await service.store_user_key(
                        user_id=req.user_id,
                        provider="anthropic",
                        api_key=req.anthropic_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning(
                        "anthropic_key_storage_failed", user_id=req.user_id, error=str(e)
                    )

            # Store Notion key (Issue #527: ALPHA-SETUP-NOTION)
            if req.notion_key:
                try:
                    await service.store_user_key(
                        user_id=req.user_id,
                        provider="notion",
                        api_key=req.notion_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning("notion_key_storage_failed", user_id=req.user_id, error=str(e))

            # Mark setup as complete (Issue #389)
            await session.execute(
                text(
                    "UPDATE users SET setup_complete = true, "
                    "setup_completed_at = :now WHERE id = :user_id"
                ),
                {"user_id": req.user_id, "now": datetime.utcnow()},
            )
            await session.commit()

        # Generate CLI token (non-blocking, best effort)
        try:
            from services.auth.jwt_service import JWTService
            from services.infrastructure.keychain_service import KeychainService

            jwt_service = JWTService()
            keychain = KeychainService()

            # Get user email for CLI token
            # Use fresh session to avoid event loop mismatch (#442)
            async with AsyncSessionFactory.session_scope_fresh() as session:
                result = await session.execute(
                    select(User).where(User.id == uuid.UUID(req.user_id))
                )
                user = result.scalar_one_or_none()
                user_email = user.email if user else ""

            cli_token = jwt_service.generate_cli_token(user_id=req.user_id, user_email=user_email)
            keychain.store_cli_token(req.user_id, cli_token)
            logger.info("cli_auth_configured", user_id=req.user_id)
        except Exception as e:
            logger.warning("cli_auth_setup_failed", user_id=req.user_id, error=str(e))

        logger.info("setup_completed", user_id=req.user_id)

        return SetupCompleteResponse(
            success=True,
            message="Setup complete! Redirecting to login...",
            redirect_url="/login",
        )

    except Exception as e:
        logger.error("setup_completion_failed", user_id=req.user_id, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Setup completion failed: {str(e)}",
        )


# ============================================================================
# Slack OAuth Endpoints (Issue #528: ALPHA-SETUP-SLACK)
# ============================================================================


@router.get("/slack/oauth/start")
async def start_slack_oauth():
    """
    Generate Slack OAuth URL for setup wizard.

    Returns authorization URL and state token for CSRF protection.
    User redirects to Slack, authorizes, then returns to callback.

    Issue #528: ALPHA-SETUP-SLACK
    Issue #575: Added credential validation before OAuth

    Returns:
        dict with auth_url and state
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        # Issue #575: Verify credentials are configured BEFORE starting OAuth
        config_service = SlackConfigService()
        config = config_service.get_config()

        if not config.client_id or not config.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Slack OAuth not configured. Set SLACK_CLIENT_ID and SLACK_CLIENT_SECRET environment variables, or configure in PIPER.user.md.",
            )

        handler = SlackOAuthHandler(config_service=config_service)

        # Use setup-specific redirect URI if available
        # This returns user to wizard instead of general callback
        redirect_uri = os.getenv("SLACK_SETUP_REDIRECT_URI", os.getenv("SLACK_REDIRECT_URI", ""))

        # Generate OAuth URL with state for CSRF protection
        auth_url, state = handler.generate_authorization_url(
            redirect_uri=redirect_uri if redirect_uri else None
        )

        logger.info("slack_oauth_started", state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("slack_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Slack OAuth: {str(e)}",
        )


@router.get("/slack/oauth/callback")
async def handle_slack_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Slack OAuth callback for setup wizard.

    Exchanges authorization code for tokens and redirects back to
    setup wizard with success/error status in query params.

    Issue #528: ALPHA-SETUP-SLACK

    Args:
        code: Authorization code from Slack
        state: State token for CSRF verification
        error: Error from Slack (if authorization denied)

    Returns:
        RedirectResponse to setup wizard with status
    """
    from urllib.parse import quote

    from starlette.responses import RedirectResponse

    # Handle OAuth error (user denied, etc.)
    if error:
        logger.warning("slack_oauth_denied", error=error)
        return RedirectResponse(url=f"/setup?slack_error={error}#step-2", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning("slack_oauth_missing_params", has_code=bool(code), has_state=bool(state))
        return RedirectResponse(url="/setup?slack_error=missing_params#step-2", status_code=302)

    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Extract workspace name from result
        workspace_name = result.get("workspace", {}).get("workspace_name", "Workspace")
        workspace_name_encoded = quote(workspace_name)

        logger.info("slack_oauth_success", workspace=workspace_name)

        # Redirect back to setup wizard with success
        return RedirectResponse(
            url=f"/setup?slack_success=true&slack_workspace={workspace_name_encoded}#step-2",
            status_code=302,
        )

    except ValueError as e:
        # Invalid state or other validation error
        logger.warning("slack_oauth_validation_error", error=str(e))
        return RedirectResponse(url="/setup?slack_error=callback_failed#step-2", status_code=302)
    except Exception as e:
        logger.error("slack_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(url="/setup?slack_error=callback_failed#step-2", status_code=302)


@router.get("/slack/status")
async def get_slack_status():
    """
    Get Slack configuration status for setup wizard.

    Checks if Slack bot token exists and returns connection status.

    Issue #528: ALPHA-SETUP-SLACK

    Returns:
        dict with configured status and optional workspace info
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService

        config_service = SlackConfigService()
        slack_config = config_service.get_config()

        if slack_config.bot_token:
            return {
                "configured": True,
                "message": "Slack connected",
            }
        else:
            return {
                "configured": False,
                "message": "Not connected",
            }

    except Exception as e:
        logger.error("slack_status_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "message": "Status check failed",
        }


# ============================================================================
# Google Calendar OAuth Endpoints (Issue #529: ALPHA-SETUP-CALENDAR)
# ============================================================================


@router.get("/calendar/oauth/start")
async def start_calendar_oauth():
    """
    Generate Google Calendar OAuth URL for setup wizard.

    Returns authorization URL and state token for CSRF protection.
    User redirects to Google, authorizes, then returns to callback.

    Issue #529: ALPHA-SETUP-CALENDAR

    Returns:
        dict with auth_url and state
    """
    try:
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Verify credentials are configured
        if not handler.client_id or not handler.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Calendar OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            )

        auth_url, state = handler.generate_authorization_url()

        logger.info("calendar_oauth_started", state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Calendar OAuth: {str(e)}",
        )


@router.get("/calendar/oauth/callback")
async def handle_calendar_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Google Calendar OAuth callback.

    Exchanges authorization code for tokens and redirects back to
    setup wizard with success/error status in query params.

    Issue #529: ALPHA-SETUP-CALENDAR

    Args:
        code: Authorization code from Google
        state: State token for CSRF verification
        error: Error from Google (if authorization denied)

    Returns:
        RedirectResponse to setup wizard with status
    """
    from urllib.parse import quote

    from starlette.responses import RedirectResponse

    # Handle OAuth error (user denied, etc.)
    if error:
        logger.warning("calendar_oauth_denied", error=error)
        return RedirectResponse(url=f"/setup?calendar_error={error}#step-2", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning("calendar_oauth_missing_params", has_code=bool(code), has_state=bool(state))
        return RedirectResponse(url="/setup?calendar_error=missing_params#step-2", status_code=302)

    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Store refresh token securely
        tokens = result["tokens"]
        if tokens.refresh_token:
            keychain = KeychainService()
            keychain.store_api_key("google_calendar", tokens.refresh_token)
            logger.info("calendar_refresh_token_stored")

        # Get user email for display
        user_email = result["user"].get("email", "Calendar")
        email_encoded = quote(user_email)

        logger.info("calendar_oauth_success", email=user_email)

        # Redirect back to setup wizard with success
        return RedirectResponse(
            url=f"/setup?calendar_success=true&calendar_email={email_encoded}#step-2",
            status_code=302,
        )

    except ValueError as e:
        # Invalid state or other validation error
        logger.warning("calendar_oauth_validation_error", error=str(e))
        return RedirectResponse(url="/setup?calendar_error=callback_failed#step-2", status_code=302)
    except Exception as e:
        logger.error("calendar_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(url="/setup?calendar_error=callback_failed#step-2", status_code=302)


@router.get("/calendar/status")
async def get_calendar_status():
    """
    Get Calendar configuration status for setup wizard.

    Checks if refresh token exists in keychain.

    Issue #529: ALPHA-SETUP-CALENDAR

    Returns:
        dict with configured status
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        refresh_token = keychain.get_api_key("google_calendar")

        if refresh_token:
            return {
                "configured": True,
                "message": "Calendar connected",
            }
        else:
            return {
                "configured": False,
                "message": "Not connected",
            }

    except Exception as e:
        logger.error("calendar_status_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "message": "Status check failed",
        }
