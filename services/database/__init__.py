"""
Database Service
Handles data persistence and retrieval
"""

from .connection import Base, db
from .models import (
    Feature,
    Intent,
    Product,
    ProjectDB,
    ProjectIntegrationDB,
    Stakeholder,
    Task,
    Workflow,
    WorkItem,
)
from .repositories import (
    FeatureRepository,
    ProductRepository,
    ProjectIntegrationRepository,
    ProjectRepository,
    RepositoryFactory,
    TaskRepository,
    WorkflowRepository,
    WorkItemRepository,
)

__all__ = [
    # Connection
    "db",
    "Base",
    # Models
    "Product",
    "Feature",
    "WorkItem",
    "Intent",
    "Workflow",
    "Task",
    "Stakeholder",
    "ProjectDB",
    "ProjectIntegrationDB",
    # Repositories
    "ProductRepository",
    "FeatureRepository",
    "WorkItemRepository",
    "WorkflowRepository",
    "TaskRepository",
    "ProjectRepository",
    "ProjectIntegrationRepository",
    "RepositoryFactory",
]
