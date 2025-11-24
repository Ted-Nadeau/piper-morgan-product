"""
Password Validation Service

Validates password strength requirements for new passwords.
Used by password change endpoint (#298) and user creation flows.

Security Features:
- Enforces OWASP password complexity requirements
- Clear, specific error messages (not generic "invalid password")
- No information leakage about password requirements
- Helps prevent weak password selection

Issue #298: AUTH-PASSWORD-CHANGE
"""

import re
from typing import Optional, Tuple


class PasswordValidator:
    """
    Validates password strength against security requirements.

    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter (A-Z)
    - At least 1 lowercase letter (a-z)
    - At least 1 digit (0-9)
    - At least 1 special character (!@#$%^&*)

    Design:
    - Static methods, no state
    - Returns tuple: (is_valid, error_message)
    - Error messages specific for each requirement
    - Can be unit tested independently
    """

    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*()"

    @classmethod
    def validate(cls, password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength.

        Args:
            password: Password string to validate

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid=True: Password meets all requirements, error_message=None
            - is_valid=False: Password invalid, error_message describes requirement

        Example:
            >>> PasswordValidator.validate("weak")
            (False, "Password must be at least 8 characters")

            >>> PasswordValidator.validate("WeakPass1")
            (False, "Password must contain at least one special character")

            >>> PasswordValidator.validate("Strong@Pass1")
            (True, None)
        """
        if not password:
            return False, "Password cannot be empty"

        # Check minimum length
        if len(password) < cls.MIN_LENGTH:
            return (
                False,
                f"Password must be at least {cls.MIN_LENGTH} characters",
            )

        # Check uppercase letter
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"

        # Check lowercase letter
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"

        # Check digit
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"

        # Check special character
        if not re.search(f"[{re.escape(cls.SPECIAL_CHARS)}]", password):
            special_chars_display = "!@#$%^&*()"
            return (
                False,
                f"Password must contain at least one special character ({special_chars_display})",
            )

        # All checks passed
        return True, None

    @classmethod
    def validate_match(cls, password1: str, password2: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that two passwords match.

        Args:
            password1: First password
            password2: Second password (confirmation)

        Returns:
            Tuple of (is_valid, error_message)

        Example:
            >>> PasswordValidator.validate_match("Pass123!", "Pass123!")
            (True, None)

            >>> PasswordValidator.validate_match("Pass123!", "Different!")
            (False, "Passwords do not match")
        """
        if password1 == password2:
            return True, None
        else:
            return False, "Passwords do not match"

    @classmethod
    def validate_strength(cls, password: str) -> Tuple[bool, Optional[str]]:
        """
        Comprehensive validation including strength and matching.

        Combines both validate() and internal strength checks.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)

        Note:
            This is the main method to use for password validation.
            Other methods (validate, validate_match) are available for specific checks.
        """
        return cls.validate(password)
