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
        self, project_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.Project]:
        """Get project by ID with integrations - optionally verify ownership"""
        filters = [ProjectDB.id == project_id]
        if owner_id:
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
            select(ProjectDB).where(ProjectDB.is_default == True, ProjectDB.is_archived == False)
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def list_active_projects(self, owner_id: Optional[str] = None) -> List[domain.Project]:
        """List active projects - optionally filter by owner"""
        filters = [ProjectDB.is_archived == False]
        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB).where(and_(*filters)).order_by(ProjectDB.name)
        )
        return [db_project.to_domain() for db_project in result.scalars().all()]

    async def count_active_projects(self, owner_id: Optional[str] = None) -> int:
        """Count active projects - optionally filter by owner"""
        filters = [ProjectDB.is_archived == False]
        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(select(func.count(ProjectDB.id)).where(and_(*filters)))
        return result.scalar() or 0

    async def find_by_name(
        self, name: str, owner_id: Optional[str] = None
    ) -> Optional[domain.Project]:
        """Find project by name - optionally filter by owner"""
        filters = [func.lower(ProjectDB.name) == name.lower(), ProjectDB.is_archived == False]
        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(select(ProjectDB).where(and_(*filters)))
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
            updated_at=datetime.utcnow(),
        )
        db_project = ProjectDB.from_domain(project)
        self.session.add(db_project)
        await self.session.commit()
        await self.session.refresh(db_project)
        return db_project.to_domain()

    async def get_project_with_integrations(
        self, project_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.Project]:
        """Get project with integrations - optionally verify ownership"""
        filters = [ProjectDB.id == project_id, ProjectDB.is_archived == False]
        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB).where(and_(*filters)).options(selectinload(ProjectDB.integrations))
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None


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
        """Get nodes for a session"""
        result = await self.session.execute(
            select(KnowledgeNodeDB).where(KnowledgeNodeDB.session_id == session_id).limit(limit)
        )
        db_nodes = result.scalars().all()
        return [db_node.to_domain() for db_node in db_nodes]

    async def get_nodes_by_type(
        self, node_type: NodeType, session_id: Optional[str] = None, limit: int = 100
    ) -> List[domain.KnowledgeNode]:
        """Get nodes by type, optionally filtered by session"""
        query = select(KnowledgeNodeDB).where(KnowledgeNodeDB.node_type == node_type)
        if session_id:
            query = query.where(KnowledgeNodeDB.session_id == session_id)
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
        """Get edges for a session"""
        result = await self.session.execute(
            select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.session_id == session_id).limit(limit)
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
class ConversationRepository(BaseRepository):
    """Repository for conversation turn operations"""

    model = None  # ConversationTurn is a domain model, not a DB model yet

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_conversation_turns(
        self, conversation_id: str, owner_id: Optional[str] = None
    ) -> List[domain.ConversationTurn]:
        """Get conversation turns - optionally filter by owner"""
        filters = [ConversationTurnDB.conversation_id == conversation_id]
        if owner_id:
            filters.append(ConversationTurnDB.user_id == owner_id)

        result = await self.session.execute(
            select(ConversationTurnDB)
            .where(and_(*filters))
            .order_by(ConversationTurnDB.turn_number)
        )
        return [turn.to_domain() for turn in result.scalars().all()]

    async def save_turn(
        self, turn: domain.ConversationTurn, owner_id: Optional[str] = None
    ) -> None:
        """Save conversation turn to database - optionally verify ownership"""
        # If owner_id provided, verify it matches turn's user_id
        if owner_id and owner_id != turn.user_id:
            raise ValueError(f"Owner ID {owner_id} does not match turn user ID {turn.user_id}")

        # For now, this is a no-op since we don't have DB table yet
        # Redis caching will handle persistence in Phase 3
        logger.info(f"ConversationTurn saved (cache-only): {turn.id}")

    async def get_next_turn_number(
        self, conversation_id: str, owner_id: Optional[str] = None
    ) -> int:
        """Get next turn number for conversation - optionally verify ownership"""
        # For now, return 1 as fallback
        # This enables basic functionality while we build out full DB schema
        return 1


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
