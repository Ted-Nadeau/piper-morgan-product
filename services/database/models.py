"""
Database Models
SQLAlchemy models for persistent storage
"""

import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

import services.domain.models as domain
from services.shared_types import (
    EdgeType,
    IntegrationType,
    IntentCategory,
    ListType,
    NodeType,
    OrderingStrategy,
    TaskStatus,
    TaskType,
    TodoPriority,
    TodoStatus,
    WorkflowStatus,
    WorkflowType,
)

from .connection import Base


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    """Product being managed"""

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    vision = Column(Text)
    strategy = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    features = relationship("Feature", back_populates="product")
    work_items = relationship("WorkItem", back_populates="product")


class Feature(Base):
    """Feature or capability"""

    __tablename__ = "features"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    hypothesis = Column(Text)
    acceptance_criteria = Column(JSON)  # List of criteria
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="features")
    work_items = relationship("WorkItem", back_populates="feature")


class WorkItem(Base):
    """Universal work item - can sync to any external system"""

    __tablename__ = "work_items"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    feature_id = Column(String, ForeignKey("features.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String)  # bug, feature, task, improvement
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    labels = Column(JSON)  # List of labels
    assignee = Column(String)  # Assigned person
    project_id = Column(String)  # Project association (separate from FK)
    source_system = Column(String)  # Source system name
    external_id = Column(String)  # External system ID
    external_url = Column(String)  # External system URL
    item_metadata = Column(JSON)  # Additional metadata (renamed to avoid SQLAlchemy conflict)

    # External system references
    external_refs = Column(JSON)  # {"github": "issue-123", "jira": "PROJ-456"}

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="work_items")
    feature = relationship("Feature", back_populates="work_items")

    def to_domain(self) -> domain.WorkItem:
        """Convert database model to domain model"""
        return domain.WorkItem(
            id=self.id,
            title=self.title,
            description=self.description,
            type=self.type or "task",
            status=self.status or "open",
            priority=self.priority or "medium",
            labels=self.labels or [],
            assignee=self.assignee,
            project_id=self.project_id,
            source_system=self.source_system or "",
            external_id=self.external_id or "",
            external_url=self.external_url,
            metadata=self.item_metadata or {},  # Map item_metadata to metadata
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, work_item: domain.WorkItem) -> "WorkItem":
        """Create database model from domain model"""
        return cls(
            id=work_item.id,
            title=work_item.title,
            description=work_item.description,
            type=work_item.type,
            status=work_item.status,
            priority=work_item.priority,
            labels=work_item.labels,
            assignee=work_item.assignee,
            project_id=work_item.project_id,
            source_system=work_item.source_system,
            external_id=work_item.external_id,
            external_url=work_item.external_url,
            item_metadata=work_item.metadata,  # Map metadata to item_metadata
        )


class Intent(Base):
    """Captured user intent"""

    __tablename__ = "intents"

    id = Column(String, primary_key=True)
    category = Column(Enum(IntentCategory))
    action = Column(String)
    confidence = Column(Float)
    context = Column(JSON)
    original_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to workflow if one was created
    workflow_id = Column(String, ForeignKey("workflows.id"))
    workflow = relationship("Workflow", back_populates="intent")


class Workflow(Base):
    """Workflow execution record"""

    __tablename__ = "workflows"

    id = Column(String, primary_key=True)
    type = Column(Enum(WorkflowType))
    status = Column(Enum(WorkflowStatus))
    input_data = Column(JSON)
    output_data = Column(JSON)
    context = Column(JSON)
    result = Column(JSON)  # Workflow execution result
    error = Column(Text)
    intent_id = Column(String(255), nullable=True)  # Matches domain Optional[str]

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    intent = relationship("Intent", back_populates="workflow", uselist=False)
    tasks = relationship("Task", back_populates="workflow")

    def to_domain(self) -> domain.Workflow:
        """Convert database model to domain model"""
        return domain.Workflow(
            id=self.id,
            type=self.type,
            status=self.status,
            context=self.context or {},
            result=self.output_data,
            error=self.error,
            intent_id=self.intent.id if self.intent else None,
            created_at=self.created_at,
            updated_at=self.completed_at
            or self.created_at,  # Use completed_at as updated_at, fallback to created_at
        )

    @classmethod
    def from_domain(cls, workflow: domain.Workflow) -> "Workflow":
        """Create database model from domain model"""
        return cls(
            id=workflow.id,
            type=workflow.type,
            status=workflow.status,
            input_data=workflow.input_data if hasattr(workflow, "input_data") else None,
            output_data=workflow.result,
            context=workflow.context,
            error=workflow.error,
            created_at=workflow.created_at,
            completed_at=workflow.completed_at,
        )


class Task(Base, TimestampMixin):
    """Individual task in a workflow"""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey("workflows.id"))
    name = Column(String, nullable=False)  # Task name
    type = Column(Enum(TaskType))
    status = Column(Enum(TaskStatus))
    input_data = Column(JSON)
    output_data = Column(JSON)
    result = Column(JSON)  # Task execution result
    error = Column(Text)

    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    workflow = relationship("Workflow", back_populates="tasks")


