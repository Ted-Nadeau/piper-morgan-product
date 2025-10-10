"""Tests for LLMDomainService"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.llm_domain_service import LLMDomainService
from services.service_registry import ServiceRegistry


class TestLLMDomainService:
    """Test LLM domain service"""

    @pytest.fixture
    def mock_config_service(self):
        """Mock LLMConfigService"""
        mock = Mock()
        mock.get_available_providers.return_value = ["openai", "gemini"]
        mock.get_default_provider.return_value = "openai"
        mock.get_api_key.return_value = "test-key"  # Now comes from keychain or env
        mock.validate_all_providers = AsyncMock(
            return_value={"openai": Mock(is_valid=True), "gemini": Mock(is_valid=True)}
        )
        return mock

    @pytest.fixture
    def mock_provider_selector(self):
        """Mock ProviderSelector"""
        mock = Mock()
        mock.select_provider.return_value = "openai"
        return mock

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM client"""
        mock = Mock()
        mock.complete = AsyncMock(return_value="test response")
        return mock

    async def test_initialization(
        self, mock_config_service, mock_provider_selector, mock_llm_client
    ):
        """Service initializes correctly"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )

            assert not service.is_initialized()

            await service.initialize()

            assert service.is_initialized()
            mock_config_service.validate_all_providers.assert_called_once()

    async def test_complete_with_task_type(
        self, mock_config_service, mock_provider_selector, mock_llm_client
    ):
        """Complete uses task_type parameter"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )
            await service.initialize()

            result = await service.complete(task_type="test_task", prompt="test prompt")

            assert result == "test response"
            mock_llm_client.complete.assert_called_once_with(
                task_type="test_task", prompt="test prompt", context=None, response_format=None
            )

    async def test_complete_with_context(
        self, mock_config_service, mock_provider_selector, mock_llm_client
    ):
        """Complete passes context to client"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )
            await service.initialize()

            context = {"key": "value"}
            result = await service.complete(
                task_type="test_task", prompt="test prompt", context=context
            )

            assert result == "test response"
            mock_llm_client.complete.assert_called_once_with(
                task_type="test_task", prompt="test prompt", context=context, response_format=None
            )

    async def test_complete_before_initialization(self):
        """Complete raises error if not initialized"""
        service = LLMDomainService()

        with pytest.raises(RuntimeError, match="not initialized"):
            await service.complete("test_task", "test")

    async def test_get_available_providers(
        self, mock_config_service, mock_provider_selector, mock_llm_client
    ):
        """Returns available providers"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )
            await service.initialize()

            providers = service.get_available_providers()
            assert providers == ["openai", "gemini"]

    async def test_get_default_provider(
        self, mock_config_service, mock_provider_selector, mock_llm_client
    ):
        """Returns default provider"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )
            await service.initialize()

            provider = service.get_default_provider()
            assert provider == "openai"

    async def test_get_providers_before_initialization(self):
        """Get providers raises error if not initialized"""
        service = LLMDomainService()

        with pytest.raises(RuntimeError, match="not initialized"):
            service.get_available_providers()

    async def test_complete_error_handling(self, mock_config_service, mock_provider_selector):
        """Complete propagates errors from client"""
        error_client = Mock()
        error_client.complete = AsyncMock(side_effect=ValueError("Client error"))

        with patch("services.llm.clients.llm_client", error_client):
            service = LLMDomainService(
                config_service=mock_config_service, provider_selector=mock_provider_selector
            )
            await service.initialize()

            with pytest.raises(ValueError, match="Client error"):
                await service.complete("test_task", "test")


class TestServiceRegistry:
    """Test ServiceRegistry"""

    def setup_method(self):
        """Clear registry before each test"""
        ServiceRegistry.clear()

    def test_register_service(self):
        """Can register service"""
        mock_service = Mock()
        ServiceRegistry.register("test", mock_service)

        assert ServiceRegistry.is_registered("test")
        assert ServiceRegistry.get("test") == mock_service

    def test_get_unregistered_service(self):
        """Raises error for unregistered service"""
        with pytest.raises(RuntimeError, match="not registered"):
            ServiceRegistry.get("nonexistent")

    def test_register_duplicate(self):
        """Raises error for duplicate registration"""
        ServiceRegistry.register("test", Mock())

        with pytest.raises(ValueError, match="already registered"):
            ServiceRegistry.register("test", Mock())

    def test_list_services(self):
        """Lists registered services"""
        ServiceRegistry.register("svc1", Mock())
        ServiceRegistry.register("svc2", Mock())

        services = ServiceRegistry.list_services()
        assert "svc1" in services
        assert "svc2" in services

    def test_get_llm_convenience(self):
        """Convenience method for LLM access"""
        mock_llm = Mock()
        ServiceRegistry.register("llm", mock_llm)

        assert ServiceRegistry.get_llm() == mock_llm

    def test_clear_registry(self):
        """Clear removes all services"""
        ServiceRegistry.register("test", Mock())
        assert ServiceRegistry.is_registered("test")

        ServiceRegistry.clear()
        assert not ServiceRegistry.is_registered("test")
        assert not ServiceRegistry.is_initialized()

    def test_mark_initialized(self):
        """Can mark registry as initialized"""
        assert not ServiceRegistry.is_initialized()

        ServiceRegistry.mark_initialized()
        assert ServiceRegistry.is_initialized()

        ServiceRegistry.clear()
        assert not ServiceRegistry.is_initialized()
