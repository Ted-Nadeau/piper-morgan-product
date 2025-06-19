class AmbiguousProjectError(Exception):
    """Raised when project cannot be uniquely determined"""
    pass

class ProjectNotFoundError(Exception):
    """Raised when specified project does not exist"""
    pass 