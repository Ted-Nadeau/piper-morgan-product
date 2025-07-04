"""File query service for read-only file operations"""
from typing import Dict, Any, Optional
from services.repositories.file_repository import FileRepository

class FileQueryService:
    """Handles read-only file queries"""
    
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
    
    async def read_file_contents(self, file_id: str) -> Dict[str, Any]:
        """Read file metadata by ID"""
        file_data = await self.file_repository.get_file_by_id(file_id)
        
        if not file_data:
            return {"success": False, "error": "File not found"}
        
        return {
            "success": True,
            "file": file_data
        } 