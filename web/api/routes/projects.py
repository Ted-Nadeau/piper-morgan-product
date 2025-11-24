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
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from web.api.dependencies import get_project_repository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])
logger = structlog.get_logger(__name__)


# Request/Response Models (SEC-RBAC Phase 3)


class ShareProjectRequest(BaseModel):
    """Request model for sharing a project with a user (SEC-RBAC Phase 3)"""

    user_id: str
    role: str = "viewer"  # Default to viewer (read-only) - can be viewer, editor, admin


class UpdateShareRoleRequest(BaseModel):
    """Request model for updating a user's role in a shared project"""

    role: str  # viewer, editor, admin


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


# Share/Unshare Endpoints (SEC-RBAC Phase 3)


@router.post("/{project_id}/share")
async def share_project(
    project_id: str,
    request: ShareProjectRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Share a project with another user at specified role (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project to share
        request: ShareProjectRequest with user_id and role
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Updated project with shared_with information

    Raises:
        HTTPException 403: User is not the project owner
        HTTPException 404: Project not found
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        role = request.role.lower() if request.role else "viewer"
        if role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(role)

        # Share the project
        updated_project = await project_repo.share_project(
            project_id=project_id,
            owner_id=current_user.sub,
            user_to_share_with=request.user_id,
            role=share_role,
        )

        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner to share it",
            )

        logger.info(
            "project_shared",
            project_id=project_id,
            owner_id=current_user.sub,
            shared_with=request.user_id,
            role=role,
        )

        return {
            "status": "shared",
            "project_id": project_id,
            "shared_with": request.user_id,
            "role": role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_share_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share project",
        )


@router.delete("/{project_id}/share/{user_id}")
async def unshare_project(
    project_id: str,
    user_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Remove user from project sharing (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        user_id: User ID to remove from sharing
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Status confirmation

    Raises:
        HTTPException 403: User is not the project owner
        HTTPException 404: Project not found or user not in shared_with
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        success = await project_repo.unshare_project(
            project_id=project_id, owner_id=current_user.sub, user_to_unshare=user_id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner or user is not currently shared",
            )

        logger.info(
            "project_unshared",
            project_id=project_id,
            owner_id=current_user.sub,
            unshared_from=user_id,
        )

        return {
            "status": "unshared",
            "project_id": project_id,
            "removed_user": user_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_unshare_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare project",
        )


@router.put("/{project_id}/share/{user_id}")
async def update_project_share(
    project_id: str,
    user_id: str,
    request: UpdateShareRoleRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Update user's sharing role for a project (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        user_id: User ID to update
        request: UpdateShareRoleRequest with new role
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Updated share information

    Raises:
        HTTPException 400: Invalid role
        HTTPException 403: User is not the project owner
        HTTPException 404: Project or user not found
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        role = request.role.lower() if request.role else "viewer"
        if role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(role)

        # Update the role
        success = await project_repo.update_share_role(
            project_id=project_id,
            owner_id=current_user.sub,
            target_user_id=user_id,
            new_role=share_role,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner or user is not currently shared",
            )

        logger.info(
            "project_share_role_updated",
            project_id=project_id,
            owner_id=current_user.sub,
            user_id=user_id,
            new_role=role,
        )

        return {
            "status": "role_updated",
            "project_id": project_id,
            "user_id": user_id,
            "new_role": role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_share_role_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update sharing role",
        )


@router.get("/{project_id}/my-role")
async def get_my_project_role(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Get current user's role for a project (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        User's role (owner/admin/editor/viewer) or None if no access

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        role = await project_repo.get_user_role(project_id=project_id, user_id=current_user.sub)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you do not have access",
            )

        logger.info(
            "get_project_role",
            project_id=project_id,
            user_id=current_user.sub,
            role=role.value,
        )

        return {
            "project_id": project_id,
            "user_id": current_user.sub,
            "role": role.value,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "get_project_role_error",
            project_id=project_id,
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get project role",
        )
