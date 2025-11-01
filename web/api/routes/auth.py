"""
Authentication API Routes

Provides JWT authentication endpoints including login, logout, and token management.
Integrates with TokenBlacklist for secure token revocation.

Issue #281: CORE-ALPHA-WEB-AUTH
"""

from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims, JWTService
from services.auth.models import LoginRequest, LoginResponse
from services.auth.password_service import PasswordService
from services.database.connection import db
from services.database.models import AlphaUser
from services.database.session_factory import AsyncSessionFactory

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
logger = structlog.get_logger(__name__)


def build_audit_context(request: Request) -> Dict[str, Any]:
    """
    Extract audit context from FastAPI request.

    Args:
        request: FastAPI Request object

    Returns:
        Dict with ip_address, user_agent, request_id, request_path

    Issue #249: Audit logging context helper
    """
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.headers.get("x-request-id"),
        "request_path": str(request.url.path),
    }


async def get_jwt_service(request: Request) -> JWTService:
    """
    Dependency injection for JWTService.

    Uses AuthContainer for singleton JWT service with proper DI.
    Fixed: Issue #258 CORE-AUTH-CONTAINER
    """
    # Get from AuthContainer (singleton pattern)
    from services.auth.container import AuthContainer

    return AuthContainer.get_jwt_service()


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    credentials: LoginRequest,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Authenticate user with username/password and return JWT token.

    Security Features:
    - Bcrypt password verification (timing-safe)
    - Generic error messages (prevent user enumeration)
    - JWT token generation with user claims
    - Cookie-based auth for web clients
    - Bearer token for API clients

    Args:
        request: FastAPI Request object for audit context
        response: FastAPI Response object for setting cookies
        credentials: Username and password
        jwt_service: JWT service for token generation

    Returns:
        LoginResponse with token, user_id, username

    Raises:
        HTTPException 401: Invalid credentials or user not active
        HTTPException 500: Server error during authentication

    Issue #281: CORE-ALPHA-WEB-AUTH
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user and update last_login in single session
        async with await db.get_session() as session:
            # Query user by username
            result = await session.execute(
                select(AlphaUser).where(AlphaUser.username == credentials.username)
            )
            user = result.scalar_one_or_none()

            # User not found - generic error message for security
            if not user:
                logger.warning(
                    "login_failed_user_not_found",
                    username=credentials.username,
                    ip_address=request.client.host if request.client else None,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                )

            # Check if user is active
            if not user.is_active:
                logger.warning(
                    "login_failed_user_inactive",
                    user_id=str(user.id),
                    username=user.username,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is inactive. Please contact administrator.",
                )

            # Check if password is set
            if not user.password_hash:
                logger.warning(
                    "login_failed_no_password",
                    user_id=str(user.id),
                    username=user.username,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Password not set for this account. Please contact administrator.",
                )

            # Verify password
            password_service = PasswordService()
            is_valid = password_service.verify_password(credentials.password, user.password_hash)

            if not is_valid:
                logger.warning(
                    "login_failed_invalid_password",
                    user_id=str(user.id),
                    username=user.username,
                    ip_address=request.client.host if request.client else None,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                )

            # Update last_login_at (in same session)
            user.last_login_at = datetime.utcnow()
            await session.commit()

            # Store user details for response (before session closes)
            user_id = str(user.id)
            username = user.username
            user_email = user.email

        # Generate JWT token (after session closed)
        audit_context = build_audit_context(request)
        token_data = jwt_service.create_access_token(
            user_id=user_id,
            username=username,
            user_email=user_email,
            scopes=["user"],  # Default scope for alpha users
        )

        # Set cookie for web clients
        response.set_cookie(
            key="auth_token",
            value=token_data["access_token"],
            httponly=True,
            secure=True,  # HTTPS only in production
            samesite="lax",
            max_age=3600,  # 1 hour (matches JWT expiry)
        )

        logger.info(
            "login_successful",
            user_id=user_id,
            username=username,
            ip_address=request.client.host if request.client else None,
        )

        return LoginResponse(
            token=token_data["access_token"],
            user_id=user_id,
            username=username,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, auth failures)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "login_error",
            username=credentials.username,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed",
        )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Logout user by revoking their access token.

    The token will be added to the blacklist and no longer valid for authentication.
    Even if the token hasn't expired, it will be rejected by the middleware.

    Args:
        request: FastAPI Request object for audit context
        current_user: Current authenticated user (from token)
        credentials: Bearer token credentials
        jwt_service: JWT service for token revocation

    Returns:
        Success message with user ID

    Raises:
        HTTPException 500: If token revocation fails

    Issue #249: Added audit logging
    """
    token = credentials.credentials

    try:
        # Build audit context from request (Issue #249)
        audit_context = build_audit_context(request)

        # Revoke the token via blacklist with audit logging
        async with AsyncSessionFactory.session_scope() as session:
            success = await jwt_service.revoke_token(
                token=token,
                reason="logout",
                user_id=current_user.user_id,
                session=session,
                audit_context=audit_context,
            )
            await session.commit()

        if success:
            logger.info(
                "User logged out successfully",
                user_id=current_user.user_id,
                user_email=current_user.user_email,
            )
            return {"message": "Logged out successfully", "user_id": current_user.user_id}
        else:
            logger.error("Failed to revoke token during logout", user_id=current_user.user_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Logout failed: Unable to revoke token",
            )

    except Exception as e:
        logger.error("Logout error", user_id=current_user.user_id, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Logout failed: {str(e)}"
        )
