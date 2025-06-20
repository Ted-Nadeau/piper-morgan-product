"""
Database Repositories
Handles CRUD operations for domain entities
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime
import structlog

from .models import Product, Feature, WorkItem, Intent, Workflow, Task, ProjectDB, ProjectIntegrationDB
import services.domain.models as domain
from .connection import db
from services.shared_types import IntegrationType

logger = structlog.get_logger()

class BaseRepository:
    """Base repository with common CRUD operations"""
    model = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, **kwargs) -> Any:
        """Create a new entity"""
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        
        entity = self.model(**kwargs)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get entity by ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    # Keep legacy get method for backwards compatibility
    async def get(self, id: str) -> Optional[Any]:
        """Get entity by ID (legacy method)"""
        return await self.get_by_id(id)
    
    async def list(self, limit: int = 100) -> List[Any]:
        """List all entities"""
        result = await self.session.execute(
            select(self.model).limit(limit)
        )
        return result.scalars().all()
    
    async def update(self, id: str, **kwargs) -> Optional[Any]:
        """Update an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return None
        
        for key, value in kwargs.items():
            setattr(entity, key, value)
        
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def delete(self, id: str) -> bool:
        """Delete an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return False
        
        await self.session.delete(entity)
        await self.session.commit()
        return True

class ProductRepository(BaseRepository):
    model = Product

class FeatureRepository(BaseRepository):
    model = Feature

class WorkItemRepository(BaseRepository):
    model = WorkItem
    
    async def create_from_workflow(self, workflow_data: Dict[str, Any]) -> WorkItem:
        """Create work item from workflow context"""
        return await self.create(
            title=workflow_data.get("title", "Untitled"),
            description=workflow_data.get("requirements", ""),
            status="open",
            external_refs={}
        )

class WorkflowRepository(BaseRepository):
    model = Workflow
    
    async def create_from_domain(self, domain_workflow) -> Workflow:
        """Create DB workflow from domain workflow"""
        return await self.create(
            id=domain_workflow.id,
            type=domain_workflow.type,
            status=domain_workflow.status,
            input_data=domain_workflow.input_data,
            output_data=domain_workflow.output_data,
            context=domain_workflow.context,
            created_at=domain_workflow.created_at
        )
    
    async def update_status(self, workflow_id: str, status, output_data=None, error=None):
        """Update workflow status"""
        updates = {"status": status}
        if output_data:
            updates["output_data"] = output_data
        if error:
            updates["error"] = error
        if status.value == "completed":
            updates["completed_at"] = datetime.utcnow()
        elif status.value == "running":
            updates["started_at"] = datetime.utcnow()
        
        return await self.update(workflow_id, **updates)

class TaskRepository(BaseRepository):
    model = Task
    
    async def create_from_domain(self, workflow_id: str, domain_task) -> Task:
        """Create DB task from domain task"""
        return await self.create(
            id=domain_task.id,
            workflow_id=workflow_id,
            type=domain_task.type,
            status=domain_task.status,
            input_data=domain_task.input_data
        )

# PM-009: Project Repository for multi-project support
class ProjectRepository(BaseRepository):
    """Repository for Project operations"""
    model = ProjectDB
    
    async def get_default_project(self) -> Optional[domain.Project]:
        result = await self.session.execute(
            select(ProjectDB).where(ProjectDB.is_default == True, ProjectDB.is_archived == False)
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None
    
    async def list_active_projects(self) -> List[domain.Project]:
        result = await self.session.execute(
            select(ProjectDB).where(ProjectDB.is_archived == False).order_by(ProjectDB.name)
        )
        return [db_project.to_domain() for db_project in result.scalars().all()]
    
    async def count_active_projects(self) -> int:
        result = await self.session.execute(
            select(func.count(ProjectDB.id)).where(ProjectDB.is_archived == False)
        )
        return result.scalar() or 0
    
    async def find_by_name(self, name: str) -> Optional[domain.Project]:
        result = await self.session.execute(
            select(ProjectDB).where(
                func.lower(ProjectDB.name) == name.lower(),
                ProjectDB.is_archived == False
            )
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None
    
    async def create_default_project(self) -> domain.Project:
        logger.info("Creating default project")
        project = domain.Project(
            id=str(uuid.uuid4()),
            name="Piper Morgan Test",
            description="Default project for Piper Morgan development and testing",
            is_default=True,
            is_archived=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_project = ProjectDB.from_domain(project)
        self.session.add(db_project)
        await self.session.commit()
        await self.session.refresh(db_project)
        return db_project.to_domain()
    
    async def get_project_with_integrations(self, project_id: str) -> Optional[domain.Project]:
        result = await self.session.execute(
            select(ProjectDB)
            .where(ProjectDB.id == project_id, ProjectDB.is_archived == False)
            .options(selectinload(ProjectDB.integrations))
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

class ProjectIntegrationRepository(BaseRepository):
    """Repository for ProjectIntegration operations"""
    model = ProjectIntegrationDB
    
    async def get_by_project_and_type(self, project_id: str, integration_type: IntegrationType) -> Optional[domain.ProjectIntegration]:
        result = await self.session.execute(
            select(ProjectIntegrationDB).where(
                ProjectIntegrationDB.project_id == project_id,
                ProjectIntegrationDB.type == integration_type,
                ProjectIntegrationDB.is_active == True
            )
        )
        db_integration = result.scalar_one_or_none()
        return db_integration.to_domain() if db_integration else None
    
    async def list_by_project(self, project_id: str, active_only: bool = True) -> List[domain.ProjectIntegration]:
        query = select(ProjectIntegrationDB).where(ProjectIntegrationDB.project_id == project_id)
        if active_only:
            query = query.where(ProjectIntegrationDB.is_active == True)
        result = await self.session.execute(query.order_by(ProjectIntegrationDB.type))
        return [db_integration.to_domain() for db_integration in result.scalars().all()]

# Repository factory
class RepositoryFactory:
    """Creates repositories with session
    NOTE: The caller is responsible for closing the returned session (repos["session"]) after use, ideally in a finally block.
    """
    @staticmethod
    async def get_repositories():
        """Get all repositories with a new session
        Caller must close repos["session"] after use to avoid connection leaks.
        """
        session = await db.get_session()
        return {
            "products": ProductRepository(session),
            "features": FeatureRepository(session),
            "work_items": WorkItemRepository(session),
            "workflows": WorkflowRepository(session),
            "tasks": TaskRepository(session),
            "projects": ProjectRepository(session),  # PM-009: Add project repository
            "project_integrations": ProjectIntegrationRepository(session),  # PM-009: Add integration repository
            "session": session
        }