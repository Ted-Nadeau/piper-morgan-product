# services/project_context/__init__.py
"""
Project Context Service for PM-009
Centralizes project resolution and context management
"""

from .project_context import ProjectContext, AmbiguousProjectError

# Add the missing exception that tests expect:
class ProjectNotFoundError(Exception):
    """Raised when a project ID is not found"""
    pass