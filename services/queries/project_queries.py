"""
Project Query Service - CQRS-lite pattern for read-only project operations
"""

from typing import List, Optional

from services.database.repositories import ProjectRepository
from services.domain.models import Project


class ProjectQueryService:
    """Query service for read-only project operations"""

    def __init__(self, project_repository: ProjectRepository):
        self.repo = project_repository

    async def list_active_projects(self) -> List[Project]:
        """List all active projects"""
        return await self.repo.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID"""
        return await self.repo.get_by_id(project_id)

    async def get_default_project(self) -> Optional[Project]:
        """Get the default project"""
        return await self.repo.get_default_project()

    async def find_project_by_name(self, name: str) -> Optional[Project]:
        """Find a project by name"""
        return await self.repo.find_by_name(name)

    async def count_active_projects(self) -> int:
        """Count active projects"""
        return await self.repo.count_active_projects()
