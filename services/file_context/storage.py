import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

async def save_file_to_storage(file: Union[UploadFile, bytes], filename: Optional[str] = None) -> str:
    """Save uploaded file and return storage path"""
    try:
        # Create upload directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Generate unique filename to avoid collisions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if isinstance(file, UploadFile):
            # Handle UploadFile object
            safe_filename = f"{timestamp}_{file.filename}"
            content = await file.read()
        else:
            # Handle bytes content
            safe_filename = f"{timestamp}_{filename or 'uploaded_file'}"
            content = file
        
        file_path = upload_dir / safe_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File saved to storage: {file_path}")
        return str(file_path)
        
    except Exception as e:
        logger.error(f"Failed to save file to storage: {e}")
        raise

def delete_file_from_storage(storage_path: str) -> bool:
    """Delete file from storage"""
    try:
        file_path = Path(storage_path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"File deleted from storage: {storage_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file from storage: {e}")
        return False

def get_file_size(storage_path: str) -> int:
    """Get file size in bytes"""
    try:
        file_path = Path(storage_path)
        if file_path.exists():
            return file_path.stat().st_size
        return 0
    except Exception as e:
        logger.error(f"Failed to get file size: {e}")
        return 0

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}" 