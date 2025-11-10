"""
Pydantic models for authentication API requests and responses.

Issue #281: CORE-ALPHA-WEB-AUTH
"""

from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    """
    Login request payload.

    Security:
    - Credentials validated before authentication
    - Generic error messages prevent user enumeration
    - Empty credentials rejected
    """

    username: str = Field(..., min_length=1, description="Username (required, non-empty)")
    password: str = Field(..., min_length=1, description="Password (required, non-empty)")

    @field_validator("username", "password")
    @classmethod
    def validate_not_empty(cls, v: str, info) -> str:
        """Ensure username and password are not empty strings."""
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v.strip()


class LoginResponse(BaseModel):
    """
    Login response payload.

    Returns:
    - token: JWT access token (Bearer token)
    - user_id: User's UUID (for API clients)
    - username: User's username

    Note:
    - Cookie auth_token also set for web clients
    - Token format: Bearer <jwt_token>
    """

    token: str = Field(..., description="JWT access token")
    user_id: UUID = Field(..., description="User UUID")
    username: str = Field(..., description="Username")
