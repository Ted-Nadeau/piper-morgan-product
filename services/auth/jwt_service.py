"""
JWT Service - Core Authentication Token Management

Provides JWT token generation, validation, and management with standard claims
for interoperability and OAuth 2.0 federation readiness.

Security Features:
- Standard JWT claims (iss, aud, sub, exp, iat, jti)
- Configurable token expiration and refresh
- Secure key management with rotation support
- Claims validation and token introspection
- MCP protocol compatibility
"""

import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

import jwt
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.security.audit_logger import Action, audit_logger

logger = structlog.get_logger(__name__)


# Custom exceptions for token errors
class TokenRevoked(Exception):
    """Token has been revoked and is no longer valid"""

    pass


class TokenExpired(Exception):
    """Token has expired"""

    pass


class TokenInvalid(Exception):
    """Token is invalid"""

    pass


class TokenType(Enum):
    """JWT token types for different use cases"""

    ACCESS = "access"
    REFRESH = "refresh"
    API = "api"
    FEDERATION = "federation"


@dataclass
class JWTClaims:
    """Standard JWT claims with Piper Morgan extensions"""

    # Standard JWT claims (RFC 7519)
    iss: str  # Issuer - "piper-morgan"
    aud: str  # Audience - "piper-morgan-api" or specific service
    sub: str  # Subject - User ID
    exp: int  # Expiration time (Unix timestamp)
    iat: int  # Issued at time (Unix timestamp)
    jti: str  # JWT ID - Unique token identifier

    # Custom claims for Piper Morgan
    user_id: UUID
    user_email: str
    scopes: List[str]  # Permissions/scopes
    token_type: str  # TokenType enum value
    session_id: Optional[str] = None
    workspace_id: Optional[str] = None  # For multi-tenant scenarios
    mcp_compatible: bool = True  # MCP protocol compatibility flag


