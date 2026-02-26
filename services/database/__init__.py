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
    ProjectRepositoryLinkDB,
    RepositoryDB,
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
    RepositoryRepository,
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
    "RepositoryDB",
    "ProjectRepositoryLinkDB",
    # Repositories
    "ProductRepository",
    "FeatureRepository",
    "WorkItemRepository",
    "WorkflowRepository",
    "TaskRepository",
    "ProjectRepository",
    "ProjectIntegrationRepository",
    "RepositoryRepository",
    "RepositoryFactory",
]
