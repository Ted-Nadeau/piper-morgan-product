# Claude Code Prompt: Phase 6 - Lock & Document Router Patterns

## Mission: Lock in Router Architecture with Automated Protection

**Context**: Phase 5 validated the router infrastructure works perfectly (100% test success, zero violations). Phase 6 locks in the architectural patterns with automated enforcement (pre-commit hooks, CI/CD checks) and documentation for future developers.

**Objective**: Add pre-commit hooks to prevent direct imports, update CI/CD to enforce router patterns, and document the architectural patterns for maintainability.

## Phase 6 Tasks

### Task 1: Add Pre-Commit Hooks

Create automated protection against direct adapter imports:

#### Pre-Commit Hook Configuration

```bash
# Check if pre-commit is installed
which pre-commit || echo "Pre-commit not found - will need installation"

# Create or update .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: prevent-direct-adapter-imports
        name: Prevent Direct Adapter Imports
        entry: python scripts/check_direct_imports.py
        language: python
        files: '^services/.*\.py$'
        pass_filenames: true
        verbose: true

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]
EOF

echo "Pre-commit config created: .pre-commit-config.yaml"
```

#### Direct Import Checker Script

```python
# Create scripts/check_direct_imports.py
import os
import sys
import re
from pathlib import Path

def create_direct_import_checker():
    """Create the direct import checker script"""

    # Ensure scripts directory exists
    os.makedirs('scripts', exist_ok=True)

    checker_content = '''#!/usr/bin/env python3
"""
Pre-commit hook to prevent direct adapter imports in favor of router pattern.
Enforces architectural protection established in CORE-QUERY-1 Phase 4.
"""

import sys
import re
from pathlib import Path

# Prohibited import patterns
PROHIBITED_PATTERNS = [
    # Calendar direct imports
    r'from\\s+services\\.mcp\\.consumer\\.google_calendar_adapter\\s+import',
    r'from\\s+.*google_calendar_adapter\\s+import',
    r'GoogleCalendarMCPAdapter(?!Router)',

    # Notion direct imports
    r'from\\s+services\\.integrations\\.mcp\\.notion_adapter\\s+import',
    r'from\\s+.*notion_adapter\\s+import',
    r'NotionMCPAdapter(?!Router)',

    # Slack direct imports
    r'from\\s+services\\.integrations\\.slack\\.spatial_adapter\\s+import',
    r'from\\s+services\\.integrations\\.slack\\.slack_client\\s+import',
    r'SlackSpatialAdapter(?!Router)',
    r'SlackClient(?!Router)',
]

# Allowed router patterns (for reference)
ALLOWED_PATTERNS = [
    r'CalendarIntegrationRouter',
    r'NotionIntegrationRouter',
    r'SlackIntegrationRouter',
]

def check_file(file_path):
    """Check a single file for prohibited imports"""
    violations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for line_num, line in enumerate(content.splitlines(), 1):
            for pattern in PROHIBITED_PATTERNS:
                if re.search(pattern, line):
                    violations.append(f"{file_path}:{line_num}: Prohibited direct adapter import: {line.strip()}")

    except Exception as e:
        violations.append(f"{file_path}: Error reading file: {e}")

    return violations

def main():
    """Main pre-commit hook function"""
    if len(sys.argv) < 2:
        print("Usage: check_direct_imports.py <file1> [file2] ...")
        sys.exit(1)

    all_violations = []

    for file_path in sys.argv[1:]:
        if Path(file_path).suffix == '.py':
            violations = check_file(file_path)
            all_violations.extend(violations)

    if all_violations:
        print("❌ ARCHITECTURAL VIOLATIONS DETECTED:")
        print()
        for violation in all_violations:
            print(f"  {violation}")
        print()
        print("Router Pattern Enforcement:")
        print("  Use CalendarIntegrationRouter instead of GoogleCalendarMCPAdapter")
        print("  Use NotionIntegrationRouter instead of NotionMCPAdapter")
        print("  Use SlackIntegrationRouter instead of SlackSpatialAdapter/SlackClient")
        print()
        print("See Phase 4 documentation for migration examples.")
        sys.exit(1)
    else:
        print("✅ No direct adapter imports detected")
        sys.exit(0)

if __name__ == "__main__":
    main()
'''

    with open('scripts/check_direct_imports.py', 'w') as f:
        f.write(checker_content)

    # Make script executable
    import stat
    st = os.stat('scripts/check_direct_imports.py')
    os.chmod('scripts/check_direct_imports.py', st.st_mode | stat.S_IEXEC)

    print("✅ Direct import checker created: scripts/check_direct_imports.py")

create_direct_import_checker()
```