class Stakeholder(Base):
    """People involved with products"""

    __tablename__ = "stakeholders"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    role = Column(String)
    interests = Column(JSON)  # List of interest areas
    influence_level = Column(Integer, default=1)
    satisfaction = Column(Float)  # Stakeholder satisfaction level
    created_at = Column(DateTime, default=datetime.utcnow)


class ProjectDB(Base):
    """A PM project with multiple tool integrations"""

    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    integrations = relationship(
        "ProjectIntegrationDB", back_populates="project", cascade="all, delete-orphan"
    )

    def to_domain(self) -> domain.Project:
        project = domain.Project(
            id=self.id,
            name=self.name,
            description=self.description,
            is_default=self.is_default,
            is_archived=self.is_archived,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        # Map integrations relationship
        project.integrations = [integration.to_domain() for integration in self.integrations]
        return project

    @classmethod
    def from_domain(cls, project: domain.Project) -> "ProjectDB":
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            is_default=project.is_default,
            is_archived=project.is_archived,
            created_at=project.created_at,
            updated_at=project.updated_at,
            # Note: integrations handled separately in repository
        )


class ProjectIntegrationDB(Base):
    """Integration configuration for a project"""

    __tablename__ = "project_integrations"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    type = Column(Enum(IntegrationType), nullable=False)
    name = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("ProjectDB", back_populates="integrations")

    def to_domain(self) -> domain.ProjectIntegration:
        return domain.ProjectIntegration(
            id=self.id,
            type=self.type,
            name=self.name,
            config=self.config,
            is_active=self.is_active,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(
        cls, integration: domain.ProjectIntegration, project_id: str
    ) -> "ProjectIntegrationDB":
        return cls(
            id=integration.id,
            project_id=project_id,
            type=integration.type,
            name=integration.name,
            config=integration.config,
            is_active=integration.is_active,
            created_at=integration.created_at,
        )


class UploadedFileDB(Base):
    """Database model for uploaded files"""

    __tablename__ = "uploaded_files"

    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(255))
    file_size = Column(Integer)
    storage_path = Column(String(1000))
    upload_time = Column(DateTime, default=datetime.utcnow)
    last_referenced = Column(DateTime, nullable=True)
    reference_count = Column(Integer, default=0)
    file_metadata = Column(JSON, default=dict)
    item_metadata = Column(JSON, default=dict)

    __table_args__ = (
        Index("idx_files_session", "session_id", "upload_time"),
        Index("idx_files_filename", "filename"),
    )

    def to_domain(self) -> domain.UploadedFile:
        return domain.UploadedFile(
            id=self.id,
            session_id=self.session_id,
            filename=self.filename,
            file_type=self.file_type,
            file_size=self.file_size,
            storage_path=self.storage_path,
            upload_time=self.upload_time,
            last_referenced=self.last_referenced,
            reference_count=self.reference_count,
            metadata=self.item_metadata or {},
            file_metadata=self.file_metadata or {},
        )

    @classmethod
    def from_domain(cls, file: domain.UploadedFile) -> "UploadedFileDB":
        return cls(
            id=file.id,
            session_id=file.session_id,
            filename=file.filename,
            file_type=file.file_type,
            file_size=file.file_size,
            storage_path=file.storage_path,
            upload_time=file.upload_time,
            last_referenced=file.last_referenced,
            reference_count=file.reference_count,
            file_metadata=file.file_metadata,
            item_metadata=file.metadata,
        )


