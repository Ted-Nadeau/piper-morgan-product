from typing import Optional, Tuple, Dict
from services.domain.models import Project, Intent
from services.database.repositories import ProjectRepository
from services.llm.clients import LLMClient
from services.shared_types import IntentCategory

class AmbiguousProjectError(Exception):
    """Raised when project cannot be determined"""
    pass

class ProjectContext:
    """Business logic for resolving project context from user intents"""
    def __init__(self, project_repo: ProjectRepository, llm_client: LLMClient):
        self.project_repo = project_repo  # Dependency injection
        self.llm_client = llm_client
        self._session_last_used: Dict[str, str] = {}  # session_id -> project_id

    async def resolve_project(
        self,
        intent: Intent,
        session_id: str,
        confirmed_this_session: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolve project following hierarchy:
        1. Explicit project_id in intent
        2. Last used project in session
        3. Infer from message context
        4. Default project
        Returns: (Project, needs_confirmation)
        """
        # 1. Explicit project_id in intent context
        project_id = intent.context.get("project_id")
        if project_id:
            project = await self.project_repo.get_by_id(project_id)
            if project:
                self._session_last_used[session_id] = project.id
                return project, False  # No confirmation needed

        # 2. Last used project in session
        last_project_id = self._session_last_used.get(session_id)
        if last_project_id:
            project = await self.project_repo.get_by_id(last_project_id)
            if project:
                return project, not confirmed_this_session  # Needs confirmation if not confirmed

        # 3. Infer from message context using LLM
        inferred_project_name = await self.llm_client.complete(f"Which project does this relate to: {intent.context.get('original_message', '')}")
        if inferred_project_name:
            # Try to find a project by name
            projects = await self.project_repo.list_active_projects()
            for project in projects:
                if project.name.lower() == inferred_project_name.strip().lower():
                    self._session_last_used[session_id] = project.id
                    return project, True  # Needs confirmation

        # 4. Default project
        default_project = await self.project_repo.get_default_project()
        if default_project:
            self._session_last_used[session_id] = default_project.id
            return default_project, True  # Needs confirmation

        # If all else fails, raise error
        raise AmbiguousProjectError("Could not resolve project for intent.")
