# Agent Prompt: Phase 4B - Architectural Lock Verification (Cursor Agent)
*Cross-verification of Code agent's Phase 4A architectural enforcement implementation*

## Mission: Verify Architectural Protection

Code agent has implemented enforcement mechanisms to prevent regression to direct GitHubAgent imports. Your role is to verify these protections actually work and would catch future violations.

**Critical Standard**: Enforcement must reliably prevent architectural regression - no false positives or false negatives accepted.

## Verification Framework

### 1. Anti-Pattern Test Verification
```python
# Verify the architectural tests exist and work correctly
import os
import subprocess
import tempfile

def verify_anti_pattern_tests():
    """Verify architectural enforcement tests catch violations"""

    print("=== Anti-Pattern Test Verification ===")

    # Check if test file exists
    test_file = "tests/test_architecture_enforcement.py"
    if os.path.exists(test_file):
        print(f"✅ {test_file} exists")
    else:
        print(f"❌ {test_file} missing")
        return False

    # Run current tests (should pass with clean codebase)
    try:
        result = subprocess.run([
            "python", "-m", "pytest", test_file, "-v"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print("✅ Current codebase passes architectural tests")
            print("Test output:")
            print(result.stdout)
        else:
            print("❌ Current codebase fails architectural tests")
            print("Error output:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Failed to run architectural tests: {e}")
        return False

    return True

verify_anti_pattern_tests()
```

### 2. Violation Detection Testing
```python
def test_violation_detection():
    """Test that enforcement catches actual violations"""

    print("\n=== Violation Detection Testing ===")

    # Create temporary violation file
    violation_content = '''
from services.integrations.github.github_agent import GitHubAgent

class TestViolation:
    def __init__(self):
        self.github = GitHubAgent()  # This should be caught
'''

    # Write violation to services directory
    violation_file = "services/test_violation_temp.py"

    try:
        with open(violation_file, 'w') as f:
            f.write(violation_content)

        print(f"Created test violation file: {violation_file}")

        # Run architectural tests (should fail)
        result = subprocess.run([
            "python", "-m", "pytest", "tests/test_architecture_enforcement.py::test_no_direct_github_agent_imports", "-v"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode != 0:
            print("✅ Architectural test correctly caught violation")
            print("Failure output:")
            print(result.stdout)
        else:
            print("❌ Architectural test failed to catch violation")
            return False

    except Exception as e:
        print(f"❌ Violation detection test failed: {e}")
        return False

    finally:
        # Clean up violation file
        if os.path.exists(violation_file):
            os.remove(violation_file)
            print(f"Cleaned up: {violation_file}")

    return True

test_violation_detection()
```

### 3. Router Usage Verification
```python
def verify_router_usage_tests():
    """Verify tests check for required router usage"""

    print("\n=== Router Usage Verification ===")

    required_services = [
        "services/orchestration/engine.py",
        "services/domain/github_domain_service.py",
        "services/domain/pm_number_manager.py",
        "services/domain/standup_orchestration_service.py",
        "services/integrations/github/issue_analyzer.py"
    ]

    # Check each service has router usage
    missing_router = []

    for service_file in required_services:
        if os.path.exists(service_file):
            with open(service_file, 'r') as f:
                content = f.read()

            if "GitHubIntegrationRouter" in content:
                print(f"✅ {service_file} uses GitHubIntegrationRouter")
            else:
                print(f"❌ {service_file} missing GitHubIntegrationRouter")
                missing_router.append(service_file)
        else:
            print(f"❌ {service_file} not found")
            missing_router.append(service_file)

    # Run router usage test
    try:
        result = subprocess.run([
            "python", "-m", "pytest", "tests/test_architecture_enforcement.py::test_services_use_router", "-v"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print("✅ Router usage test passes")
        else:
            print("❌ Router usage test fails")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Router usage test failed: {e}")
        return False

    return len(missing_router) == 0

verify_router_usage_tests()
```

### 4. Pre-commit Hook Verification (if implemented)
```bash
# Check if pre-commit hook exists and is executable
if [ -f ".git/hooks/pre-commit" ]; then
    echo "✅ Pre-commit hook exists"

    if [ -x ".git/hooks/pre-commit" ]; then
        echo "✅ Pre-commit hook is executable"

        # Test hook with a violation (temporarily)
        echo "from services.integrations.github.github_agent import GitHubAgent" > test_violation.py
        git add test_violation.py

        # Run hook manually
        if .git/hooks/pre-commit; then
            echo "❌ Pre-commit hook failed to block violation"
        else
            echo "✅ Pre-commit hook correctly blocked violation"
        fi

        # Clean up
        rm test_violation.py
        git reset HEAD test_violation.py 2>/dev/null || true
    else
        echo "❌ Pre-commit hook not executable"
    fi
else
    echo "ℹ️  Pre-commit hook not implemented (optional)"
fi
```

