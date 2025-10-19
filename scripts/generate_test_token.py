#!/usr/bin/env python3
"""Generate test JWT tokens for API testing

Usage:
    python scripts/generate_test_token.py                    # Default test_user
    python scripts/generate_test_token.py user123            # Specific user
    python scripts/generate_test_token.py user123 admin      # With admin scope
"""

import sys

from services.auth.jwt_service import JWTService


def generate_token(user_id: str = "test_user", scopes: list = None, **claims):
    """Generate a test JWT token

    Args:
        user_id: User identifier for token subject
        scopes: List of permission scopes (default: ["read", "write"])
        **claims: Additional custom claims

    Returns:
        JWT token string
    """
    if scopes is None:
        scopes = ["read", "write"]

    jwt_service = JWTService()

    token = jwt_service.generate_access_token(
        user_id=user_id, user_email=f"{user_id}@example.com", scopes=scopes, **claims
    )

    return token


if __name__ == "__main__":
    # Parse command line arguments
    user_id = sys.argv[1] if len(sys.argv) > 1 else "test_user"

    # Parse scopes from remaining arguments
    scopes = sys.argv[2:] if len(sys.argv) > 2 else ["read", "write"]

    # Generate token
    token = generate_token(user_id, scopes)

    # Output just the token (for easy piping)
    print(token)
