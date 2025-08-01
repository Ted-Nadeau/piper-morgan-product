"""
Query Degradation Handler - Graceful failure handling for QueryRouter operations

Leverages proven MCP circuit breaker architecture to provide systematic
degradation strategies for all query operations.
"""

import logging
import time
from typing import Any, Dict, Optional

from services.infrastructure.config.feature_flags import FeatureFlags

logger = logging.getLogger(__name__)


class QueryCircuitBreakerOpenError(Exception):
    """Raised when query circuit breaker is open"""

    pass


class QueryCircuitBreaker:
    """Circuit breaker for query operations - based on proven MCP pattern"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                logger.info("Query circuit breaker entering half-open state")
            else:
                raise QueryCircuitBreakerOpenError("Query circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
                logger.info("Query circuit breaker closed after successful call")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                logger.error(f"Query circuit breaker opened after {self.failure_count} failures")
            raise


class QueryDegradationHandler:
    """
    Graceful degradation handler for QueryRouter operations

    Provides intelligent fallback strategies for different types of query failures,
    leveraging proven MCP circuit breaker patterns for resilience.
    """

    def __init__(self, circuit_breaker_config: Optional[Dict] = None):
        config = circuit_breaker_config or {}
        self.circuit_breaker = QueryCircuitBreaker(
            failure_threshold=config.get("failure_threshold", 5),
            recovery_timeout=config.get("recovery_timeout", 60),
        )
        self.enabled = FeatureFlags.is_circuit_breaker_enabled()

    async def handle_database_failure(self, action: str) -> str:
        """Handle database connection failures with user-friendly messages"""
        database_fallbacks = {
            "list_projects": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "get_project": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "get_default_project": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "find_project": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "count_projects": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "get_project_details": "Database temporarily unavailable. Please ensure Docker is running or try again later.",
        }

        return database_fallbacks.get(
            action,
            "Database temporarily unavailable. Please ensure Docker is running or try again later.",
        )

    async def handle_service_failure(self, service: str, action: str, error: Exception) -> Any:
        """Handle service-specific failures with appropriate fallbacks"""

        if service == "file_queries":
            return await self._handle_file_service_failure(action, error)
        elif service == "project_queries":
            return await self._handle_project_service_failure(action, error)
        elif service == "conversation_queries":
            return await self._handle_conversation_service_failure(action, error)
        else:
            return f"Service '{service}' temporarily unavailable. Please try again later."

    async def _handle_file_service_failure(self, action: str, error: Exception) -> Dict[str, Any]:
        """Handle file service failures with structured fallback responses"""
        file_fallbacks = {
            "read_file_contents": {
                "success": False,
                "error": "Unable to read file contents. File service temporarily unavailable.",
                "suggestion": "Please check that the file exists and try again in a few moments.",
                "fallback_available": False,
            },
            "summarize_file": {
                "success": False,
                "error": "Unable to generate file summary. File analysis service temporarily unavailable.",
                "suggestion": "You can try reading the file contents directly or wait for service restoration.",
                "fallback_available": True,
                "fallback_action": "read_file_contents",
            },
            "search_files": {
                "success": False,
                "error": "Unable to search files. Search service temporarily unavailable.",
                "suggestion": "File search is temporarily unavailable. Please try again shortly.",
                "results": [],
                "query": "search temporarily unavailable",
            },
            "find_documents": {
                "success": False,
                "error": "Unable to find documents. Document discovery service temporarily unavailable.",
                "suggestion": "Document search is temporarily unavailable. Please try again shortly.",
                "results": [],
                "query": "document search temporarily unavailable",
            },
            "search_content": {
                "success": False,
                "error": "Unable to search content. Content search service temporarily unavailable.",
                "suggestion": "Content search is temporarily unavailable. Please try again shortly.",
                "results": [],
                "query": "content search temporarily unavailable",
            },
            "search_documents": {
                "success": False,
                "error": "Unable to search documents. Document search service temporarily unavailable.",
                "suggestion": "Document search is temporarily unavailable. Please try again shortly.",
                "results": [],
                "query": "document search temporarily unavailable",
            },
        }

        return file_fallbacks.get(
            action,
            {
                "success": False,
                "error": f"File service temporarily unavailable for {action}.",
                "suggestion": "Please try again in a few moments.",
            },
        )

    async def _handle_project_service_failure(self, action: str, error: Exception) -> str:
        """Handle project service failures"""
        # Database failures should use database fallback messages
        return await self.handle_database_failure(action)

    async def _handle_conversation_service_failure(self, action: str, error: Exception) -> str:
        """Handle conversation service failures with static fallbacks"""
        conversation_fallbacks = {
            "get_greeting": "Hello! I'm Piper Morgan, your AI-powered Product Management Assistant. How can I help you today?",
            "get_help": "I can help you with project management tasks like creating GitHub issues, searching documents, and analyzing project data. What would you like to do?",
            "get_status": "Piper Morgan is operational with some services temporarily limited. Most features are available.",
            "get_initial_contact": "Welcome to Piper Morgan! I'm here to help streamline your product management workflow.",
        }

        return conversation_fallbacks.get(
            action,
            "Conversation service temporarily limited. Core functionality remains available.",
        )

    async def should_degrade(self, service: str) -> bool:
        """Check if degradation should be applied for a service"""
        if not self.enabled:
            return False

        # Always degrade when circuit breaker is open
        if self.circuit_breaker.state == "open":
            return True

        return False

    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status for monitoring"""
        return {
            "state": self.circuit_breaker.state,
            "failure_count": self.circuit_breaker.failure_count,
            "last_failure_time": self.circuit_breaker.last_failure_time,
            "enabled": self.enabled,
        }
