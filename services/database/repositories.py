"""
Database Repositories
Handles CRUD operations for domain entities
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.shared_types import EdgeType, IntegrationType, NodeType

from .connection import db
from .models import (
    Feature,
    Intent,
    KnowledgeEdgeDB,
    KnowledgeNodeDB,
    Product,
    ProjectDB,
    ProjectIntegrationDB,
    Task,
    Workflow,
    WorkItem,
)
from .session_factory import AsyncSessionFactory

logger = structlog.get_logger()


class BaseRepository:
    """Base repository with common CRUD operations"""

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        """Create a new entity"""
        if "id" not in kwargs:
            kwargs["id"] = str(uuid.uuid4())

        entity = self.model(**kwargs)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get entity by ID"""
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    # Keep legacy get method for backwards compatibility
    async def get(self, id: str) -> Optional[Any]:
        """Get entity by ID (legacy method)"""
        return await self.get_by_id(id)

    async def list(self, limit: int = 100) -> List[Any]:
        """List all entities"""
        result = await self.session.execute(select(self.model).limit(limit))
        return result.scalars().all()

    async def update(self, id: str, **kwargs) -> Optional[Any]:
        """Update an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return None

        for key, value in kwargs.items():
            setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: str) -> bool:
        """Delete an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return False

        self.session.delete(entity)
        await self.session.flush()
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
            external_refs={},
        )


class WorkflowRepository(BaseRepository):
    model = Workflow

    async def create_from_domain(self, domain_workflow) -> Workflow:
        """Create DB workflow from domain workflow"""
        workflow = Workflow(
            id=domain_workflow.id,
            type=domain_workflow.type,
            status=domain_workflow.status,
            input_data={},  # Domain model has context instead
            output_data=(domain_workflow.result.__dict__ if domain_workflow.result else None),
            context=domain_workflow.context,
            created_at=domain_workflow.created_at,
        )
        self.session.add(workflow)
        await self.session.flush()
        await self.session.refresh(workflow)
        return workflow

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

    async def find_by_id(self, workflow_id: str) -> Optional[domain.Workflow]:
        """Find workflow by ID and return domain model (for API compatibility)"""
        # Use selectinload to eagerly load the intent relationship
        result = await self.session.execute(
            select(Workflow)
            .options(selectinload(Workflow.intent))
            .where(Workflow.id == workflow_id)
        )
        db_workflow = result.scalar_one_or_none()
        return db_workflow.to_domain() if db_workflow else None


class TaskRepository(BaseRepository):
    model = Task

    async def create_from_domain(self, workflow_id: str, domain_task) -> Task:
        """Create DB task from domain task"""
        return await self.create(
            id=domain_task.id,
            workflow_id=workflow_id,
            type=domain_task.type,
            status=domain_task.status,
            input_data={},  # Domain task has no input_data
        )


