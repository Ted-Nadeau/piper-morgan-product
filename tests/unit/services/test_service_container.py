"""
Unit tests for Service Container (Phase 1.5)

Tests the DDD service container pattern:
- ServiceRegistry: service registration and retrieval
- ServiceContainer: singleton pattern and lifecycle
- ServiceInitializer: ordered initialization
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.container.exceptions import (
    ContainerNotInitializedError,
    ServiceInitializationError,
    ServiceNotFoundError,
)
from services.container.initialization import ServiceInitializer
from services.container.service_container import ServiceContainer
from services.container.service_registry import ServiceRegistry


class TestServiceRegistry:
    """Test ServiceRegistry functionality."""

    @pytest.mark.smoke
    def test_register_and_get_service(self):
        """Test registering and retrieving a service."""
        registry = ServiceRegistry()
        mock_service = Mock()

        registry.register("test_service", mock_service)
        retrieved = registry.get("test_service")

        assert retrieved is mock_service

    @pytest.mark.smoke
    def test_register_with_metadata(self):
        """Test registering service with metadata."""
        registry = ServiceRegistry()
        mock_service = Mock()
        metadata = {"version": "1.0", "dependencies": ["other"]}

        registry.register("test_service", mock_service, metadata=metadata)
        retrieved_metadata = registry.get_metadata("test_service")

        assert retrieved_metadata == metadata

    @pytest.mark.smoke
    def test_has_service(self):
        """Test checking if service exists."""
        registry = ServiceRegistry()
        mock_service = Mock()

        assert not registry.has("test_service")

        registry.register("test_service", mock_service)

        assert registry.has("test_service")

    @pytest.mark.smoke
    def test_list_services(self):
        """Test listing all registered services."""
        registry = ServiceRegistry()

        # Empty initially
        assert registry.list_services() == []

        # Add services
        registry.register("service1", Mock())
        registry.register("service2", Mock())

        services = registry.list_services()
        assert len(services) == 2
        assert "service1" in services
        assert "service2" in services

    @pytest.mark.smoke
    def test_get_nonexistent_service_raises_error(self):
        """Test getting non-existent service raises KeyError."""
        registry = ServiceRegistry()

        with pytest.raises(KeyError) as exc_info:
            registry.get("nonexistent")

        assert "nonexistent" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)

    @pytest.mark.smoke
    def test_clear_services(self):
        """Test clearing all services."""
        registry = ServiceRegistry()
        registry.register("service1", Mock())
        registry.register("service2", Mock())

        assert len(registry.list_services()) == 2

        registry.clear()

        assert len(registry.list_services()) == 0


class TestServiceContainer:
    """Test ServiceContainer singleton and lifecycle."""

    def setup_method(self):
        """Reset container before each test."""
        ServiceContainer.reset()

    def teardown_method(self):
        """Reset container after each test."""
        ServiceContainer.reset()

    @pytest.mark.smoke
    def test_singleton_pattern(self):
        """Test that ServiceContainer enforces singleton pattern."""
        container1 = ServiceContainer()
        container2 = ServiceContainer()

        assert container1 is container2

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_initialize_once(self):
        """Test that initialize() is idempotent."""
        container = ServiceContainer()

        with patch.object(
            ServiceInitializer, "initialize_all", new_callable=AsyncMock
        ) as mock_init:
            # First call should initialize
            await container.initialize()
            assert mock_init.call_count == 1
            assert container.is_initialized()

            # Second call should skip
            await container.initialize()
            assert mock_init.call_count == 1  # Still 1, not called again

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_service_when_not_initialized(self):
        """Test getting service before initialization raises error."""
        container = ServiceContainer()

        with pytest.raises(ContainerNotInitializedError) as exc_info:
            container.get_service("llm")

        assert "not initialized" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_service_success(self):
        """Test getting service after initialization."""
        container = ServiceContainer()

        # Mock initialization
        mock_service = Mock()
        with patch.object(ServiceInitializer, "initialize_all", new_callable=AsyncMock):
            await container.initialize()
            # Manually register service for test
            container._registry.register("test_service", mock_service)

        retrieved = container.get_service("test_service")
        assert retrieved is mock_service

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_nonexistent_service_raises_error(self):
        """Test getting non-existent service raises ServiceNotFoundError."""
        container = ServiceContainer()

        with patch.object(ServiceInitializer, "initialize_all", new_callable=AsyncMock):
            await container.initialize()

        with pytest.raises(ServiceNotFoundError) as exc_info:
            container.get_service("nonexistent")

        assert "nonexistent" in str(exc_info.value)

    @pytest.mark.smoke
    def test_has_service_when_not_initialized(self):
        """Test has_service returns False when not initialized."""
        container = ServiceContainer()
        assert not container.has_service("llm")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_has_service_after_initialization(self):
        """Test has_service works after initialization."""
        container = ServiceContainer()

        mock_service = Mock()
        with patch.object(ServiceInitializer, "initialize_all", new_callable=AsyncMock):
            await container.initialize()
            container._registry.register("test_service", mock_service)

        assert container.has_service("test_service")
        assert not container.has_service("nonexistent")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_list_services(self):
        """Test listing services."""
        container = ServiceContainer()

        # Empty when not initialized
        assert container.list_services() == []

        # Has services after initialization
        with patch.object(ServiceInitializer, "initialize_all", new_callable=AsyncMock):
            await container.initialize()
            container._registry.register("service1", Mock())
            container._registry.register("service2", Mock())

        services = container.list_services()
        assert len(services) == 2
        assert "service1" in services
        assert "service2" in services

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_shutdown(self):
        """Test shutdown clears services."""
        container = ServiceContainer()

        with patch.object(ServiceInitializer, "initialize_all", new_callable=AsyncMock):
            await container.initialize()
            container._registry.register("test_service", Mock())

        assert container.is_initialized()
        assert len(container.list_services()) > 0

        container.shutdown()

        assert not container.is_initialized()
        assert len(container.list_services()) == 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_initialization_failure_propagates(self):
        """Test that initialization failures are propagated."""
        container = ServiceContainer()

        with patch.object(
            ServiceInitializer, "initialize_all", new_callable=AsyncMock
        ) as mock_init:
            mock_init.side_effect = Exception("Initialization failed")

            with pytest.raises(Exception) as exc_info:
                await container.initialize()

            assert "Initialization failed" in str(exc_info.value)
            assert not container.is_initialized()


class TestServiceInitializer:
    """Test ServiceInitializer initialization logic."""

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_initialize_all_calls_services_in_order(self):
        """Test that services are initialized in correct order."""
        registry = ServiceRegistry()
        initializer = ServiceInitializer(registry)

        # Mock LLM service
        mock_llm_service = Mock()
        mock_llm_service.initialize = AsyncMock()

        # Mock Intent service
        mock_intent_service = Mock()

        with patch(
            "services.domain.llm_domain_service.LLMDomainService", return_value=mock_llm_service
        ):
            with patch(
                "services.intent.intent_service.IntentService", return_value=mock_intent_service
            ):
                await initializer.initialize_all()

        # Verify LLM service initialized
        mock_llm_service.initialize.assert_called_once()
        assert registry.has("llm")

        # Verify Intent service initialized
        assert registry.has("intent")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_llm_service_initialization_failure(self):
        """Test that LLM initialization failure raises ServiceInitializationError."""
        registry = ServiceRegistry()
        initializer = ServiceInitializer(registry)

        # Mock LLM service that fails to initialize
        mock_llm_service = Mock()
        mock_llm_service.initialize = AsyncMock(side_effect=Exception("API key missing"))

        with patch(
            "services.domain.llm_domain_service.LLMDomainService", return_value=mock_llm_service
        ):
            with pytest.raises(ServiceInitializationError) as exc_info:
                await initializer.initialize_all()

            assert exc_info.value.service_name == "llm"
            assert "API key missing" in str(exc_info.value.original_error)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_intent_service_initialization_failure(self):
        """Test that Intent initialization failure raises ServiceInitializationError."""
        registry = ServiceRegistry()
        initializer = ServiceInitializer(registry)

        # Mock successful LLM service
        mock_llm_service = Mock()
        mock_llm_service.initialize = AsyncMock()

        # Mock Intent service that fails to initialize
        with patch(
            "services.domain.llm_domain_service.LLMDomainService", return_value=mock_llm_service
        ):
            with patch(
                "services.intent.intent_service.IntentService",
                side_effect=Exception("Intent service error"),
            ):
                with pytest.raises(ServiceInitializationError) as exc_info:
                    await initializer.initialize_all()

                assert exc_info.value.service_name == "intent"
                assert "Intent service error" in str(exc_info.value.original_error)
