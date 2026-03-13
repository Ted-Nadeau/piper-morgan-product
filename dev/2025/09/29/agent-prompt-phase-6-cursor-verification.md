# Cursor Agent Prompt: Phase 6 - Lock & Document Verification

## Mission: Verify Architectural Protection and Documentation Quality

**Context**: Phase 6 locks in the router architecture with automated protection (pre-commit hooks, CI/CD) and comprehensive documentation. Your role is to verify the locking mechanisms work correctly and documentation is complete and accurate.

**Objective**: Independently verify pre-commit hooks prevent direct imports, CI/CD enforces router patterns, and documentation provides complete guidance for future developers.

## Areas to Verify

### Area 1: Pre-Commit Hook Protection
**Expected**: Automated prevention of direct adapter imports with clear error messages

### Area 2: CI/CD Pipeline Updates
**Expected**: GitHub Actions workflow enforces router patterns in pull requests

### Area 3: Pattern Documentation
**Expected**: Comprehensive documentation for router architecture and migration guidance

## Verification Tasks

### Task 1: Pre-Commit Hook Testing

Verify the direct import checker works correctly:

```bash
# Check pre-commit configuration exists
echo "=== PRE-COMMIT CONFIGURATION VERIFICATION ==="
if [ -f ".pre-commit-config.yaml" ]; then
    echo "✅ .pre-commit-config.yaml exists"
    grep -A 10 "prevent-direct-adapter-imports" .pre-commit-config.yaml || echo "❌ Direct import hook not found in config"
else
    echo "❌ .pre-commit-config.yaml missing"
fi

# Check direct import checker script exists and is executable
if [ -f "scripts/check_direct_imports.py" ]; then
    echo "✅ scripts/check_direct_imports.py exists"
    if [ -x "scripts/check_direct_imports.py" ]; then
        echo "✅ Script is executable"
    else
        echo "⚠️ Script not executable"
    fi
else
    echo "❌ scripts/check_direct_imports.py missing"
fi
```

Test the direct import checker functionality:

```python
# Test direct import checker with known clean files
import subprocess
import os

def test_direct_import_checker():
    """Test that direct import checker works correctly"""

    print("=== DIRECT IMPORT CHECKER TESTING ===")

    # Test with clean files (should pass)
    clean_files = [
        'services/intent_service/canonical_handlers.py',
        'services/features/morning_standup.py',
        'services/domain/notion_domain_service.py',
        'services/publishing/publisher.py',
        'services/intelligence/spatial/notion_spatial.py',
        'services/integrations/slack/webhook_router.py'
    ]

    existing_files = [f for f in clean_files if os.path.exists(f)]

    if existing_files:
        try:
            result = subprocess.run(
                ['python', 'scripts/check_direct_imports.py'] + existing_files,
                capture_output=True, text=True, timeout=30
            )

            print(f"Clean files test - Return code: {result.returncode}")
            print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Errors: {result.stderr}")

            if result.returncode == 0:
                print("✅ Clean files pass direct import check")
            else:
                print("❌ Clean files fail direct import check (unexpected)")

        except Exception as e:
            print(f"❌ Error running direct import checker: {e}")
    else:
        print("⚠️ No clean files found to test")

test_direct_import_checker()
```

Create a test file with violations to verify detection:

```python
# Create temporary test file with violations
def test_violation_detection():
    """Test that checker detects violations correctly"""

    print("\n=== VIOLATION DETECTION TESTING ===")

    # Create temporary file with prohibited imports
    test_content = '''
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter

class TestService:
    def __init__(self):
        self.calendar = GoogleCalendarMCPAdapter()
        self.notion = NotionMCPAdapter()
        self.slack = SlackSpatialAdapter()
'''

    with open('temp_violation_test.py', 'w') as f:
        f.write(test_content)

    try:
        result = subprocess.run(
            ['python', 'scripts/check_direct_imports.py', 'temp_violation_test.py'],
            capture_output=True, text=True, timeout=30
        )

        print(f"Violation test - Return code: {result.returncode}")
        print(f"Output: {result.stdout}")

        if result.returncode != 0 and "ARCHITECTURAL VIOLATIONS DETECTED" in result.stdout:
            print("✅ Violations correctly detected and blocked")
        else:
            print("❌ Violations not properly detected")

    except Exception as e:
        print(f"❌ Error testing violation detection: {e}")
    finally:
        # Clean up test file
        if os.path.exists('temp_violation_test.py'):
            os.remove('temp_violation_test.py')

test_violation_detection()
```

### Task 2: CI/CD Pipeline Verification

Check GitHub Actions workflow configuration:

```bash
# Verify GitHub Actions workflow exists
echo "=== CI/CD PIPELINE VERIFICATION ==="
if [ -f ".github/workflows/router-enforcement.yml" ]; then
    echo "✅ GitHub Actions workflow exists"

    # Check workflow content
    echo "--- Workflow Jobs ---"
    grep -A 5 "jobs:" .github/workflows/router-enforcement.yml

    # Check for architectural protection job
    if grep -q "architectural-protection" .github/workflows/router-enforcement.yml; then
        echo "✅ Architectural protection job found"
    else
        echo "❌ Architectural protection job missing"
    fi

    # Check for direct import checking step
    if grep -q "Check Direct Adapter Imports" .github/workflows/router-enforcement.yml; then
        echo "✅ Direct import checking step found"
    else
        echo "❌ Direct import checking step missing"
    fi

else
    echo "❌ GitHub Actions workflow missing"
fi

# Check workflow directory structure
if [ -d ".github/workflows" ]; then
    echo "✅ .github/workflows directory exists"
    echo "Workflow files:"
    ls -la .github/workflows/
else
    echo "❌ .github/workflows directory missing"
fi
```

### Task 3: Documentation Quality Verification

Verify router pattern documentation exists and is comprehensive:

```bash
# Check documentation structure
echo "=== DOCUMENTATION VERIFICATION ==="

# Router patterns documentation
if [ -f "docs/architecture/router-patterns.md" ]; then
    echo "✅ Router patterns documentation exists"

    # Check key sections
    sections=("Overview" "Architecture" "Feature Flag Control" "Implementation Pattern" "Benefits")
    for section in "${sections[@]}"; do
        if grep -q "$section" docs/architecture/router-patterns.md; then
            echo "  ✅ $section section present"
        else
            echo "  ❌ $section section missing"
        fi
    done

else
    echo "❌ Router patterns documentation missing"
fi

# Migration guide documentation
if [ -f "docs/migration/router-migration-guide.md" ]; then
    echo "✅ Migration guide documentation exists"

    # Check for migration examples
    if grep -q "Calendar Services" docs/migration/router-migration-guide.md; then
        echo "  ✅ Calendar migration examples present"
    else
        echo "  ❌ Calendar migration examples missing"
    fi

    if grep -q "Notion Services" docs/migration/router-migration-guide.md; then
        echo "  ✅ Notion migration examples present"
    else
        echo "  ❌ Notion migration examples missing"
    fi

    if grep -q "Slack Services" docs/migration/router-migration-guide.md; then
        echo "  ✅ Slack migration examples present"
    else
        echo "  ❌ Slack migration examples missing"
    fi

else
    echo "❌ Migration guide documentation missing"
fi
```

Verify documentation accuracy:

```python
# Verify documentation matches actual implementation
def verify_documentation_accuracy():
    """Check that documentation examples match real router implementations"""

    print("\n=== DOCUMENTATION ACCURACY VERIFICATION ===")

    # Check Calendar router documentation vs implementation
    try:
        from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
        calendar_router = CalendarIntegrationRouter()

        # Check router has expected methods from documentation
        expected_methods = ['health_check', 'get_temporal_summary', 'authenticate']
        for method in expected_methods:
            if hasattr(calendar_router, method):
                print(f"✅ Calendar router has documented method: {method}")
            else:
                print(f"❌ Calendar router missing documented method: {method}")

    except Exception as e:
        print(f"❌ Cannot verify Calendar router documentation: {e}")

    # Check Notion router documentation vs implementation
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()

        # Check router has expected methods from documentation
        expected_methods = ['is_configured', 'connect', 'get_workspace_info']
        for method in expected_methods:
            if hasattr(notion_router, method):
                print(f"✅ Notion router has documented method: {method}")
            else:
                print(f"❌ Notion router missing documented method: {method}")

    except Exception as e:
        print(f"❌ Cannot verify Notion router documentation: {e}")

    # Check Slack router documentation vs implementation
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        slack_router = SlackIntegrationRouter()

        # Check router has expected methods from documentation
        expected_methods = ['get_spatial_adapter', 'send_message']
        for method in expected_methods:
            if hasattr(slack_router, method):
                print(f"✅ Slack router has documented method: {method}")
            else:
                print(f"❌ Slack router missing documented method: {method}")

    except Exception as e:
        print(f"❌ Cannot verify Slack router documentation: {e}")

verify_documentation_accuracy()
```

### Task 4: End-to-End Protection Testing

Test complete architectural protection workflow:

```python
# Test complete protection workflow
import asyncio

async def end_to_end_protection_test():
    """Test that complete architectural protection works"""

    print("\n=== END-TO-END PROTECTION TESTING ===")

    # Test 1: Verify no direct imports in codebase
    import os
    import glob

    service_files = glob.glob('services/**/*.py', recursive=True)
    violations = []

    direct_patterns = [
        'GoogleCalendarMCPAdapter',
        'NotionMCPAdapter',
        'SlackSpatialAdapter(?!Router)',
        'SlackClient(?!Router)'
    ]

    for file_path in service_files[:10]:  # Check first 10 files
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                for pattern in direct_patterns:
                    import re
                    if re.search(pattern, content):
                        violations.append(f"{file_path}: {pattern}")
            except:
                pass

    if violations:
        print(f"❌ Direct imports still found: {len(violations)}")
        for violation in violations[:5]:  # Show first 5
            print(f"  {violation}")
    else:
        print("✅ No direct imports found in sample files")

    # Test 2: Verify routers work correctly
    try:
        from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        routers = [
            ('Calendar', CalendarIntegrationRouter()),
            ('Notion', NotionIntegrationRouter()),
            ('Slack', SlackIntegrationRouter())
        ]

        for name, router in routers:
            if router:
                print(f"✅ {name} router instantiates correctly")
            else:
                print(f"❌ {name} router instantiation failed")

    except Exception as e:
        print(f"❌ Router instantiation test failed: {e}")

asyncio.run(end_to_end_protection_test())
```

### Task 5: Git History and Completeness Check

Verify all Phase 6 changes are properly committed:

```bash
# Check Phase 6 git history
echo "=== PHASE 6 GIT VERIFICATION ==="

# Check recent commits
echo "Recent commits:"
git log --oneline -5

# Check for Phase 6 commit
if git log --oneline -10 | grep -i "phase 6\|lock.*document"; then
    echo "✅ Phase 6 commit found"
else
    echo "❌ Phase 6 commit not found"
fi

# Check all expected files are tracked
expected_files=(
    ".pre-commit-config.yaml"
    "scripts/check_direct_imports.py"
    ".github/workflows/router-enforcement.yml"
    "docs/architecture/router-patterns.md"
    "docs/migration/router-migration-guide.md"
)

echo "Checking expected files are committed:"
for file in "${expected_files[@]}"; do
    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
        echo "✅ $file is tracked by git"
    else
        echo "❌ $file is not tracked by git"
    fi
done
```

## Cross-Validation Report Format

```markdown
# Phase 6: Lock & Document Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## Pre-Commit Hook Verification
### Configuration
- .pre-commit-config.yaml: [EXISTS/MISSING]
- Direct import hook configured: [YES/NO]

### Script Implementation
- scripts/check_direct_imports.py: [EXISTS/MISSING]
- Script executable: [YES/NO]
- Clean files test: [PASS/FAIL]
- Violation detection test: [WORKS/FAILS]

## CI/CD Pipeline Verification
### GitHub Actions Workflow
- .github/workflows/router-enforcement.yml: [EXISTS/MISSING]
- Architectural protection job: [PRESENT/MISSING]
- Direct import checking step: [PRESENT/MISSING]

## Documentation Verification
### Router Patterns Documentation
- docs/architecture/router-patterns.md: [EXISTS/MISSING]
- Key sections complete: [X/5 sections]
- Implementation accuracy: [ACCURATE/INACCURATE]

### Migration Guide
- docs/migration/router-migration-guide.md: [EXISTS/MISSING]
- Calendar examples: [PRESENT/MISSING]
- Notion examples: [PRESENT/MISSING]
- Slack examples: [PRESENT/MISSING]

## End-to-End Protection Testing
### Direct Import Detection
- Sample file check: [CLEAN/VIOLATIONS FOUND]
- Router instantiation: [ALL WORKING/X FAILING]

## Git History Verification
- Phase 6 commit: [PRESENT/MISSING]
- All files tracked: [X/5 files tracked]

## Issues Identified
### Blocking Issues
[Critical issues preventing approval]

### Non-Blocking Issues
[Minor issues for future improvement]

## Architectural Protection Assessment
**Automated Prevention**: [WORKING/NOT WORKING]
**Documentation Quality**: [COMPREHENSIVE/INCOMPLETE]
**Future Developer Guidance**: [CLEAR/UNCLEAR]

## Readiness Assessment
[APPROVED_FOR_PHASE_Z / NEEDS_FIXES / BLOCKING_PROBLEMS]

### Phase 6 Checkboxes Status
- [ ] Add pre-commit hooks: [COMPLETE/INCOMPLETE]
- [ ] Update CI/CD: [COMPLETE/INCOMPLETE]
- [ ] Document patterns: [COMPLETE/INCOMPLETE]
```

## Update Requirements

1. **Update Session Log**: Add Phase 6 verification completion
2. **Update GitHub Issue #199**: Add comment with locking/documentation verification
3. **Tag Lead Developer**: Report final approval status before Phase Z

## Critical Verification Standards

- **Automated Protection**: Pre-commit hooks must prevent direct imports reliably
- **CI/CD Enforcement**: Workflow must block pull requests with violations
- **Documentation Quality**: Must provide complete guidance for future developers
- **Implementation Accuracy**: Documentation must match actual router behavior

---

**Your Mission**: Verify architectural protection is bulletproof and documentation is comprehensive before Phase Z bookending.

**Quality Standard**: Future developers must be unable to accidentally break router pattern without clear automated warnings.
