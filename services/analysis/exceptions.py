"""File analysis exceptions"""

class FileAnalysisError(Exception):
    """Base exception for file analysis errors"""
    pass

class FileValidationError(FileAnalysisError):
    """Raised when file validation fails"""
    pass

class UnsupportedFileTypeError(FileAnalysisError):
    """Raised when file type is not supported"""
    def __init__(self, file_type: str):
        super().__init__(f"Unsupported file type: {file_type}")
        self.file_type = file_type 