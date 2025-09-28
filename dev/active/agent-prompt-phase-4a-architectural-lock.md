# Agent Prompt: Phase 4A - Architectural Lock Implementation (Code Agent)
*Following successful Phase 3A/3B: Feature flags verified working in both spatial and legacy modes*

## Mission: Lock Down Router Architecture

Phase 3A/3B confirmed all services work correctly with feature flag control between spatial and legacy modes. You're now implementing architectural enforcement to prevent future regression to direct GitHubAgent imports.

**Strategic Goal**: Create automated enforcement that catches and prevents direct GitHub imports, ensuring the router architecture remains intact as the codebase evolves.

## GitHub Issue #193 Integration

**Update Progress**: After implementing each enforcement mechanism, update GitHub issue with evidence
**Evidence Collection**: Provide test output showing enforcement catches violations
**PM Validation**: Request validation after all enforcement mechanisms are implemented

## Phase 4A Implementation Components

### 1. Anti-Pattern Test Creation
Create test that fails if services import GitHubAgent directly:

```python
# tests/test_architecture_enforcement.py
import os
import glob
import pytest

def test_no_direct_github_agent_imports():
    """Prevent services from importing GitHubAgent directly"""

    # Search for direct GitHubAgent imports in services directory
    service_files = glob.glob("services/**/*.py", recursive=True)

    # Exclude allowed files
    allowed_files = [
        "services/integrations/github/github_agent.py",  # The agent itself
        "services/integrations/github/github_integration_router.py",  # Router imports for delegation
    ]

    violations = []

    for file_path in service_files:
        # Skip test files
        if "test" in file_path or "__pycache__" in file_path:
            continue

        # Skip explicitly allowed files
        if any(allowed in file_path for allowed in allowed_files):
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for direct imports
        if "from services.integrations.github.github_agent import GitHubAgent" in content:
            violations.append(f"{file_path}: Direct GitHubAgent import found")
        if "from .github_agent import GitHubAgent" in content:
            violations.append(f"{file_path}: Relative GitHubAgent import found")
        if "import github_agent" in content and "GitHubAgent" in content:
            violations.append(f"{file_path}: GitHubAgent import pattern found")

    if violations:
        violation_message = "\n".join([
            "ARCHITECTURAL VIOLATION: Direct GitHubAgent imports found!",
            "Services must use GitHubIntegrationRouter instead.",
            "",
            "Violations found:"
        ] + violations + [
            "",
            "Fix by replacing:",
            "  from services.integrations.github.github_agent import GitHubAgent",
            "With:",
            "  from services.integrations.github.github_integration_router import GitHubIntegrationRouter"
        ])

        pytest.fail(violation_message)

def test_services_use_router():
    """Verify services use GitHubIntegrationRouter"""

    # Services that should use the router
    required_router_services = [
        "services/orchestration/engine.py",
        "services/domain/github_domain_service.py",
        "services/domain/pm_number_manager.py",
        "services/domain/standup_orchestration_service.py",
        "services/integrations/github/issue_analyzer.py"
    ]

    missing_router_imports = []

    for file_path in required_router_services:
        if not os.path.exists(file_path):
            missing_router_imports.append(f"{file_path}: File not found")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "GitHubIntegrationRouter" not in content:
            missing_router_imports.append(f"{file_path}: Missing GitHubIntegrationRouter usage")

    if missing_router_imports:
        failure_message = "\n".join([
            "ARCHITECTURAL VIOLATION: Services not using GitHubIntegrationRouter!",
            "",
            "Missing router usage:"
        ] + missing_router_imports)

        pytest.fail(failure_message)
```

### 2. Pre-commit Hook Implementation
Create Git pre-commit hook to catch violations before commits:

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running architectural compliance check..."

# Check for direct GitHubAgent imports
violations=$(grep -r "from.*github_agent import GitHubAgent" services/ --include="*.py" \
    --exclude="services/integrations/github/github_agent.py" \
    --exclude="services/integrations/github/github_integration_router.py" \
    2>/dev/null || true)

if [ ! -z "$violations" ]; then
    echo "❌ COMMIT BLOCKED: Direct GitHubAgent imports found!"
    echo ""
    echo "Violations:"
    echo "$violations"
    echo ""
    echo "Services must use GitHubIntegrationRouter instead of direct GitHubAgent imports."
    echo "Replace:"
    echo "  from services.integrations.github.github_agent import GitHubAgent"
    echo "With:"
    echo "  from services.integrations.github.github_integration_router import GitHubIntegrationRouter"
    echo ""
    exit 1
fi

