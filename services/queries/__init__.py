"""
Query Services - CQRS-lite pattern for read-only operations
"""
from .project_queries import ProjectQueryService
from .query_router import QueryRouter

__all__ = ["ProjectQueryService", "QueryRouter"] 