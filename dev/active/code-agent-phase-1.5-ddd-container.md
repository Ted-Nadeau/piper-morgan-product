# Code Agent Prompt: Phase 1.5 - DDD Service Container Implementation

**Date**: October 16, 2025, 10:30 AM  
**Sprint**: A2 - Notion & Errors (Day 2)  
**Issue**: Foundation fix (enables #215 completion)  
**Phase**: 1.5 - DDD Service Container  
**Duration**: 1.5-2 hours  
**Agent**: Claude Code

---

## Mission

Build proper DDD service container pattern to fix the architectural gap from October 10. This enables proper service initialization and allows us to complete #215 error standardization with a working system.

**Context**: Investigation revealed ServiceRegistry pattern introduced Oct 10 but startup paths broken. main.py registers services but never starts server; uvicorn starts server but never registers services. No proper way to start system!

**Philosophy**: "Fix the foundation properly, then build upon it."

---

## Cathedral View (Read This First!)

**The Big Picture**:
1. **Phase 1.5** (this): Build DDD service container (1.5-2 hrs) ← WE ARE HERE
2. **Phase 2**: Update remaining endpoints (1.5-2 hrs)
3. **Phase 3**: Update tests (45-60 min)
4. **Phase 4**: Documentation (30-45 min)

**Full gameplan**: `dev/active/gameplan-ddd-service-container-215.md`

**Why this order**: Can't test error handling without working services!

---

## What We're Building

### Service Container Architecture

```
services/
├── container/
│   ├── __init__.py                    # Public API
│   ├── service_container.py           # Singleton container
│   ├── service_registry.py            # Registry implementation
│   ├── initialization.py              # Init logic
│   └── exceptions.py                  # Container errors
```

**Key Principles**:
- **Singleton**: One container instance
- **Lifecycle management**: Init in correct order
- **Clean dependencies**: Services get what they need
- **Clear errors**: Know what's wrong when it fails

---

## Step 1: Create Container Structure (10 min)

### Create directory

```bash
mkdir -p services/container
touch services/container/__init__.py
```

### Create exceptions.py

**File**: `services/container/exceptions.py`

```python
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
        super().__init__(
            "Container not initialized. Call container.initialize() first."
        )


class ServiceInitializationError(ContainerError):
    """Raised when service fails to initialize."""
    
    def __init__(self, service_name: str, original_error: Exception):
        self.service_name = service_name
        self.original_error = original_error
        
        super().__init__(
            f"Failed to initialize service '{service_name}': {original_error}"
        )


class CircularDependencyError(ContainerError):
    """Raised when circular dependency detected."""
    
    def __init__(self, dependency_chain: list):
        self.dependency_chain = dependency_chain
        chain_str = " -> ".join(dependency_chain)
        
        super().__init__(
            f"Circular dependency detected: {chain_str}"
        )
```

---

## Step 2: Create ServiceRegistry (15 min)

**File**: `services/container/service_registry.py`

```python
"""Service registry for managing service instances."""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Registry for managing service instances and metadata."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}
        
    def register(
        self,
        name: str,
        service: Any,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Register a service.
        
        Args:
            name: Service name (e.g., 'llm', 'intent')
            service: Service instance
            metadata: Optional metadata (version, dependencies, etc.)
        """
        self._services[name] = service
        self._metadata[name] = metadata or {}
        
        logger.info(
            f"Registered service '{name}' "
            f"(type: {type(service).__name__})"
        )
        
    def get(self, name: str) -> Any:
        """
        Get service by name.
        
        Args:
            name: Service name
            
        Returns:
            Service instance
            
        Raises:
            KeyError: If service not found
        """
        if name not in self._services:
            raise KeyError(
                f"Service '{name}' not found. "
                f"Available: {list(self._services.keys())}"
            )
            
        return self._services[name]
        
    def has(self, name: str) -> bool:
        """Check if service exists."""
        return name in self._services
        
    def list_services(self) -> List[str]:
        """List all registered service names."""
        return list(self._services.keys())
        
    def get_metadata(self, name: str) -> Dict:
        """Get service metadata."""
        return self._metadata.get(name, {})
        
    def clear(self) -> None:
        """Clear all services (for testing/shutdown)."""
        logger.info("Clearing service registry")
        self._services.clear()
        self._metadata.clear()
```

---

## Step 3: Create ServiceContainer (Singleton) (30 min)

**File**: `services/container/service_container.py`

```python
"""Service container with singleton pattern."""

from typing import Any, Optional
import logging

from services.container.service_registry import ServiceRegistry
from services.container.exceptions import (
    ContainerNotInitializedError,
    ServiceNotFoundError
)

logger = logging.getLogger(__name__)


class ServiceContainer:
    """
    Singleton container for service lifecycle management.
    
    Usage:
        # Get container instance
        container = ServiceContainer()
        
        # Initialize (first time only)
        container.initialize()
        
        # Get services
        llm_service = container.get_service('llm')
    """
    
    _instance: Optional['ServiceContainer'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Enforce singleton pattern."""
        if cls._instance is None:
            logger.info("Creating ServiceContainer instance")
            cls._instance = super().__new__(cls)
            cls._instance._registry = ServiceRegistry()
        return cls._instance
    
    def __init__(self):
        """Initialize instance (only once due to singleton)."""
        # Don't reinitialize
        pass
        
    def initialize(self) -> None:
        """
        Initialize all services.
        
        This should be called once at application startup.
        Safe to call multiple times (idempotent).
        """
        if self._initialized:
            logger.info("Container already initialized")
            return
            
        logger.info("Initializing service container")
        
        try:
            # Import here to avoid circular imports
            from services.container.initialization import ServiceInitializer
            
            # Initialize services
            initializer = ServiceInitializer(self._registry)
            initializer.initialize_all()
            
            self._initialized = True
            logger.info(
                f"Container initialized successfully. "
                f"Services: {self._registry.list_services()}"
            )
            
        except Exception as e:
            logger.error(f"Container initialization failed: {e}", exc_info=True)
            raise
            
    def is_initialized(self) -> bool:
        """Check if container is initialized."""
        return self._initialized
        
    def get_service(self, name: str) -> Any:
        """
        Get service by name.
        
        Args:
            name: Service name (e.g., 'llm', 'intent')
            
        Returns:
            Service instance
            
        Raises:
            ContainerNotInitializedError: If container not initialized
            ServiceNotFoundError: If service not found
        """
        if not self._initialized:
            raise ContainerNotInitializedError()
            
        try:
            return self._registry.get(name)
        except KeyError:
            raise ServiceNotFoundError(
                name,
                available_services=self._registry.list_services()
            )
            
    def has_service(self, name: str) -> bool:
        """Check if service exists."""
        if not self._initialized:
            return False
        return self._registry.has(name)
        
    def list_services(self) -> list:
        """List all registered services."""
        if not self._initialized:
            return []
        return self._registry.list_services()
        
    def shutdown(self) -> None:
        """
        Shutdown container and clean up services.
        
        This should be called during application shutdown.
        """
        if not self._initialized:
            return
            
        logger.info("Shutting down service container")
        
        # Could add service-specific shutdown logic here
        # For now, just clear registry
        self._registry.clear()
        
        self._initialized = False
        logger.info("Container shut down successfully")
        
    @classmethod
    def reset(cls) -> None:
        """
        Reset singleton instance (FOR TESTING ONLY).
        
        This allows tests to create fresh containers.
        """
        if cls._instance is not None:
            if cls._instance._initialized:
                cls._instance.shutdown()
            cls._instance = None
            cls._initialized = False
            logger.info("Container reset (testing)")
```

---

## Step 4: Create ServiceInitializer (30 min)

**File**: `services/container/initialization.py`

```python
"""Service initialization logic."""

import logging
import os
from typing import Optional

from services.container.service_registry import ServiceRegistry
from services.container.exceptions import ServiceInitializationError

logger = logging.getLogger(__name__)


class ServiceInitializer:
    """Handles service initialization in correct order."""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        
    def initialize_all(self) -> None:
        """
        Initialize all services in correct dependency order.
        
        Order:
        1. LLM service (no dependencies)
        2. Intent service (depends on LLM)
        3. Other services (as needed)
        """
        logger.info("Starting service initialization sequence")
        
        # Initialize in dependency order
        self._initialize_llm_service()
        self._initialize_intent_service()
        
        logger.info("Service initialization sequence complete")
        
    def _initialize_llm_service(self) -> None:
        """Initialize LLM service."""
        try:
            logger.info("Initializing LLM service")
            
            # Import here to avoid circular imports
            from services.domain.llm.llm_domain_service import LLMDomainService
            from config.user_config_loader import ConfigLoader
            
            # Load config
            config_loader = ConfigLoader()
            config = config_loader.load_config()
            
            # Create LLM service
            llm_service = LLMDomainService(config)
            
            # Register
            self.registry.register(
                'llm',
                llm_service,
                metadata={'version': '1.0', 'dependencies': []}
            )
            
            logger.info("LLM service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}", exc_info=True)
            raise ServiceInitializationError('llm', e)
            
    def _initialize_intent_service(self) -> None:
        """Initialize Intent service (depends on LLM)."""
        try:
            logger.info("Initializing Intent service")
            
            # Import here to avoid circular imports
            from services.integrations.intent.intent_service import IntentService
            
            # Get LLM service dependency
            llm_service = self.registry.get('llm')
            
            # Create Intent service
            # Note: IntentService may need OrchestrationEngine
            # which needs LLM service from registry
            # This should work now!
            intent_service = IntentService()
            
            # Register
            self.registry.register(
                'intent',
                intent_service,
                metadata={'version': '1.0', 'dependencies': ['llm']}
            )
            
            logger.info("Intent service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Intent service: {e}", exc_info=True)
            raise ServiceInitializationError('intent', e)
```

---

## Step 5: Create Public API (5 min)

**File**: `services/container/__init__.py`

```python
"""
Service Container - DDD service lifecycle management.

Usage:
    from services.container import ServiceContainer
    
    # Initialize
    container = ServiceContainer()
    container.initialize()
    
    # Get services
    llm_service = container.get_service('llm')
"""

from services.container.service_container import ServiceContainer
from services.container.exceptions import (
    ContainerError,
    ServiceNotFoundError,
    ContainerNotInitializedError,
    ServiceInitializationError,
    CircularDependencyError
)

__all__ = [
    'ServiceContainer',
    'ContainerError',
    'ServiceNotFoundError',
    'ContainerNotInitializedError',
    'ServiceInitializationError',
    'CircularDependencyError',
]
```

---

## Step 6: Update main.py (10 min)

**Current main.py** needs updating to use container and start uvicorn.

**Find and update**:
```bash
# See what's currently there
cat main.py | head -50
```

**Update to**:
```python
#!/usr/bin/env python3
"""
Piper Morgan - Main Entry Point

This is the proper way to start Piper Morgan.
It initializes services and starts the web server.
"""

import logging
import sys

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    try:
        logger.info("Starting Piper Morgan...")
        
        # Initialize service container
        from services.container import ServiceContainer
        
        container = ServiceContainer()
        logger.info("Initializing services...")
        container.initialize()
        logger.info(f"Services initialized: {container.list_services()}")
        
        # Start web server
        import uvicorn
        
        logger.info("Starting web server on http://127.0.0.1:8001")
        uvicorn.run(
            "web.app:app",
            host="127.0.0.1",
            port=8001,
            reload=False,  # Disable reload (incompatible with initialized services)
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        container = ServiceContainer()
        container.shutdown()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Step 7: Update web/app.py Lifespan (15 min)

**Add lifespan handler** to web/app.py for uvicorn-only startup:

**Find current app creation**:
```bash
grep -n "app = FastAPI" web/app.py
```

**Add before app creation**:
```python
from contextlib import asynccontextmanager
from services.container import ServiceContainer
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """
    Application lifespan handler.
    
    Ensures services are initialized when using uvicorn directly.
    """
    logger.info("Application startup")
    
    # Get or initialize container
    container = ServiceContainer()
    
    if not container.is_initialized():
        logger.info("Container not initialized, initializing now...")
        container.initialize()
    else:
        logger.info("Container already initialized (started via main.py)")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown")
    container.shutdown()
```

**Update app creation**:
```python
# Find this line:
app = FastAPI(...)

# Update to:
app = FastAPI(
    title="Piper Morgan API",
    description="Intelligent PM Assistant",
    version="0.1.0",
    lifespan=lifespan  # Add this!
)
```

---

## Step 8: Write Unit Tests (20 min)

**File**: `tests/services/container/test_service_container.py`

```python
"""Unit tests for ServiceContainer."""

import pytest
from services.container import (
    ServiceContainer,
    ServiceNotFoundError,
    ContainerNotInitializedError
)


class TestServiceContainer:
    """Test ServiceContainer singleton and lifecycle."""
    
    def setup_method(self):
        """Reset container before each test."""
        ServiceContainer.reset()
        
    def test_singleton_pattern(self):
        """Test that ServiceContainer is singleton."""
        container1 = ServiceContainer()
        container2 = ServiceContainer()
        
        assert container1 is container2
        
    def test_not_initialized_by_default(self):
        """Test container not initialized on creation."""
        container = ServiceContainer()
        assert not container.is_initialized()
        
    def test_initialize_idempotent(self):
        """Test initialize can be called multiple times safely."""
        container = ServiceContainer()
        
        container.initialize()
        assert container.is_initialized()
        
        # Call again - should not error
        container.initialize()
        assert container.is_initialized()
        
    def test_get_service_before_init_raises(self):
        """Test getting service before init raises error."""
        container = ServiceContainer()
        
        with pytest.raises(ContainerNotInitializedError):
            container.get_service('llm')
            
    def test_get_nonexistent_service_raises(self):
        """Test getting nonexistent service raises error."""
        container = ServiceContainer()
        container.initialize()
        
        with pytest.raises(ServiceNotFoundError) as exc_info:
            container.get_service('nonexistent')
            
        assert 'nonexistent' in str(exc_info.value)
        assert 'Available services:' in str(exc_info.value)
        
    def test_has_service(self):
        """Test has_service method."""
        container = ServiceContainer()
        
        assert not container.has_service('llm')
        
        container.initialize()
        
        assert container.has_service('llm')
        assert not container.has_service('nonexistent')
        
    def test_list_services(self):
        """Test list_services method."""
        container = ServiceContainer()
        
        assert container.list_services() == []
        
        container.initialize()
        
        services = container.list_services()
        assert 'llm' in services
        assert 'intent' in services
        
    def test_shutdown(self):
        """Test shutdown clears services."""
        container = ServiceContainer()
        container.initialize()
        
        assert container.is_initialized()
        assert len(container.list_services()) > 0
        
        container.shutdown()
        
        assert not container.is_initialized()
        assert container.list_services() == []
        
    def test_reset_for_testing(self):
        """Test reset method (for testing)."""
        container1 = ServiceContainer()
        container1.initialize()
        
        ServiceContainer.reset()
        
        container2 = ServiceContainer()
        assert not container2.is_initialized()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Run tests**:
```bash
pytest tests/services/container/test_service_container.py -v
```

**Expected**: All tests passing!

---

## Step 9: Write Integration Test (15 min)

**File**: `tests/integration/test_service_container_integration.py`

```python
"""Integration tests for ServiceContainer with real services."""

import pytest
from services.container import ServiceContainer


class TestServiceContainerIntegration:
    """Test full service initialization and integration."""
    
    def setup_method(self):
        """Reset container before each test."""
        ServiceContainer.reset()
        
    def test_full_initialization(self):
        """Test full service initialization sequence."""
        container = ServiceContainer()
        container.initialize()
        
        # Should have both services
        assert container.has_service('llm')
        assert container.has_service('intent')
        
        # Should be able to get services
        llm_service = container.get_service('llm')
        assert llm_service is not None
        
        intent_service = container.get_service('intent')
        assert intent_service is not None
        
    def test_service_dependencies(self):
        """Test that intent service has access to LLM."""
        container = ServiceContainer()
        container.initialize()
        
        intent_service = container.get_service('intent')
        
        # Intent service should be functional
        # (This tests that it got its dependencies correctly)
        assert intent_service is not None
        # Could test actual functionality here if needed


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## Step 10: Validation - The Moment of Truth! (15 min)

### Start the server

```bash
# Kill any existing servers
pkill -f "python main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Start with main.py (proper way)
python main.py &

# Wait for startup
sleep 5

# Check server started
curl http://localhost:8001/health -s
```

### Test valid intent (should return 200!)

```bash
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "show me the standup"}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | tee dev/active/intent-test-valid-after-ddd.json

