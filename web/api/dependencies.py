"""
Dependency injection providers for FastAPI routes.

Provides reusable dependency injection functions for repositories and services
used across multiple endpoints. Following FastAPI best practices with Depends().

Issue #469: Fixed to use AsyncSessionFactory instead of non-existent request.state.db.
The original implementation expected middleware to set request.state.db, but that
middleware was never created. Now uses async generators with session_scope_fresh()
for proper session lifecycle management.
"""

from typing import AsyncGenerator

from services.database.repositories import ProjectRepository
from services.database.session_factory import AsyncSessionFactory
from services.feedback.feedback_service import FeedbackService
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.repositories.file_repository import FileRepository
from services.repositories.todo_repository import TodoListRepository
from services.repositories.universal_list_repository import UniversalListRepository


async def get_file_repository() -> AsyncGenerator[FileRepository, None]:
    """Dependency injection for FileRepository.

    Provides FileRepository with database session for file operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield FileRepository(session)


async def get_list_repository() -> AsyncGenerator[UniversalListRepository, None]:
    """Dependency injection for UniversalListRepository.

    Provides UniversalListRepository with database session for list operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield UniversalListRepository(session)


async def get_todo_repository() -> AsyncGenerator[TodoListRepository, None]:
    """Dependency injection for TodoListRepository.

    Provides TodoListRepository with database session for todo operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield TodoListRepository(session)


async def get_knowledge_graph_service() -> AsyncGenerator[KnowledgeGraphService, None]:
    """Dependency injection for KnowledgeGraphService.

    Provides KnowledgeGraphService with database session for knowledge graph operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield KnowledgeGraphService(session)


async def get_project_repository() -> AsyncGenerator[ProjectRepository, None]:
    """Dependency injection for ProjectRepository.

    Provides ProjectRepository with database session for project operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield ProjectRepository(session)


async def get_feedback_service() -> AsyncGenerator[FeedbackService, None]:
    """Dependency injection for FeedbackService.

    Provides FeedbackService with database session for feedback operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield FeedbackService(session)
