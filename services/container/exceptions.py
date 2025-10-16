"""Service container exceptions."""


class ContainerError(Exception):
    """Base exception for container errors."""

    pass


class ServiceNotFoundError(ContainerError):
    """Raised when requested service not found in container."""

    def __init__(self, service_name: str, available_services: list = None):
        self.service_name = service_name
        self.available_services = available_services or []

        msg = f"Service '{service_name}' not found in container."
        if self.available_services:
            msg += f" Available services: {', '.join(self.available_services)}"
        else:
            msg += " No services registered."

        super().__init__(msg)


class ContainerNotInitializedError(ContainerError):
    """Raised when attempting to use uninitialized container."""

    def __init__(self):
        super().__init__("Container not initialized. Call container.initialize() first.")


class ServiceInitializationError(ContainerError):
    """Raised when service fails to initialize."""

    def __init__(self, service_name: str, original_error: Exception):
        self.service_name = service_name
        self.original_error = original_error

        super().__init__(f"Failed to initialize service '{service_name}': {original_error}")


class CircularDependencyError(ContainerError):
    """Raised when circular dependency detected."""

    def __init__(self, dependency_chain: list):
        self.dependency_chain = dependency_chain
        chain_str = " -> ".join(dependency_chain)

        super().__init__(f"Circular dependency detected: {chain_str}")
