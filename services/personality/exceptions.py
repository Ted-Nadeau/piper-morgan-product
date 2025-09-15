"""
Domain-specific exceptions for personality enhancement
"""


class PersonalityEnhancementError(Exception):
    """Base exception for personality enhancement failures"""

    def __init__(self, message: str, service: str = None, suggestion: str = None):
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)


class ProfileLoadError(PersonalityEnhancementError):
    """Raised when personality profile cannot be loaded"""

    pass


class TransformationError(PersonalityEnhancementError):
    """Raised when content transformation fails"""

    pass


class PerformanceTimeoutError(PersonalityEnhancementError):
    """Raised when enhancement exceeds performance budget"""

    pass


class ConfigurationError(PersonalityEnhancementError):
    """Raised when PIPER.user.md configuration is invalid"""

    pass


class CacheError(PersonalityEnhancementError):
    """Raised when profile caching fails"""

    pass
