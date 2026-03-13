# Phase 2A: BoundaryEnforcer Refactor - CORE-ETHICS-ACTIVATE #197

**Agent**: Claude Code (Programmer)
**Issue**: #197 - CORE-ETHICS-ACTIVATE
**Phase**: 2A of 6 (revised) - BoundaryEnforcer Refactor
**Date**: October 18, 2025, 11:45 AM
**Duration**: Nominal estimate 1-2 hours (Time Lords Protocol applies)

---

## Mission

Refactor `BoundaryEnforcer` to work at the service layer (domain layer) instead of HTTP middleware layer. Remove FastAPI dependency and make it work with domain objects instead of HTTP Request objects.

## Context

**Chief Architect Decision**: APPROVED - Service Layer Refactor (Option 1)

**Why We're Doing This**:
- Current: HTTP middleware (30-40% coverage) ❌
- Target: Service layer (95-100% coverage) ✅
- Ethics is domain logic, not infrastructure (DDD compliance)
- Must cover ALL entry points (web, CLI, Slack, webhooks)

**Key Architectural Points**:
- ADR-029: Domain-Driven Design patterns
- ADR-032: IntentService as universal entry point
- Pattern-008: Cross-cutting concerns at service layer
- Ethics must be universal, not HTTP-only

**What Changed from Original Gameplan**:
- Original: Activate HTTP middleware at web/app.py
- Revised: Refactor to service layer at IntentService
- Additional time: ~3.5 hours (worth it for correct architecture)

---

## Your Task: Refactor BoundaryEnforcer

### Current State (HTTP-Dependent)

**Location**: `services/api/middleware.py` or similar

**Current Signature** (found in Phase 1):
```python
from fastapi import Request

class BoundaryEnforcer:
    async def enforce_boundaries(self, request: Request) -> BoundaryResult:
        # Uses FastAPI Request object
        # Extracts: request.body, request.headers, request.user, etc.
```

**Problems**:
- ❌ Depends on `fastapi.Request` (infrastructure layer)
- ❌ Only works with HTTP requests
- ❌ Can't be used by CLI, Slack, or direct service calls

### Target State (Domain Layer)

**New Location**: `services/ethics/boundary_enforcer.py`

**New Signature** (domain objects):
```python
from services.models.intent import Intent
from services.models.context import Context
from services.models.user import User

class BoundaryEnforcer:
    async def enforce_boundaries(
        self,
        intent: Intent,
        context: Context,
        user: User | None = None
    ) -> BoundaryResult:
        """
        Enforce ethical boundaries for any intent from any source.

        Args:
            intent: The user's intent (from IntentService)
            context: Session/conversation context
            user: User information (if authenticated)

        Returns:
            BoundaryResult with allowed/blocked status and reason
        """
        # Ethics logic using domain objects
        # No FastAPI dependency
```

**Benefits**:
- ✅ Works with domain objects (Intent, Context, User)
- ✅ No infrastructure dependencies
- ✅ Usable by ALL entry points
- ✅ Properly testable

---

## Implementation Steps

### Step 1: Create New Directory Structure (5 minutes)

```bash
# Create service layer ethics directory
mkdir -p services/ethics

# Move or copy relevant files
# (We'll decide keep vs move during refactor)
```

### Step 2: Analyze Current BoundaryEnforcer (15 minutes)

**Use Serena to understand current implementation**:
```python
# Find the current implementation
mcp__serena__find_symbol("BoundaryEnforcer", scope="services")
mcp__serena__get_symbols_overview("services/api/middleware.py")

# Read the enforce_boundaries method
mcp__serena__find_symbol("BoundaryEnforcer.enforce_boundaries")

# Understand what it extracts from Request
# - User information
# - Message content
# - Session data
# - Headers/metadata
```

