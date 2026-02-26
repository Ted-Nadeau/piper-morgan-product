"""
Domain Layer
Pure business logic and domain models for Piper Morgan
"""

from .models import (  # Core Entities; PM-009: Project Management; Workflow & Intent; Events
    Event,
    Feature,
    FeatureCreated,
    InsightGenerated,
    Intent,
    Product,
    Project,
    ProjectIntegration,
    ProjectRepositoryLink,
    Repository,
    Stakeholder,
    Task,
    Workflow,
    WorkflowResult,
    WorkItem,
)

__all__ = [
    # Core Entities
    "Product",
    "Feature",
    "Stakeholder",
    "WorkItem",
    # PM-009: Project Management
    "Project",
    "ProjectIntegration",
    # #866: Repository as first-class entity
    "Repository",
    "ProjectRepositoryLink",
    # Workflow & Intent
    "Intent",
    "Task",
    "Workflow",
    "WorkflowResult",
    # Events
    "Event",
    "FeatureCreated",
    "InsightGenerated",
]
