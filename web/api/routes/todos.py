"""
Todo Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides todo CRUD endpoints with ownership validation:
- Create, read, update, delete todos
- Todo filtering by owner
- User-isolated todo access
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from web.api.dependencies import get_todo_repository

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])
logger = structlog.get_logger(__name__)


# Pydantic models for sharing operations
class ShareTodoRequest(BaseModel):
    """Request model for sharing a todo with a user"""

    user_id: str


class ShareTodoResponse(BaseModel):
    """Response model for sharing operations"""

    id: str
    title: str
    owner_id: str
    shared_with: List[str]
    message: str


class SharedTodosResponse(BaseModel):
    """Response model for shared todos"""

    todos: List[dict]
    count: int


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


@router.post("/{todo_id}/share")
async def share_todo(
    todo_id: str,
    request: ShareTodoRequest,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> ShareTodoResponse:
    """
    Share a todo with another user (owner only - SEC-RBAC Phase 1.4).

    Grants read-only access to the specified user. Only the owner can share.

    Args:
        todo_id: ID of the todo to share
        request: ShareTodoRequest with user_id to share with
        current_user: Current authenticated user (must be owner)
        todo_repo: Todo repository (injected)

    Returns:
        Updated todo with shared_with array

    Raises:
        HTTPException 400: Invalid user_id
        HTTPException 404: Todo not found or user not owner
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        if not request.user_id or not request.user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required",
            )

        # Share todo (owner-only operation)
        shared_todo = await todo_repo.share_todo(todo_id, current_user.sub, request.user_id)

        if not shared_todo:
            logger.warning(
                "todo_share_unauthorized",
                user_id=current_user.sub,
                todo_id=todo_id,
                target_user=request.user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or you don't have permission to share it",
            )

        logger.info(
            "todo_shared",
            owner_id=current_user.sub,
            todo_id=todo_id,
            shared_with_user=request.user_id,
        )

        return ShareTodoResponse(
            id=shared_todo.id,
            title=shared_todo.title,
            owner_id=shared_todo.owner_id,
            shared_with=shared_todo.shared_with,
            message=f"Todo shared with user {request.user_id}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_share_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share todo",
        )


@router.delete("/{todo_id}/share/{user_id}")
async def unshare_todo(
    todo_id: str,
    user_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Remove sharing access from a todo (owner only - SEC-RBAC Phase 1.4).

    Revokes read access for the specified user.

    Args:
        todo_id: ID of the todo to unshare
        user_id: ID of user to remove from shared_with
        current_user: Current authenticated user (must be owner)
        todo_repo: Todo repository (injected)

    Returns:
        Success status

    Raises:
        HTTPException 404: Todo not found or user not owner
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        # Unshare todo (owner-only operation)
        unshared_todo = await todo_repo.unshare_todo(todo_id, current_user.sub, user_id)

        if not unshared_todo:
            logger.warning(
                "todo_unshare_unauthorized",
                user_id=current_user.sub,
                todo_id=todo_id,
                unshare_from_user=user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or you don't have permission to unshare it",
            )

        logger.info(
            "todo_unshared",
            owner_id=current_user.sub,
            todo_id=todo_id,
            unshared_from_user=user_id,
        )

        return {
            "success": True,
            "message": f"User {user_id} no longer has access to this todo",
            "todo_id": todo_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_unshare_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare todo",
        )


@router.get("/shared-with-me")
async def get_shared_todos(
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> SharedTodosResponse:
    """
    Get todos shared with the current user (SEC-RBAC Phase 1.4).

    Returns all todos where the current user is in the shared_with array.
    Does not include todos owned by the current user (see GET / for owned todos).

    Args:
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        List of todos shared with this user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        shared_todos = await todo_repo.get_todos_shared_with_me(current_user.sub)

        logger.info(
            "shared_todos_retrieved",
            user_id=current_user.sub,
            count=len(shared_todos),
        )

        return SharedTodosResponse(
            todos=[
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "owner_id": t.owner_id,
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in shared_todos
            ],
            count=len(shared_todos),
        )

    except Exception as e:
        logger.error(
            "shared_todos_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve shared todos",
        )