class KnowledgeNodeDB(Base):
    """Database model for knowledge graph nodes"""

    __tablename__ = "knowledge_nodes"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    node_type = Column(Enum(NodeType), nullable=False)
    description = Column(Text)
    node_metadata = Column(JSON, default=dict)
    properties = Column(JSON, default=dict)
    session_id = Column(String)
    embedding_vector = Column(JSON)  # Will be upgraded to pgvector VECTOR type later
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    outgoing_edges = relationship(
        "KnowledgeEdgeDB",
        foreign_keys="KnowledgeEdgeDB.source_node_id",
        back_populates="source_node",
    )
    incoming_edges = relationship(
        "KnowledgeEdgeDB",
        foreign_keys="KnowledgeEdgeDB.target_node_id",
        back_populates="target_node",
    )

    __table_args__ = (
        Index("idx_nodes_session", "session_id"),
        Index("idx_nodes_type", "node_type"),
        Index("idx_nodes_name", "name"),
    )

    def to_domain(self) -> domain.KnowledgeNode:
        return domain.KnowledgeNode(
            id=self.id,
            name=self.name,
            node_type=self.node_type,
            description=self.description,
            metadata=self.node_metadata or {},
            properties=self.properties or {},
            created_at=self.created_at,
            updated_at=self.updated_at,
            session_id=self.session_id,
        )

    @classmethod
    def from_domain(cls, node: domain.KnowledgeNode) -> "KnowledgeNodeDB":
        return cls(
            id=node.id,
            name=node.name,
            node_type=node.node_type,
            description=node.description,
            node_metadata=node.metadata,
            properties=node.properties,
            created_at=node.created_at,
            updated_at=node.updated_at,
            session_id=node.session_id,
        )


class KnowledgeEdgeDB(Base):
    """Database model for knowledge graph edges"""

    __tablename__ = "knowledge_edges"

    id = Column(String, primary_key=True)
    source_node_id = Column(String, ForeignKey("knowledge_nodes.id"), nullable=False)
    target_node_id = Column(String, ForeignKey("knowledge_nodes.id"), nullable=False)
    edge_type = Column(Enum(EdgeType), nullable=False)
    weight = Column(Float, default=1.0)
    node_metadata = Column(JSON, default=dict)
    properties = Column(JSON, default=dict)
    session_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_node = relationship(
        "KnowledgeNodeDB", foreign_keys=[source_node_id], back_populates="outgoing_edges"
    )
    target_node = relationship(
        "KnowledgeNodeDB", foreign_keys=[target_node_id], back_populates="incoming_edges"
    )

    __table_args__ = (
        Index("idx_edges_source", "source_node_id"),
        Index("idx_edges_target", "target_node_id"),
        Index("idx_edges_type", "edge_type"),
        Index("idx_edges_session", "session_id"),
        Index("idx_edges_source_target", "source_node_id", "target_node_id"),
    )

    def to_domain(self) -> domain.KnowledgeEdge:
        return domain.KnowledgeEdge(
            id=self.id,
            source_node_id=self.source_node_id,
            target_node_id=self.target_node_id,
            edge_type=self.edge_type,
            weight=self.weight,
            metadata=self.node_metadata or {},
            properties=self.properties,
            created_at=self.created_at,
            updated_at=self.updated_at,
            session_id=self.session_id,
        )

    @classmethod
    def from_domain(cls, edge: domain.KnowledgeEdge) -> "KnowledgeEdgeDB":
        return cls(
            id=edge.id,
            source_node_id=edge.source_node_id,
            target_node_id=edge.target_node_id,
            edge_type=edge.edge_type,
            weight=edge.weight,
            node_metadata=edge.metadata,
            properties=edge.properties,
            created_at=edge.created_at,
            updated_at=edge.updated_at,
            session_id=edge.session_id,
        )


