"""
Password Service for Issue #281: CORE-ALPHA-WEB-AUTH

Provides secure password hashing and verification using bcrypt.

Security Features:
- Bcrypt rounds: 12 (OWASP recommended minimum)
- Timing-safe password comparison
- Cryptographically secure random password generation
- Unicode password support

Issue #281: CORE-ALPHA-WEB-AUTH
"""

import secrets
import string

import bcrypt


class PasswordService:
    """
    Secure password hashing and verification.

    Uses bcrypt with 12 rounds for password hashing.
    Provides timing-safe verification and secure temp password generation.
    """

    def __init__(self, rounds: int = 12):
        """
        Initialize PasswordService.

        Args:
            rounds: Bcrypt rounds (default 12, minimum for security)
        """
        if rounds < 12:
            raise ValueError("Bcrypt rounds must be >= 12 for security")
        self.rounds = rounds

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password to hash

        Returns:
            Bcrypt hash string (60 characters, starts with $2b$)

        Example:
            >>> ps = PasswordService()
            >>> hashed = ps.hash_password("my_password")
            >>> hashed[:4]
            '$2b$'
            >>> len(hashed)
            60
        """
        # Encode password to bytes (bcrypt requirement)
        password_bytes = password.encode("utf-8")

        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)

        # Return as string
        return hashed_bytes.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a bcrypt hash.

        Uses timing-safe comparison to prevent timing attacks.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Bcrypt hash to verify against

        Returns:
            True if password matches, False otherwise

        Note:
            Returns False (not exception) for invalid hashes.
            This prevents information leakage via error messages.

        Example:
            >>> ps = PasswordService()
            >>> hashed = ps.hash_password("test123")
            >>> ps.verify_password("test123", hashed)
            True
            >>> ps.verify_password("wrong", hashed)
            False
        """
        try:
            # Encode both password and hash to bytes
            password_bytes = plain_password.encode("utf-8")
            hash_bytes = hashed_password.encode("utf-8")

            # Verify with bcrypt (timing-safe comparison)
            return bcrypt.checkpw(password_bytes, hash_bytes)

        except (ValueError, AttributeError, UnicodeEncodeError, UnicodeDecodeError):
            # Invalid hash format, encoding issues, or bcrypt errors
            # Return False instead of raising exception
            # This prevents information leakage
            return False

    def generate_temp_password(self, length: int = 16) -> str:
        """
        Generate a cryptographically secure temporary password.

        Generated password meets security requirements:
        - Minimum 16 characters (default)
        - Contains uppercase, lowercase, digits, and special characters
        - Cryptographically random (uses secrets module)

        Args:
            length: Password length (default 16, minimum 16)

        Returns:
            Random password string

        Raises:
            ValueError: If length < 16

        Example:
            >>> ps = PasswordService()
            >>> pwd = ps.generate_temp_password()
            >>> len(pwd) >= 16
            True
            >>> pwd == ps.generate_temp_password()  # Different each time
            False
        """
        if length < 16:
            raise ValueError("Temporary password must be >= 16 characters for security")

        # Character sets for password generation
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()"

        # All characters combined
        all_chars = lowercase + uppercase + digits + special

        # Ensure at least one character from each category
        password_chars = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special),
        ]

        # Fill remaining length with random characters
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        # Shuffle to avoid predictable pattern
        # (first 4 chars are one from each category)
        secrets.SystemRandom().shuffle(password_chars)

        return "".join(password_chars)
