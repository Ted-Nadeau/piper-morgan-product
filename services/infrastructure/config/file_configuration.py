"""
File configuration service implementing ADR-010 patterns.

Provides configuration access for file repository components following
the established patterns for Application/Domain layer services.
"""

import os
from typing import Any, Dict, Optional


class FileConfigService:
    """
    Centralized file configuration service implementing ADR-010 patterns.

    Provides configuration access for file repository components following
    the established patterns for Application/Domain layer services.
    """

    def __init__(self):
        self._config_cache: Dict[str, Any] = {}

    def get_int(self, key: str, default: int) -> int:
        """Get integer configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        try:
            value = int(os.getenv(key, str(default)))
            self._config_cache[key] = value
            return value
        except (ValueError, TypeError):
            return default

    def get_float(self, key: str, default: float) -> float:
        """Get float configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        try:
            value = float(os.getenv(key, str(default)))
            self._config_cache[key] = value
            return value
        except (ValueError, TypeError):
            return default

    def get_boolean(self, key: str, default: bool) -> bool:
        """Get boolean configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        value = os.getenv(key, str(default)).lower()
        result = value in ("true", "1", "yes", "on")
        self._config_cache[key] = result
        return result

    def get_file_cache_ttl(self) -> int:
        """Get file cache TTL in seconds"""
        if "file_cache_ttl" in self._config_cache:
            return self._config_cache["file_cache_ttl"]

        ttl = self.get_int("FILE_CACHE_TTL", 300)  # 5 minutes default
        self._config_cache["file_cache_ttl"] = ttl
        return ttl

    def get_max_file_results(self) -> int:
        """Get maximum number of file results to return"""
        if "max_file_results" in self._config_cache:
            return self._config_cache["max_file_results"]

        max_results = self.get_int("MAX_FILE_RESULTS", 1000)
        self._config_cache["max_file_results"] = max_results
        return max_results

    def get_file_search_timeout(self) -> float:
        """Get file search timeout in seconds"""
        if "file_search_timeout" in self._config_cache:
            return self._config_cache["file_search_timeout"]

        timeout = self.get_float("FILE_SEARCH_TIMEOUT", 30.0)  # 30 seconds default
        self._config_cache["file_search_timeout"] = timeout
        return timeout

    def get_mcp_search_enabled(self) -> bool:
        """Check if MCP content search is enabled"""
        if "mcp_search_enabled" in self._config_cache:
            return self._config_cache["mcp_search_enabled"]

        enabled = self.get_boolean("ENABLE_MCP_FILE_SEARCH", False)
        self._config_cache["mcp_search_enabled"] = enabled
        return enabled

    def get_file_metadata_cache_size(self) -> int:
        """Get file metadata cache size"""
        if "file_metadata_cache_size" in self._config_cache:
            return self._config_cache["file_metadata_cache_size"]

        cache_size = self.get_int("FILE_METADATA_CACHE_SIZE", 1000)
        self._config_cache["file_metadata_cache_size"] = cache_size
        return cache_size

    def get_repository_config(self) -> Dict[str, Any]:
        """Get comprehensive repository configuration"""
        return {
            "cache_ttl": self.get_file_cache_ttl(),
            "max_results": self.get_max_file_results(),
            "search_timeout": self.get_file_search_timeout(),
            "mcp_search_enabled": self.get_mcp_search_enabled(),
            "metadata_cache_size": self.get_file_metadata_cache_size(),
        }

    def clear_cache(self):
        """Clear configuration cache"""
        self._config_cache.clear()


def get_file_config_service() -> FileConfigService:
    """Get file configuration service instance"""
    return FileConfigService()