# Check for required router usage
required_files=(
    "services/orchestration/engine.py"
    "services/domain/github_domain_service.py"
    "services/domain/pm_number_manager.py"
    "services/domain/standup_orchestration_service.py"
    "services/integrations/github/issue_analyzer.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        if ! grep -q "GitHubIntegrationRouter" "$file"; then
            echo "❌ COMMIT BLOCKED: $file missing GitHubIntegrationRouter usage!"
            exit 1
        fi
    fi
done

echo "✅ Architectural compliance verified"
exit 0
```

### 3. CI/CD Pipeline Integration
Add architectural testing to CI pipeline:

```yaml
# .github/workflows/architecture-compliance.yml
name: Architecture Compliance

on: [push, pull_request]

jobs:
  architecture-check:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install pytest

    - name: Run architecture compliance tests
      run: |
        pytest tests/test_architecture_enforcement.py -v

    - name: Check for direct GitHub imports
      run: |
        violations=$(grep -r "from.*github_agent import GitHubAgent" services/ --include="*.py" \
          --exclude="services/integrations/github/github_agent.py" \
          --exclude="services/integrations/github/github_integration_router.py" \
          2>/dev/null || true)

        if [ ! -z "$violations" ]; then
          echo "❌ Direct GitHubAgent imports found:"
          echo "$violations"
          exit 1
        fi

        echo "✅ No direct GitHubAgent imports found"
```

### 4. Documentation Creation
Create architectural documentation explaining the router pattern:

```markdown
# docs/architecture/github-integration-router.md

# GitHub Integration Router Architecture

## Overview
All GitHub operations must flow through the GitHubIntegrationRouter to enable feature flag control and spatial intelligence capabilities.

## Required Usage Pattern

### Correct Import
```python
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

class MyService:
    def __init__(self):
        self.github = GitHubIntegrationRouter()
```

### Prohibited Import
```python
# ❌ NEVER DO THIS
from services.integrations.github.github_agent import GitHubAgent

class MyService:
    def __init__(self):
        self.github = GitHubAgent()  # Bypasses router architecture
```

## Benefits of Router Architecture

1. **Feature Flag Control**: Enable/disable spatial intelligence via USE_SPATIAL_GITHUB
2. **Spatial Intelligence**: 8-dimensional GitHub analysis when enabled
3. **Deprecation Management**: Automatic warnings for legacy usage
4. **Consistent Error Handling**: Standardized RuntimeError patterns
5. **Future-Proof**: Ready for additional integration routers

## Enforcement Mechanisms

1. **Automated Tests**: `tests/test_architecture_enforcement.py`
2. **Pre-commit Hooks**: Blocks commits with direct imports
3. **CI/CD Pipeline**: Architecture compliance verification
4. **Code Review**: Manual verification during PR reviews

## Migration Guide

If you find direct GitHubAgent imports:

1. Replace import statement
2. Update instantiation
3. Verify functionality
4. Run tests to confirm compliance

For questions, see CORE-GREAT-2 issue #193.
```

## Implementation Verification

### Test the Anti-Pattern Detection
```bash
# Test that architectural tests work
python -m pytest tests/test_architecture_enforcement.py -v

# Test pre-commit hook (if implemented)
echo "from services.integrations.github.github_agent import GitHubAgent" > test_violation.py
git add test_violation.py
git commit -m "test violation"  # Should be blocked
rm test_violation.py
```

### Verify Current Compliance
```bash
# Verify no current violations exist
python -m pytest tests/test_architecture_enforcement.py::test_no_direct_github_agent_imports -v

# Verify router usage
python -m pytest tests/test_architecture_enforcement.py::test_services_use_router -v
```

## Evidence Collection Requirements

### For GitHub Issue #193 Updates
```bash
# Architecture enforcement test results
echo "=== Architecture Enforcement Evidence ==="
python -m pytest tests/test_architecture_enforcement.py -v

# Pre-commit hook verification (if implemented)
echo "=== Pre-commit Hook Test ==="
# [Show hook blocking violations]

# CI/CD integration verification (if implemented)
echo "=== CI/CD Integration ==="
# [Show pipeline configuration]

# Documentation creation verification
echo "=== Documentation Created ==="
ls -la docs/architecture/github-integration-router.md
```

## Success Criteria Checklist

- [ ] Anti-pattern test created and passing
- [ ] Pre-commit hook implemented (optional but recommended)
- [ ] CI/CD integration added (optional but recommended)
- [ ] Architecture documentation created
- [ ] Current codebase passes all architectural tests
- [ ] Enforcement mechanisms prevent future violations
- [ ] Evidence collected and documented

## PM Validation Request Format

```markdown
@PM - Phase 4A complete and ready for validation:

**Architectural Lock**: Enforcement mechanisms implemented ✅
**Anti-Pattern Tests**: Prevent direct GitHubAgent imports ✅
**Current Compliance**: All services pass architectural tests ✅
**Documentation**: Router architecture explained and documented ✅

**Evidence**: [link to test outputs and enforcement verification]
**Future Protection**: Automated prevention of architectural regression

Request validation before proceeding to Phase 5 (documentation and completion).
```

---

**Your Mission**: Lock down the router architecture with automated enforcement. Prevent future regression to direct GitHubAgent imports while maintaining current functionality.
