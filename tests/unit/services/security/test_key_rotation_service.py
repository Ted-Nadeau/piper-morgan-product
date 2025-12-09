"""Tests for Key Rotation Service"""

import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.security.key_rotation_service import (
    KeyPair,
    KeyRotationService,
    RotationConfig,
    RotationMetrics,
    RotationPhase,
    RotationStatus,
    RotationStrategy,
    get_rotation_status,
    rotate_api_key,
)


class TestKeyRotationService:
    """Test key rotation service"""

    @pytest.fixture
    def rotation_service(self):
        """KeyRotationService instance for testing"""
        service = KeyRotationService()
        # Mock the dependencies
        service.keychain = Mock()
        service.llm_config = Mock()
        service.llm_config.validate_api_key = AsyncMock()
        service.validator = AsyncMock()
        service.user_service = Mock()
        return service

    @pytest.fixture
    def rotation_config(self):
        """Default rotation configuration"""
        return RotationConfig(
            strategy=RotationStrategy.GRADUAL,
            transition_duration_minutes=1,  # Short for testing
            health_check_interval_seconds=1,
            failure_threshold=2,
            rollback_on_failure=True,
        )

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_start_rotation_success(self, rotation_service, rotation_config):
        """Test starting a successful rotation"""
        # Mock existing key
        rotation_service.llm_config.get_api_key.return_value = "old-key-123"

        rotation_id = await rotation_service.start_rotation(
            "openai", "new-key-456", rotation_config
        )

        assert rotation_id is not None
        assert rotation_id in rotation_service.active_rotations

        status = rotation_service.active_rotations[rotation_id]
        assert status.provider == "openai"
        assert status.strategy == RotationStrategy.GRADUAL
        assert status.phase == RotationPhase.PREPARING

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_start_rotation_no_existing_key(self, rotation_service, rotation_config):
        """Test starting rotation with no existing key"""
        # Mock no existing key
        rotation_service.llm_config.get_api_key.return_value = None

        with pytest.raises(ValueError, match="No existing key found"):
            await rotation_service.start_rotation("openai", "new-key-456", rotation_config)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_start_rotation_user_specific_not_implemented(
        self, rotation_service, rotation_config
    ):
        """Test that user-specific rotation raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            await rotation_service.start_rotation(
                "openai", "new-key-456", rotation_config, user_id="user123"
            )

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_phase_validate_new_key_success(self, rotation_service):
        """Test successful new key validation phase"""
        # Mock successful validation
        validation_report = Mock()
        validation_report.is_valid = True
        rotation_service.validator.validate_api_key.return_value = validation_report

        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.PREPARING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=0,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        await rotation_service._phase_validate_new_key(status, key_pair)

        assert status.phase == RotationPhase.VALIDATING
        assert status.progress_percentage == 20
        rotation_service.validator.validate_api_key.assert_called_once_with(
            "openai", "new-key", skip_rate_limit=True
        )

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_phase_validate_new_key_failure(self, rotation_service):
        """Test new key validation failure"""
        # Mock validation failure
        validation_report = Mock()
        validation_report.is_valid = False
        validation_report.errors = [Mock(message="Invalid key format")]
        rotation_service.validator.validate_api_key.return_value = validation_report

        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.PREPARING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=0,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        with pytest.raises(ValueError, match="New key validation failed"):
            await rotation_service._phase_validate_new_key(status, key_pair)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_phase_begin_transition_gradual(self, rotation_service):
        """Test beginning gradual transition"""
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.VALIDATING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=20,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        await rotation_service._phase_begin_transition(status, key_pair)

        assert status.phase == RotationPhase.TRANSITIONING
        assert "openai" in rotation_service.key_usage_weights
        weights = rotation_service.key_usage_weights["openai"]
        assert weights["old"] == 0.9
        assert weights["new"] == 0.1

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_phase_begin_transition_immediate(self, rotation_service):
        """Test immediate transition strategy"""
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.VALIDATING,
            strategy=RotationStrategy.IMMEDIATE,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=20,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        await rotation_service._phase_begin_transition(status, key_pair)

        weights = rotation_service.key_usage_weights["openai"]
        assert weights["old"] == 0.0
        assert weights["new"] == 1.0
        assert status.progress_percentage == 80

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_phase_begin_transition_canary(self, rotation_service):
        """Test canary transition strategy"""
        config = RotationConfig(strategy=RotationStrategy.CANARY, canary_percentage=20)
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.VALIDATING,
            strategy=RotationStrategy.CANARY,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=20,
            metrics=RotationMetrics(),
            config=config,
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        await rotation_service._phase_begin_transition(status, key_pair)

        weights = rotation_service.key_usage_weights["openai"]
        assert weights["old"] == 0.8
        assert weights["new"] == 0.2

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_test_key_health_success(self, rotation_service):
        """Test successful key health check"""
        rotation_service.llm_config.validate_api_key.return_value = True

        result = await rotation_service._test_key_health("openai", "test-key")

        assert result is True
        rotation_service.llm_config.validate_api_key.assert_called_once_with("openai", "test-key")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_test_key_health_failure(self, rotation_service):
        """Test failed key health check"""
        rotation_service.llm_config.validate_api_key.return_value = False

        result = await rotation_service._test_key_health("openai", "test-key")

        assert result is False

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_test_key_health_exception(self, rotation_service):
        """Test key health check with exception"""
        rotation_service.llm_config.validate_api_key.side_effect = Exception("Network error")

        result = await rotation_service._test_key_health("openai", "test-key")

        assert result is False

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_perform_health_check_both_keys(self, rotation_service):
        """Test health check with both keys active"""
        # Mock successful health checks
        rotation_service.llm_config.validate_api_key.return_value = True

        # Set up weights for both keys
        rotation_service.key_usage_weights["openai"] = {"old": 0.5, "new": 0.5}

        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        result = await rotation_service._perform_health_check(status, key_pair)

        assert result is True
        assert status.metrics.old_key_requests == 1
        assert status.metrics.new_key_requests == 1
        assert status.metrics.old_key_failures == 0
        assert status.metrics.new_key_failures == 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_perform_health_check_with_callback(self, rotation_service):
        """Test health check with custom callback"""
        # Mock successful API health checks
        rotation_service.llm_config.validate_api_key.return_value = True

        # Add custom health callback
        callback_mock = Mock(return_value=True)
        rotation_service.add_health_callback(callback_mock)

        rotation_service.key_usage_weights["openai"] = {"old": 0.0, "new": 1.0}

        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        result = await rotation_service._perform_health_check(status, key_pair)

        assert result is True
        callback_mock.assert_called_once_with("openai", "test-123")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_perform_health_check_callback_failure(self, rotation_service):
        """Test health check with failing callback"""
        # Mock successful API health checks
        rotation_service.llm_config.validate_api_key.return_value = True

        # Add failing custom health callback
        callback_mock = Mock(return_value=False)
        rotation_service.add_health_callback(callback_mock)

        rotation_service.key_usage_weights["openai"] = {"old": 0.0, "new": 1.0}

        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        key_pair = KeyPair("old-key", "new-key", "openai")

        result = await rotation_service._perform_health_check(status, key_pair)

        assert result is False  # Should fail because callback returned False

    @pytest.mark.smoke
    def test_get_rotation_status(self, rotation_service):
        """Test getting rotation status"""
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Testing",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        rotation_service.active_rotations["test-123"] = status

        result = rotation_service.get_rotation_status("test-123")
        assert result == status

        # Test non-existent rotation
        result = rotation_service.get_rotation_status("non-existent")
        assert result is None

    @pytest.mark.smoke
    def test_get_active_rotations(self, rotation_service):
        """Test getting all active rotations"""
        status1 = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Testing",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        status2 = RotationStatus(
            rotation_id="test-456",
            provider="anthropic",
            phase=RotationPhase.TRANSITIONING,
            strategy=RotationStrategy.CANARY,
            started_at=datetime.now(),
            current_step="Testing",
            progress_percentage=30,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        rotation_service.active_rotations["test-123"] = status1
        rotation_service.active_rotations["test-456"] = status2

        active = rotation_service.get_active_rotations()
        assert len(active) == 2
        assert status1 in active
        assert status2 in active

    @pytest.mark.smoke
    def test_get_rotation_history(self, rotation_service):
        """Test getting rotation history"""
        # Add some history
        for i in range(5):
            status = RotationStatus(
                rotation_id=f"test-{i}",
                provider="openai",
                phase=RotationPhase.COMPLETED,
                strategy=RotationStrategy.GRADUAL,
                started_at=datetime.now(),
                current_step="Completed",
                progress_percentage=100,
                metrics=RotationMetrics(),
                config=RotationConfig(),
            )
            rotation_service.rotation_history.append(status)

        history = rotation_service.get_rotation_history(limit=3)
        assert len(history) == 3

        # Should get the last 3
        assert history[0].rotation_id == "test-2"
        assert history[1].rotation_id == "test-3"
        assert history[2].rotation_id == "test-4"

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_cancel_rotation_success(self, rotation_service):
        """Test successful rotation cancellation"""
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Testing",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
            can_rollback=True,
        )

        rotation_service.active_rotations["test-123"] = status

        result = await rotation_service.cancel_rotation("test-123", "User requested")

        assert result is True
        assert status.phase == RotationPhase.FAILED
        assert "User requested" in status.errors[0]

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_cancel_rotation_not_found(self, rotation_service):
        """Test cancelling non-existent rotation"""
        result = await rotation_service.cancel_rotation("non-existent")
        assert result is False

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_cancel_rotation_already_completed(self, rotation_service):
        """Test cancelling already completed rotation"""
        status = RotationStatus(
            rotation_id="test-123",
            provider="openai",
            phase=RotationPhase.COMPLETED,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Completed",
            progress_percentage=100,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        rotation_service.active_rotations["test-123"] = status

        result = await rotation_service.cancel_rotation("test-123")
        assert result is False

    @pytest.mark.smoke
    def test_get_key_for_request_no_rotation(self, rotation_service):
        """Test getting key when no rotation is active"""
        rotation_service.llm_config.get_api_key.return_value = "normal-key"

        key = rotation_service.get_key_for_request("openai")

        assert key == "normal-key"
        rotation_service.llm_config.get_api_key.assert_called_once_with("openai")

    @pytest.mark.smoke
    def test_get_key_for_request_during_rotation(self, rotation_service):
        """Test getting key during rotation"""
        rotation_service.llm_config.get_api_key.return_value = "current-key"
        rotation_service.key_usage_weights["openai"] = {"old": 0.3, "new": 0.7}

        # Mock random to always return new key
        with patch("random.random", return_value=0.5):  # 0.5 < 0.7, so new key
            key = rotation_service.get_key_for_request("openai")

        assert key == "current-key"

    @pytest.mark.smoke
    def test_cleanup_completed_rotations(self, rotation_service):
        """Test cleaning up completed rotations"""
        # Add active rotation
        active_status = RotationStatus(
            rotation_id="active-123",
            provider="openai",
            phase=RotationPhase.MONITORING,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Active",
            progress_percentage=50,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        # Add completed rotation
        completed_status = RotationStatus(
            rotation_id="completed-123",
            provider="anthropic",
            phase=RotationPhase.COMPLETED,
            strategy=RotationStrategy.GRADUAL,
            started_at=datetime.now(),
            current_step="Completed",
            progress_percentage=100,
            metrics=RotationMetrics(),
            config=RotationConfig(),
        )

        rotation_service.active_rotations["active-123"] = active_status
        rotation_service.active_rotations["completed-123"] = completed_status

        cleaned = rotation_service.cleanup_completed_rotations()

        assert cleaned == 1
        assert "active-123" in rotation_service.active_rotations
        assert "completed-123" not in rotation_service.active_rotations

    @pytest.mark.smoke
    def test_add_health_callback(self, rotation_service):
        """Test adding health callback"""
        callback = Mock()

        rotation_service.add_health_callback(callback)

        assert callback in rotation_service.health_callbacks


class TestKeyPair:
    """Test KeyPair dataclass"""

    @pytest.mark.smoke
    def test_key_pair_creation(self):
        """Test KeyPair creation and hash generation"""
        key_pair = KeyPair("old-key-123", "new-key-456", "openai")

        assert key_pair.old_key == "old-key-123"
        assert key_pair.new_key == "new-key-456"
        assert key_pair.provider == "openai"
        assert len(key_pair.old_key_hash) == 16
        assert len(key_pair.new_key_hash) == 16
        assert key_pair.old_key_hash != key_pair.new_key_hash


class TestConvenienceFunctions:
    """Test convenience functions"""

    @pytest.mark.asyncio
    @patch("services.security.key_rotation_service.key_rotation_service")
    @pytest.mark.smoke
    async def test_rotate_api_key_convenience(self, mock_service):
        """Test rotate_api_key convenience function"""
        mock_service.start_rotation = AsyncMock(return_value="rotation-123")

        rotation_id = await rotate_api_key("openai", "new-key", RotationStrategy.CANARY, 45)

        assert rotation_id == "rotation-123"
        mock_service.start_rotation.assert_called_once()

        # Check config was created correctly
        call_args = mock_service.start_rotation.call_args
        config = call_args[0][2]  # Third argument is config
        assert config.strategy == RotationStrategy.CANARY
        assert config.transition_duration_minutes == 45

    @patch("services.security.key_rotation_service.key_rotation_service")
    @pytest.mark.smoke
    def test_get_rotation_status_convenience(self, mock_service):
        """Test get_rotation_status convenience function"""
        mock_status = Mock()
        mock_service.get_rotation_status.return_value = mock_status

        result = get_rotation_status("rotation-123")

        assert result == mock_status
        mock_service.get_rotation_status.assert_called_once_with("rotation-123")