#### Install and Test Pre-Commit

```bash
# Install pre-commit if needed
pip install pre-commit --break-system-packages || echo "Pre-commit installation may be needed"

# Install the hooks
pre-commit install || echo "Pre-commit hook installation attempted"

# Test the hook
echo "Testing pre-commit hook..."
pre-commit run prevent-direct-adapter-imports --all-files || echo "Pre-commit test completed"

# Verify hook works by testing against known clean files
python scripts/check_direct_imports.py services/intent_service/canonical_handlers.py || echo "Direct import checker test completed"
```

### Task 2: Update CI/CD Pipeline

Add router pattern enforcement to CI/CD:

#### GitHub Actions Workflow

```yaml
# Create or update .github/workflows/router-enforcement.yml
name: Router Pattern Enforcement

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  architectural-protection:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install pre-commit

    - name: Check Direct Adapter Imports
      run: |
        python scripts/check_direct_imports.py $(find services -name "*.py" -type f)

    - name: Router Completeness Check
      run: |
        python scripts/verify_router_completeness.py

    - name: Integration Architecture Test
      run: |
        python scripts/test_integration_architecture.py

  router-testing:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Test Router Feature Flags
      run: |
        python -m pytest tests/test_router_feature_flags.py -v

    - name: Test Router Completeness
      run: |
        python -m pytest tests/test_router_completeness.py -v
```

Create the workflow directory and file:

```bash
# Create GitHub Actions workflow
mkdir -p .github/workflows

cat > .github/workflows/router-enforcement.yml << 'EOF'
name: Router Pattern Enforcement

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  architectural-protection:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Check Direct Adapter Imports
      run: |
        python scripts/check_direct_imports.py $(find services -name "*.py" -type f)
EOF

echo "✅ GitHub Actions workflow created: .github/workflows/router-enforcement.yml"
```

### Task 3: Document Router Patterns

Create comprehensive documentation for the router architecture:

#### Router Pattern Documentation

```markdown
# Create docs/architecture/router-patterns.md
mkdir -p docs/architecture

cat > docs/architecture/router-patterns.md << 'EOF'
# Router Pattern Architecture

## Overview

The Router Pattern provides a unified abstraction layer over external integrations, enabling feature flag control and spatial intelligence capabilities while maintaining backward compatibility.

## Architecture

### Integration Routers

Three integration routers provide complete abstraction:

1. **CalendarIntegrationRouter** - Abstracts GoogleCalendarMCPAdapter (12 methods)
2. **NotionIntegrationRouter** - Abstracts NotionMCPAdapter (22 methods)
3. **SlackIntegrationRouter** - Abstracts SlackSpatialAdapter + SlackClient (15 methods)

### Feature Flag Control

Each router respects feature flags for spatial intelligence:

- `USE_SPATIAL_CALENDAR` (default: true)
- `USE_SPATIAL_NOTION` (default: true)
- `USE_SPATIAL_SLACK` (default: true)
- `ALLOW_LEGACY_SLACK` (default: false)

### Router Implementation Pattern

```python
class IntegrationRouter(BaseSpatialAdapter):
    def __init__(self, config_service=None):
        super().__init__(config_service)
        self.use_spatial = self._should_use_spatial()
        self.allow_legacy = self._allow_legacy()

    def _get_preferred_integration(self, context):
        if self.use_spatial:
            return self._get_spatial_integration(), False
        elif self.allow_legacy:
            return self._get_legacy_integration(), True
        else:
            return None, False

    async def method_name(self, *args, **kwargs):
        integration, is_legacy = self._get_preferred_integration("method_context")
        if integration:
            return await integration.method_name(*args, **kwargs)
        else:
            raise IntegrationNotAvailableError("Integration disabled")
```

## Service Migration Pattern

### Before (Direct Import)
```python
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

class SomeService:
    def __init__(self):
        self.calendar = GoogleCalendarMCPAdapter()
```

### After (Router Pattern)
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

class SomeService:
    def __init__(self):
        self.calendar = CalendarIntegrationRouter()
```

## Architectural Protection

### Pre-Commit Hooks
- `prevent-direct-adapter-imports` - Blocks direct adapter imports
- Enforces router pattern usage

### CI/CD Checks
- Direct import detection
- Router completeness verification
- Integration architecture testing

## Implementation History

- **Phase 1**: Router interface design and base implementation
- **Phase 2**: Individual router development (Calendar, Notion, Slack)
- **Phase 3**: Router completeness verification and debugging
- **Phase 4**: Service migration with anti-80% pattern safeguards
- **Phase 5**: Comprehensive testing and validation
- **Phase 6**: Architectural protection and documentation

