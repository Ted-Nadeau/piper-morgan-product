"""
File Upload API Routes (Issue #282: CORE-ALPHA-FILE-UPLOAD)

Provides file upload endpoint with:
- User-isolated file storage
- File validation (size, type)
- Database metadata tracking
- Progress indication support
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.connection import db
from services.database.models import UploadedFileDB
from services.file_context.storage import save_file_to_storage

router = APIRouter(prefix="/api/v1/files", tags=["files"])
logger = structlog.get_logger(__name__)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/markdown",
    "application/json",
}
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx", ".md", ".json"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Upload a file with validation and user isolation.

    Security:
    - Max 10MB file size
    - Allowed types: text, PDF, Word, Markdown, JSON
    - User-isolated storage
    - Proper error handling

    Args:
        file: Uploaded file
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with file_id, filename, size, and metadata

    Raises:
        HTTPException 413: File too large (>10MB)
        HTTPException 415: Unsupported file type
        HTTPException 500: Server error during upload

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # 1. Validate file exists
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is required",
            )

        # 2. Read file content
        file_content = await file.read()

        # 3. Validate file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            logger.warning(
                "file_too_large",
                user_id=current_user.sub,
                filename=file.filename,
                size=file_size,
                max_size=MAX_FILE_SIZE,
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large: {file_size} bytes (max {MAX_FILE_SIZE})",
            )

        # 4. Validate file type (MIME type)
        if file.content_type not in ALLOWED_MIME_TYPES:
            logger.warning(
                "file_type_not_allowed",
                user_id=current_user.sub,
                filename=file.filename,
                content_type=file.content_type,
            )
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}",
            )

        # 5. Validate file extension
        file_path = Path(file.filename)
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            logger.warning(
                "file_extension_not_allowed",
                user_id=current_user.sub,
                filename=file.filename,
                extension=file_path.suffix,
            )
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file extension: {file_path.suffix}. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # 6. Create user-isolated directory
        upload_dir = Path("uploads") / current_user.sub
        upload_dir.mkdir(parents=True, exist_ok=True)

        # 7. Generate unique file ID and safe filename
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file_id}_{file.filename}"
        safe_file_path = upload_dir / safe_filename

        # 8. Save file to disk
        try:
            with open(safe_file_path, "wb") as f:
                f.write(file_content)

            logger.info(
                "file_saved_to_disk",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                path=str(safe_file_path),
                size=file_size,
            )
        except IOError as e:
            logger.error(
                "file_save_failed",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                error=str(e),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file to storage",
            )

        # 9. Store metadata in database
        try:
            # Initialize database if needed
            if not db._initialized:
                await db.initialize()

            # Create database record
            async with await db.get_session() as session:
                uploaded_file = UploadedFileDB(
                    id=file_id,
                    session_id=current_user.sub,  # Use user ID as session for now
                    filename=file.filename,
                    file_type=file.content_type,
                    file_size=file_size,
                    storage_path=str(safe_file_path),
                    upload_time=datetime.utcnow(),
                    file_metadata={
                        "original_filename": file.filename,
                        "uploaded_by": current_user.sub,
                        "uploaded_at": datetime.utcnow().isoformat(),
                    },
                )

                session.add(uploaded_file)
                await session.commit()

            logger.info(
                "file_metadata_stored",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
            )

        except Exception as e:
            logger.warning(
                "file_metadata_storage_failed",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                error=str(e),
            )
            # File is saved on disk, but metadata storage failed
            # This is not critical - return success but log warning

        # 10. Return response
        response = {
            "file_id": file_id,
            "filename": file.filename,
            "size": file_size,
            "content_type": file.content_type,
            "status": "uploaded",
            "uploaded_at": datetime.utcnow().isoformat(),
            "storage_path": str(safe_file_path),  # For testing/admin only
        }

        logger.info(
            "file_upload_complete",
            user_id=current_user.sub,
            file_id=file_id,
            filename=file.filename,
            size=file_size,
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "file_upload_error",
            user_id=current_user.sub,
            filename=file.filename if file else "unknown",
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        )


@router.get("/list")
async def list_files(
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    List all files uploaded by current user.

    Returns:
        List of files with metadata

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user's files
        async with await db.get_session() as session:
            result = await session.execute(
                select(UploadedFileDB).where(UploadedFileDB.session_id == current_user.sub)
            )
            files = result.scalars().all()

        # Format response
        file_list = [
            {
                "file_id": f.id,
                "filename": f.filename,
                "size": f.file_size,
                "content_type": f.file_type,
                "uploaded_at": f.upload_time.isoformat() if f.upload_time else None,
                "reference_count": f.reference_count,
                "last_referenced": (f.last_referenced.isoformat() if f.last_referenced else None),
            }
            for f in files
        ]

        logger.info(
            "files_listed",
            user_id=current_user.sub,
            count=len(file_list),
        )

        return {
            "files": file_list,
            "count": len(file_list),
        }

    except Exception as e:
        logger.error(
            "file_list_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list files",
        )


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Delete a file uploaded by current user.

    Args:
        file_id: File ID to delete
        current_user: Current authenticated user

    Returns:
        Success message

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Find file
        async with await db.get_session() as session:
            result = await session.execute(
                select(UploadedFileDB).where(
                    UploadedFileDB.id == file_id,
                    UploadedFileDB.session_id == current_user.sub,
                )
            )
            file = result.scalar_one_or_none()

            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File not found: {file_id}",
                )

            # Delete from storage
            file_path = Path(file.storage_path)
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(
                        "file_deleted_from_storage",
                        user_id=current_user.sub,
                        file_id=file_id,
                        path=file.storage_path,
                    )
                except OSError as e:
                    logger.warning(
                        "file_delete_from_storage_failed",
                        user_id=current_user.sub,
                        file_id=file_id,
                        path=file.storage_path,
                        error=str(e),
                    )
                    # Continue to delete from database even if file deletion fails

            # Delete from database
            await session.delete(file)
            await session.commit()

            logger.info(
                "file_deleted",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
            )

            return {
                "status": "deleted",
                "file_id": file_id,
                "filename": file.filename,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "file_delete_error",
            user_id=current_user.sub,
            file_id=file_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file",
        )
