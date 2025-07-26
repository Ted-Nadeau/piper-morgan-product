"""
Query Router - Routes QUERY intents to appropriate query services
"""

from typing import Any, Dict, List

from services.domain.models import Intent
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.shared_types import IntentCategory


class QueryRouter:
    """Routes QUERY intents to appropriate query services"""

    def __init__(
        self,
        project_query_service: ProjectQueryService,
        conversation_query_service: ConversationQueryService,
        file_query_service: FileQueryService,
        test_mode: bool = False,
    ):
        self.project_queries = project_query_service
        self.conversation_queries = conversation_query_service
        self.file_queries = file_query_service
        self.test_mode = test_mode  # PM-063: Enable graceful degradation when database unavailable

    async def route_query(self, intent: Intent) -> Any:
        """Route a QUERY intent to the appropriate query service"""
        if intent.category != IntentCategory.QUERY:
            raise ValueError(f"QueryRouter can only handle QUERY intents, got {intent.category}")

        if intent.action == "list_projects":
            if self.test_mode:
                # PM-063: Graceful degradation when database unavailable
                return "Database temporarily unavailable. Please ensure Docker is running or try again later."
            return await self.project_queries.list_active_projects()
        elif intent.action == "get_project":
            if self.test_mode:
                return "Database temporarily unavailable. Please ensure Docker is running or try again later."
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project query requires project_id in context")
            return await self.project_queries.get_project_by_id(project_id)
        elif intent.action == "get_default_project":
            if self.test_mode:
                return "Database temporarily unavailable. Please ensure Docker is running or try again later."
            return await self.project_queries.get_default_project()
        elif intent.action == "find_project":
            name = intent.context.get("name")
            if not name:
                raise ValueError("find_project query requires name in context")
            return await self.project_queries.find_project_by_name(name)
        elif intent.action == "count_projects":
            if self.test_mode:
                return "Database temporarily unavailable. Please ensure Docker is running or try again later."
            return await self.project_queries.count_active_projects()
        elif intent.action == "get_project_details":
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project_details query requires project_id in context")
            return await self.project_queries.get_project_details(project_id)
        elif intent.action == "get_greeting":
            return await self.conversation_queries.get_greeting()
        elif intent.action == "get_help":
            return await self.conversation_queries.get_help()
        elif intent.action == "get_status":
            return await self.conversation_queries.get_status()
        elif intent.action == "get_initial_contact":
            return await self.conversation_queries.get_initial_contact()
        elif intent.action == "read_file_contents":
            file_id = intent.context.get("resolved_file_id")
            print(f"DEBUG: QueryRouter - file_id from context: {file_id}")
            print(f"DEBUG: QueryRouter - full context: {intent.context}")
            return await self.file_queries.read_file_contents(file_id)
        elif intent.action == "summarize_file":
            file_id = intent.context.get("resolved_file_id")
            print(f"DEBUG: QueryRouter - summarize file_id: {file_id}")
            return await self.file_queries.summarize_file(file_id)
        elif intent.action == "search_files":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_files query requires search_query in context")
            print(f"DEBUG: QueryRouter - searching files for: {search_query}")
            return await self.file_queries.search_files_by_query(search_query, session_id)
        elif intent.action == "find_documents":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("find_documents query requires search_query in context")
            print(f"DEBUG: QueryRouter - finding documents about: {search_query}")
            return await self.file_queries.find_documents_about_topic(search_query, session_id)
        elif intent.action == "search_content":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_content query requires search_query in context")
            print(f"DEBUG: QueryRouter - searching content for: {search_query}")
            return await self.file_queries.search_content_by_query(search_query, session_id)
        elif intent.action == "search_documents":
            # Handle LLM-generated search_documents action (maps to find_documents)
            search_query = intent.context.get("search_query") or intent.context.get(
                "original_message", ""
            )
            session_id = intent.context.get("session_id")
            print(f"DEBUG: QueryRouter - searching documents for: {search_query}")
            return await self.file_queries.find_documents_about_topic(search_query, session_id)
        else:
            raise ValueError(f"Unknown query action: {intent.action}")

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