# Expected: HTTP 200 with success response!
# If we get this, DDD fix is validated! 🎉
```

### Test invalid intent (should return 422)

```bash
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": ""}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | tee dev/active/intent-test-invalid-after-ddd.json

# Expected: HTTP 422 with validation error
# Confirms Phase 1 error handling still working!
```

### Document results

**Create**: `dev/active/phase-1.5-validation-results.md`

```markdown
# Phase 1.5 Validation Results

**Date**: October 16, 2025  
**Time**: [completion time]  
**Duration**: [actual duration]

---

## Test Results

### Valid Intent Test
```bash
$ curl -X POST /api/v1/intent -d '{"intent": "show me the standup"}'
```

**Result**: HTTP [code]
**Response**: [paste response]
**Status**: [✅ SUCCESS / ❌ FAILED]

### Invalid Intent Test
```bash
$ curl -X POST /api/v1/intent -d '{"intent": ""}'
```

**Result**: HTTP [code]
**Response**: [paste response]
**Status**: [✅ SUCCESS / ❌ FAILED]

---

## Services Initialized

```
[paste output from logs showing services initialized]
```

---

## Test Suite Results

**Unit Tests**:
```bash
$ pytest tests/services/container/ -v
```
[paste output]

**Integration Tests**:
```bash
$ pytest tests/integration/test_service_container_integration.py -v
```
[paste output]

