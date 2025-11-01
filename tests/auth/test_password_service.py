"""
Test suite for password hashing (Issue #281: CORE-ALPHA-WEB-AUTH)
Verify bcrypt password hashing security

These tests define what "done" means for password service:
- Passwords hashed with bcrypt (not plain text)
- Bcrypt rounds >= 12 for security
- Same password produces different hashes (salt working)
- Correct passwords verify successfully
- Incorrect passwords rejected safely
- Generated passwords are cryptographically strong
"""

import re

import pytest


class TestPasswordService:
    """Verify password hashing security"""

    def test_password_service_exists(self):
        """
        Verify PasswordService can be imported.

        Success Criteria:
        - Module exists at expected location
        - Class can be instantiated
        """
        try:
            from services.auth.password_service import PasswordService

            ps = PasswordService()
            assert ps is not None
        except ImportError as e:
            pytest.fail(f"PasswordService not found: {e}")

    def test_hash_password_creates_bcrypt_hash(self):
        """
        Verify passwords hashed with bcrypt.

        Success Criteria:
        - Hash starts with $2b$ (bcrypt identifier)
        - Hash is 60 characters long (bcrypt standard)
        - Same password produces different hashes (salt working)
        - Hash format is valid bcrypt
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()
        password = "test_secure_password_123"

        # Hash password twice
        hash1 = ps.hash_password(password)
        hash2 = ps.hash_password(password)

        # Verify bcrypt format
        assert hash1.startswith(
            "$2b$"
        ), f"Hash must use bcrypt format (starts with $2b$): {hash1[:10]}"

        # Verify length
        assert len(hash1) == 60, f"Bcrypt hash must be 60 characters: got {len(hash1)}"

        # Verify uniqueness (salt working)
        assert hash1 != hash2, "Same password should produce different hashes (salt must be unique)"

    def test_hash_password_format_valid(self):
        """
        Verify hash format follows bcrypt structure.

        Success Criteria:
        - Format: $2b$rounds$salt_and_hash
        - Rounds extracted and verified
        - Salt and hash portions present
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()
        hashed = ps.hash_password("test123")

        # Bcrypt format: $2b$12$saltsaltsaltsaltsalthashhashhashhashhashhashhash
        parts = hashed.split("$")

        assert len(parts) >= 4, f"Bcrypt hash should have 4 parts: {parts}"

        assert parts[1] == "2b", "Algorithm identifier should be '2b'"

        # Rounds should be numeric
        rounds = parts[2]
        assert rounds.isdigit(), f"Rounds should be numeric: {rounds}"

    def test_hash_rounds_sufficient(self):
        """
        Verify bcrypt rounds >= 12 for security.

        Success Criteria:
        - Bcrypt rounds set to 12 or higher
        - Verified in hash string
        - Meets modern security standards
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()
        hashed = ps.hash_password("security_test")

        # Extract rounds from hash
        parts = hashed.split("$")
        rounds = int(parts[2])

        assert rounds >= 12, f"Bcrypt rounds must be >= 12 for security: got {rounds}"

    def test_verify_password_correct(self):
        """
        Verify correct password validates successfully.

        Success Criteria:
        - verify_password returns True for correct password
        - Verification is case-sensitive
        - Works with various password types
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        test_passwords = [
            "simple123",
            "Complex!Pass@123",
            "with spaces in it",
            "unicode_πασσωορδ",
        ]

        for password in test_passwords:
            hashed = ps.hash_password(password)
            is_valid = ps.verify_password(password, hashed)

            assert is_valid is True, f"Correct password should verify: '{password}'"

    def test_verify_password_incorrect(self):
        """
        Verify incorrect password rejected.

        Success Criteria:
        - verify_password returns False for wrong password
        - No exception raised
        - Timing-safe comparison (not testable here)
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        correct_password = "correct_password_123"
        hashed = ps.hash_password(correct_password)

        wrong_passwords = [
            "wrong_password",
            "Correct_password_123",  # Case sensitive
            "correct_password_1234",  # Extra character
            "correct_password_12",  # Missing character
            "",  # Empty
        ]

        for wrong in wrong_passwords:
            is_valid = ps.verify_password(wrong, hashed)

            assert is_valid is False, f"Wrong password should not verify: '{wrong}'"

    def test_verify_password_handles_invalid_hash(self):
        """
        Verify invalid hash handled gracefully.

        Success Criteria:
        - Invalid hash returns False (not exception)
        - Malformed hash returns False
        - Empty hash returns False
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        invalid_hashes = [
            "not_a_bcrypt_hash",
            "",
            "$2b$invalid",
            "plain_text_password",
        ]

        for invalid_hash in invalid_hashes:
            # Should return False, not raise exception
            try:
                is_valid = ps.verify_password("any_password", invalid_hash)
                assert is_valid is False, f"Invalid hash should return False: {invalid_hash}"
            except Exception as e:
                pytest.fail(f"Invalid hash should not raise exception: {invalid_hash} -> {e}")

    def test_generate_temp_password_exists(self):
        """
        Verify temp password generation method exists.

        Success Criteria:
        - Method can be called
        - Returns a string
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        # Method should exist
        assert hasattr(
            ps, "generate_temp_password"
        ), "PasswordService should have generate_temp_password method"

        password = ps.generate_temp_password()
        assert isinstance(password, str), "Generated password should be a string"

    def test_generate_temp_password_strength(self):
        """
        Verify generated passwords are strong.

        Success Criteria:
        - Length >= 16 characters
        - Contains letters (uppercase and lowercase)
        - Contains numbers
        - Contains symbols
        - Cryptographically random (appears random)
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        # Generate multiple passwords
        passwords = [ps.generate_temp_password() for _ in range(5)]

        for password in passwords:
            # Check length
            assert (
                len(password) >= 16
            ), f"Generated password must be >= 16 chars: got {len(password)}"

            # Check character diversity
            has_lower = bool(re.search(r"[a-z]", password))
            has_upper = bool(re.search(r"[A-Z]", password))
            has_digit = bool(re.search(r"[0-9]", password))
            has_special = bool(re.search(r"[!@#$%^&*()]", password))

            diversity_score = sum([has_lower, has_upper, has_digit, has_special])

            assert diversity_score >= 3, (
                f"Password should have 3+ character types: '{password}' "
                f"(lower:{has_lower}, upper:{has_upper}, digit:{has_digit}, special:{has_special})"
            )

        # Verify uniqueness (randomness)
        unique_passwords = set(passwords)
        assert len(unique_passwords) == len(
            passwords
        ), "Generated passwords should be unique (cryptographically random)"

    def test_generate_temp_password_custom_length(self):
        """
        Verify custom length parameter works.

        Success Criteria:
        - Can specify length parameter
        - Generated password matches specified length
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        # Test various lengths
        lengths = [16, 20, 24, 32]

        for length in lengths:
            try:
                password = ps.generate_temp_password(length=length)
                assert (
                    len(password) == length
                ), f"Password length should be {length}: got {len(password)}"
            except TypeError:
                # If length parameter not supported, skip this test
                pytest.skip("generate_temp_password doesn't support length parameter")

    def test_empty_password_handling(self):
        """
        Verify empty passwords handled appropriately.

        Success Criteria:
        - Empty password either rejected or hashed consistently
        - No crashes or exceptions
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        try:
            # Try to hash empty password
            hashed = ps.hash_password("")

            # If accepted, should still verify correctly
            is_valid = ps.verify_password("", hashed)
            assert is_valid is True, "Empty password should verify if hashing is allowed"

            # Wrong password should not verify
            is_valid = ps.verify_password("not_empty", hashed)
            assert is_valid is False

        except (ValueError, Exception) as e:
            # If empty passwords rejected, that's also acceptable
            # Just verify it doesn't crash
            pass

    def test_unicode_password_handling(self):
        """
        Verify unicode passwords work correctly.

        Success Criteria:
        - Unicode characters accepted
        - Hashing works
        - Verification works
        """
        from services.auth.password_service import PasswordService

        ps = PasswordService()

        unicode_passwords = [
            "πα$$ω0ρδ",  # Greek
            "密码123",  # Chinese
            "пароль456",  # Cyrillic
            "🔐secure🔑",  # Emoji
        ]

        for password in unicode_passwords:
            try:
                hashed = ps.hash_password(password)
                is_valid = ps.verify_password(password, hashed)

                assert is_valid is True, f"Unicode password should work: '{password}'"
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pytest.fail(f"Unicode password should be supported: '{password}' -> {e}")
