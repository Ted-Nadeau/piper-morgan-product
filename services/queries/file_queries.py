"""File query service for read-only file operations"""

import logging
from typing import Any, Dict, List, Optional

from services.repositories.file_repository import FileRepository

# Import centralized configuration service
try:
    from services.infrastructure.config.mcp_configuration import get_config

    CONFIG_SERVICE_AVAILABLE = True
except ImportError:
    CONFIG_SERVICE_AVAILABLE = False

logger = logging.getLogger(__name__)


class FileQueryService:
    """Handles read-only file queries"""

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def read_file_contents(self, file_id: str) -> Dict[str, Any]:
        """Read file metadata by ID"""
        file_data = await self.file_repository.get_file_by_id(file_id)

        if not file_data:
            return {"success": False, "error": "File not found"}

        return {"success": True, "file": file_data}

    async def summarize_file(self, file_id: str) -> Dict[str, Any]:
        """Generate a summary of file contents"""
        # Get file metadata
        file_data = await self.file_repository.get_file_by_id(file_id)

        if not file_data:
            return {"success": False, "error": "File not found"}

        # For now, return metadata with a placeholder for actual summary
        return {
            "success": True,
            "file": file_data,
            "summary": f"Summary of {file_data.get('filename', 'unknown file')} would go here. (Not yet implemented - needs file content reading)",
        }

    async def search_files(self, session_id: str, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Enhanced file search with content awareness.
        Uses MCP content search when enabled, falls back to filename search.
        """
        try:
            logger.info(f"Searching files for session {session_id} with query: '{query}'")

            # Use enhanced search method from FileRepository
            # This method handles MCP integration and fallback automatically
            files = await self.file_repository.search_files_with_content(session_id, query, limit)

            logger.info(f"Found {len(files)} files matching query '{query}'")

            # Convert to dict format for API response
            file_results = []
            for file in files:
                file_dict = {
                    "id": file.id,
                    "filename": file.filename,
                    "file_type": file.file_type,
                    "size": file.size,
                    "upload_time": file.upload_time.isoformat() if file.upload_time else None,
                    "last_referenced": (
                        file.last_referenced.isoformat() if file.last_referenced else None
                    ),
                    "reference_count": file.reference_count,
                    "session_id": file.session_id,
                }
                file_results.append(file_dict)

            return {
                "success": True,
                "files": file_results,
                "total_count": len(files),
                "query": query,
                "search_type": "enhanced" if self._is_mcp_enabled() else "filename_only",
            }

        except Exception as e:
            logger.error(f"File search failed for query '{query}': {e}")
            return {"success": False, "error": f"Search failed: {str(e)}", "query": query}

    async def search_files_all_sessions(
        self, query: str, session_id: str, days: int = 30, limit: int = 10
    ) -> Dict[str, Any]:
        """
        Enhanced file search across all sessions (scoped to user) with content awareness.
        Uses MCP content search when enabled, falls back to filename search.
        """
        try:
            logger.info(
                f"Searching files across all sessions for session {session_id} with query: '{query}' (last {days} days)"
            )

            # Use enhanced search method from FileRepository
            # This method handles MCP integration and fallback automatically
            files = await self.file_repository.search_files_with_content_all_sessions(
                query, session_id, days, limit
            )

            logger.info(f"Found {len(files)} files matching query '{query}' across all sessions")

            # Convert to dict format for API response
            file_results = []
            for file in files:
                file_dict = {
                    "id": file.id,
                    "filename": file.filename,
                    "file_type": file.file_type,
                    "size": file.size,
                    "upload_time": file.upload_time.isoformat() if file.upload_time else None,
                    "last_referenced": (
                        file.last_referenced.isoformat() if file.last_referenced else None
                    ),
                    "reference_count": file.reference_count,
                    "session_id": file.session_id,
                }
                file_results.append(file_dict)

            return {
                "success": True,
                "files": file_results,
                "total_count": len(files),
                "query": query,
                "search_type": "enhanced" if self._is_mcp_enabled() else "filename_only",
                "days_searched": days,
            }

        except Exception as e:
            logger.error(f"File search failed for query '{query}': {e}")
            return {"success": False, "error": f"Search failed: {str(e)}", "query": query}

    async def search_files_by_query(
        self, search_query: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search files using natural language query (maps to existing search_files method)"""
        if not session_id:
            return {"success": False, "error": "session_id is required for file search"}

        # Search across all sessions for this user (scoped to session_id/user)
        return await self.search_files_all_sessions(search_query, session_id)

    async def find_documents_about_topic(
        self, topic: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Find documents about a specific topic (alias for search_files_by_query)"""
        logger.info(f"Finding documents about topic: '{topic}'")
        return await self.search_files_by_query(topic, session_id)

    async def search_content_by_query(
        self, content_query: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search file content using natural language query (alias for search_files_by_query)"""
        logger.info(f"Searching content for query: '{content_query}'")
        return await self.search_files_by_query(content_query, session_id)

    def _is_mcp_enabled(self) -> bool:
        """Check if MCP file search is enabled"""
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()
            return config.mcp_enabled
        else:
            # Fallback to direct environment access
            import os

            return os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"