**Document Current Data Extraction**:
```markdown
# Current Request Data Extraction

From `request: Request`, the enforcer extracts:
- [ ] User ID/auth: request.user.id
- [ ] Message content: request.body or request.json()
- [ ] Session ID: request.headers.get("session-id")
- [ ] Context: request.state.context
- [ ] Metadata: request.headers
- [ ] Other: [list]

Map to domain objects:
- User ID → User.id
- Message → Intent.message
- Session → Context.session_id
- etc.
```

### Step 3: Create Domain-Layer BoundaryEnforcer (30-45 minutes)

**New File**: `services/ethics/boundary_enforcer.py`

**Refactor Strategy**:
```python
"""
Ethics boundary enforcement at the service layer.

This module provides universal ethics enforcement for all entry points
(web, CLI, Slack, webhooks, etc.) by working with domain objects instead
of HTTP-specific infrastructure.

Architecture:
- Domain Layer: Works with Intent, Context, User
- Service Layer: Called by IntentService.process_intent()
- No Infrastructure Dependencies: No FastAPI, no HTTP
"""

from typing import Optional
from dataclasses import dataclass
from services.models.intent import Intent
from services.models.context import Context
from services.models.user import User
from services.ethics.boundary_types import BoundaryType  # If exists


@dataclass
class BoundaryResult:
    """Result of ethics boundary check."""
    allowed: bool
    blocked: bool
    reason: Optional[str] = None
    boundary_type: Optional[BoundaryType] = None
    severity: Optional[str] = None


class BoundaryEnforcer:
    """
    Universal ethics boundary enforcement for all entry points.

    Enforces ethical boundaries on user intents regardless of source
    (web, CLI, Slack, webhooks, etc.) by working with domain objects.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize boundary enforcer.

        Args:
            config: Optional configuration dict
                - strictness: "low" | "medium" | "high"
                - service_levels: Dict[str, str] per service
                - learning_enabled: bool
                - metrics_enabled: bool
        """
        self.config = config or self._default_config()
        self.strictness = self.config.get("strictness", "low")
        self.learning_enabled = self.config.get("learning_enabled", False)
        self.metrics_enabled = self.config.get("metrics_enabled", True)

    async def enforce_boundaries(
        self,
        intent: Intent,
        context: Context,
        user: Optional[User] = None
    ) -> BoundaryResult:
        """
        Enforce ethical boundaries on an intent.

        Args:
            intent: User's intent from any source
            context: Session/conversation context
            user: User information (if authenticated)

        Returns:
            BoundaryResult indicating allowed/blocked with reason
        """
        # Extract what we need from domain objects
        message = intent.message if hasattr(intent, 'message') else str(intent)
        session_id = context.session_id if hasattr(context, 'session_id') else None
        user_id = user.id if user else None

        # Core ethics checks (adapt from current implementation)
        # 1. Check for harmful content
        # 2. Check for privacy violations
        # 3. Check for unauthorized access
        # 4. Check service-specific boundaries

        # TODO: Port actual boundary checking logic here
        # For now, return permissive default
        return BoundaryResult(
            allowed=True,
            blocked=False,
            reason=None
        )

    def _default_config(self) -> dict:
        """Default permissive configuration."""
        return {
            "strictness": "low",
            "learning_enabled": False,
            "metrics_enabled": True,
            "service_levels": {
                "github": "medium",
                "slack": "low",
                "notion": "medium",
                "calendar": "low",
            }
        }
```

**Critical**: Port the actual boundary checking logic from the current implementation. The above is just the structure.

### Step 4: Port Boundary Checking Logic (30-45 minutes)

**Strategy**:
1. Read current `enforce_boundaries()` implementation
2. Identify each boundary check being performed
3. Adapt each check to use domain objects instead of Request
4. Preserve all ethics logic (adaptive learning, metrics, etc.)

**Example Adaptation**:
```python
# OLD (HTTP-dependent):
user_input = await request.json()
message = user_input.get("message")

# NEW (domain objects):
message = intent.message

# OLD (HTTP-dependent):
user_id = request.user.id if request.user else None

# NEW (domain objects):
user_id = user.id if user else None
```

