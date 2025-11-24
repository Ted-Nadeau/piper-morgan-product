"""
Dependency injection providers for FastAPI routes.

Provides reusable dependency injection functions for repositories and services
used across multiple endpoints. Following FastAPI best practices with Depends().
"""

from fastapi import Request

from services.database.repositories import ProjectRepository
from services.feedback.feedback_service import FeedbackService
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.repositories.file_repository import FileRepository
from services.repositories.todo_repository import TodoListRepository
from services.repositories.universal_list_repository import UniversalListRepository


async def get_file_repository(request: Request) -> FileRepository:
    """Dependency injection for FileRepository.

    Provides FileRepository with database session for file operations.
    Database session is stored in request.state.db by middleware.
    """
    return FileRepository(request.state.db)


async def get_list_repository(request: Request) -> UniversalListRepository:
    """Dependency injection for UniversalListRepository.

    Provides UniversalListRepository with database session for list operations.
    Database session is stored in request.state.db by middleware.
    """
    return UniversalListRepository(request.state.db)


async def get_todo_repository(request: Request) -> TodoListRepository:
    """Dependency injection for TodoListRepository.

    Provides TodoListRepository with database session for todo operations.
    Database session is stored in request.state.db by middleware.
    """
    return TodoListRepository(request.state.db)


async def get_knowledge_graph_service(request: Request) -> KnowledgeGraphService:
    """Dependency injection for KnowledgeGraphService.

    Provides KnowledgeGraphService with database session for knowledge graph operations.
    Database session is stored in request.state.db by middleware.
    """
    return KnowledgeGraphService(request.state.db)


async def get_project_repository(request: Request) -> ProjectRepository:
    """Dependency injection for ProjectRepository.

    Provides ProjectRepository with database session for project operations.
    Database session is stored in request.state.db by middleware.
    """
    return ProjectRepository(request.state.db)


async def get_feedback_service(request: Request) -> FeedbackService:
    """Dependency injection for FeedbackService.

    Provides FeedbackService with database session for feedback operations.
    Database session is stored in request.state.db by middleware.
    """
    return FeedbackService(request.state.db)