# PM-081: Todo Management System Database Models
class TodoListDB(Base):
    """Database model for TodoList with strategic indexing"""

    __tablename__ = "todo_lists"

    # Primary key
    id = Column(String, primary_key=True)

    # Core fields
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    list_type = Column(Enum(ListType), nullable=False, default=ListType.PERSONAL)
    ordering_strategy = Column(
        Enum(OrderingStrategy), nullable=False, default=OrderingStrategy.MANUAL
    )

    # UI customization
    color = Column(String(7))  # Hex color codes
    emoji = Column(String(4))  # Unicode emoji

    # Status flags
    is_archived = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Metadata and tags
    list_metadata = Column(JSON, default=dict)
    tags = Column(JSON, default=list)  # Array of tag strings

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Ownership and sharing
    owner_id = Column(String, nullable=False)
    shared_with = Column(JSON, default=list)  # Array of user IDs

    # Performance optimization - cached counts
    todo_count = Column(Integer, default=0, nullable=False)
    completed_count = Column(Integer, default=0, nullable=False)

    # Relationships
    memberships = relationship(
        "ListMembershipDB", back_populates="todo_list", cascade="all, delete-orphan"
    )

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_todo_lists_owner_type", "owner_id", "list_type"),
        Index("idx_todo_lists_owner_archived", "owner_id", "is_archived"),
        Index("idx_todo_lists_shared", "shared_with"),  # GIN index for JSON array
        Index("idx_todo_lists_default", "owner_id", "is_default"),
        Index("idx_todo_lists_tags", "tags"),  # GIN index for tag search
    )

    def to_domain(self) -> domain.TodoList:
        """Convert to domain model"""
        return domain.TodoList(
            id=self.id,
            name=self.name,
            description=self.description,
            list_type=self.list_type,
            ordering_strategy=self.ordering_strategy,
            color=self.color,
            emoji=self.emoji,
            is_archived=self.is_archived,
            is_default=self.is_default,
            metadata=self.list_metadata or {},
            tags=self.tags or [],
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner_id=self.owner_id,
            shared_with=self.shared_with or [],
            todo_count=self.todo_count,
            completed_count=self.completed_count,
        )

    @classmethod
    def from_domain(cls, todo_list: domain.TodoList) -> "TodoListDB":
        """Create from domain model"""
        return cls(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            list_type=todo_list.list_type,
            ordering_strategy=todo_list.ordering_strategy,
            color=todo_list.color,
            emoji=todo_list.emoji,
            is_archived=todo_list.is_archived,
            is_default=todo_list.is_default,
            list_metadata=todo_list.metadata,
            tags=todo_list.tags,
            created_at=todo_list.created_at,
            updated_at=todo_list.updated_at,
            owner_id=todo_list.owner_id,
            shared_with=todo_list.shared_with,
            todo_count=todo_list.todo_count,
            completed_count=todo_list.completed_count,
        )