---

## Conclusion

**DDD Service Container**: [✅ WORKING / ❌ ISSUES]
**Intent Endpoint**: [✅ FUNCTIONAL / ❌ ISSUES]
**Error Handling**: [✅ VALIDATED / ❌ ISSUES]

**Ready for Phase 2**: [YES / NO]
```

---

## Step 11: Commit Changes (10 min)

### Use the pre-commit script!

```bash
./scripts/commit.sh "feat(services): implement DDD service container pattern

Architectural Changes:
- Add ServiceContainer (singleton pattern)
- Add ServiceRegistry for service management
- Add ServiceInitializer with dependency ordering
- Add container-specific exceptions

Integration:
- Update main.py to initialize services and start uvicorn
- Add lifespan handler to web/app.py
- Services: LLM and Intent initialized properly

Testing:
- Unit tests for container (8 tests)
- Integration tests for full initialization
- All tests passing

Validation:
- Intent endpoint now returns 200 for valid requests (was 422)
- Intent endpoint returns 422 for invalid requests (correct)
- Services initialize in correct dependency order

Fixes: October 10 architectural gap (commit d6b8aa09)
Enables: #215 error standardization completion

Part of: Sprint A2, DDD refactor + #215
Duration: [actual time]"
```

---

## Deliverables Phase 1.5

When complete, you should have:

- [ ] services/container/ directory created
- [ ] exceptions.py with 4 exception classes
- [ ] service_registry.py implemented
- [ ] service_container.py (singleton) implemented
- [ ] initialization.py with service init logic
- [ ] __init__.py with public API
- [ ] main.py updated to use container
- [ ] web/app.py updated with lifespan
- [ ] Unit tests written (8+ tests)
- [ ] Integration tests written (2+ tests)
- [ ] All tests passing
- [ ] Valid intent returns 200 (validated!)
- [ ] Invalid intent returns 422 (validated!)
- [ ] Changes committed
- [ ] Validation results documented

---

## Success Criteria

**Phase 1.5 is complete when**:

- ✅ Container singleton working
- ✅ Services initialize in correct order
- ✅ Intent endpoint returns 200 for valid requests
- ✅ Intent endpoint returns 422 for invalid requests
- ✅ All unit tests passing (8+)
- ✅ All integration tests passing (2+)
- ✅ No regressions in other endpoints
- ✅ Changes committed and pushed

---

## Time Budget

**Target**: 1.5-2 hours

- Container structure: 10 min
- Exceptions: 5 min
- ServiceRegistry: 15 min
- ServiceContainer: 30 min
- ServiceInitializer: 30 min
- Public API: 5 min
- main.py update: 10 min
- web/app.py update: 15 min
- Unit tests: 20 min
- Integration tests: 15 min
- Validation: 15 min
- Commit: 10 min

**Total**: ~2.5 hours (with buffer)

---

## What NOT to Do

- ❌ Don't skip tests (foundation must be solid)
- ❌ Don't skip validation (prove it works!)
- ❌ Don't use tmp/ for files (use dev/active/)
- ❌ Don't proceed if valid intent doesn't return 200

## What TO Do

- ✅ Follow DDD principles
- ✅ Write comprehensive tests
- ✅ Validate thoroughly
- ✅ Document results
- ✅ Use proper file locations (dev/active/)

---

**Phase 1.5 Start**: 10:35 AM  
**Expected Done**: ~12:30 PM (2 hours)  
**Status**: Ready to build proper foundation!

**LET'S FIX THIS RIGHT!** 🏗️

---

*"The foundation must be solid before building the cathedral."*  
*- DDD Philosophy*
