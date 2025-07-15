"""
FileRepository implementation using SQLAlchemy AsyncSession
Following Pattern #1: Repository Pattern from pattern-catalog.md
"""

import json
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import UploadedFileDB
from services.database.repositories import BaseRepository
from services.domain.models import UploadedFile


class FileRepository(BaseRepository):
    """Repository for file metadata operations using SQLAlchemy"""

    model = UploadedFileDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def save_file_metadata(self, file: UploadedFile) -> UploadedFile:
        """Save file metadata to database"""
        # Convert domain model to DB model
        db_file = UploadedFileDB.from_domain(file)

        # Use merge to handle both insert and update
        async with self.session.begin():
            self.session.add(db_file)
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
        async with self.session.begin():
            await self.session.execute(
                update(UploadedFileDB)
                .where(UploadedFileDB.id == file_id)
                .values(
                    reference_count=UploadedFileDB.reference_count + 1,
                    last_referenced=datetime.now(),
                )
            )
        await self.session.commit()

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
            async with self.session.begin():
                await self.session.delete(db_file)
            return True
        return False
