"""
CLI Authentication Helper (Issue #397)

Provides auto-authentication functionality for CLI commands by
retrieving stored tokens from the macOS Keychain.

Usage:
    from cli.auth_helper import get_cli_auth_token, get_authenticated_user_id

    token = get_cli_auth_token()
    if token:
        # Use token for API calls
        headers = {"Authorization": f"Bearer {token}"}
"""

from typing import Optional, Tuple

import structlog

logger = structlog.get_logger(__name__)


def get_cli_auth_token() -> Optional[str]:
    """
    Get CLI authentication token from keychain (Issue #397).

    Searches for stored CLI session tokens and validates them.

    Returns:
        Valid JWT token if available and not expired, None otherwise
    """
    try:
        from services.auth.jwt_service import JWTService
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        jwt_service = JWTService()

        # Get list of known providers to find CLI tokens
        # CLI tokens are stored with format: {user_id}_cli_session_api_key
        # We need to find user IDs by checking the database
        try:
            import os

            from sqlalchemy import create_engine, text

            # Build sync database URL from environment (same as connection.py)
            user = os.getenv("POSTGRES_USER", "piper")
            password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5433")
            database = os.getenv("POSTGRES_DB", "piper_morgan")
            sync_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

            engine = create_engine(sync_url)

            with engine.connect() as conn:
                # Order by most recent first - CLI token was stored for most recent user
                result = conn.execute(
                    text("SELECT id FROM users ORDER BY created_at DESC LIMIT 10")
                )
                user_ids = [str(row[0]) for row in result.fetchall()]

            for user_id in user_ids:
                token = keychain.get_cli_token(user_id)
                if token:
                    # Validate token is still valid (not expired)
                    try:
                        # Use synchronous validation (validate_token is async but we just decode)
                        import jwt as pyjwt

                        claims = pyjwt.decode(
                            token,
                            jwt_service.secret_key,
                            algorithms=[jwt_service.algorithm],
                            audience=jwt_service.audience,
                            issuer=jwt_service.issuer,
                        )
                        if claims:
                            logger.debug(
                                "CLI token validated",
                                user_id=user_id,
                                token_type=claims.get("token_type"),
                            )
                            return token
                    except pyjwt.ExpiredSignatureError:
                        logger.debug("CLI token expired", user_id=user_id)
                        continue
                    except pyjwt.InvalidTokenError as e:
                        logger.debug("CLI token invalid", user_id=user_id, error=str(e))
                        continue

        except Exception as e:
            logger.debug(f"Failed to query user IDs: {e}")

        return None

    except ImportError as e:
        logger.warning(f"CLI auth helper import failed: {e}")
        return None
    except Exception as e:
        logger.warning(f"CLI auth helper error: {e}")
        return None


def get_authenticated_user_id() -> Optional[str]:
    """
    Get the user ID from a valid CLI token.

    Returns:
        User ID string if valid token found, None otherwise
    """
    token = get_cli_auth_token()
    if not token:
        return None

    try:
        import jwt as pyjwt

        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()
        claims = pyjwt.decode(
            token,
            jwt_service.secret_key,
            algorithms=[jwt_service.algorithm],
            audience=jwt_service.audience,
            issuer=jwt_service.issuer,
        )
        return claims.get("sub")  # subject = user_id
    except Exception as e:
        logger.debug(f"Failed to extract user ID from token: {e}")
        return None


def get_cli_auth_info() -> Optional[Tuple[str, str]]:
    """
    Get CLI authentication info (token and user_id).

    Returns:
        Tuple of (token, user_id) if valid token found, None otherwise
    """
    token = get_cli_auth_token()
    if not token:
        return None

    try:
        import jwt as pyjwt

        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()
        claims = pyjwt.decode(
            token,
            jwt_service.secret_key,
            algorithms=[jwt_service.algorithm],
            audience=jwt_service.audience,
            issuer=jwt_service.issuer,
        )
        user_id = claims.get("sub")
        if user_id:
            return (token, user_id)
        return None
    except Exception as e:
        logger.debug(f"Failed to extract auth info from token: {e}")
        return None