### 5. CI/CD Integration Verification (if implemented)
```bash
# Check for CI/CD configuration
if [ -f ".github/workflows/architecture-compliance.yml" ]; then
    echo "✅ GitHub Actions workflow exists"

    # Verify workflow content
    if grep -q "architecture-compliance" .github/workflows/architecture-compliance.yml; then
        echo "✅ Workflow includes architecture compliance steps"
    else
        echo "❌ Workflow missing architecture compliance steps"
    fi
else
    echo "ℹ️  GitHub Actions workflow not implemented (optional)"
fi
```

### 6. Documentation Verification
```bash
# Check for architecture documentation
if [ -f "docs/architecture/github-integration-router.md" ]; then
    echo "✅ Architecture documentation exists"

    # Check documentation content
    if grep -q "GitHubIntegrationRouter" docs/architecture/github-integration-router.md; then
        echo "✅ Documentation covers router usage"
    else
        echo "❌ Documentation missing router details"
    fi

    if grep -q "Prohibited Import" docs/architecture/github-integration-router.md; then
        echo "✅ Documentation explains prohibited patterns"
    else
        echo "❌ Documentation missing prohibition explanation"
    fi
else
    echo "❌ Architecture documentation missing"
fi
```

## Comprehensive Enforcement Testing

### Test False Positive Prevention
```python
def test_false_positive_prevention():
    """Ensure enforcement doesn't flag legitimate code"""

    print("\n=== False Positive Prevention Testing ===")

    # Test that allowed files don't trigger violations
    allowed_files = [
        "services/integrations/github/github_agent.py",
        "services/integrations/github/github_integration_router.py"
    ]

    for file_path in allowed_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

            if "GitHubAgent" in content:
                print(f"✅ {file_path} legitimately contains GitHubAgent")
            else:
                print(f"ℹ️  {file_path} doesn't contain GitHubAgent")
        else:
            print(f"❌ {file_path} not found")

    # Run tests to ensure they pass with current legitimate usage
    try:
        result = subprocess.run([
            "python", "-m", "pytest", "tests/test_architecture_enforcement.py", "-v"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print("✅ No false positives - legitimate code passes")
            return True
        else:
            print("❌ False positives detected - legitimate code fails")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ False positive test failed: {e}")
        return False

test_false_positive_prevention()
```

## Quality Assurance Checklist

### Enforcement Implementation
- [ ] Anti-pattern tests exist and are functional
- [ ] Tests catch direct GitHubAgent imports
- [ ] Tests verify required router usage
- [ ] Tests pass with current clean codebase

### Violation Detection
- [ ] Enforcement catches actual violations (no false negatives)
- [ ] Enforcement doesn't flag legitimate usage (no false positives)
- [ ] Error messages are clear and actionable
- [ ] Tests run reliably in different environments

### Optional Enforcement Mechanisms
- [ ] Pre-commit hook implemented and functional (if present)
- [ ] CI/CD integration working (if present)
- [ ] Documentation created and comprehensive (if present)

## Reporting Format

### Phase 4B Verification Results
```markdown
## Phase 4B Results: Architectural Lock Verification

### Core Enforcement
- Anti-pattern tests: [WORKING/BROKEN]
- Violation detection: [CATCHES_VIOLATIONS/MISSES_VIOLATIONS]
- Router usage verification: [WORKING/BROKEN]
- False positive prevention: [CLEAN/ISSUES]

### Optional Enforcement
- Pre-commit hook: [WORKING/NOT_IMPLEMENTED/BROKEN]
- CI/CD integration: [WORKING/NOT_IMPLEMENTED/BROKEN]
- Documentation: [COMPREHENSIVE/BASIC/MISSING]

### Quality Assessment
[READY_FOR_PHASE_5 / NEEDS_FIXES]

### Issues Requiring Resolution
[List any problems that must be fixed]
```

## Success Criteria (All Must Pass)

- [ ] Anti-pattern tests exist and function correctly
- [ ] Tests catch direct GitHubAgent import violations
- [ ] Tests verify all required services use router
- [ ] Current codebase passes all architectural tests
- [ ] No false positives flagged for legitimate usage
- [ ] No false negatives allowing actual violations
- [ ] Evidence provided for all verification steps

## Critical Standards Reminder

**Reliable Enforcement**: Tests must consistently catch violations and never flag legitimate code. Inconsistent enforcement is worse than no enforcement.

**Evidence Required**: All verification must include test output demonstrating enforcement works.

**Quality Gate**: This verification determines if architectural protection is reliable enough for production use.

---

**Your Mission**: Verify architectural enforcement mechanisms reliably protect against future regression while allowing legitimate usage patterns.