## Benefits

1. **Feature Flag Control** - Enable/disable spatial intelligence per integration
2. **Backward Compatibility** - Legacy mode support where needed
3. **Uniform Interface** - Consistent API across all integrations
4. **Spatial Intelligence** - Built-in spatial adapter coordination
5. **Architectural Protection** - Automated enforcement prevents regression

## Future Extensions

The router pattern can be extended for:
- New integration types
- Enhanced feature flag granularity
- Advanced spatial intelligence capabilities
- Performance optimization layers

EOF

echo "✅ Router pattern documentation created: docs/architecture/router-patterns.md"
```

#### Migration Guide Documentation

```markdown
# Create docs/migration/router-migration-guide.md
mkdir -p docs/migration

cat > docs/migration/router-migration-guide.md << 'EOF'
# Router Migration Guide

## Quick Reference

### Calendar Services
```python
# OLD
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
calendar = GoogleCalendarMCPAdapter()

# NEW
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
calendar = CalendarIntegrationRouter()
```

### Notion Services
```python
# OLD
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
notion = NotionMCPAdapter()

# NEW
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
notion = NotionIntegrationRouter()
```

### Slack Services
```python
# OLD
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.slack_client import SlackClient
spatial = SlackSpatialAdapter()
client = SlackClient()

# NEW
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
slack = SlackIntegrationRouter()
# Access spatial: slack.get_spatial_adapter()
# Client methods available directly on slack router
```

## Migration Process

1. **Import Replacement** - Update import statements
2. **Instantiation Update** - Replace adapter with router
3. **Method Calls** - Usually unchanged (transparent delegation)
4. **Testing** - Verify functionality preserved
5. **Commit** - Document migration with evidence

## Completed Migrations

- services/intent_service/canonical_handlers.py (Calendar)
- services/features/morning_standup.py (Calendar)
- services/domain/notion_domain_service.py (Notion)
- services/publishing/publisher.py (Notion)
- services/intelligence/spatial/notion_spatial.py (Notion)
- services/integrations/slack/webhook_router.py (Slack)

EOF

echo "✅ Migration guide created: docs/migration/router-migration-guide.md"
```

### Task 4: Commit All Phase 6 Changes

```bash
# Add all Phase 6 changes
git add .pre-commit-config.yaml
git add scripts/check_direct_imports.py
git add .github/workflows/router-enforcement.yml
git add docs/architecture/router-patterns.md
git add docs/migration/router-migration-guide.md

# Commit Phase 6 changes
git commit -m "Phase 6: Lock & Document Router Patterns

- Add pre-commit hooks to prevent direct adapter imports
- Add GitHub Actions workflow for router pattern enforcement
- Create comprehensive router pattern documentation
- Add migration guide for future reference
- Establish automated architectural protection

CORE-QUERY-1 Phase 6 complete - router infrastructure locked and documented"

git log --oneline -1
```

## Evidence Requirements

Document Phase 6 completion:

```markdown
# Phase 6: Lock & Document Router Patterns Report

## Pre-Commit Hooks Added
- Configuration: .pre-commit-config.yaml ✅
- Direct import checker: scripts/check_direct_imports.py ✅
- Hook installation: pre-commit install ✅
- Testing: Hook prevents direct imports ✅

## CI/CD Updates
- GitHub Actions workflow: .github/workflows/router-enforcement.yml ✅
- Architectural protection checks: Direct import detection ✅
- Router testing integration: Feature flags and completeness ✅

## Documentation Created
- Router patterns: docs/architecture/router-patterns.md ✅
- Migration guide: docs/migration/router-migration-guide.md ✅
- Implementation history documented ✅
- Future extension guidance provided ✅

## Architectural Protection
- Automated enforcement: Pre-commit + CI/CD ✅
- Pattern documentation: Complete reference available ✅
- Migration examples: All patterns documented ✅

## Git History
- Phase 6 commit: [hash and message] ✅
- All changes documented and committed ✅

## Ready for Phase Z (Bookending): YES/NO
```

## Update Requirements

1. **Update Session Log**: Add Phase 6 completion with automation evidence
2. **Update GitHub Issue #199**: Add comment with locking/documentation evidence
3. **Tag Lead Developer**: Request final checkbox approval

## Success Criteria

✅ Pre-commit hooks prevent direct imports automatically
✅ CI/CD enforces router patterns in pull requests
✅ Comprehensive documentation available for maintenance
✅ All architectural protection automated
✅ Future developers have clear migration guidance

---

**Your Mission**: Lock in the router architecture with automated protection and comprehensive documentation.

**Quality Standard**: Bulletproof architectural enforcement that prevents regression to direct imports.
