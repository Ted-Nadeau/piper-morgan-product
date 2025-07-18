"""MCP-specific exceptions for Piper Morgan integration"""


class MCPError(Exception):
    """Base exception for MCP-related errors"""

    pass


class MCPConnectionError(MCPError):
    """Raised when MCP server connection fails"""

    pass


class MCPTimeoutError(MCPError):
    """Raised when MCP operation times out"""

    pass


class MCPCircuitBreakerOpenError(MCPError):
    """Raised when circuit breaker is open"""

    pass


class MCPResourceNotFoundError(MCPError):
    """Raised when requested MCP resource is not found"""

    pass


class MCPValidationError(MCPError):
    """Raised when MCP request validation fails"""

    pass
