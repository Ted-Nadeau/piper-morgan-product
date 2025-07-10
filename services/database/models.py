"""
Database Models
SQLAlchemy models for persistent storage
"""

import enum
from datetime import datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, Enum, Float,
                        ForeignKey, Index, Integer, String, Text)
from sqlalchemy.orm import relationship

import services.domain.models as domain
from services.shared_types import (IntegrationType, IntentCategory, TaskStatus,
                                   TaskType, WorkflowStatus, WorkflowType)

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
    status = Column(String, default="open")
    priority = Column(String, default="medium")

    # External system references
    external_refs = Column(JSON)  # {"github": "issue-123", "jira": "PROJ-456"}

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="work_items")
    feature = relationship("Feature", back_populates="work_items")


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
    error = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

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
    type = Column(Enum(TaskType))
    status = Column(Enum(TaskStatus))
    input_data = Column(JSON)
    output_data = Column(JSON)
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
        project.integrations = [
            integration.to_domain() for integration in self.integrations
        ]
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
    last_referenced = Column(DateTime)
    reference_count = Column(Integer, default=0)
    file_metadata = Column(JSON, default=dict)

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
            metadata=self.file_metadata or {},
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
            file_metadata=file.metadata,
        )
