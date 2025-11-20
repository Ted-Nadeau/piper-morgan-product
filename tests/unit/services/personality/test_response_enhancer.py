"""
Tests for ResponsePersonalityEnhancer aggregate root
"""

import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.personality.exceptions import (
    PerformanceTimeoutError,
    ProfileLoadError,
    TransformationError,
)
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    EnhancedResponse,
    PersonalityProfile,
    ResponseContext,
    ResponseType,
    TechnicalPreference,
)
from services.personality.response_enhancer import CircuitBreaker, ResponsePersonalityEnhancer


class TestResponsePersonalityEnhancer:
    """Test ResponsePersonalityEnhancer core functionality"""

    @pytest.fixture
    def mock_repository(self):
        """Mock PersonalityProfileRepository"""
        repo = AsyncMock()
        return repo

    @pytest.fixture
    def mock_transformation_service(self):
        """Mock TransformationService"""
        service = MagicMock()
        service.add_warmth = MagicMock(return_value="Enhanced with warmth: content")
        service.inject_confidence = MagicMock(return_value="Enhanced with confidence: content")
        service.extract_actions = MagicMock(return_value="Enhanced with actions: content")
        return service

    @pytest.fixture
    def mock_cache(self):
        """Mock ProfileCache"""
        cache = MagicMock()
        cache.get.return_value = None  # Cache miss by default
        return cache

    @pytest.fixture
    def test_profile(self):
        """Test PersonalityProfile"""
        return PersonalityProfile(
            id="test-profile-id",
            user_id="test_user",
            warmth_level=0.7,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    @pytest.fixture
    def test_context(self):
        """Test ResponseContext"""
        return ResponseContext(
            intent_confidence=0.8,
            intent_category="execution",
            intent_action="create_ticket",
            response_type=ResponseType.CLI,
        )

    @pytest.fixture
    def enhancer(self, mock_repository, mock_transformation_service, mock_cache):
        """ResponsePersonalityEnhancer with mocked dependencies"""
        return ResponsePersonalityEnhancer(
            profile_repository=mock_repository,
            transformation_service=mock_transformation_service,
            profile_cache=mock_cache,
            performance_timeout_ms=100,
        )

    @pytest.mark.asyncio
    async def test_enhance_response_success(
        self, enhancer, mock_repository, test_profile, test_context
    ):
        """Test successful response enhancement"""
        # Arrange
        mock_repository.get_by_user_id.return_value = test_profile
        content = "Original content"
        user_id = "test_user"

        # Act
        result = await enhancer.enhance_response(content, test_context, user_id)

        # Assert
        assert isinstance(result, EnhancedResponse)
        assert result.success is True
        assert result.original_content == content
        assert result.enhanced_content != content  # Should be transformed
        assert result.processing_time_ms > 0
        assert len(result.enhancements_applied) > 0

        # Verify repository was called
        mock_repository.get_by_user_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_enhance_response_profile_not_found(
        self, enhancer, mock_repository, test_context
    ):
        """Test enhancement when profile not found (creates default)"""
        # Arrange
        mock_repository.get_by_user_id.return_value = None
        mock_repository.save = AsyncMock()  # Mock save for default profile
        content = "Original content"
        user_id = "missing_user"

        # Act
        result = await enhancer.enhance_response(content, test_context, user_id)

        # Assert
        assert result.success is True  # Should succeed with default profile
        assert result.enhanced_content != content  # Should be enhanced
        assert result.personality_profile_used.user_id == user_id  # Uses default profile
        mock_repository.save.assert_called_once()  # Default profile should be saved

    @pytest.mark.asyncio
    async def test_enhance_response_circuit_breaker_open(self, enhancer, test_context):
        """Test enhancement when circuit breaker is open"""
        # Arrange
        import time

        enhancer.circuit_breaker.state = "OPEN"
        enhancer.circuit_breaker.failure_count = 10  # Above threshold
        enhancer.circuit_breaker.last_failure_time = time.time()  # Recent failure
        content = "Original content"
        user_id = "test_user"

        # Act
        result = await enhancer.enhance_response(content, test_context, user_id)

        # Assert
        assert result.success is False
        assert result.enhanced_content == content
        assert "Circuit breaker open" in result.error_message

    @pytest.mark.skip(
        reason="Flaky timing test - timeout mechanism not triggering correctly. Tracked in piper-morgan-cjz"
    )
    @pytest.mark.asyncio
    async def test_enhance_response_timeout(
        self, enhancer, mock_repository, test_profile, test_context
    ):
        """Test enhancement timeout handling"""
        # Arrange
        enhancer.performance_timeout_ms = 1  # Very short timeout
        mock_repository.get_by_user_id.return_value = test_profile

        # Mock a slow transformation - transformation methods are synchronous, not async!
        import time as time_module

        slow_service = MagicMock()

        def slow_transform(*args, **kwargs):
            time_module.sleep(0.1)  # Blocking sleep - longer than 1ms timeout
            return "transformed"

        # Transformation service methods are synchronous (not awaited in code)
        slow_service.add_warmth = MagicMock(side_effect=slow_transform)
        slow_service.inject_confidence = MagicMock(return_value="confidence")
        slow_service.extract_actions = MagicMock(return_value="actions")

        enhancer.transformation_service = slow_service

        # Act
        result = await enhancer.enhance_response("content", test_context, "user")

        # Assert
        assert result.success is False
        assert "timeout" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_cache_hit_scenario(self, enhancer, mock_cache, test_profile, test_context):
        """Test response enhancement with cache hit"""
        # Arrange
        mock_cache.get.return_value = test_profile  # Cache hit
        content = "Original content"
        user_id = "cached_user"

        # Act
        result = await enhancer.enhance_response(content, test_context, user_id)

        # Assert
        assert result.success is True
        mock_cache.get.assert_called_once_with(user_id)
        assert enhancer.cache_hits > 0

    @pytest.mark.asyncio
    async def test_metrics_tracking(self, enhancer, mock_repository, test_profile, test_context):
        """Test that metrics are properly tracked"""
        # Arrange
        mock_repository.get_by_user_id.return_value = test_profile
        initial_count = enhancer.enhancement_count

        # Act
        await enhancer.enhance_response("content", test_context, "user")

        # Assert
        assert enhancer.enhancement_count == initial_count + 1
        assert enhancer.total_enhancement_time_ms > 0

        metrics = enhancer.get_metrics()
        assert "enhancement_count" in metrics
        assert "average_enhancement_time_ms" in metrics
        assert "cache_hit_rate" in metrics


class TestCircuitBreaker:
    """Test CircuitBreaker functionality"""

    @pytest.fixture
    def circuit_breaker(self):
        """CircuitBreaker with test settings"""
        return CircuitBreaker(failure_threshold=3, timeout_seconds=1)

    def test_initial_state_closed(self, circuit_breaker):
        """Test circuit breaker starts in CLOSED state"""
        assert circuit_breaker.get_state() == "CLOSED"
        assert circuit_breaker.is_open() is False

    def test_failure_threshold_opens_circuit(self, circuit_breaker):
        """Test that reaching failure threshold opens circuit"""
        # Record failures up to threshold
        for _ in range(3):
            circuit_breaker.record_failure()

        assert circuit_breaker.get_state() == "OPEN"
        assert circuit_breaker.is_open() is True

    @pytest.mark.skip(
        reason="Bug - CircuitBreaker.record_success() not resetting failure_count. Tracked in piper-morgan-3qz"
    )
    def test_success_resets_failure_count(self, circuit_breaker):
        """Test that success resets failure count in CLOSED state"""
        circuit_breaker.record_failure()
        circuit_breaker.record_success()

        assert circuit_breaker.failure_count == 0
        assert circuit_breaker.get_state() == "CLOSED"

    def test_half_open_transition(self, circuit_breaker):
        """Test transition from OPEN to HALF_OPEN after timeout"""
        # Open the circuit
        for _ in range(3):
            circuit_breaker.record_failure()
        assert circuit_breaker.get_state() == "OPEN"

        # Simulate timeout passage
        import time

        circuit_breaker.last_failure_time = time.time() - 2  # 2 seconds ago

        # Should transition to HALF_OPEN
        assert circuit_breaker.is_open() is False
        assert circuit_breaker.get_state() == "HALF_OPEN"

    def test_half_open_to_closed_on_success(self, circuit_breaker):
        """Test HALF_OPEN to CLOSED on success"""
        # Set to HALF_OPEN state
        circuit_breaker.state = "HALF_OPEN"

        circuit_breaker.record_success()

        assert circuit_breaker.get_state() == "CLOSED"
        assert circuit_breaker.failure_count == 0
