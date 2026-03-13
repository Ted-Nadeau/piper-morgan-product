# Revised Gameplan: CORE-GREAT-2B - Fix GitHub Architectural Bypass

**Date**: September 28, 2025 (Revised 1:40 PM)
**Issue**: #193
**Architect**: Claude Opus 4.1
**Lead Developer**: Claude Sonnet 4

---

## Critical Discovery: Complete Infrastructure Being Bypassed

### What We Found (1:34 PM Investigation)
- ✅ Sophisticated deprecation router EXISTS and WORKS
- ✅ Spatial implementation COMPLETE (16KB file from Aug 12)
- ✅ Feature flags properly configured (USE_SPATIAL_GITHUB=True)
- ❌ Services BYPASS router via direct legacy imports

### The Real Problem
Not incomplete implementation - it's architectural pattern violation. Services import `GitHubAgent` directly instead of using `GitHubIntegrationRouter`.

### Evidence
Only QueryRouter uses the router. These bypass it:
- orchestration/engine.py
- domain/github_domain_service.py
- domain/pm_number_manager.py
- domain/standup_orchestration_service.py
- integrations/github/issue_analyzer.py

---

## Revised Scope: Fix Architectural Bypass

This is NOT about completing spatial migration. It's about making services use the sophisticated infrastructure that already exists.

---

## Phase 0: Verify Router Completeness (30 min)

### Both Agents Together

#### 0A. Confirm Router Handles All Operations
```bash
# List all methods in GitHubAgent
grep "def " services/integrations/github/github_agent.py | grep -v "__"

# List all methods router can handle
grep "def " services/integrations/github/github_integration_router.py | grep -v "__"

# Verify router can handle everything GitHubAgent does
```

#### 0B. Test Router Works for Each Operation
```python
# Create test script: test_router_completeness.py
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

router = GitHubIntegrationRouter()

# Test each operation the bypassing services use
operations = [
    'create_issue',
    'update_issue',
    'create_workflow_issue',
    'get_issue',
    # ... add all operations used by bypassing services
]

for op in operations:
    assert hasattr(router, op), f"Router missing operation: {op}"
    print(f"✓ Router supports {op}")
```

---

## Phase 1: Replace Direct Imports (2 hours)

### Deploy: Both Agents - Systematic Import Replacement

#### 1A. Fix orchestration/engine.py
```python
# BEFORE (Direct bypass)
from services.integrations.github.github_agent import GitHubAgent

class OrchestrationEngine:
    def __init__(self):
        self.github = GitHubAgent()

# AFTER (Use router)
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

class OrchestrationEngine:
    def __init__(self):
        self.github = GitHubIntegrationRouter()
```

#### 1B. Fix Each Bypassing Service
Apply same pattern to:
- domain/github_domain_service.py
- domain/pm_number_manager.py
- domain/standup_orchestration_service.py
- integrations/github/issue_analyzer.py

#### 1C. Verify No Direct Imports Remain
```bash
# Should return ONLY test files or the router itself
grep -r "from.*github_agent import GitHubAgent" . --include="*.py" | grep -v test | grep -v router

# If any remain, fix them
```

---

## Phase 2: Test Feature Flag Control (1 hour)

### Both Agents - Verify Router Control Works

#### 2A. Test Spatial Path
```bash
# Force spatial mode
export USE_SPATIAL_GITHUB=true
export ALLOW_LEGACY_GITHUB=false

# Run tests
pytest tests/integrations/github/ -v

# Verify spatial implementation used
grep "spatial" test_output.log
```

#### 2B. Test Legacy Fallback
```bash
# Force legacy mode
export USE_SPATIAL_GITHUB=false
export ALLOW_LEGACY_GITHUB=true

# Run tests
pytest tests/integrations/github/ -v

# Verify legacy implementation used
grep "legacy\|GitHubAgent" test_output.log
```

#### 2C. Test Each Service with Router
```python
# Test each previously-bypassing service
services_to_test = [
    'orchestration.engine',
    'domain.github_domain_service',
    'domain.pm_number_manager',
    'domain.standup_orchestration_service',
    'integrations.github.issue_analyzer'
]

for service in services_to_test:
    # Import and test it uses router
    # Verify feature flags control its behavior
```

---

## Phase 3: Architectural Compliance (30 min)

### Both Agents - Ensure Pattern Compliance

#### 3A. Create Import Guard Test
```python
# tests/architecture/test_no_direct_github_imports.py
def test_no_direct_github_agent_imports():
    """Ensure no service bypasses the router"""

    import subprocess
    result = subprocess.run(
        ["grep", "-r", "from.*github_agent import GitHubAgent", ".",
         "--include=*.py"],
        capture_output=True,
        text=True
    )

    # Filter out allowed imports (tests, router itself)
    violations = []
    for line in result.stdout.split('\n'):
        if line and 'test' not in line and 'router' not in line:
            violations.append(line)

    assert not violations, f"Direct GitHubAgent imports found:\n{violations}"
```

#### 3B. Add to CI/CD
```yaml
# .github/workflows/ci.yml
- name: Check Architectural Compliance
  run: |
    pytest tests/architecture/test_no_direct_github_imports.py -v
```

---

## Phase 4: Documentation (30 min)

### Both Agents - Document the Pattern

#### 4A. Create Architecture Decision Record
```markdown
# ADR-XXX: Integration Router Pattern Enforcement

## Status: Accepted

## Context
Services were bypassing the integration router through direct imports,
undermining feature flag control and spatial migration.

## Decision
All services MUST use integration routers. Direct imports to legacy
agents are forbidden.

## Consequences
- Feature flags control all integration behavior
- Spatial migration can be toggled centrally
- Architecture maintains consistency
```

#### 4B. Update Import Guidelines
```markdown
# docs/development/import-guidelines.md

## Integration Services

### ✅ CORRECT: Use Router
```python
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
```

### ❌ WRONG: Direct Import
```python
from services.integrations.github.github_agent import GitHubAgent  # FORBIDDEN
```
```

---

## Phase Z: Verification & Lock

### Evidence Collection
- No direct imports remain
- All services use router
- Feature flags control behavior
- Tests pass with both spatial and legacy

### Lock Implementation
- Architecture test prevents direct imports
- CI/CD enforces compliance
- Documentation clear on pattern

### GitHub Issue Update
```markdown
## GREAT-2B Complete

### Problem Discovered
- Infrastructure complete but bypassed
- Services using direct imports instead of router

### Solution Implemented
- Replaced all direct imports with router usage
- Verified feature flag control works
- Added architectural compliance tests

### Evidence
- No direct imports remain: [grep output]
- Tests pass with router: [test results]
- Feature flags verified: [test output]
```

---

## Success Criteria

- [ ] Zero direct GitHubAgent imports (except router/tests)
- [ ] All services use GitHubIntegrationRouter
- [ ] Feature flags control spatial/legacy switching
- [ ] Tests pass with both modes
- [ ] Architectural compliance test in CI/CD
- [ ] Documentation updated

---

## Time Estimate (Revised)

- Phase 0: 30 minutes (verify router completeness)
- Phase 1: 2 hours (replace imports systematically)
- Phase 2: 1 hour (test feature flag control)
- Phase 3: 30 minutes (architectural compliance)
- Phase 4: 30 minutes (documentation)
- **Total: ~4.5 hours**

This is actually SIMPLER than the original scope - it's import replacement, not feature implementation.

---

*The infrastructure is perfect. Make services use it.*
