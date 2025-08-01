"""
Query Router - Routes QUERY intents to appropriate query services
"""

import logging
from typing import Any, Dict, List, Optional

from services.domain.models import Intent
from services.queries.conversation_queries import ConversationQueryService
from services.queries.degradation import QueryDegradationHandler
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.shared_types import IntentCategory

logger = logging.getLogger(__name__)


class QueryRouter:
    """Routes QUERY intents to appropriate query services"""

    def __init__(
        self,
        project_query_service: ProjectQueryService,
        conversation_query_service: ConversationQueryService,
        file_query_service: FileQueryService,
        test_mode: bool = False,
        degradation_config: Optional[Dict] = None,
    ):
        self.project_queries = project_query_service
        self.conversation_queries = conversation_query_service
        self.file_queries = file_query_service
        self.test_mode = test_mode  # PM-063: Backward compatibility with existing test_mode
        self.degradation_handler = QueryDegradationHandler(
            degradation_config
        )  # PM-063: Comprehensive degradation framework

    async def route_query(self, intent: Intent) -> Any:
        """Route a QUERY intent to the appropriate query service with graceful degradation"""
        if intent.category != IntentCategory.QUERY:
            raise ValueError(f"QueryRouter can only handle QUERY intents, got {intent.category}")

        # PM-063: Comprehensive degradation handling
        try:
            return await self._route_query_with_protection(intent)
        except (ValueError, ImportError) as e:
            # Re-raise ValueError and ImportError - these should not be degraded
            raise
        except Exception as e:
            logger.error(f"Query routing failed for action {intent.action}: {e}")
            # Determine service and apply appropriate degradation
            service = self._get_service_for_action(intent.action)
            return await self.degradation_handler.handle_service_failure(service, intent.action, e)

    async def _route_query_with_protection(self, intent: Intent) -> Any:
        """Internal routing with circuit breaker protection"""

        if intent.action == "list_projects":
            if self.test_mode:
                # PM-063: Backward compatibility with test_mode
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.project_queries.list_active_projects, "project_queries", intent.action
            )
        elif intent.action == "get_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project query requires project_id in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.get_project_by_id(project_id),
                "project_queries",
                intent.action,
            )
        elif intent.action == "get_default_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.project_queries.get_default_project, "project_queries", intent.action
            )
        elif intent.action == "find_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            name = intent.context.get("name")
            if not name:
                raise ValueError("find_project query requires name in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.find_project_by_name(name),
                "project_queries",
                intent.action,
            )
        elif intent.action == "count_projects":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.project_queries.count_active_projects, "project_queries", intent.action
            )
        elif intent.action == "get_project_details":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project_details query requires project_id in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.get_project_details(project_id),
                "project_queries",
                intent.action,
            )
        elif intent.action == "get_greeting":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_greeting, "conversation_queries", intent.action
            )
        elif intent.action == "get_help":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_help, "conversation_queries", intent.action
            )
        elif intent.action == "get_status":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_status, "conversation_queries", intent.action
            )
        elif intent.action == "get_initial_contact":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_initial_contact, "conversation_queries", intent.action
            )
        elif intent.action == "read_file_contents":
            file_id = intent.context.get("resolved_file_id")
            if not file_id:
                raise ValueError("read_file_contents query requires resolved_file_id in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - file_id from context: {file_id}")
            print(f"DEBUG: QueryRouter - full context: {intent.context}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.read_file_contents(file_id), "file_queries", intent.action
            )
        elif intent.action == "summarize_file":
            file_id = intent.context.get("resolved_file_id")
            if not file_id:
                raise ValueError("summarize_file query requires resolved_file_id in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - summarize file_id: {file_id}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.summarize_file(file_id), "file_queries", intent.action
            )
        elif intent.action == "search_files":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_files query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching files for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.search_files_by_query(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "find_documents":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("find_documents query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - finding documents about: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.find_documents_about_topic(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "search_content":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_content query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching content for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.search_content_by_query(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "search_documents":
            # Handle LLM-generated search_documents action (maps to find_documents)
            search_query = intent.context.get("search_query") or intent.context.get(
                "original_message", ""
            )
            session_id = intent.context.get("session_id")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching documents for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.find_documents_about_topic(search_query, session_id),
                "file_queries",
                intent.action,
            )
        else:
            raise ValueError(f"Unknown query action: {intent.action}")

    async def _execute_with_circuit_breaker(self, func, service: str, action: str) -> Any:
        """Execute function with circuit breaker protection and degradation handling"""
        try:
            if self.degradation_handler.enabled and await self.degradation_handler.should_degrade(
                service
            ):
                logger.info(f"Applying degradation for {service}.{action}")
                return await self.degradation_handler.handle_service_failure(
                    service, action, Exception("Circuit breaker open")
                )

            # Execute with circuit breaker protection
            return await self.degradation_handler.circuit_breaker.call(func)

        except (ValueError, ImportError) as e:
            # Re-raise these exceptions - they should not be degraded
            raise
        except Exception as e:
            logger.error(f"Circuit breaker execution failed for {service}.{action}: {e}")
            return await self.degradation_handler.handle_service_failure(service, action, e)

    def _get_service_for_action(self, action: str) -> str:
        """Map query action to service name for degradation handling"""
        project_actions = {
            "list_projects",
            "get_project",
            "get_default_project",
            "find_project",
            "count_projects",
            "get_project_details",
        }
        file_actions = {
            "read_file_contents",
            "summarize_file",
            "search_files",
            "find_documents",
            "search_content",
            "search_documents",
        }
        conversation_actions = {"get_greeting", "get_help", "get_status", "get_initial_contact"}

        if action in project_actions:
            return "project_queries"
        elif action in file_actions:
            return "file_queries"
        elif action in conversation_actions:
            return "conversation_queries"
        else:
            return "unknown_service"

    def get_supported_queries(self) -> List[str]:
        """Get list of supported query actions"""
        return [
            "list_projects",
            "get_project",
            "get_project_details",
            "get_default_project",
            "find_project",
            "count_projects",
            "get_greeting",
            "get_help",
            "get_status",
            "get_initial_contact",
            "read_file_contents",
            "summarize_file",
            "search_files",
            "find_documents",
            "search_content",
            "search_documents",  # LLM-generated action
        ]

    def get_degradation_status(self) -> Dict[str, Any]:
        """Get current degradation handler status for monitoring and debugging"""
        return {
            "test_mode": self.test_mode,
            "degradation_handler": self.degradation_handler.get_circuit_breaker_status(),
            "supported_queries": len(self.get_supported_queries()),
            "services": {
                "project_queries": "available",
                "file_queries": "available",
                "conversation_queries": "available",
            },
        }
