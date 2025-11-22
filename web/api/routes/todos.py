"""
Todo Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides todo CRUD endpoints with ownership validation:
- Create, read, update, delete todos
- Todo filtering by owner
- User-isolated todo access
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from web.api.dependencies import get_todo_repository

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])
logger = structlog.get_logger(__name__)


@router.post("")
async def create_todo(
    title: str,
    description: Optional[str] = None,
    status: Optional[str] = "pending",
    priority: Optional[str] = "medium",
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Create a new todo with ownership validation (SEC-RBAC).

    Args:
        title: Todo title
        description: Optional todo description
        status: Todo status (pending, in_progress, completed, etc.)
        priority: Todo priority (low, medium, high, urgent)
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Created todo with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not title or not title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todo title is required",
            )

        # Create todo with ownership
        new_todo = domain.Todo(
            title=title,
            description=description or "",
            status=status or "pending",
            priority=priority or "medium",
            owner_id=current_user.sub,
        )

        created_todo = await todo_repo.create_todo(new_todo)

        logger.info(
            "todo_created",
            user_id=current_user.sub,
            todo_id=created_todo.id,
            title=title,
        )

        return {
            "id": created_todo.id,
            "title": created_todo.title,
            "description": created_todo.description,
            "status": created_todo.status,
            "priority": created_todo.priority,
            "owner_id": created_todo.owner_id,
            "created_at": created_todo.created_at.isoformat() if created_todo.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo",
        )


@router.get("/{todo_id}")
async def get_todo(
    todo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Get todo by ID with ownership validation (SEC-RBAC).

    Only returns todo if current user is the owner.

    Args:
        todo_id: Todo ID to retrieve
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Todo metadata (if owned by current user)

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        logger.info(
            "todo_retrieved",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "id": todo_obj.id,
            "title": todo_obj.title,
            "description": todo_obj.description,
            "status": todo_obj.status,
            "priority": todo_obj.priority,
            "owner_id": todo_obj.owner_id,
            "created_at": todo_obj.created_at.isoformat() if todo_obj.created_at else None,
            "updated_at": todo_obj.updated_at.isoformat() if todo_obj.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_get_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo",
        )


@router.get("")
async def list_todos(
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    List all todos owned by current user (SEC-RBAC).

    Returns:
        List of todos owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        todos = await todo_repo.get_todos_by_owner(current_user.sub)

        logger.info(
            "todos_retrieved",
            user_id=current_user.sub,
            count=len(todos),
        )

        return {
            "todos": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority,
                    "owner_id": t.owner_id,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in todos
            ],
            "count": len(todos),
        }

    except Exception as e:
        logger.error(
            "todos_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todos",
        )


@router.put("/{todo_id}")
async def update_todo(
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Update todo with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        todo_id: Todo ID to update
        title: New todo title (optional)
        description: New todo description (optional)
        status: New todo status (optional)
        priority: New todo priority (optional)
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Updated todo

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        # Update fields
        if title is not None:
            if not title.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Todo title cannot be empty",
                )
            todo_obj.title = title

        if description is not None:
            todo_obj.description = description

        if status is not None:
            todo_obj.status = status

        if priority is not None:
            todo_obj.priority = priority

        updated = await todo_repo.update_todo(todo_obj)

        logger.info(
            "todo_updated",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "id": updated.id,
            "title": updated.title,
            "status": updated.status,
            "priority": updated.priority,
            "owner_id": updated.owner_id,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_update_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo",
        )


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Delete todo with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        todo_id: Todo ID to delete
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        await todo_repo.delete_todo(todo_id, owner_id=current_user.sub)

        logger.info(
            "todo_deleted",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "status": "deleted",
            "todo_id": todo_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_delete_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo",
        )
