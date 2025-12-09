"""
Tests for PersonalityProfileRepository data access layer
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest

from services.personality.exceptions import ConfigurationError, ProfileLoadError
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)
from services.personality.repository import PersonalityProfileRepository


class TestPersonalityProfileRepository:
    """Test PersonalityProfileRepository data access and PIPER.user.md integration"""

    @pytest.fixture
    def repository(self):
        """PersonalityProfileRepository instance"""
        return PersonalityProfileRepository()

    @pytest.fixture
    def test_profile(self):
        """Test PersonalityProfile"""
        return PersonalityProfile(
            id="test-id",
            user_id="test_user",
            warmth_level=0.7,
            confidence_style=ConfidenceDisplayStyle.NUMERIC,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
        )

    @pytest.mark.asyncio
    @patch("services.personality.repository.AsyncSessionFactory")
    @pytest.mark.smoke
    async def test_get_by_user_id_success(self, mock_session_factory, repository, test_profile):
        """Test successful profile retrieval from database"""
        # Arrange
        mock_session = AsyncMock()
        mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_model.user_id = test_profile.user_id
        mock_model.warmth_level = test_profile.warmth_level
        mock_model.confidence_style = test_profile.confidence_style.value
        mock_model.action_orientation = test_profile.action_orientation.value
        mock_model.technical_depth = test_profile.technical_depth.value
        mock_model.created_at = test_profile.created_at
        mock_model.updated_at = test_profile.updated_at
        mock_model.is_active = test_profile.is_active
        mock_model.id = test_profile.id

        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_by_user_id("test_user")

        # Assert
        assert result is not None
        assert result.user_id == test_profile.user_id
        assert result.warmth_level == test_profile.warmth_level
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @patch("services.personality.repository.AsyncSessionFactory")
    @pytest.mark.smoke
    async def test_get_by_user_id_not_found_creates_default(self, mock_session_factory, repository):
        """Test that get_by_user_id creates default profile when not found"""
        # Arrange
        mock_session = AsyncMock()
        mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None  # Not found
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_by_user_id("new_user")

        # Assert
        assert result is not None
        assert result.user_id == "new_user"
        assert 0.0 <= result.warmth_level <= 1.0
        # Should have called save to create the profile
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    @patch("services.personality.repository.AsyncSessionFactory")
    @pytest.mark.smoke
    async def test_save_new_profile(self, mock_session_factory, repository, test_profile):
        """Test saving new profile to database"""
        # Arrange
        mock_session = AsyncMock()
        mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None  # No existing profile
        mock_session.execute.return_value = mock_result

        # Act
        await repository.save(test_profile)

        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @patch("services.personality.repository.AsyncSessionFactory")
    @pytest.mark.smoke
    async def test_save_existing_profile_updates(
        self, mock_session_factory, repository, test_profile
    ):
        """Test updating existing profile in database"""
        # Arrange
        mock_session = AsyncMock()
        mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_existing = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_existing  # Existing profile
        mock_session.execute.return_value = mock_result

        # Act
        await repository.save(test_profile)

        # Assert
        mock_session.execute.assert_called()  # Both SELECT and UPDATE
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_piper_config_parsing_success(self, repository):
        """Test successful PIPER.user.md configuration parsing"""
        yaml_content = """
personality:
  profile:
    warmth_level: 0.8
    confidence_style: "high"
    action_orientation: "high"
    technical_depth: "detailed"
"""

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getmtime", return_value=1234567890.0):
                    config = await repository._load_piper_config_overrides()

        assert config is not None
        assert config["profile"]["warmth_level"] == 0.8
        assert config["profile"]["confidence_style"] == "high"

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_piper_config_file_not_found(self, repository):
        """Test handling when PIPER.user.md doesn't exist"""
        with patch("os.path.exists", return_value=False):
            config = await repository._load_piper_config_overrides()

        assert config is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_piper_config_invalid_yaml(self, repository):
        """Test handling of invalid YAML in PIPER.user.md"""
        invalid_yaml = "personality:\n  invalid: yaml: content:"

        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getmtime", return_value=1234567890.0):
                    config = await repository._load_piper_config_overrides()

        assert config is None

    @pytest.mark.smoke
    def test_apply_overrides_valid_values(self, repository, test_profile):
        """Test applying valid PIPER.user.md overrides"""
        overrides = {
            "warmth_level": 0.9,
            "confidence_style": "numeric",
            "action_orientation": "low",
            "technical_depth": "simplified",
        }

        result = repository._apply_overrides(test_profile, overrides)

        assert result.warmth_level == 0.9
        assert result.confidence_style == ConfidenceDisplayStyle.NUMERIC
        assert result.action_orientation == ActionLevel.LOW
        assert result.technical_depth == TechnicalPreference.SIMPLIFIED

    @pytest.mark.smoke
    def test_apply_overrides_invalid_values(self, repository, test_profile):
        """Test applying invalid override values falls back to defaults"""
        overrides = {
            "warmth_level": 1.5,  # Invalid: > 1.0
            "confidence_style": "invalid_style",
            "action_orientation": "invalid_action",
            "technical_depth": "invalid_depth",
        }

        result = repository._apply_overrides(test_profile, overrides)

        # Should fall back to original values for invalid overrides
        assert result.warmth_level == test_profile.warmth_level  # Invalid warmth reverted
        assert result.confidence_style == test_profile.confidence_style  # Invalid style reverted
        assert (
            result.action_orientation == test_profile.action_orientation
        )  # Invalid action reverted
        assert result.technical_depth == test_profile.technical_depth  # Invalid depth reverted

    @pytest.mark.smoke
    def test_apply_overrides_partial_values(self, repository, test_profile):
        """Test applying partial overrides keeps existing values"""
        overrides = {
            "warmth_level": 0.9,
            # Other values not specified
        }

        result = repository._apply_overrides(test_profile, overrides)

        assert result.warmth_level == 0.9  # Overridden
        assert result.confidence_style == test_profile.confidence_style  # Preserved
        assert result.action_orientation == test_profile.action_orientation  # Preserved
        assert result.technical_depth == test_profile.technical_depth  # Preserved

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_delete_profile_success(self, repository):
        """Test successful profile deletion"""
        with patch("services.personality.repository.AsyncSessionFactory") as mock_session_factory:
            mock_session = AsyncMock()
            mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

            mock_result = MagicMock()
            mock_result.rowcount = 1
            mock_session.execute.return_value = mock_result

            result = await repository.delete("test_user")

            assert result is True
            mock_session.execute.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_delete_profile_not_found(self, repository):
        """Test deletion when profile doesn't exist"""
        with patch("services.personality.repository.AsyncSessionFactory") as mock_session_factory:
            mock_session = AsyncMock()
            mock_session_factory.session_scope.return_value.__aenter__.return_value = mock_session

            mock_result = MagicMock()
            mock_result.rowcount = 0  # No rows deleted
            mock_session.execute.return_value = mock_result

            result = await repository.delete("nonexistent_user")

            assert result is False
