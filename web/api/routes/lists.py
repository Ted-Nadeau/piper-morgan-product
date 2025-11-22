"""
List Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides list CRUD endpoints with ownership validation:
- Create, read, update, delete lists
- List filtering by owner
- User-isolated list access
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.models import ListDB
from services.domain import models as domain
from web.api.dependencies import get_list_repository

router = APIRouter(prefix="/api/v1/lists", tags=["lists"])
logger = structlog.get_logger(__name__)


# Pydantic models for sharing operations
class ShareListRequest(BaseModel):
    """Request model for sharing a list with a user"""

    user_id: str


class ShareListResponse(BaseModel):
    """Response model for sharing operations"""

    id: str
    name: str
    owner_id: str
    shared_with: List[str]
    message: str


class SharedListsResponse(BaseModel):
    """Response model for shared lists"""

    lists: List[dict]
    count: int


@router.post("")
async def create_list(
    name: str,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Create a new list with ownership validation (SEC-RBAC).

    Args:
        name: List name
        description: Optional list description
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Created list with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="List name is required",
            )

        # Create list with ownership
        new_list = domain.List(
            name=name,
            description=description or "",
            owner_id=current_user.sub,
        )

        created_list = await list_repo.create_list(new_list)

        logger.info(
            "list_created",
            user_id=current_user.sub,
            list_id=created_list.id,
            name=name,
        )

        return {
            "id": created_list.id,
            "name": created_list.name,
            "description": created_list.description,
            "owner_id": created_list.owner_id,
            "created_at": created_list.created_at.isoformat() if created_list.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create list",
        )


@router.get("/{list_id}")
async def get_list(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Get list by ID with ownership validation (SEC-RBAC).

    Only returns list if current user is the owner.

    Args:
        list_id: List ID to retrieve
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        List metadata (if owned by current user)

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        logger.info(
            "list_retrieved",
            user_id=current_user.sub,
            list_id=list_id,
        )

        return {
            "id": list_obj.id,
            "name": list_obj.name,
            "description": list_obj.description,
            "owner_id": list_obj.owner_id,
            "created_at": list_obj.created_at.isoformat() if list_obj.created_at else None,
            "updated_at": list_obj.updated_at.isoformat() if list_obj.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_get_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve list",
        )


@router.get("")
async def list_lists(
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    List all lists owned by current user (SEC-RBAC).

    Returns:
        List of lists owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        lists = await list_repo.get_lists_by_owner(current_user.sub)

        logger.info(
            "lists_retrieved",
            user_id=current_user.sub,
            count=len(lists),
        )

        return {
            "lists": [
                {
                    "id": list_item.id,
                    "name": list_item.name,
                    "description": list_item.description,
                    "owner_id": list_item.owner_id,
                    "created_at": (
                        list_item.created_at.isoformat() if list_item.created_at else None
                    ),
                }
                for list_item in lists
            ],
            "count": len(lists),
        }

    except Exception as e:
        logger.error(
            "lists_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve lists",
        )


@router.put("/{list_id}")
async def update_list(
    list_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Update list with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        list_id: List ID to update
        name: New list name (optional)
        description: New list description (optional)
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Updated list

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Update fields
        if name is not None:
            if not name.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="List name cannot be empty",
                )
            list_obj.name = name

        if description is not None:
            list_obj.description = description

        updated = await list_repo.update_list(list_obj)

        logger.info(
            "list_updated",
            user_id=current_user.sub,
            list_id=list_id,
        )

        return {
            "id": updated.id,
            "name": updated.name,
            "description": updated.description,
            "owner_id": updated.owner_id,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_update_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update list",
        )


@router.delete("/{list_id}")
async def delete_list(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Delete list with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        list_id: List ID to delete
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        await list_repo.delete_list(list_id, owner_id=current_user.sub)

        logger.info(
            "list_deleted",
            user_id=current_user.sub,
            list_id=list_id,
        )

        return {
            "status": "deleted",
            "list_id": list_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_delete_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete list",
        )
