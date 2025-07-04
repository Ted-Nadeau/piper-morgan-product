"""
Query Router - Routes QUERY intents to appropriate query services
"""
from typing import Any, Dict, List
from services.domain.models import Intent
from services.shared_types import IntentCategory
from services.queries.project_queries import ProjectQueryService
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService


class QueryRouter:
    """Routes QUERY intents to appropriate query services"""
    
    def __init__(self, project_query_service: ProjectQueryService, conversation_query_service: ConversationQueryService, file_query_service: FileQueryService):
        self.project_queries = project_query_service
        self.conversation_queries = conversation_query_service
        self.file_queries = file_query_service
    
    async def route_query(self, intent: Intent) -> Any:
        """Route a QUERY intent to the appropriate query service"""
        if intent.category != IntentCategory.QUERY:
            raise ValueError(f"QueryRouter can only handle QUERY intents, got {intent.category}")
        
        if intent.action == "list_projects":
            return await self.project_queries.list_active_projects()
        elif intent.action == "get_project":
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project query requires project_id in context")
            return await self.project_queries.get_project_by_id(project_id)
        elif intent.action == "get_default_project":
            return await self.project_queries.get_default_project()
        elif intent.action == "find_project":
            name = intent.context.get("name")
            if not name:
                raise ValueError("find_project query requires name in context")
            return await self.project_queries.find_project_by_name(name)
        elif intent.action == "count_projects":
            return await self.project_queries.count_active_projects()
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
        else:
            raise ValueError(f"Unknown query action: {intent.action}")
    
    def get_supported_queries(self) -> List[str]:
        """Get list of supported query actions"""
        return [
            "list_projects",
            "get_project", 
            "get_default_project",
            "find_project",
            "count_projects",
            "get_greeting",
            "get_help",
            "get_status",
            "get_initial_contact"
        ] 