# PM-009: Project Repository for multi-project support
class ProjectRepository(BaseRepository):
    """Repository for Project operations"""

    model = ProjectDB

    async def get_by_id(
        self,
        project_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Get project by ID with integrations - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.id == project_id]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB).options(selectinload(ProjectDB.integrations)).where(and_(*filters))
        )
        db_project = result.scalar_one_or_none()
        if db_project:
            return db_project.to_domain()
        return None

    async def get_default_project(self) -> Optional[domain.Project]:
        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(ProjectDB.is_default == True, ProjectDB.is_archived == False)
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def list_active_projects(
        self,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> List[domain.Project]:
        """List active projects - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(and_(*filters))
            .order_by(ProjectDB.name)
        )
        return [db_project.to_domain() for db_project in result.scalars().all()]

    async def count_active_projects(
        self,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> int:
        """Count active projects - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(select(func.count(ProjectDB.id)).where(and_(*filters)))
        return result.scalar() or 0

    async def find_by_name(
        self,
        name: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Find project by name - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [
            func.lower(ProjectDB.name) == name.lower(),
            ProjectDB.is_archived == False,
        ]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(and_(*filters))
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def search_projects(
        self,
        query: str,
        owner_id: Optional[str] = None,
        include_archived: bool = False,
        limit: int = 20,
    ) -> List[domain.Project]:
        """
        Search projects by name (partial match, case-insensitive).

        Part of #567 MUX-INTERACT-CONV-SEARCH.

        Args:
            query: Search query (matches against project name)
            owner_id: Filter to this user's projects
            include_archived: Whether to include archived projects
            limit: Maximum results to return

        Returns:
            List of matching projects, ordered by name
        """
        filters = [
            ProjectDB.name.ilike(f"%{query}%"),
        ]

        if not include_archived:
            filters.append(ProjectDB.is_archived == False)

        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))
            .where(and_(*filters))
            .order_by(ProjectDB.name)
            .limit(limit)
        )
        db_projects = result.scalars().all()
        return [db_project.to_domain() for db_project in db_projects]

    async def create_default_project(self) -> domain.Project:
        logger.info("Creating default project")
        project = domain.Project(
            id=str(uuid.uuid4()),
            name="Piper Morgan Test",
            description="Default project for Piper Morgan development and testing",
            is_default=True,
            is_archived=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db_project = ProjectDB.from_domain(project)
        self.session.add(db_project)
        await self.session.commit()
        await self.session.refresh(db_project)
        return db_project.to_domain()

    async def get_project_with_integrations(
        self,
        project_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Get project with integrations - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.id == project_id, ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB).where(and_(*filters)).options(selectinload(ProjectDB.integrations))
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def share_project(
        self,
        project_id: str,
        owner_id: str,
        user_to_share_with: str,
        role: domain.ShareRole = None,
    ) -> Optional[domain.Project]:
        """Share a project with another user at specified role (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project to share
            owner_id: User making the share request (must be owner)
            user_to_share_with: User to share with
            role: ShareRole (viewer, editor, admin) - defaults to viewer if None

        Returns:
            Updated Project with new shared_with entry, or None if not found/not owner
        """
        # Default role if not specified
        if role is None:
            role = domain.ShareRole.VIEWER

        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return None  # Not found or not owner

        # Prevent owner from sharing with themselves (no-op)
        if user_to_share_with == owner_id:
            return db_project.to_domain()

        # Convert to domain object to work with SharePermission objects
        domain_project = db_project.to_domain()

        # Check if user already shared with - update role if exists, otherwise add new share
        permission = domain.SharePermission(user_id=user_to_share_with, role=role)
        existing_index = None

        for idx, perm in enumerate(domain_project.shared_with):
            if perm.user_id == user_to_share_with:
                existing_index = idx
                break

        if existing_index is not None:
            # Update existing permission
            domain_project.shared_with[existing_index] = permission
        else:
            # Add new permission
            domain_project.shared_with.append(permission)

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated project
        await self.session.refresh(db_project)
        return db_project.to_domain()

    async def unshare_project(self, project_id: str, owner_id: str, user_to_unshare: str) -> bool:
        """Remove user from project sharing (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            owner_id: User making the unshare request (must be owner)
            user_to_unshare: User to remove from sharing

        Returns:
            True if user was unshared, False if not found/not owner
        """
        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return False  # Not found or not owner

        # Convert to domain object
        domain_project = db_project.to_domain()

        # Remove user from shared_with
        initial_length = len(domain_project.shared_with)
        domain_project.shared_with = [
            perm for perm in domain_project.shared_with if perm.user_id != user_to_unshare
        ]

        # If nothing changed, return False
        if len(domain_project.shared_with) == initial_length:
            return False

        # Convert back to JSONB format
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def update_share_role(
        self,
        project_id: str,
        owner_id: str,
        target_user_id: str,
        new_role: domain.ShareRole,
    ) -> bool:
        """Update sharing role for a user (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            owner_id: User making the request (must be owner)
            target_user_id: User whose role to update
            new_role: New ShareRole (viewer, editor, admin)

        Returns:
            True if role was updated, False if not found/not owner/user not shared
        """
        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(selectinload(ProjectDB.integrations))  # Eager load for async
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return False  # Not found or not owner

        # Convert to domain object
        domain_project = db_project.to_domain()

        # Find and update the user's role
        updated = False
        for perm in domain_project.shared_with:
            if perm.user_id == target_user_id:
                perm.role = new_role
                updated = True
                break

        if not updated:
            return False  # User not in shared_with list

        # Convert back to JSONB format
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def get_user_role(self, project_id: str, user_id: str) -> Optional[domain.ShareRole]:
        """Get user's role for a project (owner/viewer/editor/admin) (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            user_id: User ID to check

        Returns:
            ShareRole if user has access (owner or in shared_with), None otherwise
        """
        result = await self.session.execute(select(ProjectDB).where(ProjectDB.id == project_id))
        db_project = result.scalar_one_or_none()

        if not db_project:
            return None

        # Check if user is owner
        if db_project.owner_id == user_id:
            return domain.ShareRole.ADMIN  # Owner is treated as admin role

        # Check shared_with
        if db_project.shared_with:
            for perm_dict in db_project.shared_with:
                if perm_dict["user_id"] == user_id:
                    return domain.ShareRole(perm_dict["role"])

        return None  # User has no access


class ProjectIntegrationRepository(BaseRepository):
    """Repository for ProjectIntegration operations"""

    model = ProjectIntegrationDB

    async def get_by_project_and_type(
        self, project_id: str, integration_type: IntegrationType, owner_id: Optional[str] = None
    ) -> Optional[domain.ProjectIntegration]:
        """Get integration by project and type - optionally verify project ownership"""
        filters = [
            ProjectIntegrationDB.project_id == project_id,
            ProjectIntegrationDB.type == integration_type,
            ProjectIntegrationDB.is_active == True,
        ]

        # If owner_id provided, join with projects to verify ownership
        if owner_id:
            from .models import ProjectDB

            result = await self.session.execute(
                select(ProjectIntegrationDB)
                .where(and_(*filters))
                .join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id)
                .where(ProjectDB.owner_id == owner_id)
            )
        else:
            result = await self.session.execute(select(ProjectIntegrationDB).where(and_(*filters)))

        db_integration = result.scalar_one_or_none()
        return db_integration.to_domain() if db_integration else None

    async def list_by_project(
        self, project_id: str, active_only: bool = True, owner_id: Optional[str] = None
    ) -> List[domain.ProjectIntegration]:
        """List integrations by project - optionally verify project ownership"""
        query = select(ProjectIntegrationDB).where(ProjectIntegrationDB.project_id == project_id)
        if active_only:
            query = query.where(ProjectIntegrationDB.is_active == True)

        # If owner_id provided, join with projects to verify ownership
        if owner_id:
            from .models import ProjectDB

            query = query.join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id).where(
                ProjectDB.owner_id == owner_id
            )

        result = await self.session.execute(query.order_by(ProjectIntegrationDB.type))
        return [db_integration.to_domain() for db_integration in result.scalars().all()]