class TodoDB(Base):
    """Database model for Todo with comprehensive indexing"""

    __tablename__ = "todos"

    # Primary key
    id = Column(String, primary_key=True)

    # Core fields
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    status = Column(Enum(TodoStatus), nullable=False, default=TodoStatus.PENDING)
    priority = Column(Enum(TodoPriority), nullable=False, default=TodoPriority.MEDIUM)

    # Hierarchical structure
    parent_id = Column(String, ForeignKey("todos.id"))
    position = Column(Integer, default=0, nullable=False)

    # Scheduling
    due_date = Column(DateTime)
    reminder_date = Column(DateTime)
    scheduled_date = Column(DateTime)

    # Context and categorization
    tags = Column(JSON, default=list)
    project_id = Column(String, ForeignKey("projects.id"))
    context = Column(String)  # @home, @work, etc.

    # Progress tracking
    estimated_minutes = Column(Integer)
    actual_minutes = Column(Integer)
    completion_notes = Column(Text, default="")

    # PM-040 Knowledge Graph integration
    list_metadata = Column(JSON, default=dict)
    knowledge_node_id = Column(String)  # Link to Knowledge Graph
    related_todos = Column(JSON, default=list)  # Array of todo IDs

    # PM-034 Intent Classification integration
    creation_intent = Column(String)
    intent_confidence = Column(Float)

    # External integrations
    external_refs = Column(JSON, default=dict)  # {"github_issue": "123"}

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    # Ownership
    owner_id = Column(String, nullable=False)
    assigned_to = Column(String)

    # Relationships
    parent = relationship("TodoDB", remote_side=[id], back_populates="children")
    children = relationship("TodoDB", back_populates="parent", cascade="all, delete-orphan")
    memberships = relationship(
        "ListMembershipDB", back_populates="todo", cascade="all, delete-orphan"
    )

    # Comprehensive indexes for query performance
    __table_args__ = (
        # Core query patterns
        Index("idx_todos_owner_status", "owner_id", "status"),
        Index("idx_todos_owner_priority", "owner_id", "priority"),
        Index("idx_todos_assigned_status", "assigned_to", "status"),
        # Date-based queries
        Index("idx_todos_due_date", "due_date"),
        Index("idx_todos_owner_due", "owner_id", "due_date"),
        Index("idx_todos_scheduled", "scheduled_date"),
        Index("idx_todos_reminder", "reminder_date"),
        # Hierarchical queries
        Index("idx_todos_parent", "parent_id"),
        Index("idx_todos_parent_position", "parent_id", "position"),
        # Context and categorization
        Index("idx_todos_context", "context"),
        Index("idx_todos_project", "project_id"),
        Index("idx_todos_tags", "tags"),  # GIN index for tag search
        # PM-040/PM-034 integration
        Index("idx_todos_knowledge_node", "knowledge_node_id"),
        Index("idx_todos_creation_intent", "creation_intent"),
        # External references
        Index("idx_todos_external_refs", "external_refs"),  # GIN index for JSON search
        # Performance queries
        Index("idx_todos_owner_created", "owner_id", "created_at"),
        Index("idx_todos_owner_updated", "owner_id", "updated_at"),
    )

    def to_domain(self) -> domain.Todo:
        """Convert to domain model"""
        return domain.Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            parent_id=self.parent_id,
            position=self.position,
            due_date=self.due_date,
            reminder_date=self.reminder_date,
            scheduled_date=self.scheduled_date,
            tags=self.tags or [],
            project_id=self.project_id,
            context=self.context,
            estimated_minutes=self.estimated_minutes,
            actual_minutes=self.actual_minutes,
            completion_notes=self.completion_notes,
            metadata=self.list_metadata or {},
            knowledge_node_id=self.knowledge_node_id,
            related_todos=self.related_todos or [],
            creation_intent=self.creation_intent,
            intent_confidence=self.intent_confidence,
            external_refs=self.external_refs or {},
            created_at=self.created_at,
            updated_at=self.updated_at,
            completed_at=self.completed_at,
            owner_id=self.owner_id,
            assigned_to=self.assigned_to,
        )

    @classmethod
    def from_domain(cls, todo: domain.Todo) -> "TodoDB":
        """Create from domain model"""
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            parent_id=todo.parent_id,
            position=todo.position,
            due_date=todo.due_date,
            reminder_date=todo.reminder_date,
            scheduled_date=todo.scheduled_date,
            tags=todo.tags,
            project_id=todo.project_id,
            context=todo.context,
            estimated_minutes=todo.estimated_minutes,
            actual_minutes=todo.actual_minutes,
            completion_notes=todo.completion_notes,
            list_metadata=todo.metadata,
            knowledge_node_id=todo.knowledge_node_id,
            related_todos=todo.related_todos,
            creation_intent=todo.creation_intent,
            intent_confidence=todo.intent_confidence,
            external_refs=todo.external_refs,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            completed_at=todo.completed_at,
            owner_id=todo.owner_id,
            assigned_to=todo.assigned_to,
        )


