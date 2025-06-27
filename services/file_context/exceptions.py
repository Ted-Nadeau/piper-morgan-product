"""Exceptions for file resolution"""

class FileResolutionError(Exception):
    """Base exception for file resolution"""
    pass

class AmbiguousFileReferenceError(FileResolutionError):
    """Multiple files match the reference"""
    def __init__(self, files, scores):
        self.files = files
        self.scores = scores
        file_names = [f.filename for f in files]
        super().__init__(f"Multiple files match: {file_names}")

class NoFilesFoundError(FileResolutionError):
    """No files found for the reference"""
    def __init__(self, session_id: str, reference: str):
        self.session_id = session_id
        self.reference = reference
        super().__init__(f"No files found in session {session_id} matching '{reference}'")

class FileNotFoundError(FileResolutionError):
    """Specific file not found"""
    def __init__(self, file_id: str):
        self.file_id = file_id
        super().__init__(f"File with ID {file_id} not found") 