"""
Project Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides project CRUD endpoints with ownership validation:
- Create, read, update, delete projects
- Project filtering by owner
- User-isolated project access
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from web.api.dependencies import get_project_repository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])
logger = structlog.get_logger(__name__)


@router.post("")
async def create_project(
    name: str,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Create a new project with ownership validation (SEC-RBAC).

    Args:
        name: Project name
        description: Optional project description
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Created project with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name is required",
            )

        # Create project with ownership
        new_project = domain.Project(
            name=name,
            description=description or "",
            owner_id=current_user.sub,
        )

        created_project = await project_repo.create_project(new_project)

        logger.info(
            "project_created",
            user_id=current_user.sub,
            project_id=created_project.id,
            name=name,
        )

        return {
            "id": created_project.id,
            "name": created_project.name,
            "description": created_project.description,
            "owner_id": created_project.owner_id,
            "created_at": (
                created_project.created_at.isoformat() if created_project.created_at else None
            ),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project",
        )


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Get project by ID with ownership validation (SEC-RBAC).

    Only returns project if current user is the owner.

    Args:
        project_id: Project ID to retrieve
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Project metadata (if owned by current user)

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        project_obj = await project_repo.get_project_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        logger.info(
            "project_retrieved",
            user_id=current_user.sub,
            project_id=project_id,
        )

        return {
            "id": project_obj.id,
            "name": project_obj.name,
            "description": project_obj.description,
            "owner_id": project_obj.owner_id,
            "created_at": project_obj.created_at.isoformat() if project_obj.created_at else None,
            "updated_at": project_obj.updated_at.isoformat() if project_obj.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_get_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project",
        )


@router.get("")
async def list_projects(
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    List all projects owned by current user (SEC-RBAC).

    Returns:
        List of projects owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        projects = await project_repo.get_projects_by_owner(current_user.sub)

        logger.info(
            "projects_retrieved",
            user_id=current_user.sub,
            count=len(projects),
        )

        return {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "owner_id": p.owner_id,
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                }
                for p in projects
            ],
            "count": len(projects),
        }

    except Exception as e:
        logger.error(
            "projects_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects",
        )


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Update project with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        project_id: Project ID to update
        name: New project name (optional)
        description: New project description (optional)
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Updated project

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        project_obj = await project_repo.get_project_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        # Update fields
        if name is not None:
            if not name.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project name cannot be empty",
                )
            project_obj.name = name

        if description is not None:
            project_obj.description = description

        updated = await project_repo.update_project(project_obj)

        logger.info(
            "project_updated",
            user_id=current_user.sub,
            project_id=project_id,
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
            "project_update_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project",
        )


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Delete project with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        project_id: Project ID to delete
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        project_obj = await project_repo.get_project_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        await project_repo.delete_project(project_id, owner_id=current_user.sub)

        logger.info(
            "project_deleted",
            user_id=current_user.sub,
            project_id=project_id,
        )

        return {
            "status": "deleted",
            "project_id": project_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_delete_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project",
        )
