"""
FileRepository implementation using SQLAlchemy AsyncSession
Following Pattern #1: Repository Pattern from pattern-catalog.md
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import UploadedFileDB
from services.database.repositories import BaseRepository
from services.domain.models import UploadedFile
from services.infrastructure.config.feature_flags import FeatureFlags

# Import centralized configuration service
try:
    from services.infrastructure.config.mcp_configuration import get_config

    CONFIG_SERVICE_AVAILABLE = True
except ImportError:
    CONFIG_SERVICE_AVAILABLE = False

logger = logging.getLogger(__name__)


class FileRepository(BaseRepository):
    """Repository for file metadata operations using SQLAlchemy"""

    model = UploadedFileDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def save_file_metadata(self, file: UploadedFile) -> UploadedFile:
        """Save file metadata to database"""
        # Convert domain model to DB model
        db_file = UploadedFileDB.from_domain(file)

        # Add to session - transaction managed by caller
        self.session.add(db_file)
        await self.session.flush()
        await self.session.refresh(db_file)

        # Convert back to domain model
        return db_file.to_domain()

    async def get_file_by_id(self, file_id: str) -> Optional[UploadedFile]:
        """Get file by ID"""
        result = await self.session.execute(
            select(UploadedFileDB).where(UploadedFileDB.id == file_id)
        )
        db_file = result.scalar_one_or_none()
        return db_file.to_domain() if db_file else None

    async def get_files_for_session(self, session_id: str, limit: int = 10) -> List[UploadedFile]:
        """Get files for a session, ordered by upload time (most recent first)"""
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(UploadedFileDB.session_id == session_id)
            .order_by(UploadedFileDB.upload_time.desc())
            .limit(limit)
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def increment_reference_count(self, file_id: str):
        """Increment reference count and update last_referenced timestamp"""
        await self.session.execute(
            update(UploadedFileDB)
            .where(UploadedFileDB.id == file_id)
            .values(
                reference_count=UploadedFileDB.reference_count + 1,
                last_referenced=datetime.now(),
            )
        )

    async def search_files_by_name(self, session_id: str, query: str) -> List[UploadedFile]:
        """Search files by name within a session (case-insensitive partial match)"""
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.session_id == session_id,
                    UploadedFileDB.filename.ilike(f"%{query}%"),
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def get_recent_files(self, session_id: str, hours: int = 24) -> List[UploadedFile]:
        """Get files uploaded within the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.session_id == session_id,
                    UploadedFileDB.upload_time > cutoff_time,
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def search_files_by_name_all_sessions(
        self, query: str, days: int = 30
    ) -> List[UploadedFile]:
        """Search files by name across all sessions within the last N days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.filename.ilike(f"%{query}%"),
                    UploadedFileDB.upload_time > cutoff_time,
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def get_recent_files_all_sessions(self, days: int = 7) -> List[UploadedFile]:
        """Get files uploaded across all sessions within the last N days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(UploadedFileDB.upload_time > cutoff_time)
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def delete_file(self, file_id: str) -> bool:
        """Delete file metadata by ID"""
        result = await self.session.execute(
            select(UploadedFileDB).where(UploadedFileDB.id == file_id)
        )
        db_file = result.scalar_one_or_none()

        if db_file:
            await self.session.delete(db_file)
            return True
        return False

    async def search_files_with_content(
        self, session_id: str, query: str, limit: int = 10
    ) -> List[UploadedFile]:
        """
        Enhanced search combining filename and content search.
        Falls back to filename-only search if MCP is disabled.
        """
        logger.info(f"Searching files with content for session {session_id}, query: {query}")

        # Get files matching by filename first (always available)
        filename_matches = await self.search_files_by_name(session_id, query)

        # Check if MCP content search is enabled using infrastructure feature flags
        mcp_enabled = FeatureFlags.is_mcp_content_search_enabled()

        if not mcp_enabled:
            logger.debug("MCP content search disabled, returning filename matches only")
            return filename_matches[:limit]

        # Import MCP components only if enabled to avoid import errors
        try:
            from services.mcp.resources import MCPResourceManager

            # Initialize MCP resource manager
            mcp_manager = MCPResourceManager()
            mcp_initialized = await mcp_manager.initialize(enabled=True)

            if not mcp_initialized:
                logger.warning("MCP initialization failed, falling back to filename search")
                return filename_matches[:limit]

            # Perform MCP content search
            mcp_results = await mcp_manager.enhanced_file_search(query)

            # Convert MCP results to UploadedFile objects by matching file_id
            content_matches = []
            for mcp_result in mcp_results:
                # Find corresponding file in database
                db_file = await self.get_file_by_id(mcp_result.file_id)
                if db_file and db_file.session_id == session_id:
                    content_matches.append(db_file)

            # Combine results: content matches first, then filename matches
            # Remove duplicates while preserving order
            seen_ids = set()
            combined_results = []

            # Add content matches first (higher priority)
            for file in content_matches:
                if file.id not in seen_ids:
                    combined_results.append(file)
                    seen_ids.add(file.id)

            # Add filename matches that aren't already included
            for file in filename_matches:
                if file.id not in seen_ids:
                    combined_results.append(file)
                    seen_ids.add(file.id)

            # Clean up MCP resources
            await mcp_manager.cleanup()

            logger.info(f"Combined search returned {len(combined_results)} results")
            return combined_results[:limit]

        except Exception as e:
            logger.error(f"MCP content search failed: {e}, falling back to filename search")
            return filename_matches[:limit]

    async def search_files_with_content_all_sessions(
        self, query: str, days: int = 30, limit: int = 10
    ) -> List[UploadedFile]:
        """
        Enhanced search across all sessions combining filename and content search.
        Falls back to filename-only search if MCP is disabled.
        """
        logger.info(f"Searching files with content across all sessions, query: {query}")

        # Get files matching by filename first (always available)
        filename_matches = await self.search_files_by_name_all_sessions(query, days)

        # Check if MCP content search is enabled using infrastructure feature flags
        mcp_enabled = FeatureFlags.is_mcp_content_search_enabled()

        if not mcp_enabled:
            logger.debug("MCP content search disabled, returning filename matches only")
            return filename_matches[:limit]

        # Import MCP components only if enabled to avoid import errors
        try:
            from services.mcp.resources import MCPResourceManager

            # Initialize MCP resource manager
            mcp_manager = MCPResourceManager()
            mcp_initialized = await mcp_manager.initialize(enabled=True)

            if not mcp_initialized:
                logger.warning("MCP initialization failed, falling back to filename search")
                return filename_matches[:limit]

            # Perform MCP content search
            mcp_results = await mcp_manager.enhanced_file_search(query)

            # Convert MCP results to UploadedFile objects by matching file_id
            # Filter by time cutoff
            cutoff_time = datetime.now() - timedelta(days=days)
            content_matches = []
            for mcp_result in mcp_results:
                # Find corresponding file in database
                db_file = await self.get_file_by_id(mcp_result.file_id)
                if db_file and db_file.upload_time > cutoff_time:
                    content_matches.append(db_file)

            # Combine results: content matches first, then filename matches
            # Remove duplicates while preserving order
            seen_ids = set()
            combined_results = []

            # Add content matches first (higher priority)
            for file in content_matches:
                if file.id not in seen_ids:
                    combined_results.append(file)
                    seen_ids.add(file.id)

            # Add filename matches that aren't already included
            for file in filename_matches:
                if file.id not in seen_ids:
                    combined_results.append(file)
                    seen_ids.add(file.id)

            # Clean up MCP resources
            await mcp_manager.cleanup()

            logger.info(f"Combined search returned {len(combined_results)} results")
            return combined_results[:limit]

        except Exception as e:
            logger.error(f"MCP content search failed: {e}, falling back to filename search")
            return filename_matches[:limit]
