"""
Test suite for Issue #280: CORE-ALPHA-DATA-LEAK
Verify personal data isolation between users

These tests define what "done" means for the data leak fix:
- PIPER.md must contain zero personal/company information
- User-specific data must be stored in database (alpha_users.preferences)
- ConfigService must properly isolate data by user_id
- No data leakage between users
"""

import re
from pathlib import Path

import pytest
from sqlalchemy import select

from services.database.models import AlphaUser


class TestDataIsolation:
    """Verify PIPER.md has no personal data and user data is isolated"""

    def test_piper_md_has_no_personal_data(self):
        """
        Verify PIPER.md contains zero personal/company information.

        Success Criteria:
        - No mentions of: Q4, VA, DRAGONS, Kind Systems, Christian, xian
        - No specific project names or team structures
        - Only generic capabilities and personality
        - No company-specific examples
        """
        piper_md_path = Path("config/PIPER.md")

        assert piper_md_path.exists(), "PIPER.md must exist"

        content = piper_md_path.read_text()

        # Check for personal data patterns
        personal_patterns = [
            r"\bQ4\b",
            r"\bVA\b",
            r"\bDRAGONS\b",
            r"\bKind\s+Systems\b",
            r"\bChristian\b",
            r"\bxian\b",
            r"\bVeterans\s+Affairs\b",
            # Add more patterns as needed
        ]

        violations = []
        for pattern in personal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append(f"Found personal data: '{pattern}' matched {len(matches)} times")

        assert not violations, f"PIPER.md contains personal data:\n" + "\n".join(violations)

    def test_piper_md_has_generic_capabilities(self):
        """
        Verify PIPER.md contains generic system capabilities.

        Success Criteria:
        - Documents available capabilities
        - Describes personality traits
        - Lists integrations
        - All content is generic (not user-specific)
        """
        piper_md_path = Path("config/PIPER.md")
        content = piper_md_path.read_text().lower()

        # Check for expected generic sections
        expected_sections = [
            "capabilities",
            "integrations",
            "personality",
        ]

        for section in expected_sections:
            assert section in content, f"PIPER.md should document '{section}' generically"

    @pytest.mark.asyncio
    async def test_xian_personal_data_in_database(self, db_session):
        """
        Verify xian's personal data moved to alpha_users.preferences.

        Success Criteria:
        - User 'xian' exists in alpha_users
        - preferences field is populated (JSONB)
        - Contains projects, q4_goals, team info
        - Data structure is valid JSON
        """
        result = await db_session.execute(select(AlphaUser).where(AlphaUser.username == "xian"))
        user = result.scalar_one_or_none()

        assert user is not None, "User 'xian' must exist in alpha_users table"
        assert user.preferences is not None, "xian's preferences must be populated"
        assert isinstance(user.preferences, dict), "preferences must be a dictionary"

        # Check for expected personal data keys
        expected_keys = ["projects", "preferences", "q4_goals", "team", "context"]
        for key in expected_keys:
            assert (
                key in user.preferences
            ), f"xian's preferences must include '{key}' (personal data from PIPER.md)"

    @pytest.mark.asyncio
    async def test_config_service_generic_load(self, db_session):
        """
        Verify ConfigService returns only generic config when no user_id.

        Success Criteria:
        - load_config() with no user_id returns generic only
        - No personal data in generic config
        - Response includes capabilities and personality
        """
        from services.config.config_service import ConfigService

        config_service = ConfigService(db_session)

        # Load config without user_id (generic only)
        config = await config_service.load_config(user_id=None)

        assert config is not None, "ConfigService must return config"
        assert isinstance(config, dict), "Config must be a dictionary"

        # Verify no personal data in generic config
        config_str = str(config).lower()
        personal_terms = ["q4", "dragons", "kind systems", "va portal"]

        for term in personal_terms:
            assert (
                term not in config_str
            ), f"Generic config should not contain personal data: '{term}'"

    @pytest.mark.asyncio
    async def test_config_service_user_overlay(self, db_session):
        """
        Verify ConfigService merges user preferences over base config.

        Success Criteria:
        - load_config(user_id) includes user's personal data
        - Generic config preserved
        - User data overlays correctly
        - Personal data only visible to that user
        """
        from services.config.config_service import ConfigService

        # Get xian's user_id
        result = await db_session.execute(select(AlphaUser).where(AlphaUser.username == "xian"))
        user = result.scalar_one()

        config_service = ConfigService(db_session)

        # Load config with xian's user_id
        config = await config_service.load_config(user_id=str(user.id))

        assert config is not None, "ConfigService must return config for user"

        # Verify personal data present
        config_str = str(config).lower()
        assert (
            "projects" in config_str or "q4" in config_str
        ), "User config should include personal data from preferences"

        # Verify generic config still present
        assert (
            "capabilities" in config_str or "integrations" in config_str
        ), "User config should still include generic base config"

    @pytest.mark.asyncio
    async def test_multi_user_isolation(self, db_session):
        """
        Verify different users get different configs.

        Success Criteria:
        - User A's config has User A's data only
        - User B's config has User B's data only
        - No data leakage between users
        - Generic config shared by all users
        """
        from services.config.config_service import ConfigService

        # Get xian (existing user with personal data)
        result = await db_session.execute(select(AlphaUser).where(AlphaUser.username == "xian"))
        user_xian = result.scalar_one_or_none()

        # Create test user B with different preferences
        user_b = AlphaUser(
            username="test_user_b",
            email="testb@example.com",
            preferences={"projects": ["Test Project B"], "team": {"engineers": 3}},
        )
        db_session.add(user_b)
        await db_session.commit()

        config_service = ConfigService(db_session)

        # Load configs for both users
        if user_xian:
            config_xian = await config_service.load_config(user_id=str(user_xian.id))
            config_xian_str = str(config_xian).lower()

        config_b = await config_service.load_config(user_id=str(user_b.id))
        config_b_str = str(config_b).lower()

        # Verify user B's config has their data
        assert "test project b" in config_b_str, "User B's config should include their projects"

        # Verify user B's config does NOT have xian's data
        if user_xian:
            xian_projects = ["dragons", "va portal", "kind systems"]
            for project in xian_projects:
                assert (
                    project not in config_b_str
                ), f"User B's config should NOT include xian's data: '{project}'"

        # Cleanup
        await db_session.delete(user_b)
        await db_session.commit()

    def test_piper_md_backup_exists(self):
        """
        Verify backup was created before modifications.

        Success Criteria:
        - Backup file exists with date suffix
        - Backup contains original content (before extraction)
        """
        backup_files = list(Path("config").glob("PIPER.md.backup-*"))

        assert len(backup_files) > 0, "PIPER.md backup should exist before modifications"


# Fixtures for database session
@pytest.fixture
async def db_session():
    """Provide database session for tests"""
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        yield session