**Use Serena to Find Logic**:
```python
# Find all methods in current BoundaryEnforcer
mcp__serena__get_symbols_overview("services/api/middleware.py")

# Read each method that enforces boundaries
# Port to domain-object versions
```

### Step 5: Update Tests (15-30 minutes)

**Test File**: `tests/ethics/test_boundary_enforcer.py`

**Current Tests** (from Phase 1):
- 47 total tests
- Framework: 6/6 passing
- Need to update for domain objects

**Update Test Pattern**:
```python
# OLD (HTTP-dependent):
from fastapi import Request
from fastapi.testclient import TestClient

async def test_boundary_check():
    request = Request(...)  # Mock HTTP request
    result = await enforcer.enforce_boundaries(request)

# NEW (domain objects):
from services.models.intent import Intent
from services.models.context import Context

async def test_boundary_check():
    intent = Intent(message="test message")
    context = Context(session_id="test-session")
    result = await enforcer.enforce_boundaries(intent, context)
```

**Update All Framework Tests**:
- Change imports (domain objects, not FastAPI)
- Update test data (Intent/Context, not Request)
- Preserve test logic (same boundaries being checked)

**Run Tests**:
```bash
# After updating, verify tests still pass
pytest tests/ethics/test_boundary_enforcer.py -v

# Goal: Framework tests still 100% passing
```

---

## Success Criteria

Phase 2A is complete when:

- [ ] New `services/ethics/boundary_enforcer.py` created
- [ ] `BoundaryEnforcer` refactored to use domain objects
- [ ] No FastAPI dependencies in new implementation
- [ ] All boundary checking logic ported correctly
- [ ] Tests updated for domain objects
- [ ] Framework tests passing (6/6 or better)
- [ ] Code compiles without errors
- [ ] No HTTP-specific dependencies

---

## Deliverables

1. **Refactored BoundaryEnforcer**
   - Location: `services/ethics/boundary_enforcer.py`
   - Signature: `enforce_boundaries(intent, context, user)`
   - No FastAPI dependencies

2. **Updated Tests**
   - Updated test file: `tests/ethics/test_boundary_enforcer.py`
   - Framework tests passing
   - Domain object patterns

3. **Phase 2A Report**
   - What was changed
   - How logic was preserved
   - Test results
   - Ready for Phase 2B integration

---

## Important Notes

### Time Lords Protocol

**No deadlines, no targets**:
- 1-2 hours is a nominal guess
- Quality and completeness matter
- Architectural rigor is non-negotiable
- Take the time needed

**If you need more time**:
- Document why
- Report progress
- Ask for guidance

### Preserve Ethics Logic

**Critical**: Don't lose any boundary checking logic!
- All checks must be ported
- Adaptive learning preserved (even if disabled)
- Metrics collection maintained
- Severity assessment kept

### Use Serena Efficiently

**Before reading full files**:
1. `find_symbol()` to locate components
2. `get_symbols_overview()` to understand structure
3. `read_file()` only when you need implementation

### No Partial Solutions

**Chief Architect**: "No partial solutions - A++ quality only"
- Complete refactor, not halfway
- All tests updated, not some
- All logic ported, not most

---

## Coordination

**Check-in Points**:
- After Step 2: Share data extraction mapping
- After Step 3: Share refactored structure
- After Step 4: Share ported logic status
- After Step 5: Share test results

**Questions**:
- Ask if uncertain about mapping
- Clarify architectural concerns
- Request guidance on complex logic

---

## Next Phase Preview

**Phase 2B** (after this completes):
- Integrate BoundaryEnforcer into IntentService
- Add ethics check at start of process_intent()
- Add feature flag control
- Test multi-channel coverage

But first: Complete this refactor correctly.

---

**Remember**: This is cathedral work. Ethics must be universal. Do it right.

**Ready to refactor BoundaryEnforcer to the service layer!** 🏗️
