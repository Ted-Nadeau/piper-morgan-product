"""
Database Service
Handles data persistence and retrieval
"""
from .connection import db, Base
from .models import Product, Feature, WorkItem, Intent, Workflow, Task, Stakeholder, ProjectDB, ProjectIntegrationDB
from .repositories import (
    ProductRepository,
    FeatureRepository, 
    WorkItemRepository,
    WorkflowRepository,
    TaskRepository,
    ProjectRepository,
    ProjectIntegrationRepository,
    RepositoryFactory
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
    "RepositoryFactory"
]