class JWTService:
    """
    JWT-based authentication service with OAuth 2.0 federation readiness.

    Provides secure token generation, validation, and management following
    industry standards for interoperability.
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
        issuer: str = "piper-morgan",
        audience: str = "piper-morgan-api",
        blacklist: Optional[
            Any
        ] = None,  # TokenBlacklist instance (using Any to avoid Pydantic issues)
    ):
        """
        Initialize JWT service with security configuration.

        Args:
            secret_key: JWT signing secret (from environment if not provided)
            algorithm: JWT signing algorithm (HS256 for symmetric, RS256 for asymmetric)
            access_token_expire_minutes: Access token expiration in minutes
            refresh_token_expire_days: Refresh token expiration in days
            issuer: JWT issuer claim
            audience: JWT audience claim
            blacklist: Optional TokenBlacklist for token revocation
        """
        self.secret_key = secret_key or self._get_secret_key()
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.issuer = issuer
        self.audience = audience
        self.blacklist = blacklist

        logger.info(
            "JWTService initialized",
            algorithm=algorithm,
            access_expire_min=access_token_expire_minutes,
            refresh_expire_days=refresh_token_expire_days,
            blacklist_enabled=blacklist is not None,
        )

    def _get_secret_key(self) -> str:
        """Get JWT secret key from environment with secure fallback"""
        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key:
            logger.warning("JWT_SECRET_KEY not set, using development fallback")
            # Development fallback - should never be used in production
            secret_key = "dev-secret-key-change-in-production"
        return secret_key

    def generate_access_token(
        self,
        user_id: UUID,
        user_email: str,
        scopes: List[str],
        session_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        """
        Generate JWT access token with standard claims.

        Args:
            user_id: Unique user identifier
            user_email: User email address
            scopes: List of permission scopes
            session_id: Optional session identifier
            workspace_id: Optional workspace/tenant identifier

        Returns:
            Encoded JWT access token string
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)

        claims = JWTClaims(
            iss=self.issuer,
            aud=self.audience,
            sub=str(user_id),  # Convert UUID to string for JWT standard claim
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
            jti=str(uuid.uuid4()),
            user_id=user_id,
            user_email=user_email,
            scopes=scopes,
            token_type=TokenType.ACCESS.value,
            session_id=session_id,
            workspace_id=workspace_id,
        )

        # Convert dataclass to dict for JWT encoding
        # Convert UUID objects to strings for JSON serialization
        claims_dict = {}
        for field in claims.__dataclass_fields__.values():
            value = getattr(claims, field.name)
            if isinstance(value, UUID):
                claims_dict[field.name] = str(value)
            else:
                claims_dict[field.name] = value

        token = jwt.encode(claims_dict, self.secret_key, algorithm=self.algorithm)

        logger.info(
            "Access token generated", user_id=user_id, scopes=scopes, expires_at=expire.isoformat()
        )

        return token

    def generate_refresh_token(
        self, user_id: UUID, user_email: str, session_id: Optional[str] = None
    ) -> str:
        """
        Generate JWT refresh token for long-term authentication.

        Args:
            user_id: Unique user identifier
            user_email: User email address
            session_id: Optional session identifier

        Returns:
            Encoded JWT refresh token string
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.refresh_token_expire_days)

        claims = JWTClaims(
            iss=self.issuer,
            aud=self.audience,
            sub=str(user_id),  # Convert UUID to string for JWT standard claim
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
            jti=str(uuid.uuid4()),
            user_id=user_id,
            user_email=user_email,
            scopes=["refresh"],  # Limited scope for refresh tokens
            token_type=TokenType.REFRESH.value,
            session_id=session_id,
        )

        # Convert dataclass to dict for JWT encoding
        # Convert UUID objects to strings for JSON serialization
        claims_dict = {}
        for field in claims.__dataclass_fields__.values():
            value = getattr(claims, field.name)
            if isinstance(value, UUID):
                claims_dict[field.name] = str(value)
            else:
                claims_dict[field.name] = value

        token = jwt.encode(claims_dict, self.secret_key, algorithm=self.algorithm)

        logger.info("Refresh token generated", user_id=user_id, expires_at=expire.isoformat())

        return token

    async def validate_token(self, token: str) -> Optional[JWTClaims]:
        """
        Validate JWT token and return claims if valid.

        Checks token signature, expiration, and blacklist status.

        Args:
            token: JWT token string to validate

        Returns:
            JWTClaims object if token is valid, None otherwise

        Raises:
            TokenRevoked: If token has been revoked
            TokenExpired: If token has expired
            TokenInvalid: If token is invalid
        """
        try:
            # Decode and validate token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )

            # Convert back to JWTClaims dataclass
            claims = JWTClaims(
                iss=payload["iss"],
                aud=payload["aud"],
                sub=payload["sub"],
                exp=payload["exp"],
                iat=payload["iat"],
                jti=payload["jti"],
                user_id=payload["user_id"],
                user_email=payload["user_email"],
                scopes=payload["scopes"],
                token_type=payload["token_type"],
                session_id=payload.get("session_id"),
                workspace_id=payload.get("workspace_id"),
                mcp_compatible=payload.get("mcp_compatible", True),
            )

            # NEW: Check blacklist if enabled
            if self.blacklist:
                token_id = claims.jti
                if await self.blacklist.is_blacklisted(token_id):
                    logger.warning(
                        "Token validation failed: revoked",
                        jti=token_id,
                        user_id=claims.user_id,
                    )
                    raise TokenRevoked(f"Token {token_id} has been revoked")

            logger.debug(
                "Token validated successfully",
                user_id=claims.user_id,
                token_type=claims.token_type,
                jti=claims.jti,
            )

            return claims

        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: expired")
            raise TokenExpired("Token has expired")
        except TokenRevoked:
            # Re-raise TokenRevoked as-is
            raise
        except jwt.InvalidTokenError as e:
            logger.warning("Token validation failed: invalid", error=str(e))
            raise TokenInvalid(f"Invalid token: {e}")
        except Exception as e:
            logger.error("Token validation error", error=str(e))
            raise TokenInvalid(f"Token validation error: {e}")

    async def refresh_access_token(
        self,
        refresh_token: str,
        session: Optional[AsyncSession] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Generate new access token from valid refresh token.

        Args:
            refresh_token: Valid JWT refresh token
            session: Optional database session for audit logging (Issue #249)
            audit_context: Optional request context for audit logging (Issue #249)

        Returns:
            New access token string if refresh token is valid, None otherwise

        Issue #249: Added audit logging
        """
        try:
            claims = await self.validate_token(refresh_token)
            if not claims or claims.token_type != TokenType.REFRESH.value:
                logger.warning("Invalid refresh token provided")
                return None

            # Generate new access token with same user info
            # Note: Scopes would typically be fetched from user service
            new_access_token = self.generate_access_token(
                user_id=claims.user_id,
                user_email=claims.user_email,
                scopes=["read", "write"],  # Default scopes - should be user-specific
                session_id=claims.session_id,
                workspace_id=claims.workspace_id,
            )

            logger.info("Access token refreshed", user_id=claims.user_id)

            # Audit logging (Issue #249)
            if session:
                await audit_logger.log_auth_event(
                    action=Action.TOKEN_REFRESHED,
                    status="success",
                    message="Access token refreshed from valid refresh token",
                    session=session,
                    user_id=claims.user_id,
                    session_id=claims.session_id,
                    details={
                        "refresh_token_id": claims.jti,
                        "scopes": ["read", "write"],
                    },
                    audit_context=audit_context,
                )

            return new_access_token
        except (TokenRevoked, TokenExpired, TokenInvalid):
            logger.warning("Refresh token validation failed")
            return None

    async def revoke_token(
        self,
        token: str,
        reason: str = "logout",
        user_id: Optional[UUID] = None,
        session: Optional[AsyncSession] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Revoke JWT token by adding to blacklist.

        Args:
            token: JWT token to revoke
            reason: Reason for revocation (logout, security, admin)
            user_id: Optional user ID for audit trail
            session: Optional database session for audit logging (Issue #249)
            audit_context: Optional request context for audit logging (Issue #249)

        Returns:
            True if token was successfully revoked, False otherwise

        Issue #249: Added audit logging
        """
        if not self.blacklist:
            logger.warning("Blacklist not configured, cannot revoke token")
            return False

        try:
            # Decode token to get JTI and expiration
            # Don't validate fully - we want to revoke even if expired/invalid
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={
                    "verify_exp": False,  # Don't fail on expired tokens
                    "verify_aud": False,  # Don't validate audience
                    "verify_iss": False,  # Don't validate issuer
                },
            )

            token_id = payload.get("jti")
            exp_timestamp = payload.get("exp", 0)
            expires_at = datetime.utcfromtimestamp(exp_timestamp)

            if not token_id:
                logger.warning("Token missing JTI claim, cannot blacklist")
                return False

            # Add to blacklist
            success = await self.blacklist.add(
                token_id=token_id,
                reason=reason,
                expires_at=expires_at,
                user_id=user_id or payload.get("user_id"),
            )

            if success:
                logger.info(
                    "Token revoked successfully",
                    jti=token_id,
                    user_id=user_id or payload.get("user_id"),
                    reason=reason,
                )

                # Audit logging (Issue #249)
                if session:
                    await audit_logger.log_auth_event(
                        action=Action.TOKEN_REVOKED,
                        status="success",
                        message=f"JWT token revoked: {reason}",
                        session=session,
                        user_id=user_id or payload.get("user_id"),
                        details={
                            "token_id": token_id,
                            "reason": reason,
                            "expires_at": expires_at.isoformat(),
                        },
                        audit_context=audit_context,
                    )
            else:
                logger.error("Failed to add token to blacklist", jti=token_id)

            return success

        except Exception as e:
            logger.error("Token revocation failed", error=str(e))
            return False

    async def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get token information for introspection (OAuth 2.0 style).

        Args:
            token: JWT token to introspect

        Returns:
            Token information dict if valid, None otherwise
        """
        try:
            claims = await self.validate_token(token)
            if not claims:
                return None

            return {
                "active": True,
                "user_id": claims.user_id,
                "user_email": claims.user_email,
                "scopes": claims.scopes,
                "token_type": claims.token_type,
                "exp": claims.exp,
                "iat": claims.iat,
                "iss": claims.iss,
                "aud": claims.aud,
                "jti": claims.jti,
                "session_id": claims.session_id,
                "workspace_id": claims.workspace_id,
                "mcp_compatible": claims.mcp_compatible,
            }
        except (TokenRevoked, TokenExpired, TokenInvalid):
            return {"active": False}
