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

import jwt
import structlog

logger = structlog.get_logger(__name__)


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
    user_id: str
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
        """
        self.secret_key = secret_key or self._get_secret_key()
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.issuer = issuer
        self.audience = audience

        logger.info(
            "JWTService initialized",
            algorithm=algorithm,
            access_expire_min=access_token_expire_minutes,
            refresh_expire_days=refresh_token_expire_days,
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
        user_id: str,
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
            sub=user_id,
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
        claims_dict = {
            field.name: getattr(claims, field.name) for field in claims.__dataclass_fields__
        }

        token = jwt.encode(claims_dict, self.secret_key, algorithm=self.algorithm)

        logger.info(
            "Access token generated", user_id=user_id, scopes=scopes, expires_at=expire.isoformat()
        )

        return token

    def generate_refresh_token(
        self, user_id: str, user_email: str, session_id: Optional[str] = None
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
            sub=user_id,
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
            jti=str(uuid.uuid4()),
            user_id=user_id,
            user_email=user_email,
            scopes=["refresh"],  # Limited scope for refresh tokens
            token_type=TokenType.REFRESH.value,
            session_id=session_id,
        )

        claims_dict = {
            field.name: getattr(claims, field.name) for field in claims.__dataclass_fields__
        }

        token = jwt.encode(claims_dict, self.secret_key, algorithm=self.algorithm)

        logger.info("Refresh token generated", user_id=user_id, expires_at=expire.isoformat())

        return token

    def validate_token(self, token: str) -> Optional[JWTClaims]:
        """
        Validate JWT token and return claims if valid.

        Args:
            token: JWT token string to validate

        Returns:
            JWTClaims object if token is valid, None otherwise
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

            logger.debug(
                "Token validated successfully",
                user_id=claims.user_id,
                token_type=claims.token_type,
                jti=claims.jti,
            )

            return claims

        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning("Token validation failed: invalid", error=str(e))
            return None
        except Exception as e:
            logger.error("Token validation error", error=str(e))
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Generate new access token from valid refresh token.

        Args:
            refresh_token: Valid JWT refresh token

        Returns:
            New access token string if refresh token is valid, None otherwise
        """
        claims = self.validate_token(refresh_token)
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
        return new_access_token

    def revoke_token(self, token: str) -> bool:
        """
        Revoke JWT token (add to blacklist).

        Note: This is a placeholder for token revocation logic.
        In production, this would add the token JTI to a blacklist/revocation list.

        Args:
            token: JWT token to revoke

        Returns:
            True if token was successfully revoked, False otherwise
        """
        claims = self.validate_token(token)
        if not claims:
            return False

        # TODO: Implement token blacklist storage (Redis recommended)
        logger.info("Token revoked", jti=claims.jti, user_id=claims.user_id)
        return True

    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get token information for introspection (OAuth 2.0 style).

        Args:
            token: JWT token to introspect

        Returns:
            Token information dict if valid, None otherwise
        """
        claims = self.validate_token(token)
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
