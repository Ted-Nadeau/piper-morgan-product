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


class PasswordChangeRequest(BaseModel):
    """
    Password change request payload.

    Requires:
    - current_password: User's existing password (for verification)
    - new_password: New password to set
    - new_password_confirm: Confirmation of new password (must match)

    Security:
    - Current password verified before accepting change
    - New password validated for strength requirements
    - Passwords must match exactly
    - Case-sensitive comparison

    Issue #298: AUTH-PASSWORD-CHANGE
    """

    current_password: str = Field(
        ..., min_length=1, description="Current password (required, non-empty)"
    )
    new_password: str = Field(..., min_length=1, description="New password (required, non-empty)")
    new_password_confirm: str = Field(
        ..., min_length=1, description="Confirmation of new password (must match)"
    )

    @field_validator("current_password", "new_password", "new_password_confirm")
    @classmethod
    def validate_not_empty(cls, v: str, info) -> str:
        """Ensure all password fields are not empty strings."""
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v


class PasswordChangeResponse(BaseModel):
    """
    Password change response payload.

    Returns:
    - success: True if password changed successfully
    - message: Human-readable success or error message

    Note:
    - After successful password change, user must log in again
    - Previous token is invalidated and added to blacklist
    - New password takes effect immediately

    Issue #298: AUTH-PASSWORD-CHANGE
    """

    success: bool = Field(..., description="Whether password change succeeded")
    message: str = Field(..., description="Status message (success or error details)")