class KnowledgeGraphRepository(BaseRepository):
    """Repository for knowledge graph operations"""

    model = KnowledgeNodeDB  # Default to nodes, but we'll handle both

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    # Node operations
    async def create_node(self, node: domain.KnowledgeNode) -> domain.KnowledgeNode:
        """Create a knowledge node"""
        db_node = KnowledgeNodeDB.from_domain(node)
        return await self.create(**db_node.__dict__)

    async def get_node_by_id(
        self, node_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.KnowledgeNode]:
        """Get node by ID - optionally verify ownership"""
        filters = [KnowledgeNodeDB.id == node_id]
        if owner_id:
            filters.append(KnowledgeNodeDB.owner_id == owner_id)

        result = await self.session.execute(select(KnowledgeNodeDB).where(and_(*filters)))
        db_node = result.scalar_one_or_none()
        return db_node.to_domain() if db_node else None

    async def get_nodes_by_session(
        self, session_id: str, limit: int = 100
    ) -> List[domain.KnowledgeNode]:
        """Get nodes for an owner (parameter named session_id for backward compatibility)"""
        result = await self.session.execute(
            select(KnowledgeNodeDB).where(KnowledgeNodeDB.owner_id == session_id).limit(limit)
        )
        db_nodes = result.scalars().all()
        return [db_node.to_domain() for db_node in db_nodes]

    async def get_nodes_by_type(
        self, node_type: NodeType, session_id: Optional[str] = None, limit: int = 100
    ) -> List[domain.KnowledgeNode]:
        """Get nodes by type, optionally filtered by owner (parameter named session_id for backward compatibility)"""
        query = select(KnowledgeNodeDB).where(KnowledgeNodeDB.node_type == node_type)
        if session_id:
            query = query.where(KnowledgeNodeDB.owner_id == session_id)
        query = query.limit(limit)

        result = await self.session.execute(query)
        db_nodes = result.scalars().all()
        return [db_node.to_domain() for db_node in db_nodes]

    # Edge operations
    async def create_edge(self, edge: domain.KnowledgeEdge) -> domain.KnowledgeEdge:
        """Create a knowledge edge"""
        db_edge = KnowledgeEdgeDB.from_domain(edge)
        return await self.create(**db_edge.__dict__)

    async def get_edge_by_id(
        self, edge_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.KnowledgeEdge]:
        """Get edge by ID - optionally verify ownership"""
        filters = [KnowledgeEdgeDB.id == edge_id]
        if owner_id:
            filters.append(KnowledgeEdgeDB.owner_id == owner_id)

        result = await self.session.execute(select(KnowledgeEdgeDB).where(and_(*filters)))
        db_edge = result.scalar_one_or_none()
        return db_edge.to_domain() if db_edge else None

    async def get_edges_by_session(
        self, session_id: str, limit: int = 100
    ) -> List[domain.KnowledgeEdge]:
        """Get edges for an owner (parameter named session_id for backward compatibility)"""
        result = await self.session.execute(
            select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.owner_id == session_id).limit(limit)
        )
        db_edges = result.scalars().all()
        return [db_edge.to_domain() for db_edge in db_edges]

    # Graph-specific operations
    async def find_neighbors(
        self,
        node_id: str,
        edge_type: Optional[EdgeType] = None,
        direction: str = "both",
        owner_id: Optional[str] = None,
    ) -> List[domain.KnowledgeNode]:
        """Find neighboring nodes - optionally verify ownership of root node"""
        # Verify ownership of the root node if owner_id provided
        if owner_id:
            root_node = await self.get_node_by_id(node_id, owner_id)
            if not root_node:
                return []  # Node not found or doesn't belong to owner

        if direction == "outgoing":
            query = select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.source_node_id == node_id)
        elif direction == "incoming":
            query = select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.target_node_id == node_id)
        else:  # both
            query = select(KnowledgeEdgeDB).where(
                or_(
                    KnowledgeEdgeDB.source_node_id == node_id,
                    KnowledgeEdgeDB.target_node_id == node_id,
                )
            )

        if edge_type:
            query = query.where(KnowledgeEdgeDB.edge_type == edge_type)

        result = await self.session.execute(query)
        edges = result.scalars().all()

        # Get unique neighbor node IDs
        neighbor_ids = set()
        for edge in edges:
            if edge.source_node_id == node_id:
                neighbor_ids.add(edge.target_node_id)
            else:
                neighbor_ids.add(edge.source_node_id)

        # Fetch neighbor nodes
        if neighbor_ids:
            result = await self.session.execute(
                select(KnowledgeNodeDB).where(KnowledgeNodeDB.id.in_(neighbor_ids))
            )
            db_nodes = result.scalars().all()
            return [db_node.to_domain() for db_node in db_nodes]

        return []

    async def get_subgraph(
        self, node_ids: List[str], max_depth: int = 2, owner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get a subgraph around specified nodes - optionally verify ownership"""
        nodes = {}
        edges = []
        visited_nodes = set()
        nodes_to_visit = set(node_ids)

        # If owner_id provided, verify all starting nodes belong to owner
        if owner_id:
            result = await self.session.execute(
                select(KnowledgeNodeDB.id).where(
                    and_(KnowledgeNodeDB.id.in_(node_ids), KnowledgeNodeDB.owner_id == owner_id)
                )
            )
            valid_node_ids = set(row[0] for row in result.fetchall())
            nodes_to_visit = nodes_to_visit.intersection(valid_node_ids)

            if not nodes_to_visit:
                # No valid starting nodes
                return {"nodes": [], "edges": [], "depth": max_depth}

        for depth in range(max_depth):
            if not nodes_to_visit:
                break

            # Get nodes at current depth
            result = await self.session.execute(
                select(KnowledgeNodeDB).where(KnowledgeNodeDB.id.in_(nodes_to_visit))
            )
            db_nodes = result.scalars().all()

            # Add nodes to result
            for db_node in db_nodes:
                nodes[db_node.id] = db_node.to_domain()
                visited_nodes.add(db_node.id)

            # Find edges connecting to these nodes
            result = await self.session.execute(
                select(KnowledgeEdgeDB).where(
                    or_(
                        KnowledgeEdgeDB.source_node_id.in_(nodes_to_visit),
                        KnowledgeEdgeDB.target_node_id.in_(nodes_to_visit),
                    )
                )
            )
            db_edges = result.scalars().all()

            # Add edges to result and collect next level nodes
            next_level_nodes = set()
            for db_edge in db_edges:
                edges.append(db_edge.to_domain())
                if (
                    db_edge.source_node_id in nodes_to_visit
                    and db_edge.target_node_id not in visited_nodes
                ):
                    next_level_nodes.add(db_edge.target_node_id)
                elif (
                    db_edge.target_node_id in nodes_to_visit
                    and db_edge.source_node_id not in visited_nodes
                ):
                    next_level_nodes.add(db_edge.source_node_id)

            nodes_to_visit = next_level_nodes

        return {"nodes": list(nodes.values()), "edges": edges, "depth": max_depth}

    async def find_paths(
        self, source_id: str, target_id: str, max_paths: int = 5, owner_id: Optional[str] = None
    ) -> List[List[domain.KnowledgeNode]]:
        """Find paths between two nodes - optionally verify ownership"""
        # This is a simplified path finding - in production you'd want a more sophisticated algorithm
        paths = []

        # Get direct connections
        result = await self.session.execute(
            select(KnowledgeEdgeDB).where(
                and_(
                    KnowledgeEdgeDB.source_node_id == source_id,
                    KnowledgeEdgeDB.target_node_id == target_id,
                )
            )
        )
        direct_edges = result.scalars().all()

        if direct_edges:
            # Direct path exists - verify ownership if required
            source_node = await self.get_node_by_id(source_id, owner_id)
            target_node = await self.get_node_by_id(target_id, owner_id)
            if source_node and target_node:
                paths.append([source_node, target_node])

        # For simplicity, we'll limit to direct connections for now
        # A full implementation would use recursive CTEs or graph algorithms
        return paths[:max_paths]

    # Bulk operations
    async def create_nodes_bulk(
        self, nodes: List[domain.KnowledgeNode]
    ) -> List[domain.KnowledgeNode]:
        """Create multiple nodes efficiently"""
        db_nodes = [KnowledgeNodeDB.from_domain(node) for node in nodes]
        self.session.add_all(db_nodes)
        await self.session.flush()

        # Refresh to get generated IDs
        for db_node in db_nodes:
            await self.session.refresh(db_node)

        return [db_node.to_domain() for db_node in db_nodes]

    async def create_edges_bulk(
        self, edges: List[domain.KnowledgeEdge]
    ) -> List[domain.KnowledgeEdge]:
        """Create multiple edges efficiently"""
        db_edges = [KnowledgeEdgeDB.from_domain(edge) for edge in edges]
        self.session.add_all(db_edges)
        await self.session.flush()

        # Refresh to get generated IDs
        for db_edge in db_edges:
            await self.session.refresh(db_edge)

        return [db_edge.to_domain() for db_edge in db_edges]

    # Privacy-aware operations (ready for BoundaryEnforcer integration)
    async def get_nodes_with_privacy_check(
        self, session_id: str, privacy_level: str = "standard"
    ) -> List[domain.KnowledgeNode]:
        """Get nodes with privacy considerations"""
        # This method is ready for BoundaryEnforcer integration
        # For now, it's a simple wrapper around get_nodes_by_session
        nodes = await self.get_nodes_by_session(session_id)

        # Future: Add privacy filtering based on content analysis
        # Future: Integrate with BoundaryEnforcer for content validation
        # Future: Add redaction for sensitive information

        return nodes

    async def create_node_with_privacy_check(
        self, node: domain.KnowledgeNode, privacy_level: str = "standard"
    ) -> domain.KnowledgeNode:
        """Create node with privacy validation"""
        # This method is ready for BoundaryEnforcer integration
        # For now, it's a simple wrapper around create_node

        # Future: Add content validation before creation
        # Future: Integrate with BoundaryEnforcer for boundary checking
        # Future: Add automatic redaction of sensitive information

        return await self.create_node(node)


# PM-034 Phase 3: Conversation Repository for ConversationManager
# Issue #563: Implemented actual persistence (was stubbed)
class ConversationRepository(BaseRepository):
    """Repository for conversation turn operations"""

    model = None  # Uses ConversationTurnDB directly via from_domain/to_domain

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_conversation_turns(
        self, conversation_id: str, limit: int = 100, is_admin: bool = False
    ) -> List[domain.ConversationTurn]:
        """Get conversation turns for a conversation ID.

        Args:
            conversation_id: The conversation to fetch turns for
            limit: Maximum number of turns to return (default 100)
            is_admin: SEC-RBAC Phase 3 - admins can access any conversation

        Returns:
            List of ConversationTurn domain objects, ordered by turn_number
        """
        from services.database.models import ConversationTurnDB

        stmt = (
            select(ConversationTurnDB)
            .where(ConversationTurnDB.conversation_id == conversation_id)
            .order_by(ConversationTurnDB.turn_number)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        db_turns = result.scalars().all()

        return [t.to_domain() for t in db_turns]

    async def save_turn(
        self, turn: domain.ConversationTurn, is_admin: bool = False, user_id: Optional[str] = None
    ) -> None:
        """Save conversation turn to database.

        Args:
            turn: The ConversationTurn domain object to persist
            is_admin: SEC-RBAC Phase 3 - admins can save turns for any conversation
            user_id: Optional user ID to associate with conversation (Issue #563)
        """
        from services.database.models import ConversationDB, ConversationTurnDB

        # Issue #563: Ensure conversation exists before saving turn (FK constraint)
        await self.ensure_conversation_exists(turn.conversation_id, user_id)

        # Check if turn already exists (upsert logic)
        existing = await self.session.get(ConversationTurnDB, turn.id)

        if existing:
            # Update existing turn
            existing.user_message = turn.user_message
            existing.assistant_response = turn.assistant_response
            existing.intent = turn.intent
            existing.entities = turn.entities
            existing.references = turn.references
            existing.context_used = turn.context_used
            existing.turn_metadata = turn.metadata
            existing.processing_time = turn.processing_time
            existing.completed_at = turn.completed_at
            logger.debug(f"ConversationTurn updated: {turn.id}")
        else:
            # Create new turn
            db_turn = ConversationTurnDB.from_domain(turn)
            self.session.add(db_turn)
            logger.debug(f"ConversationTurn created: {turn.id}")

            # Issue #598: Auto-title conversation on first turn
            if turn.turn_number == 1 and turn.user_message:
                db_conv = await self.session.get(ConversationDB, turn.conversation_id)
                if db_conv and db_conv.title == "New conversation":
                    new_title = self.generate_title_from_message(turn.user_message)
                    db_conv.title = new_title
                    logger.debug(
                        f"Auto-titled conversation: {turn.conversation_id} -> {new_title[:30]}..."
                    )

        await self.session.commit()
        logger.info(f"ConversationTurn saved to database: {turn.id}")

    async def get_next_turn_number(self, conversation_id: str, is_admin: bool = False) -> int:
        """Get next turn number for conversation.

        Args:
            conversation_id: The conversation to get next turn number for
            is_admin: SEC-RBAC Phase 3 - admins can get next turn for any conversation

        Returns:
            The next sequential turn number (max existing + 1, or 1 if no turns)
        """
        from services.database.models import ConversationTurnDB

        stmt = select(func.max(ConversationTurnDB.turn_number)).where(
            ConversationTurnDB.conversation_id == conversation_id
        )

        result = await self.session.execute(stmt)
        max_turn = result.scalar()

        return (max_turn or 0) + 1

    async def ensure_conversation_exists(
        self, conversation_id: str, user_id: Optional[str] = None
    ) -> None:
        """
        Ensure a conversation exists, creating it if necessary.

        This is needed because conversation_turns has a FK to conversations.
        Issue #563: Called before saving turns to handle new sessions.

        Args:
            conversation_id: The conversation/session ID
            user_id: Optional user ID to associate with conversation
        """
        from services.database.models import ConversationDB

        # Check if conversation exists
        existing = await self.session.get(ConversationDB, conversation_id)
        if existing:
            return

        # Create new conversation
        conversation = ConversationDB(
            id=conversation_id,
            user_id=user_id or conversation_id,  # Use conversation_id as fallback
            session_id=conversation_id,
            title=f"Conversation",
            context={},
            is_active=True,
        )

        self.session.add(conversation)
        await self.session.commit()
        logger.debug(f"Created conversation: {conversation_id}")

    async def get_latest_for_user(self, user_id: str) -> Optional[domain.Conversation]:
        """
        Get the most recent active conversation for a user.

        Issue #563: Used for "Continue where you left off" prompt.

        Args:
            user_id: The user ID to find conversations for

        Returns:
            The most recent Conversation domain object, or None if no conversations exist
        """
        from services.database.models import ConversationDB

        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.is_active == True)
            .order_by(ConversationDB.created_at.desc())
            .limit(1)
        )

        result = await self.session.execute(stmt)
        db_conv = result.scalar_one_or_none()

        if db_conv:
            return db_conv.to_domain()
        return None

    # Issue #565: Additional methods for conversation sidebar

    async def list_for_user(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> List[domain.Conversation]:
        """
        List conversations for a user, ordered by most recent first.

        Issue #565: Used for conversation history sidebar.

        Args:
            user_id: The user ID to find conversations for
            limit: Maximum number of conversations to return (default 50)
            offset: Number of conversations to skip for pagination

        Returns:
            List of Conversation domain objects, newest first
        """
        from services.database.models import ConversationDB

        # Issue #587: Sort by last_activity_at (most recently active first)
        # Use COALESCE to fall back to created_at for conversations with no activity yet
        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.is_active == True)
            .order_by(
                func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        db_convs = result.scalars().all()

        return [c.to_domain() for c in db_convs]

    async def get_by_id(self, conversation_id: str) -> Optional[domain.Conversation]:
        """
        Get a specific conversation by ID.

        Issue #565: Used when switching conversations in sidebar.

        Args:
            conversation_id: The conversation ID to fetch

        Returns:
            Conversation domain object, or None if not found
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)

        if db_conv:
            return db_conv.to_domain()
        return None

    async def create(self, user_id: str, title: Optional[str] = None) -> domain.Conversation:
        """
        Create a new conversation for a user.

        Issue #565: Used when clicking "New Chat" in sidebar.

        Args:
            user_id: The user ID to create conversation for
            title: Optional title (defaults to "New conversation")

        Returns:
            The newly created Conversation domain object
        """
        import uuid

        from services.database.models import ConversationDB

        conversation_id = str(uuid.uuid4())

        conversation = ConversationDB(
            id=conversation_id,
            user_id=user_id,
            session_id=conversation_id,
            title=title or "New conversation",
            context={},
            is_active=True,
        )

        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)

        logger.debug(f"Created new conversation: {conversation_id} for user: {user_id}")

        return conversation.to_domain()

    async def get_turn_count(self, conversation_id: str) -> int:
        """
        Get the number of turns in a conversation.

        Issue #565: Used for conversation list display.

        Args:
            conversation_id: The conversation to count turns for

        Returns:
            Number of turns in the conversation
        """
        from services.database.models import ConversationTurnDB

        stmt = select(func.count(ConversationTurnDB.id)).where(
            ConversationTurnDB.conversation_id == conversation_id
        )

        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def update_title(self, conversation_id: str, title: str) -> None:
        """
        Update conversation title.

        Issue #598: Used to auto-generate title from first user message.

        Args:
            conversation_id: The conversation to update
            title: The new title
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if db_conv:
            db_conv.title = title
            await self.session.commit()
            logger.debug(f"Updated conversation title: {conversation_id} -> {title[:30]}...")

    @staticmethod
    def generate_title_from_message(message: str, max_length: int = 50) -> str:
        """
        Generate a conversation title from a user message.

        Issue #598: Auto-title conversations based on first user message.

        Args:
            message: The user message to derive title from
            max_length: Maximum title length (default 50)

        Returns:
            A cleaned, truncated title string
        """
        import re

        if not message:
            return "New conversation"

        # Strip markdown formatting
        cleaned = re.sub(r"\*\*|__|\*|_|`|##+\s*", "", message)
        # Strip URLs
        cleaned = re.sub(r"https?://\S+", "", cleaned)
        # Strip excessive whitespace
        cleaned = " ".join(cleaned.split())
        # Trim leading/trailing whitespace
        cleaned = cleaned.strip()

        if not cleaned:
            return "New conversation"

        # Truncate with ellipsis if too long
        if len(cleaned) > max_length:
            # Try to break at word boundary
            truncated = cleaned[:max_length].rsplit(" ", 1)[0]
            if len(truncated) < max_length * 0.7:  # If we lost too much, just hard truncate
                truncated = cleaned[: max_length - 3]
            return truncated + "..."

        return cleaned


# Repository factory
class RepositoryFactory:
    """Creates repositories with session
    NOTE: The caller is responsible for closing the returned session (repos["session"]) after use, ideally in a finally block.
    """

    @staticmethod
    async def get_repositories():
        """Get all repositories with a new session
        DEPRECATED: Use AsyncSessionFactory.session_scope() directly for better resource management.
        This method is maintained for backward compatibility only.
        """
        session = await AsyncSessionFactory.create_session()
        return {
            "products": ProductRepository(session),
            "features": FeatureRepository(session),
            "work_items": WorkItemRepository(session),
            "workflows": WorkflowRepository(session),
            "tasks": TaskRepository(session),
            "projects": ProjectRepository(session),  # PM-009: Add project repository
            "project_integrations": ProjectIntegrationRepository(
                session
            ),  # PM-009: Add integration repository
            "knowledge_graph": KnowledgeGraphRepository(
                session
            ),  # PM-040: Add knowledge graph repository
            "session": session,
        }
