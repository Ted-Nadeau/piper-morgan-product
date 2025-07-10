import json
from datetime import datetime, timedelta
from typing import List, Optional

import asyncpg

from services.domain.models import UploadedFile


class FileRepository:
    """Repository for file metadata operations"""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def save_file_metadata(self, file: UploadedFile) -> UploadedFile:
        """Save file metadata to database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO uploaded_files (
                    id, session_id, filename, file_type, file_size,
                    storage_path, upload_time, last_referenced,
                    reference_count, file_metadata
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (id) DO UPDATE SET
                    session_id = $2, filename = $3, file_type = $4,
                    file_size = $5, storage_path = $6, upload_time = $7,
                    last_referenced = $8, reference_count = $9, file_metadata = $10
            """,
                file.id,
                file.session_id,
                file.filename,
                file.file_type,
                file.file_size,
                file.storage_path,
                file.upload_time,
                file.last_referenced,
                file.reference_count,
                json.dumps(file.metadata),
            )
        return file

    async def get_file_by_id(self, file_id: str) -> Optional[UploadedFile]:
        """Get file by ID"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM uploaded_files WHERE id = $1", file_id
            )
            if row:
                return self._row_to_file(row)
        return None

    async def get_files_for_session(
        self, session_id: str, limit: int = 10
    ) -> List[UploadedFile]:
        """Get files for a session, ordered by upload time (most recent first)"""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM uploaded_files
                WHERE session_id = $1
                ORDER BY upload_time DESC
                LIMIT $2
            """,
                session_id,
                limit,
            )
            return [self._row_to_file(row) for row in rows]

    async def increment_reference_count(self, file_id: str):
        """Increment reference count and update last_referenced timestamp"""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE uploaded_files
                SET reference_count = reference_count + 1,
                    last_referenced = $2
                WHERE id = $1
            """,
                file_id,
                datetime.now(),
            )

    async def search_files_by_name(
        self, session_id: str, query: str
    ) -> List[UploadedFile]:
        """Search files by name within a session (case-insensitive partial match)"""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM uploaded_files
                WHERE session_id = $1 AND filename ILIKE $2
                ORDER BY upload_time DESC
            """,
                session_id,
                f"%{query}%",
            )
            return [self._row_to_file(row) for row in rows]

    async def get_recent_files(
        self, session_id: str, hours: int = 24
    ) -> List[UploadedFile]:
        """Get files uploaded within the last N hours"""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM uploaded_files
                WHERE session_id = $1 AND upload_time > $2
                ORDER BY upload_time DESC
            """,
                session_id,
                datetime.now() - timedelta(hours=hours),
            )
            return [self._row_to_file(row) for row in rows]

    async def search_files_by_name_all_sessions(
        self, query: str, days: int = 30
    ) -> List[UploadedFile]:
        """Search files by name across all sessions within the last N days"""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM uploaded_files
                WHERE filename ILIKE $1 AND upload_time > $2
                ORDER BY upload_time DESC
            """,
                f"%{query}%",
                datetime.now() - timedelta(days=days),
            )
            return [self._row_to_file(row) for row in rows]

    async def get_recent_files_all_sessions(self, days: int = 7) -> List[UploadedFile]:
        """Get files uploaded across all sessions within the last N days"""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM uploaded_files
                WHERE upload_time > $1
                ORDER BY upload_time DESC
            """,
                datetime.now() - timedelta(days=days),
            )
            return [self._row_to_file(row) for row in rows]

    async def delete_file(self, file_id: str) -> bool:
        """Delete file metadata by ID"""
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM uploaded_files WHERE id = $1", file_id
            )
            return result == "DELETE 1"

    def _row_to_file(self, row) -> UploadedFile:
        """Convert database row to UploadedFile object"""
        return UploadedFile(
            id=row["id"],
            session_id=row["session_id"],
            filename=row["filename"],
            file_type=row["file_type"],
            file_size=row["file_size"],
            storage_path=row["storage_path"],
            upload_time=row["upload_time"],
            last_referenced=row["last_referenced"],
            reference_count=row["reference_count"],
            metadata=json.loads(row["file_metadata"]) if row["file_metadata"] else {},
        )