class ListMembershipDB(Base):
    """Database model for many-to-many Todo-to-List relationships"""

    __tablename__ = "list_memberships"

    # Primary key
    id = Column(String, primary_key=True)

    # Foreign keys
    list_id = Column(String, ForeignKey("todo_lists.id"), nullable=False)
    todo_id = Column(String, ForeignKey("todos.id"), nullable=False)

    # Position tracking
    position = Column(Integer, default=0, nullable=False)

    # Membership metadata
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    added_by = Column(String, nullable=False)

    # List-specific overrides
    list_priority = Column(Enum(TodoPriority))
    list_due_date = Column(DateTime)
    list_notes = Column(Text, default="")

    # Relationships
    todo_list = relationship("TodoListDB", back_populates="memberships")
    todo = relationship("TodoDB", back_populates="memberships")

    # Strategic indexes for many-to-many queries
    __table_args__ = (
        # Ensure unique membership per list-todo pair
        Index("idx_unique_list_todo", "list_id", "todo_id", unique=True),
        # Position-based ordering within lists
        Index("idx_membership_list_position", "list_id", "position"),
        # Todo-centric queries
        Index("idx_membership_todo", "todo_id"),
        # List-centric queries
        Index("idx_membership_list", "list_id"),
        # User-added tracking
        Index("idx_membership_added_by", "added_by"),
        Index("idx_membership_added_at", "added_at"),
        # List-specific overrides
        Index("idx_membership_list_priority", "list_id", "list_priority"),
        Index("idx_membership_list_due", "list_id", "list_due_date"),
    )

    def to_domain(self) -> domain.ListMembership:
        """Convert to domain model"""
        return domain.ListMembership(
            id=self.id,
            list_id=self.list_id,
            todo_id=self.todo_id,
            position=self.position,
            added_at=self.added_at,
            added_by=self.added_by,
            list_priority=self.list_priority,
            list_due_date=self.list_due_date,
            list_notes=self.list_notes,
        )

    @classmethod
    def from_domain(cls, membership: domain.ListMembership) -> "ListMembershipDB":
        """Create from domain model"""
        return cls(
            id=membership.id,
            list_id=membership.list_id,
            todo_id=membership.todo_id,
            position=membership.position,
            added_at=membership.added_at,
            added_by=membership.added_by,
            list_priority=membership.list_priority,
            list_due_date=membership.list_due_date,
            list_notes=membership.list_notes,
        )


# PM-081: Universal List Architecture Database Models
# Chief Architect's universal composition over specialization principle


