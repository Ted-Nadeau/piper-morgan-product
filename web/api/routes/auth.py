"""
Authentication API Routes

Provides JWT authentication endpoints including login, logout, and token management.
Integrates with TokenBlacklist for secure token revocation.
"""

from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims, JWTService
from services.database.session_factory import AsyncSessionFactory

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
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
