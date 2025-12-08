"""
Authentication API Routes

Provides JWT authentication endpoints including login, logout, and token management.
Integrates with TokenBlacklist for secure token revocation.

Issue #281: CORE-ALPHA-WEB-AUTH
"""

from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims, JWTService
from services.auth.models import (
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    PasswordChangeResponse,
)
from services.auth.password_service import PasswordService
from services.auth.password_validator import PasswordValidator
from services.database.connection import db
from services.database.models import User
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
    username: str = Form(..., min_length=1),
    password: str = Form(..., min_length=1),
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
        username: Username from form data
        password: Password from form data
        jwt_service: JWT service for token generation

    Returns:
        LoginResponse with token, user_id, username

    Raises:
        HTTPException 401: Invalid credentials or user not active
        HTTPException 500: Server error during authentication

    Issue #281: CORE-ALPHA-WEB-AUTH
    Issue #393: Auth UI Phase 1 - Form data support
    """
    try:
        # Validate credentials are not empty
        username = username.strip()
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user and update last_login in single session
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Query user by username
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()

            # User not found - generic error message for security
            if not user:
                logger.warning(
                    "login_failed_user_not_found",
                    username=username,
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
            is_valid = password_service.verify_password(password, user.password_hash)

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
        token = jwt_service.generate_access_token(
            user_id=user_id,
            user_email=user_email,
            scopes=["user"],  # Default scope for alpha users
        )

        # Set cookie for web clients
        # Detect if request is HTTPS to set secure flag appropriately
        # This allows HTTP development while enforcing HTTPS cookies in production
        is_https = request.url.scheme == "https"
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=is_https,  # Only set secure flag for HTTPS requests
            samesite="lax",
            max_age=28800,  # 8 hours for better alpha testing UX
        )

        logger.info(
            "login_successful",
            user_id=user_id,
            username=username,
            ip_address=request.client.host if request.client else None,
        )

        return LoginResponse(
            token=token,
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
            username=username,
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

        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Revoke the token via blacklist with audit logging
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
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


@router.get("/me")
async def get_me(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get current authenticated user's information.

    Returns the user's basic profile information by querying the database
    with the user_id from the authenticated JWT token.

    Args:
        current_user: Current authenticated user (from JWT token)

    Returns:
        User information (user_id, username, email)

    Raises:
        HTTPException 401: If not authenticated or token invalid
        HTTPException 404: If user not found in database

    Issue #281: CORE-ALPHA-WEB-AUTH
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user by ID from token
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(select(User).where(User.id == current_user.user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            return {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_me_error", user_id=current_user.user_id, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information",
        )


@router.post("/change-password", response_model=PasswordChangeResponse)
async def change_password(
    request: Request,
    data: PasswordChangeRequest,
    current_user: JWTClaims = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Change user password and invalidate current token.

    Requires valid authentication. User must provide their current password
    for verification. New password is validated for strength requirements.

    After successful password change:
    - Current token is added to blacklist
    - User must log in again with new password
    - Old token will be rejected (401 Unauthorized)

    Args:
        request: FastAPI Request object for audit context
        data: PasswordChangeRequest with current_password, new_password, new_password_confirm
        current_user: Current authenticated user (from JWT token)
        credentials: Bearer token credentials
        jwt_service: JWT service for token management

    Returns:
        PasswordChangeResponse with success=True and success message

    Raises:
        HTTPException 400: Password validation fails (specific requirement)
        HTTPException 400: New passwords don't match
        HTTPException 401: Current password incorrect
        HTTPException 401: Token invalid/expired
        HTTPException 500: Unexpected server error

    Security:
    - Current password verified before accepting change
    - New password validated for strength (8+ chars, upper, lower, number, special)
    - Passwords must match exactly (case-sensitive)
    - Token invalidated immediately (force re-authentication)
    - Constant-time password comparison (bcrypt)

    Issue #298: AUTH-PASSWORD-CHANGE
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Verify new passwords match
        if data.new_password != data.new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New passwords do not match",
            )

        # Validate new password strength
        is_valid, error_message = PasswordValidator.validate(data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        # Get database session for password update
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Hash new password
            password_service = PasswordService()
            new_password_hash = password_service.hash_password(data.new_password)

            # Change password via JWT service
            # This will verify current password, update password hash, and revoke token
            token = credentials.credentials
            try:
                success = await jwt_service.change_password(
                    user_id=current_user.user_id,
                    current_password=data.current_password,
                    new_password_hash=new_password_hash,
                    current_token=token,
                    session=session,
                    password_service=password_service,
                )

                if success:
                    logger.info(
                        "Password changed successfully",
                        user_id=current_user.user_id,
                        username=current_user.user_email,
                    )
                    return PasswordChangeResponse(
                        success=True,
                        message="Password changed successfully. Please log in with your new password.",
                    )
                else:
                    logger.error(
                        "Password change failed in service",
                        user_id=current_user.user_id,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to change password",
                    )

            except ValueError as e:
                # Current password incorrect or validation error
                if "Current password is incorrect" in str(e):
                    logger.warning(
                        "Password change failed: incorrect current password",
                        user_id=current_user.user_id,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Current password is incorrect",
                    )
                else:
                    logger.warning(
                        "Password change failed: validation error",
                        user_id=current_user.user_id,
                        error=str(e),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=str(e),
                    )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, auth failures)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "password_change_error",
            user_id=current_user.user_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed",
        )
