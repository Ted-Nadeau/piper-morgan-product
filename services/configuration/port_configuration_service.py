"""
Port Configuration Service
Centralized port and URL configuration management following DDD principles

Created: 2025-09-12 by Code Agent Step 4 - Configuration Architecture Centralization
Eliminates hardcoded port values and provides environment-based configuration
"""

import os
from dataclasses import dataclass
from typing import Dict, Optional

import structlog

logger = structlog.get_logger()


@dataclass
class PortConfiguration:
    """Type-safe port configuration for all services"""

    backend_port: int
    web_port: int
    backend_host: str = "127.0.0.1"
    web_host: str = "127.0.0.1"

    def get_backend_url(self) -> str:
        """Get backend API base URL"""
        return f"http://{self.backend_host}:{self.backend_port}"

    def get_web_url(self) -> str:
        """Get web interface base URL"""
        return f"http://{self.web_host}:{self.web_port}"

    def get_api_base_url(self) -> str:
        """Get API base URL for service communication"""
        return self.get_backend_url()


class PortConfigurationService:
    """
    Domain service for centralized port and URL configuration management

    Follows DDD principles:
    - Encapsulates port configuration logic
    - Provides environment-based configuration
    - Eliminates hardcoded values across the application
    - Supports development, staging, and production environments
    """

    def __init__(self, environment: Optional[str] = None):
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self._config = None
        logger.debug("PortConfigurationService initialized", environment=self.environment)

    def get_configuration(self) -> PortConfiguration:
        """
        Get port configuration based on environment

        Returns:
            PortConfiguration with environment-specific settings
        """
        if self._config is None:
            self._config = self._load_configuration()

        return self._config

    def _load_configuration(self) -> PortConfiguration:
        """Load configuration based on environment"""

        if self.environment == "production":
            return PortConfiguration(
                backend_port=int(os.getenv("BACKEND_PORT", "8001")),
                web_port=int(os.getenv("WEB_PORT", "8080")),
                backend_host=os.getenv("BACKEND_HOST", "0.0.0.0"),
                web_host=os.getenv("WEB_HOST", "0.0.0.0"),
            )

        elif self.environment == "staging":
            return PortConfiguration(
                backend_port=int(os.getenv("BACKEND_PORT", "8001")),
                web_port=int(os.getenv("WEB_PORT", "8081")),
                backend_host=os.getenv("BACKEND_HOST", "127.0.0.1"),
                web_host=os.getenv("WEB_HOST", "127.0.0.1"),
            )

        else:  # development
            return PortConfiguration(
                backend_port=int(os.getenv("BACKEND_PORT", "8001")),
                web_port=int(os.getenv("WEB_PORT", "8081")),
                backend_host=os.getenv("BACKEND_HOST", "127.0.0.1"),
                web_host=os.getenv("WEB_HOST", "127.0.0.1"),
            )

    def get_port_for_service(self, service_name: str) -> int:
        """
        Get port for specific service

        Args:
            service_name: "backend" or "web"

        Returns:
            Port number for the service
        """
        config = self.get_configuration()

        if service_name == "backend":
            return config.backend_port
        elif service_name == "web":
            return config.web_port
        else:
            raise ValueError(f"Unknown service: {service_name}. Must be 'backend' or 'web'")

    def get_service_urls(self) -> Dict[str, str]:
        """
        Get all service URLs for service discovery

        Returns:
            Dictionary mapping service names to URLs
        """
        config = self.get_configuration()

        return {
            "backend": config.get_backend_url(),
            "web": config.get_web_url(),
            "api_base": config.get_api_base_url(),
        }


# Global service instance for easy access
_port_config_service = None


def get_port_configuration_service() -> PortConfigurationService:
    """
    Get global port configuration service instance

    Returns:
        Singleton PortConfigurationService instance
    """
    global _port_config_service

    if _port_config_service is None:
        _port_config_service = PortConfigurationService()

    return _port_config_service


def get_port_configuration() -> PortConfiguration:
    """
    Convenience function to get port configuration

    Returns:
        PortConfiguration for current environment
    """
    return get_port_configuration_service().get_configuration()
