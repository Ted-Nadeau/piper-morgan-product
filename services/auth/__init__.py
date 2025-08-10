"""
Authentication Service Package

JWT-based authentication system with OAuth 2.0 federation readiness.
Provides portable identity management and secure session handling.

Components:
- jwt_service: JWT token generation and validation
- user_service: User identity and context management
- auth_middleware: FastAPI authentication middleware
- oauth_federation: OAuth 2.0 provider federation
- session_manager: Secure session management
- audit_logger: Authentication audit logging
"""

__version__ = "1.0.0"
__author__ = "Piper Morgan Security Team"

from .auth_middleware import AuthMiddleware
from .jwt_service import JWTService
from .user_service import UserService

__all__ = [
    "JWTService",
    "UserService",
    "AuthMiddleware",
]