class ListDB(Base):
    """Universal List database model for ANY item type"""

    __tablename__ = "lists"

    # Primary key
    id = Column(String, primary_key=True)

    # Core fields
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    item_type = Column(String, nullable=False, default="todo")  # todo, feature, bug, attendee, etc.
    list_type = Column(String, nullable=False, default="personal")  # personal, shared, project
    ordering_strategy = Column(
        String, nullable=False, default="manual"
    )  # manual, due_date, priority, created

    # UI customization
    color = Column(String(7))  # Hex color codes
    emoji = Column(String(4))  # Unicode emoji

    # Status flags
    is_archived = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Metadata and tags
    list_metadata = Column(JSON, default=dict)
    tags = Column(JSON, default=list)  # Array of tag strings

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Ownership and sharing
    owner_id = Column(String, nullable=False)
    shared_with = Column(JSON, default=list)  # Array of user IDs

    # Performance optimization - cached counts
    item_count = Column(Integer, default=0, nullable=False)
    completed_count = Column(Integer, default=0, nullable=False)

    # Relationships
    items = relationship("ListItemDB", back_populates="list", cascade="all, delete-orphan")

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_lists_owner_type", "owner_id", "item_type"),
        Index("idx_lists_owner_list_type", "owner_id", "list_type"),
        Index("idx_lists_owner_archived", "owner_id", "is_archived"),
        Index("idx_lists_shared", "shared_with"),  # GIN index for JSON array
        Index("idx_lists_default", "owner_id", "item_type", "is_default"),
        Index("idx_lists_tags", "tags"),  # GIN index for tag search
    )

    def to_domain(self) -> domain.List:
        """Convert to domain model"""
        return domain.List(
            id=self.id,
            name=self.name,
            description=self.description,
            item_type=self.item_type,
            list_type=self.list_type,
            ordering_strategy=self.ordering_strategy,
            color=self.color,
            emoji=self.emoji,
            is_archived=self.is_archived,
            is_default=self.is_default,
            metadata=self.list_metadata or {},
            tags=self.tags or [],
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner_id=self.owner_id,
            shared_with=self.shared_with or [],
            item_count=self.item_count,
            completed_count=self.completed_count,
        )

    @classmethod
    def from_domain(cls, list_obj: domain.List) -> "ListDB":
        """Create from domain model"""
        return cls(
            id=list_obj.id,
            name=list_obj.name,
            description=list_obj.description,
            item_type=list_obj.item_type,
            list_type=list_obj.list_type,
            ordering_strategy=list_obj.ordering_strategy,
            color=list_obj.color,
            emoji=list_obj.emoji,
            is_archived=list_obj.is_archived,
            is_default=list_obj.is_default,
            list_metadata=list_obj.metadata,
            tags=list_obj.tags,
            created_at=list_obj.created_at,
            updated_at=list_obj.updated_at,
            owner_id=list_obj.owner_id,
            shared_with=list_obj.shared_with,
            item_count=getattr(list_obj, "item_count", 0),
            completed_count=getattr(list_obj, "completed_count", 0),
        )


class ListItemDB(Base):
    """Universal ListItem database model - polymorphic relationship"""

    __tablename__ = "list_items"

    # Primary key
    id = Column(String, primary_key=True)

    # Foreign keys
    list_id = Column(String, ForeignKey("lists.id"), nullable=False)
    item_id = Column(String, nullable=False)  # Polymorphic reference
    item_type = Column(String, nullable=False)  # todo, feature, bug, attendee, etc.

    # Position tracking
    position = Column(Integer, default=0, nullable=False)

    # Membership metadata
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    added_by = Column(String, nullable=False)

    # List-specific overrides
    list_priority = Column(String)  # Override item's default priority
    list_due_date = Column(DateTime)  # Override item's default due date
    list_notes = Column(Text, default="")

    # Relationships
    list = relationship("ListDB", back_populates="items")

    # Strategic indexes for many-to-many queries
    __table_args__ = (
        # Ensure unique membership per list-item pair
        Index("idx_unique_list_item", "list_id", "item_id", unique=True),
        # Position-based ordering within lists
        Index("idx_list_item_position", "list_id", "position"),
        # Item-centric queries
        Index("idx_list_item_by_item", "item_id", "item_type"),
        # List-centric queries
        Index("idx_list_item_by_list", "list_id"),
        # User-added tracking
        Index("idx_list_item_added_by", "added_by"),
        Index("idx_list_item_added_at", "added_at"),
        # List-specific overrides
        Index("idx_list_item_priority", "list_id", "list_priority"),
        Index("idx_list_item_due", "list_id", "list_due_date"),
    )

    def to_domain(self) -> domain.ListItem:
        """Convert to domain model"""
        return domain.ListItem(
            id=self.id,
            list_id=self.list_id,
            item_id=self.item_id,
            item_type=self.item_type,
            position=self.position,
            added_at=self.added_at,
            added_by=self.added_by,
            list_priority=self.list_priority,
            list_due_date=self.list_due_date,
            list_notes=self.list_notes,
        )

    @classmethod
    def from_domain(cls, item: domain.ListItem) -> "ListItemDB":
        """Create from domain model"""
        return cls(
            id=item.id,
            list_id=item.list_id,
            item_id=item.item_id,
            item_type=item.item_type,
            position=item.position,
            added_at=item.added_at,
            added_by=item.added_by,
            list_priority=item.list_priority,
            list_due_date=item.list_due_date,
            list_notes=item.list_notes,
        )
